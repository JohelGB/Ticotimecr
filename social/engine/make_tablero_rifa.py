# Historia 1080x1920 con el tablero 00-99 de la rifa (vendidos tachados).
# uso: python3 social/engine/make_tablero_rifa.py "01,15,33" ["07,08"]   (pagados, reservados opcional)
#      -> social/reels/rifa-tablero.png
import sys, os
from PIL import Image, ImageDraw, ImageFont
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W,H=1080,1920
BLK='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; BLD='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; MED='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
GOLD=(232,197,122); WHITE=(246,242,234); RED=(214,58,47); NAVY=(10,20,38); YEL=(255,214,102)
def nums(s): return {int(x) for x in s.replace(' ','').split(',') if x.strip().isdigit()}
pag=nums(sys.argv[1]) if len(sys.argv)>1 else set(); res=nums(sys.argv[2]) if len(sys.argv)>2 else set(); res-=pag
im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
for y in range(H):
    k=1-abs(y-H*0.45)/(H*0.6); d.line([(0,y),(W,y)],fill=(int(10+22*k),int(20+34*k),int(38+60*k)))
F=lambda p,s: ImageFont.truetype(p,s)
def ct(y,t,f,c):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=c)
logo=Image.open(os.path.join(ROOT,'public/assets/logo.png')).convert('RGBA').resize((150,150)); im.paste(logo,((W-150)//2,90),logo)
ct(270,'RIFA NAVIDEÑA',F(BLK,92),GOLD)
libres=100-len(pag)-len(res)
ct(385,f'¡Quedan {libres} números!' if libres<100 else '¡Todos los números disponibles!',F(BLK,60),WHITE)
ct(468,'₡1.500 · Domingo 13 de diciembre · Lotería Nacional',F(MED,36),(200,206,218))
x0,y0,cs,g=70,560,86,8
for n in range(100):
    r,c=divmod(n,10); x=x0+c*(cs+g)+ (W-2*x0-10*cs-9*g)//2; y=y0+r*(cs+g)
    if n in pag:
        d.rounded_rectangle([x,y,x+cs,y+cs],16,fill=RED); t=f'{n:02d}'; f=F(BLK,40); w=d.textlength(t,font=f)
        d.text((x+(cs-w)/2,y+18),t,font=f,fill=(255,200,195)); d.line([(x+12,y+cs-12),(x+cs-12,y+12)],fill=WHITE,width=6)
    elif n in res:
        d.rounded_rectangle([x,y,x+cs,y+cs],16,fill=YEL); t=f'{n:02d}'; f=F(BLK,40); w=d.textlength(t,font=f); d.text((x+(cs-w)/2,y+18),t,font=f,fill=NAVY)
    else:
        d.rounded_rectangle([x,y,x+cs,y+cs],16,fill=(255,255,255)); t=f'{n:02d}'; f=F(BLK,40); w=d.textlength(t,font=f); d.text((x+(cs-w)/2,y+18),t,font=f,fill=NAVY)
yl=y0+10*(cs+g)+20
items=[((255,255,255),'Disponible'),(YEL,'Reservado'),(RED,'Vendido')]
fx=F(BLD,34); tot=sum(50+d.textlength(t,font=fx)+40 for _,t in items); x=(W-tot)/2
for c,t in items:
    d.rounded_rectangle([x,yl,x+36,yl+36],8,fill=c); d.text((x+50,yl-2),t,font=fx,fill=WHITE); x+=50+d.textlength(t,font=fx)+40
ct(yl+90,'Pagá por SINPE Móvil',F(BLD,50),WHITE)
ct(yl+160,'8640-0835',F(BLK,110),GOLD)
ct(yl+300,'y mandá el comprobante por WhatsApp con tu número',F(MED,34),(200,206,218))
out=os.path.join(ROOT,'social/reels/rifa-tablero.png'); im.save(out); print('ok',out,'libres',libres)
