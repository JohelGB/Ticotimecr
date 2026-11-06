# Historia 1080x1920 SOLO con los números libres de la rifa, grandes.
# uso: python3 social/engine/make_disponibles_rifa.py "34,37,40,..."  -> social/reels/rifa-disponibles.png
import sys, os, math
from PIL import Image, ImageDraw, ImageFont
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W,H=1080,1920
BLK='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; BLD='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; MED='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
GOLD=(232,197,122); WHITE=(246,242,234); NAVY=(10,20,38); MUT=(200,206,218); RED=(255,107,94)
libres=sorted({int(x) for x in sys.argv[1].replace(' ','').split(',') if x.strip().isdigit()})
im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
for y in range(H):
    k=max(0,1-abs(y-H*0.42)/(H*0.6)); d.line([(0,y),(W,y)],fill=(int(10+22*k),int(20+34*k),int(38+60*k)))
F=lambda p,s: ImageFont.truetype(p,s)
def ct(y,t,f,c):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=c)
from PIL import ImageFilter
logo=Image.open(os.path.join(ROOT,'public/assets/logo.png')).convert('RGBA').resize((112,112),Image.LANCZOS); im.paste(logo,(60,48),logo)
d.text((190,58),'RIFA NAVIDEÑA',font=F(BLK,76),fill=GOLD)
d.text((192,140),'₡1.500 el número · Domingo 13 de diciembre',font=F(BLD,32),fill=MUT)
PZ=[('323','1.er PREMIO','Bolt Valkir',GOLD),('313','2.º PREMIO','Pro Diver Digital',(216,221,229)),('347','3.er PREMIO','Specialty Compass',(216,221,229))]
cw,ch,gp=318,300,23; x=(W-3*cw-2*gp)//2; yp=225
for ref,lab,name,col in PZ:
    sh=Image.new('RGBA',(cw+40,ch+40),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([20,26,cw+20,ch+26],26,fill=(0,0,0,120)); bl=sh.filter(ImageFilter.GaussianBlur(10)); im.paste(bl,(x-20,yp-20),bl)
    d.rounded_rectangle([x,yp,x+cw,yp+ch],26,fill=(255,255,255),outline=col if ref=='323' else None,width=6)
    w=Image.open(os.path.join(ROOT,f'public/assets/disponibles/{ref}.webp')).convert('RGB'); sc=min((cw-40)/w.width,(ch-96)/w.height); w=w.resize((int(w.width*sc),int(w.height*sc)),Image.LANCZOS)
    im.paste(w,(x+(cw-w.width)//2,yp+44))
    f=F(BLK,24); tw=d.textlength(lab,font=f); d.rounded_rectangle([x+cw/2-tw/2-16,yp-18,x+cw/2+tw/2+16,yp+20],20,fill=col); d.text((x+cw/2-tw/2,yp-14),lab,font=f,fill=NAVY)
    t=name; f2=F(BLK,30); tw=d.textlength(t,font=f2); d.text((x+cw/2-tw/2,yp+ch-46),t,font=f2,fill=NAVY)
    x+=cw+gp
ct(560,'NÚMEROS DISPONIBLES',F(BLK,56),WHITE)
ct(630,f'¡Solo quedan {len(libres)}!',F(BLK,48),RED)
# cuadrícula
n=len(libres); cols=6 if n>30 else 5 if n>16 else 4
rows=math.ceil(n/cols); top,bot=710,1590
cs=min(150,int((W-120-(cols-1)*18)/cols),int((bot-top-(rows-1)*18)/rows)); g=18
gw=cols*cs+(cols-1)*g; x0=(W-gw)//2; gh=rows*cs+(rows-1)*g; y0=top+((bot-top)-gh)//2
f=F(BLK,int(cs*0.5))
for i,nn in enumerate(libres):
    r,c=divmod(i,cols); x=x0+c*(cs+g); y=y0+r*(cs+g)
    d.rounded_rectangle([x,y,x+cs,y+cs],int(cs*0.2),fill=(255,255,255))
    t=f'{nn:02d}'; w=d.textlength(t,font=f); bb=d.textbbox((0,0),t,font=f)
    d.text((x+(cs-w)/2,y+(cs-(bb[3]-bb[1]))/2-bb[1]),t,font=f,fill=NAVY)
ct(1630,'Pagá por SINPE Móvil',F(BLD,44),WHITE)
ct(1685,'8640-0835',F(BLK,110),GOLD)
ct(1825,'Mandá el comprobante por WhatsApp con tu número',F(MED,32),MUT)
out=os.path.join(ROOT,'social/reels/rifa-disponibles.png'); im.save(out); print('ok',out,n)
