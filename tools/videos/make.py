import json,subprocess,sys,os
def run(c): subprocess.run(c,shell=True,check=True)
def dur(f): return float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{f}"',shell=True))
def make(src,d,out,web_dir):
    w=f"/home/claude/vid/work/{d['ref']}"; os.makedirs(w,exist_ok=True)
    run(f"NODE_PATH=$(npm root -g) node /home/claude/vid/ov2.js '{json.dumps(d)}' {w}")
    run(f'ffmpeg -v error -y -i "{src}" -vf "vidstabdetect=shakiness=6:accuracy=12:result={w}/tr.trf" -f null -')
    D=dur(src); X=2.0; T=D+X
    run(f'ffmpeg -v error -y -i "{src}" -vf "vidstabtransform=input={w}/tr.trf:smoothing=15:zoom=4:optzoom=0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.7,eq=contrast=1.06:saturation=1.12:brightness=0.02,fps=30,tpad=stop_mode=clone:stop_duration={X}" -c:v libx264 -crf 16 -preset fast -an {w}/stab.mp4')
    cta=3.5; rest=T-cta-0.3; a=0.3+rest*0.38; b=a+rest*0.37; c=T-cta
    off=bool(d.get('offer'))
    tag=(f"[7]format=rgba,pad=w=iw+80:h=ih*2+40:x=40:y=ih+40:color=black@0,rotate=a='0.13*sin(2*PI*t/2.8)':c=none:ow=iw:oh=ih,fade=in:st={a:.2f}:d=0.4:alpha=1[tg];[e][tg]overlay=x=760:y=-140:enable='gte(t,{a:.2f})'" if off else "[e]null")
    fc=f"""[2]format=rgba,fade=in:st=0.1:d=0.4:alpha=1[br];
[3]format=rgba,fade=in:st=0.3:d=0.3:alpha=1,fade=out:st={a-0.25:.2f}:d=0.25:alpha=1[ti];
[4]format=rgba,fade=in:st={a:.2f}:d=0.3:alpha=1,fade=out:st={b-0.25:.2f}:d=0.25:alpha=1[pr];
[5]format=rgba,fade=in:st={b:.2f}:d=0.3:alpha=1,fade=out:st={c-0.25:.2f}:d=0.25:alpha=1[pe];
[6]format=rgba,fade=in:st={c:.2f}:d=0.3:alpha=1[ct];
[0][br]overlay[a1];[a1][ti]overlay=enable='between(t,0.3,{a:.2f})'[a2];[a2][pr]overlay=enable='between(t,{a:.2f},{b:.2f})'[a3];
[a3][pe]overlay=enable='between(t,{b:.2f},{c:.2f})'[a4];[a4][ct]overlay=enable='gte(t,{c:.2f})'[e];
{tag},fade=out:st={T-0.45:.2f}:d=0.45[v];
[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad,afade=out:st={T-0.6:.2f}:d=0.6[au]"""
    ins=" ".join(f"-loop 1 -t {T:.2f} -i {w}/{n}.png" for n in ['brand','title','price','perks','cta','tag'])
    run(f'ffmpeg -v error -y -i {w}/stab.mp4 -i "{src}" {ins} -filter_complex "{fc}" -map "[v]" -map "[au]" -t {T:.2f} -c:v libx264 -crf 19 -preset medium -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -movflags +faststart "{out}"')
    wv=f"{web_dir}/{d['ref']}.mp4"
    run(f'ffmpeg -v error -y -i "{out}" -vf scale=720:1280:flags=lanczos -c:v libx264 -crf 27 -maxrate 1.6M -bufsize 3.2M -preset slow -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart {wv}')
    run(f'ffmpeg -v error -y -ss {(a+b)/2:.2f} -i {wv} -frames:v 1 -q:v 4 {web_dir}/{d["ref"]}.jpg')
    run(f'ffmpeg -v error -y -ss {(a+b)/2:.2f} -i "{out}" -frames:v 1 -vf scale=270:-1 {w}/p.jpg')
    print(d['ref'], f"{T:.1f}s", os.path.getsize(out)//1024, "KB", os.path.getsize(wv)//1024, "KB web")
if __name__=="__main__":
    jobs=json.load(open(sys.argv[1]))
    for j in jobs: make(j['src'],j['d'],j['out'],j['web'])
