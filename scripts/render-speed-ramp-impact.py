#!/usr/bin/env python3
import argparse
import json
import math
import subprocess
from pathlib import Path


SEGMENTS = [
    {"pct": 0.02, "timeline": 1.80, "speed": 0.85, "zoom": 1.09, "role": "hero-open"},
    {"pct": 0.16, "timeline": 0.70, "speed": 1.85, "zoom": 1.18, "role": "whip-burst"},
    {"pct": 0.30, "timeline": 2.00, "speed": 0.92, "zoom": 1.12, "role": "detail-hold"},
    {"pct": 0.46, "timeline": 1.90, "speed": 1.05, "zoom": 1.08, "role": "profile-move"},
    {"pct": 0.61, "timeline": 0.65, "speed": 1.95, "zoom": 1.20, "role": "impact-burst"},
    {"pct": 0.73, "timeline": 1.35, "speed": 0.95, "zoom": 1.13, "role": "texture-hold"},
    {"pct": 0.84, "timeline": 2.40, "speed": 0.82, "zoom": 1.10, "role": "final-hero"},
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
    duration = float(data["format"]["duration"])
    has_audio = any(stream.get("codec_type") == "audio" for stream in data["streams"])
    video = next(stream for stream in data["streams"] if stream.get("codec_type") == "video")
    width = int(video["width"])
    height = int(video["height"])
    return duration, has_audio, width, height


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def atempo(speed):
    # Keep the chain valid on older FFmpeg builds where atempo prefers 0.5-2.0.
    parts = []
    remaining = speed
    while remaining > 2.0:
        parts.append("atempo=2.0")
        remaining /= 2.0
    while remaining < 0.5:
        parts.append("atempo=0.5")
        remaining /= 0.5
    parts.append(f"atempo={remaining:.6f}")
    return ",".join(parts)


def frame_luma(input_path, timestamp):
    try:
        result = subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{timestamp:.3f}",
                "-i",
                str(input_path),
                "-frames:v",
                "1",
                "-vf",
                "scale=1:1,format=gray",
                "-f",
                "rawvideo",
                "-",
            ],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        return 0
    return result.stdout[0] if result.stdout else 0


def choose_start(input_path, segment, wanted_start, source_len, usable_start, usable_end, usable, lower_start):
    max_start = max(usable_start, usable_end - source_len)
    min_start = min(lower_start, max_start)
    offsets = [-0.14, -0.08, -0.04, 0.0, 0.04, 0.08, 0.14]
    if segment["role"] == "final-hero":
        offsets = [-0.06, 0.0, 0.04, 0.08, 0.12]

    candidates = []
    for offset in offsets:
        start = clamp(wanted_start + usable * offset, min_start, max_start)
        center = min(usable_end - 0.05, start + source_len * 0.55)
        luma = frame_luma(input_path, center)
        # Prefer visible frames, but keep a small bias toward the original target.
        distance_penalty = abs(start - wanted_start) / max(usable, 0.001) * 24
        candidates.append((luma - distance_penalty, start, luma))

    candidates.sort(reverse=True)
    return candidates[0][1]


def build_plan(input_path, duration, target_duration):
    usable_start = min(0.25, duration * 0.03)
    usable_end = max(usable_start + 0.1, duration - usable_start)
    usable = usable_end - usable_start
    scale = target_duration / sum(segment["timeline"] for segment in SEGMENTS)

    plan = []
    previous_end = usable_start
    for segment in SEGMENTS:
        timeline = segment["timeline"] * scale
        source_len = timeline * segment["speed"]
        source_len = clamp(source_len, min(0.45, usable), min(max(0.50, usable * 0.32), usable))
        wanted_start = usable_start + usable * segment["pct"]
        start = choose_start(
            input_path,
            segment,
            wanted_start,
            source_len,
            usable_start,
            usable_end,
            usable,
            previous_end + 0.08,
        )

        end = min(usable_end, start + source_len)
        plan.append({**segment, "start": start, "end": end, "timeline": (end - start) / segment["speed"]})
        previous_end = end
    return plan


