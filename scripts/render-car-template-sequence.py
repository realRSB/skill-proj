#!/usr/bin/env python3
import argparse
import json
import math
import subprocess
from pathlib import Path


TEMPLATE_DURATION = 13.0
EFFECTS = {
    "flicker": 3.0 / TEMPLATE_DURATION,
    "whoosh": 5.0 / TEMPLATE_DURATION,
    "slash": 7.0 / TEMPLATE_DURATION,
    "cut": 10.0 / TEMPLATE_DURATION,
}


def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def probe(path):
    result = run(
        [
            "ffprobe",
            "-hide_banner",
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            str(path),
        ]
    )
    data = json.loads(result.stdout)
    video = next(stream for stream in data["streams"] if stream.get("codec_type") == "video")
    return {
        "duration": float(video.get("duration") or data["format"]["duration"]),
        "width": int(video["width"]),
        "height": int(video["height"]),
    }


def even(value):
    return int(math.ceil(value / 2) * 2)


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def scale_expr(width, height, canvas_zoom):
    if width / height >= 720 / 1280:
        return f"scale=-2:{even(1280 * canvas_zoom)}"
    return f"scale={even(720 * canvas_zoom)}:-2"


def timeline_windows(duration):
    flicker = duration * EFFECTS["flicker"]
    whoosh = duration * EFFECTS["whoosh"]
    slash = duration * EFFECTS["slash"]
    cut = duration * EFFECTS["cut"]

    flicker_d = clamp(duration * 0.030, 0.22, 0.42)
    whoosh_d = clamp(duration * 0.070, 0.42, 0.90)
    slash_d = clamp(duration * 0.040, 0.28, 0.48)
    cut_d = clamp(duration * 0.018, 0.07, 0.14)
    fade_d = clamp(duration * 0.095, 0.70, 1.30)

    return {
        "flicker": flicker,
        "whoosh": whoosh,
        "slash": slash,
        "cut": cut,
        "fade_start": max(0, duration - fade_d),
        "flicker_d": flicker_d,
        "whoosh_d": whoosh_d,
        "slash_d": slash_d,
        "cut_d": cut_d,
        "fade_d": fade_d,
    }


def between(center, half):
    return center - half, center + half


def effect_enables(w):
    f0, f1 = between(w["flicker"], w["flicker_d"] / 2)
    whoosh0, whoosh1 = between(w["whoosh"], w["whoosh_d"] / 2)
    cut0, cut1 = between(w["cut"], w["cut_d"] / 2)

    # Three fast pulses, like the template's early stutter/flicker.
    pulse = w["flicker_d"] / 7
    flicker_white = "+".join(
        f"between(t,{f0 + pulse * i:.3f},{f0 + pulse * i + pulse * 0.62:.3f})"
        for i in (0, 2, 4)
    )
    flicker_black = "+".join(
        f"between(t,{f0 + pulse * i:.3f},{f0 + pulse * i + pulse * 0.55:.3f})"
        for i in (1, 3, 5)
    )

    return {
        "flicker_white": flicker_white,
        "flicker_black": flicker_black,
        "whoosh": f"between(t,{whoosh0:.3f},{whoosh1:.3f})",
        "cut": f"between(t,{cut0:.3f},{cut1:.3f})",
    }


def crop_x_expr(width, height, duration, w):
    if width / height >= 720 / 1280:
        # Horizontal car footage often moves across frame; sweep gently left-to-right.
        base = f"(iw-ow)*(0.30+0.36*t/{duration:.6f})"
    else:
        base = "(iw-ow)/2"
    return base


def build_filter(info):
    duration = info["duration"]
    w = timeline_windows(duration)
    e = effect_enables(w)
    slash_d = w["slash_d"]
    slash_start = w["slash"] - slash_d / 2
    slash_end = w["slash"] + slash_d / 2
    pre_scale = scale_expr(info["width"], info["height"], 1.20)
    crop_x = crop_x_expr(info["width"], info["height"], duration, w)

    return ";".join(
        [
            (
                f"[0:v]trim=start=0:end={slash_end:.3f},setpts=PTS-STARTPTS,"
                f"{pre_scale},fps=30,settb=AVTB,setsar=1[pre]"
            ),
            (
                f"[0:v]trim=start={slash_start:.3f}:end={duration:.3f},setpts=PTS-STARTPTS,"
                f"{pre_scale},fps=30,settb=AVTB,setsar=1[post]"
            ),
            (
                # edit-slashing-diagonal-fade
                f"[pre][post]xfade=transition=diagbr:duration={slash_d:.3f}:"
                f"offset={slash_start:.3f}[slashed]"
            ),
            (
                f"[slashed]crop=720:1280:{crop_x}:(ih-oh)/2,"
                "eq=contrast=1.18:brightness=-0.030:saturation=1.14:gamma=0.98,"
                "curves=preset=medium_contrast,unsharp=5:5:0.48:3:3:0.18,"
                "vignette=PI/5,"
                # edit-whoosh-motion-blur
                f"boxblur=lr=8:lp=1:cr=4:cp=1:enable='{e['whoosh']}',"
                # edit-flicker-stutter
                f"drawbox=x=0:y=0:w=iw:h=ih:color=white@0.40:t=fill:enable='{e['flicker_white']}',"
                f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.40:t=fill:enable='{e['flicker_black']}',"
                # edit-hard-flash-cut
                f"drawbox=x=0:y=0:w=iw:h=ih:color=white@0.34:t=fill:enable='{e['cut']}',"
                # edit-final-fade-out
                f"fade=t=out:st={w['fade_start']:.3f}:d={w['fade_d']:.3f},"
                "format=yuv420p[finalv]"
            ),
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="Apply the car-edit.mp4 five-effect template to one raw clip.")
    parser.add_argument("input", help="Raw source video")
    parser.add_argument("output", help="Rendered MP4 output")
    parser.add_argument("--print-plan", action="store_true", help="Print scaled effect timings")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    info = probe(input_path)
    if info["duration"] < 4:
        raise SystemExit("Input video must be at least 4 seconds for the five-effect template.")

    plan = {"input": str(input_path), **info, **timeline_windows(info["duration"])}
    if args.print_plan:
        print(json.dumps(plan, indent=2))

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i",
        str(input_path),
        "-filter_complex",
        build_filter(info),
        "-map",
        "[finalv]",
        "-an",
        "-r",
        "30",
        "-fps_mode",
        "cfr",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
