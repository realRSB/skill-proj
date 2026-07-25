#!/usr/bin/env python3
import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MUSIC = SKILL_DIR / "assets" / "backgroundsong.mp3"
DEFAULT_INTRO = SKILL_DIR / "assets" / "intro-caption-720x1280.png"
DEFAULT_MENU_STATES = [
    SKILL_DIR / "assets" / "menu-1-continue.png",
    SKILL_DIR / "assets" / "menu-2-new-game.png",
    SKILL_DIR / "assets" / "menu-3-settings.png",
    SKILL_DIR / "assets" / "menu-4-exit.png",
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


def base_filters(info, zoom, image_input=False):
    crop = "crop=720:1280:(iw-ow)/2:(ih-oh)/2"
    if image_input:
        crop = "crop=720:1280:'(iw-ow)/2+(iw-ow)*0.08*sin(t*0.42)':'(ih-oh)/2+(ih-oh)*0.06*cos(t*0.33)'"
    return [
        scale_expr(info["width"], info["height"], zoom),
        crop,
        "fps=30",
        "settb=AVTB",
        "setsar=1",
    ]


def loading_grade():
    return [
        "eq=contrast=1.18:brightness=-0.02:saturation=1.14:gamma=0.96",
        "curves=preset=medium_contrast",
        "unsharp=5:5:0.45:3:3:0.16",
    ]


def trim_source(label, start, end, image_input):
    if image_input:
        return f"[{label}]fps=30,setpts=N/(30*TB),trim=start={start:.3f}:end={end:.3f}"
    return f"[{label}]trim=start={start:.3f}:end={end:.3f}"


def click_flashes():
    return [
        "drawbox=x=0:y=0:w=iw:h=ih:color=white@0.42:t=fill:enable='between(t,0,0.070)'",
        "drawbox=x=0:y=0:w=iw:h=ih:color=black@0.28:t=fill:enable='between(t,0.070,0.130)'",
        "drawbox=x=0:y=0:w=iw:h=ih:color=0xFFE4A1@0.18:t=fill:enable='between(t,1.250,1.330)'",
        "drawbox=x=0:y=0:w=iw:h=ih:color=0xFFE4A1@0.18:t=fill:enable='between(t,2.500,2.580)'",
        "drawbox=x=0:y=0:w=iw:h=ih:color=0xFFE4A1@0.18:t=fill:enable='between(t,3.750,3.830)'",
    ]


def build_filter(info, output_duration, drop_time, slowmo_speed, image_input):
    pre_duration = min(drop_time, output_duration * 0.45)
    post_duration = max(0.1, output_duration - pre_duration)
    post_source_duration = post_duration * slowmo_speed
    post_source_start = 0 if image_input else pre_duration
    intro_start = min(0.55, max(0, pre_duration - 1.4))
    intro_end = max(intro_start + 0.8, pre_duration - 0.32)
    source_split = "[0:v]split=2[srcpre][srcpost]"

    normal = [
        trim_source("srcpre", 0, pre_duration, image_input),
        "setpts=PTS-STARTPTS",
        *base_filters(info, 1.14 if image_input else 1.06, image_input=image_input),
        "eq=contrast=1.07:brightness=0.01:saturation=1.08",
        "format=rgba[prebase]",
    ]

    intro_overlay = [
        "[2:v]format=rgba[intro]",
        f"[prebase][intro]overlay=0:0:eof_action=repeat:enable='between(t,{intro_start:.3f},{intro_end:.3f})'",
        f"drawbox=x=0:y=0:w=iw:h=ih:color=white@0.35:t=fill:enable='between(t,{max(0, pre_duration - 0.08):.3f},{pre_duration:.3f})'",
        "format=yuv420p[pre]",
    ]

    post = [
        trim_source("srcpost", post_source_start, post_source_start + post_source_duration, image_input),
        f"setpts=(PTS-STARTPTS)/{slowmo_speed:.6f}",
        *base_filters(info, 1.24 if image_input else 1.16, image_input=image_input),
        *loading_grade(),
        "format=rgba[postbase]",
    ]

    step = max(0.58, post_duration / 4)
    menu_segments = []
    for index in range(4):
        menu_segments.append(
            f"[{index + 3}:v]format=rgba,tpad=stop_mode=clone:stop_duration={step:.3f},"
            f"trim=start=0:duration={step:.3f},setpts=PTS-STARTPTS[menuseg{index}]"
        )
    menu_overlays = [
        *menu_segments,
        "[menuseg0][menuseg1][menuseg2][menuseg3]"
        f"concat=n=4:v=1:a=0,trim=start=0:end={post_duration:.3f},setpts=PTS-STARTPTS,format=rgba[menu]",
    ]

    flashes = click_flashes()
    post_overlay = [
        f"[postbase][menu]overlay=0:0:eof_action=repeat,{flashes[0]}",
        *flashes[1:],
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
            source_split,
            ",".join(normal),
            ",".join(intro_overlay),
            ",".join(post),
            ";".join(menu_overlays),
            ",".join(post_overlay),
            f"[pre][post]concat=n=2:v=1:a=0,trim=start=0:end={output_duration:.3f},format=yuv420p[finalv]",
            ",".join(audio),
        ]
    )