def filter_complex(plan, has_audio, source_width, source_height):
    video_parts = []
    audio_parts = []
    concat_inputs = []
    cursor = 0.0
    flash_times = []

    for index, segment in enumerate(plan):
        if source_width / source_height >= 720 / 1280:
            scale_expr = f"scale=-2:{int(math.ceil(1280 * segment['zoom'] / 2) * 2)}"
        else:
            scale_expr = f"scale={int(math.ceil(720 * segment['zoom'] / 2) * 2)}:-2"
        shake = "+18*sin(t*18)" if "burst" in segment["role"] else ""
        video_parts.append(
            f"[0:v]trim=start={segment['start']:.3f}:end={segment['end']:.3f},"
            f"setpts=(PTS-STARTPTS)/{segment['speed']:.6f},"
            f"{scale_expr},crop=720:1280:(iw-ow)/2{shake}:(ih-oh)/2,"
            f"fps=30,settb=AVTB,setsar=1[v{index}]"
        )
        concat_inputs.append(f"[v{index}]")

        if has_audio:
            audio_parts.append(
                f"[0:a]atrim=start={segment['start']:.3f}:end={segment['end']:.3f},"
                f"asetpts=PTS-STARTPTS,{atempo(segment['speed'])}[a{index}]"
            )
            concat_inputs.append(f"[a{index}]")

        cursor += segment["timeline"]
        if index < len(plan) - 1 and ("burst" in segment["role"] or index in {1, 4}):
            flash_times.append(cursor)

    if has_audio:
        concat = "".join(concat_inputs) + f"concat=n={len(plan)}:v=1:a=1[cutv][cuta]"
    else:
        concat = "".join(concat_inputs) + f"concat=n={len(plan)}:v=1:a=0[cutv]"

    flash_enable = "+".join(f"between(t,{t - 0.035:.3f},{t + 0.045:.3f})" for t in flash_times) or "0"
    final_video = (
        "[cutv]fps=30,settb=AVTB,eq=contrast=1.12:brightness=0.005:saturation=1.22:gamma=1.05,"
        "curves=preset=medium_contrast,"
        "unsharp=5:5:0.45:3:3:0.16,vignette=PI/7,"
        f"drawbox=x=0:y=0:w=iw:h=ih:color=white@0.34:t=fill:enable='{flash_enable}',"
        "drawbox=x=42:y=104:w=188:h=3:color=0xFFE166@0.90:t=fill:enable='between(t,0.12,1.75)',"
        "drawbox=x=42:y=118:w=108:h=3:color=white@0.68:t=fill:enable='between(t,0.12,1.75)',"
        "drawbox=x=(w-220)/2:y=h-102:w=220:h=5:color=white@0.82:t=fill:enable='gte(t,8.0)',"
        "drawbox=x=(w-120)/2:y=h-84:w=120:h=3:color=0xFFE166@0.92:t=fill:enable='gte(t,8.0)',"
        "format=yuv420p[finalv]"
    )

    parts = video_parts + audio_parts + [concat, final_video]
    if has_audio:
        output_duration = sum(segment["timeline"] for segment in plan)
        fade_start = max(0, output_duration - 0.25)
        parts.append(
            "[cuta]aresample=async=1:first_pts=0,asetpts=N/SR/TB,"
            f"afade=t=in:st=0:d=0.08,afade=t=out:st={fade_start:.3f}:d=0.18,"
            "loudnorm=I=-16:TP=-1.5:LRA=11[finala]"
        )
    return ";".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Render a reusable speed-ramp impact car promo edit.")
    parser.add_argument("input", help="Raw source video")
    parser.add_argument("output", help="Rendered MP4 output")
    parser.add_argument("--target-duration", type=float, default=13.0, help="Approximate output duration in seconds")
    parser.add_argument("--print-plan", action="store_true", help="Print the generated edit plan before rendering")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    duration, has_audio, source_width, source_height = probe(input_path)
    if duration < 3:
        raise SystemExit("Input video must be at least 3 seconds long for a speed-ramp edit.")

    plan = build_plan(input_path, duration, args.target_duration)
    if args.print_plan:
        print(json.dumps({"duration": duration, "has_audio": has_audio, "width": source_width, "height": source_height, "clips": plan}, indent=2))

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-i",
        str(input_path),
        "-filter_complex",
        filter_complex(plan, has_audio, source_width, source_height),
        "-map",
        "[finalv]",
    ]
    if has_audio:
        cmd.extend(["-map", "[finala]"])
    cmd.extend(["-r", "30", "-fps_mode", "cfr", "-c:v", "libx264", "-preset", "medium", "-crf", "18"])
    if has_audio:
        cmd.extend(["-c:a", "aac", "-b:a", "160k"])
    cmd.extend(["-movflags", "+faststart", str(output_path)])

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
