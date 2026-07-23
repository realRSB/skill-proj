#!/usr/bin/env bash
set -euo pipefail

input="${1:-/Users/bedir/Downloads/download.mp4}"
output="${2:-renders/car-edit.mp4}"

mkdir -p "$(dirname "$output")"

ffmpeg -hide_banner -y -i "$input" -filter_complex "\
[0:v]trim=start=0.20:end=1.75,setpts=(PTS-STARTPTS)/0.82,scale=800:-2,crop=720:1280:(iw-ow)/2:(ih-oh)/2,setsar=1[v0];\
[0:a]atrim=start=0.20:end=1.75,asetpts=PTS-STARTPTS,atempo=0.82[a0];\
[0:v]trim=start=1.80:end=3.20,setpts=(PTS-STARTPTS)/1.90,scale=880:-2,crop=720:1280:(iw-ow)/2+24*sin(t*20):(ih-oh)/2,setsar=1[v1];\
[0:a]atrim=start=1.80:end=3.20,asetpts=PTS-STARTPTS,atempo=1.90[a1];\
[0:v]trim=start=4.05:end=6.20,setpts=(PTS-STARTPTS)/0.90,scale=835:-2,crop=720:1280:(iw-ow)/2:(ih-oh)/2,setsar=1[v2];\
[0:a]atrim=start=4.05:end=6.20,asetpts=PTS-STARTPTS,atempo=0.90[a2];\
[0:v]trim=start=6.35:end=8.90,setpts=(PTS-STARTPTS)/1.05,scale=810:-2,crop=720:1280:(iw-ow)/2:(ih-oh)/2,setsar=1[v3];\
[0:a]atrim=start=6.35:end=8.90,asetpts=PTS-STARTPTS,atempo=1.05[a3];\
[0:v]trim=start=9.10:end=10.55,setpts=(PTS-STARTPTS)/1.80,scale=900:-2,crop=720:1280:(iw-ow)/2+32*sin(t*18):(ih-oh)/2,setsar=1[v4];\
[0:a]atrim=start=9.10:end=10.55,asetpts=PTS-STARTPTS,atempo=1.80[a4];\
[0:v]trim=start=11.80:end=12.85,setpts=(PTS-STARTPTS)/0.90,scale=840:-2,crop=720:1280:(iw-ow)/2:(ih-oh)/2,setsar=1[v5];\
[0:a]atrim=start=11.80:end=12.85,asetpts=PTS-STARTPTS,atempo=0.90[a5];\
[0:v]trim=start=15.10:end=18.05,setpts=(PTS-STARTPTS)/0.85,scale=820:-2,crop=720:1280:(iw-ow)/2:(ih-oh)/2,setsar=1[v6];\
[0:a]atrim=start=15.10:end=18.05,asetpts=PTS-STARTPTS,atempo=0.85[a6];\
[v0][a0][v1][a1][v2][a2][v3][a3][v4][a4][v5][a5][v6][a6]concat=n=7:v=1:a=1[cutv][cuta];\
[cutv]fps=30,eq=contrast=1.12:brightness=0.005:saturation=1.22:gamma=1.05,curves=preset=medium_contrast,unsharp=5:5:0.45:3:3:0.16,vignette=PI/7,\
drawbox=x=0:y=0:w=iw:h=ih:color=white@0.36:t=fill:enable='between(t,1.82,1.91)+between(t,5.13,5.20)+between(t,7.55,7.62)+between(t,10.55,10.64)',\
drawbox=x=42:y=104:w=188:h=3:color=0xFFE166@0.90:t=fill:enable='between(t,0.12,1.75)',\
drawbox=x=42:y=118:w=108:h=3:color=white@0.68:t=fill:enable='between(t,0.12,1.75)',\
drawbox=x=(w-250)/2:y=92:w=250:h=5:color=white@0.82:t=fill:enable='between(t,2.05,5.15)',\
drawbox=x=(w-138)/2:y=110:w=138:h=3:color=0xE51B23@0.95:t=fill:enable='between(t,2.05,5.15)',\
drawbox=x=42:y=h-132:w=258:h=4:color=0xE51B23@0.95:t=fill:enable='between(t,5.25,8.55)',\
drawbox=x=42:y=h-115:w=124:h=3:color=white@0.62:t=fill:enable='between(t,5.25,8.55)',\
drawbox=x=(w-220)/2:y=h-102:w=220:h=5:color=white@0.86:t=fill:enable='between(t,8.65,11.05)',\
drawbox=x=(w-120)/2:y=h-84:w=120:h=3:color=0xFFE166@0.92:t=fill:enable='gte(t,11.15)',\
format=yuv420p[finalv];\
[cuta]aresample=async=1:first_pts=0,asetpts=N/SR/TB,afade=t=in:st=0:d=0.08,afade=t=out:st=12.70:d=0.18,loudnorm=I=-16:TP=-1.5:LRA=11[finala]" \
  -map "[finalv]" -map "[finala]" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 160k -movflags +faststart "$output"