def pre_filter(info, pre_duration, image_input):
    intro_start = min(0.55, max(0, pre_duration - 1.4))
    intro_end = max(intro_start + 0.8, pre_duration - 0.32)
    normal = [
        trim_source("0:v", 0, pre_duration, image_input),
        "setpts=PTS-STARTPTS",
        *base_filters(info, 1.14 if image_input else 1.06, image_input=image_input),
        "eq=contrast=1.07:brightness=0.01:saturation=1.08",
        "format=rgba[prebase]",
    ]
    intro = [
        "[1:v]format=rgba[intro]",
        f"[prebase][intro]overlay=0:0:eof_action=repeat:enable='between(t,{intro_start:.3f},{intro_end:.3f})'",
        f"drawbox=x=0:y=0:w=iw:h=ih:color=white@0.35:t=fill:enable='between(t,{max(0, pre_duration - 0.08):.3f},{pre_duration:.3f})'",
        "format=yuv420p[v]",
    ]
    return ";".join([",".join(normal), ",".join(intro)])


def post_filter(info, pre_duration, post_duration, slowmo_speed, image_input):
    post_source_start = 0 if image_input else pre_duration
    post_source_duration = post_duration * slowmo_speed
    post = [
        trim_source("0:v", post_source_start, post_source_start + post_source_duration, image_input),
        f"setpts=(PTS-STARTPTS)/{slowmo_speed:.6f}",
        *base_filters(info, 1.24 if image_input else 1.16, image_input=image_input),
        *loading_grade(),
        "format=rgba[postbase]",
    ]

    step = max(0.58, post_duration / 4)
    menu_segments = []
    for index in range(4):
        menu_segments.append(
            f"[{index + 1}:v]format=rgba,tpad=stop_mode=clone:stop_duration={step:.3f},"
            f"trim=start=0:duration={step:.3f},setpts=PTS-STARTPTS[menuseg{index}]"
        )
    menu = [
        *menu_segments,
        "[menuseg0][menuseg1][menuseg2][menuseg3]"
        f"concat=n=4:v=1:a=0,trim=start=0:end={post_duration:.3f},setpts=PTS-STARTPTS,format=rgba[menu]",
    ]

    flashes = click_flashes()
    overlay = [
        f"[postbase][menu]overlay=0:0:eof_action=repeat,{flashes[0]}",
        *flashes[1:],
        f"tpad=stop_mode=clone:stop_duration={post_duration:.3f}",
        f"trim=start=0:end={post_duration:.3f}",
        "setpts=PTS-STARTPTS",
        "format=yuv420p[v]",
    ]
    return ";".join([",".join(post), ";".join(menu), ",".join(overlay)])


def audio_filter(output_duration):
    audio_fade = min(0.6, max(0.35, output_duration * 0.06))
    return ",".join(
        [
            f"[2:a]atrim=start=0:end={output_duration:.3f}",
            "asetpts=PTS-STARTPTS",
            "afade=t=in:st=0:d=0.04",
            f"afade=t=out:st={max(0, output_duration - audio_fade):.3f}:d={audio_fade:.3f}",
            "loudnorm=I=-16:TP=-1.5:LRA=11",
            "aresample=48000[finala]",
        ]
    )


def add_visual_input(cmd, input_path, image_input):
    if image_input:
        cmd.extend(["-loop", "1", "-framerate", "30"])
    cmd.extend(["-i", str(input_path)])


