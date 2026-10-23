import subprocess
from PIL import Image,ImageFilter,ImageStat
W="/home/claude/ticotimecr/public/assets/videos"; p="/home/claude/vid/pp.jpg"
for r in [208,337,347,367,338,349,323]:
    f=f"{W}/{r}.mp4"; D=float(subprocess.check_output(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {f}',shell=True))
    rest=D-3.5-0.3; a=0.3+rest*0.38; b=a+rest*0.37; best=None; t=a+0.35
    while t<b-0.3:
        subprocess.run(f'ffmpeg -v error -y -ss {t:.2f} -i {f} -frames:v 1 -vf "crop=iw:ih*0.45:0:ih*0.12" {p}',shell=True)
        v=ImageStat.Stat(Image.open(p).convert('L').filter(ImageFilter.FIND_EDGES)).var[0]
        if not best or v>best[0]: best=(v,t)
        t+=0.2
    subprocess.run(f'ffmpeg -v error -y -ss {best[1]:.2f} -i {f} -frames:v 1 -q:v 4 {W}/{r}.jpg',shell=True); print(r,round(best[1],2))
