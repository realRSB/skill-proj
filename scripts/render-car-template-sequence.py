#!/usr/bin/env python3
import argparse
import json
import math
import subprocess
from pathlib import Path


DEFAULT_MUSIC_PATH = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "car-edit" / "assets" / "trap-beat.mp3"
TEMPLATE_DURATION = 18.1
EFFECTS = {
    "flicker": 2.35 / TEMPLATE_DURATION,
    "whoosh": 6.65 / TEMPLATE_DURATION,
    "slash": 13.85 / TEMPLATE_DURATION,
    "cut": 10.85 / TEMPLATE_DURATION,
}

BEATS = [
    {"end": 0.120, "style": "hold", "zoom": 1.08, "x": 0.42, "y": 0.48},
    {"end": 0.160, "style": "flicker", "zoom": 1.18, "x": 0.50, "y": 0.46},
    {"end": 0.235, "style": "hold", "zoom": 1.12, "x": 0.58, "y": 0.48},
    {"end": 0.270, "style": "black"},
    {"end": 0.355, "style": "hold", "zoom": 1.24, "x": 0.68, "y": 0.50},
    {"end": 0.385, "style": "whoosh", "zoom": 1.42, "x": 0.50, "y": 0.50},
    {"end": 0.590, "style": "hold", "zoom": 1.30, "x": 0.36, "y": 0.50},
    {"end": 0.625, "style": "cut", "zoom": 1.44, "x": 0.56, "y": 0.50},
    {"end": 0.725, "style": "hold", "zoom": 1.28, "x": 0.44, "y": 0.50},
    {"end": 0.785, "style": "slash", "zoom": 1.22, "x": 0.55, "y": 0.50},
    {"end": 0.910, "style": "hold", "zoom": 1.08, "x": 0.50, "y": 0.50},
    {"end": 1.000, "style": "final", "zoom": 1.10, "x": 0.50, "y": 0.50},
]


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

    flicker_d = clamp(duration * 0.040, 0.20, 0.55)
    whoosh_d = clamp(duration * 0.030, 0.18, 0.45)
    slash_d = clamp(duration * 0.060, 0.30, 0.75)
    cut_d = clamp(duration * 0.035, 0.12, 0.42)
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


def flicker_enables(duration):
    # Three fast pulses, like the template's early stutter/flicker.
    pulse = duration / 7
    flicker_white = "+".join(
        f"between(t,{pulse * i:.3f},{pulse * i + pulse * 0.62:.3f})"
        for i in (0, 2, 4)
    )
    flicker_black = "+".join(
        f"between(t,{pulse * i:.3f},{pulse * i + pulse * 0.55:.3f})"
        for i in (1, 3, 5)
    )
    return flicker_white, flicker_black


def crop_expr(axis_bias):
    return f"(i{'w' if axis_bias[0] else 'h'}-o{'w' if axis_bias[0] else 'h'})*{axis_bias[1]:.3f}"


def segment_filter(index, beat, start, end, info):
    duration = max(0.001, end - start)
    output = f"v{index}"
    if beat["style"] == "black":
        return f"color=c=black:s=720x1280:r=30:d={duration:.3f}[{output}]"

    filters = [
        f"[0:v]trim=start={start:.3f}:end={end:.3f}",
        "setpts=PTS-STARTPTS",
        scale_expr(info["width"], info["height"], beat["zoom"]),
        f"crop=720:1280:{crop_expr((True, beat['x']))}:{crop_expr((False, beat['y']))}",
        "fps=30",
        "settb=AVTB",
        "setsar=1",
        "eq=contrast=1.18:brightness=-0.030:saturation=1.14:gamma=0.98",
        "curves=preset=medium_contrast",
        "unsharp=5:5:0.48:3:3:0.18",
        "vignette=PI/5",
    ]

    if beat["style"] == "flicker":
        white, black = flicker_enables(duration)
        filters.extend(
            [
                "boxblur=lr=10:lp=1:cr=5:cp=1",
                f"drawbox=x=0:y=0:w=iw:h=ih:color=white@0.45:t=fill:enable='{white}'",
                f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.42:t=fill:enable='{black}'",
            ]
        )
    elif beat["style"] == "whoosh":
        filters.extend(
            [
                "boxblur=lr=18:lp=1:cr=9:cp=1",
                "tblend=all_mode=average",
                "eq=contrast=1.25:saturation=1.35",
            ]
        )
    elif beat["style"] == "cut":
        filters.extend(
            [
                "boxblur=lr=14:lp=1:cr=8:cp=1",
                "tblend=all_mode=average",
                f"drawbox=x=0:y=0:w=iw:h=ih:color=white@0.42:t=fill:enable='between(t,0,{min(0.12, duration * 0.35):.3f})'",
            ]
        )
    elif beat["style"] == "slash":
        filters.extend(
            [
                "rotate=0.055:fillcolor=black",
                "boxblur=lr=6:lp=1:cr=3:cp=1",
            ]
        )
    elif beat["style"] == "final":
        fade_d = clamp(info["duration"] * 0.095, 0.70, 1.30)
        filters.append(f"fade=t=out:st={max(0, duration - fade_d):.3f}:d={min(duration, fade_d):.3f}")

    return ",".join(filters) + f"[{output}]"


def build_filter(info):
    duration = info["duration"]
    parts = []
    start = 0.0
    for index, beat in enumerate(BEATS):
        end = duration * beat["end"]
        parts.append(segment_filter(index, beat, start, end, info))
        start = end
    concat_inputs = "".join(f"[v{index}]" for index in range(len(BEATS)))
    parts.append(f"{concat_inputs}concat=n={len(BEATS)}:v=1:a=0,format=yuv420p[finalv]")
    audio_fade = clamp(duration * 0.095, 0.70, 1.30)
    parts.append(
        "[1:a]"
        f"atrim=start=0:end={duration:.3f},"
        "asetpts=PTS-STARTPTS,"
        "afade=t=in:st=0:d=0.05,"
        f"afade=t=out:st={max(0, duration - audio_fade):.3f}:d={audio_fade:.3f},"
        "loudnorm=I=-16:TP=-1.5:LRA=11,"
        "aresample=48000[finala]"
    )
    return ";".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Apply the car-edit five-effect template to one raw clip.")
    parser.add_argument("input", help="Raw source video")
    parser.add_argument("output", help="Rendered MP4 output")
    parser.add_argument("--music", default=str(DEFAULT_MUSIC_PATH), help="Background beat to loop/trim to the output length")
    parser.add_argument("--print-plan", action="store_true", help="Print scaled effect timings")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    music_path = Path(args.music).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not music_path.exists():
        raise SystemExit(f"Music file does not exist: {music_path}")

    info = probe(input_path)
    if info["duration"] < 4:
        raise SystemExit("Input video must be at least 4 seconds for the five-effect template.")

    plan = {
        "input": str(input_path),
        "music": str(music_path),
        **info,
        **timeline_windows(info["duration"]),
        "beats": [
            {
                **beat,
                "start": (0 if index == 0 else BEATS[index - 1]["end"]) * info["duration"],
                "end": beat["end"] * info["duration"],
            }
            for index, beat in enumerate(BEATS)
        ],
    }
    if args.print_plan:
        print(json.dumps(plan, indent=2))

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i",
        str(input_path),
        "-stream_loop",
        "-1",
        "-i",
        str(music_path),
        "-filter_complex",
        build_filter(info),
        "-map",
        "[finalv]",
        "-map",
        "[finala]",
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
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