def encode_video_args(output_path):
    return [
        "-map",
        "[v]",
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
        "-pix_fmt",
        "yuv420p",
        str(output_path),
    ]


def render_two_pass(input_path, output_path, music_path, intro_path, menu_paths, input_info, output_duration, drop_time, slowmo_speed, image_input):
    pre_duration = min(drop_time, output_duration * 0.45)
    post_duration = max(0.1, output_duration - pre_duration)
    with tempfile.TemporaryDirectory(prefix="loading-screen-edit-") as tmp:
        tmp_dir = Path(tmp)
        pre_path = tmp_dir / "pre.mp4"
        post_path = tmp_dir / "post.mp4"

        pre_cmd = ["ffmpeg", "-hide_banner", "-y"]
        add_visual_input(pre_cmd, input_path, image_input)
        pre_cmd.extend(["-loop", "1", "-framerate", "30", "-i", str(intro_path)])
        pre_cmd.extend(["-filter_complex", pre_filter(input_info, pre_duration, image_input)])
        pre_cmd.extend(["-t", f"{pre_duration:.3f}"])
        pre_cmd.extend(encode_video_args(pre_path))
        subprocess.run(pre_cmd, check=True)

        post_cmd = ["ffmpeg", "-hide_banner", "-y"]
        add_visual_input(post_cmd, input_path, image_input)
        for menu_path in menu_paths:
            post_cmd.extend(["-loop", "1", "-framerate", "30", "-i", str(menu_path)])
        post_cmd.extend(["-filter_complex", post_filter(input_info, pre_duration, post_duration, slowmo_speed, image_input)])
        post_cmd.extend(["-t", f"{post_duration:.3f}"])
        post_cmd.extend(encode_video_args(post_path))
        subprocess.run(post_cmd, check=True)

        final_filter = ";".join(
            [
                f"[0:v][1:v]concat=n=2:v=1:a=0,trim=start=0:end={output_duration:.3f},format=yuv420p[finalv]",
                audio_filter(output_duration),
            ]
        )
        final_cmd = [
            "ffmpeg",
            "-hide_banner",
            "-y",
            "-i",
            str(pre_path),
            "-i",
            str(post_path),
            "-stream_loop",
            "-1",
            "-i",
            str(music_path),
            "-filter_complex",
            final_filter,
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
        subprocess.run(final_cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="Render a video game loading screen trend edit.")
    parser.add_argument("input", help="Input video or image")
    parser.add_argument("output", help="Output MP4")
    parser.add_argument("--music", default=str(DEFAULT_MUSIC), help="Background song")
    parser.add_argument("--intro", default=str(DEFAULT_INTRO), help="Transparent intro caption overlay")
    parser.add_argument(
        "--menu-state",
        action="append",
        dest="menu_states",
        help="Transparent menu overlay state. Repeat four times to override the bundled menu states.",
    )
    parser.add_argument("--drop-time", type=float, default=4.5, help="Beat drop time in seconds")
    parser.add_argument("--duration", type=float, default=None, help="Output duration override")
    parser.add_argument("--slowmo-speed", type=float, default=0.48, help="Post-drop source speed, lower is slower")
    parser.add_argument("--print-plan", action="store_true", help="Print render plan")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()
    music_path = Path(args.music).expanduser()
    intro_path = Path(args.intro).expanduser()
    menu_paths = [Path(p).expanduser() for p in (args.menu_states or DEFAULT_MENU_STATES)]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    input_info = probe(input_path)
    music_info = probe(music_path)
    if not input_info["has_video"]:
        raise SystemExit("Input must contain a video stream or be an image.")
    if not music_info["has_audio"]:
        raise SystemExit("Music file must contain an audio stream.")
    if not intro_path.exists():
        raise SystemExit(f"Intro overlay does not exist: {intro_path}")
    if len(menu_paths) != 4:
        raise SystemExit("Exactly four menu overlay states are required.")
    for menu_path in menu_paths:
        if not menu_path.exists():
            raise SystemExit(f"Menu overlay does not exist: {menu_path}")

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
        "intro": str(intro_path),
        "menu_states": [str(path) for path in menu_paths],
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

    render_two_pass(
        input_path,
        output_path,
        music_path,
        intro_path,
        menu_paths,
        input_info,
        output_duration,
        drop_time,
        args.slowmo_speed,
        image_input,
    )


if __name__ == "__main__":
    main()
