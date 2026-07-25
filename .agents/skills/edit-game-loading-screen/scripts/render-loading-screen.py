#!/usr/bin/env python3
import argparse
import json
import math
import subprocess
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MUSIC = SKILL_DIR / "assets" / "backgroundsong.mp3"
DEFAULT_HUD = SKILL_DIR / "assets" / "loading-hud-720x1280.png"


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
    video = next((s for s in data["streams"] if s.get("codec_type") == "video"), None)
    audio = next((s for s in data["streams"] if s.get("codec_type") == "audio"), None)
    duration = float(data.get("format", {}).get("duration") or 0)
    return {
        "duration": duration,
        "width": int(video["width"]) if video else None,
        "height": int(video["height"]) if video else None,
        "has_video": video is not None,
        "has_audio": audio is not None,
    }


def is_still(path, info):
    return path.suffix.lower() in {".jpg", ".jpeg", ".png", ".heic", ".webp"} or info["duration"] < 0.2


def even(value):
    return int(math.ceil(value / 2) * 2)


def scale_expr(width, height, zoom):
    if width / height >= 720 / 1280:
        return f"scale=-2:{even(1280 * zoom)}"
    return f"scale={even(720 * zoom)}:-2"


def base_filters(info, zoom):
    return [
        scale_expr(info["width"], info["height"], zoom),
        "crop=720:1280:(iw-ow)/2:(ih-oh)/2",
        "fps=30",
        "settb=AVTB",
        "setsar=1",
    ]


def loading_grade():
    return [
        "eq=contrast=1.23:brightness=-0.055:saturation=1.18:gamma=0.94",
        "curves=preset=medium_contrast",
        "unsharp=5:5:0.45:3:3:0.16",
        "vignette=PI/4",
    ]


def hud_animation(post_duration):
    bar_width = f"max(8,min(520,520*t/{post_duration:.6f}))"
    return [
        f"drawbox=x=94:y=h-98:w='{bar_width}':h=12:color=0x65D9FF@0.95:t=fill",
        "drawbox=x=0:y=0:w=iw:h=ih:color=white@0.42:t=fill:enable='between(t,0,0.070)'",
        "drawbox=x=0:y=0:w=iw:h=ih:color=black@0.28:t=fill:enable='between(t,0.070,0.130)'",
    ]


def build_filter(info, output_duration, drop_time, slowmo_speed):
    pre_duration = min(drop_time, output_duration * 0.45)
    post_duration = max(0.1, output_duration - pre_duration)
    post_source_duration = post_duration * slowmo_speed

    normal = [
        f"[0:v]trim=start=0:end={pre_duration:.3f}",
        "setpts=PTS-STARTPTS",
        *base_filters(info, 1.06),
        "eq=contrast=1.04:brightness=0.005:saturation=1.04",
        f"drawbox=x=0:y=0:w=iw:h=ih:color=white@0.35:t=fill:enable='between(t,{max(0, pre_duration - 0.08):.3f},{pre_duration:.3f})'",
        "format=yuv420p[pre]",
    ]

    post = [
        f"[0:v]trim=start={pre_duration:.3f}:end={pre_duration + post_source_duration:.3f}",
        f"setpts=(PTS-STARTPTS)/{slowmo_speed:.6f}",
        *base_filters(info, 1.16),
        *loading_grade(),
        "format=rgba[postbase]",
    ]

    post_overlay = [
        "[2:v]format=rgba[hud]",
        "[postbase][hud]overlay=0:0:eof_action=repeat",
        *hud_animation(post_duration),
        f"tpad=stop_mode=clone:stop_duration={output_duration:.3f}",
        f"trim=start=0:end={post_duration:.3f}",
        "setpts=PTS-STARTPTS",
        "format=yuv420p[post]",
    ]

    audio_fade = min(0.6, max(0.35, output_duration * 0.06))
    audio = [
        f"[1:a]atrim=start=0:end={output_duration:.3f}",
        "asetpts=PTS-STARTPTS",
        "afade=t=in:st=0:d=0.04",
        f"afade=t=out:st={max(0, output_duration - audio_fade):.3f}:d={audio_fade:.3f}",
        "loudnorm=I=-16:TP=-1.5:LRA=11",
        "aresample=48000[finala]",
    ]

    return ";".join(
        [
            ",".join(normal),
            ",".join(post),
            ",".join(post_overlay),
            f"[pre][post]concat=n=2:v=1:a=0,trim=start=0:end={output_duration:.3f},format=yuv420p[finalv]",
            ",".join(audio),
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="Render a video game loading screen trend edit.")
    parser.add_argument("input", help="Input video or image")
    parser.add_argument("output", help="Output MP4")
    parser.add_argument("--music", default=str(DEFAULT_MUSIC), help="Background song")
    parser.add_argument("--hud", default=str(DEFAULT_HUD), help="Transparent loading screen HUD overlay")
    parser.add_argument("--drop-time", type=float, default=4.5, help="Beat drop time in seconds")
    parser.add_argument("--duration", type=float, default=None, help="Output duration override")
    parser.add_argument("--slowmo-speed", type=float, default=0.48, help="Post-drop source speed, lower is slower")
    parser.add_argument("--print-plan", action="store_true", help="Print render plan")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    music_path = Path(args.music).expanduser()
    hud_path = Path(args.hud).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    input_info = probe(input_path)
    music_info = probe(music_path)
    if not input_info["has_video"]:
        raise SystemExit("Input must contain a video stream or be an image.")
    if not music_info["has_audio"]:
        raise SystemExit("Music file must contain an audio stream.")
    if not hud_path.exists():
        raise SystemExit(f"HUD overlay does not exist: {hud_path}")

    image_input = is_still(input_path, input_info)
    music_duration = music_info["duration"]
    if args.duration:
        output_duration = args.duration
    elif image_input:
        output_duration = music_duration
    else:
        output_duration = min(music_duration, input_info["duration"])
    if output_duration <= args.drop_time + 1:
        output_duration = min(music_duration, max(input_info["duration"], args.drop_time + 2.5))
    drop_time = min(args.drop_time, output_duration - 1.0)

    plan = {
        "input": str(input_path),
        "music": str(music_path),
        "hud": str(hud_path),
        "image_input": image_input,
        "output": str(output_path),
        "duration": output_duration,
        "drop_time": drop_time,
        "source_audio_muted": True,
        "width": input_info["width"],
        "height": input_info["height"],
    }
    if args.print_plan:
        print(json.dumps(plan, indent=2))

    cmd = ["ffmpeg", "-hide_banner", "-y"]
    if image_input:
        cmd.extend(["-loop", "1", "-framerate", "30"])
    cmd.extend(["-i", str(input_path), "-stream_loop", "-1", "-i", str(music_path)])
    cmd.extend(["-loop", "1", "-framerate", "30", "-i", str(hud_path)])
    cmd.extend(
        [
            "-filter_complex",
            build_filter(input_info, output_duration, drop_time, args.slowmo_speed),
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
    )
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
