# Historia 1080x1920 con los 3 premios y el tablero 00-99 de la rifa (vendidos tachados).
# uso: python3 social/engine/make_tablero_rifa.py "01,15,33" ["07,08"]   (pagados, reservados opcional)
#      -> social/reels/rifa-tablero.png
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W,H=1080,1920
BLK='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; BLD='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; MED='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
GOLD=(232,197,122); WHITE=(246,242,234); RED=(214,58,47); NAVY=(10,20,38); YEL=(255,214,102); MUT=(200,206,218)
def nums(s): return {int(x) for x in s.replace(' ','').split(',') if x.strip().isdigit()}
pag=nums(sys.argv[1]) if len(sys.argv)>1 else set(); res=nums(sys.argv[2]) if len(sys.argv)>2 else set(); res-=pag
im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
for y in range(H):
    k=max(0,1-abs(y-H*0.4)/(H*0.6)); d.line([(0,y),(W,y)],fill=(int(10+22*k),int(20+34*k),int(38+60*k)))
F=lambda p,s: ImageFont.truetype(p,s)
def ct(y,t,f,c,cx=W/2):
    w=d.textlength(t,font=f); d.text((cx-w/2,y),t,font=f,fill=c)
# encabezado
logo=Image.open(os.path.join(ROOT,'public/assets/logo.png')).convert('RGBA').resize((112,112),Image.LANCZOS); im.paste(logo,(60,48),logo)
d.text((190,58),'RIFA NAVIDEÑA',font=F(BLK,76),fill=GOLD)
d.text((192,140),'₡1.500 el número · Domingo 13 de diciembre',font=F(BLD,32),fill=MUT)
# premios
PZ=[('323','1.er PREMIO','Bolt Valkir',GOLD),('313','2.º PREMIO','Pro Diver Digital',(216,221,229)),('347','3.er PREMIO','Specialty Compass',(216,221,229))]
cw,ch,gap=318,300,23; x=(W-3*cw-2*gap)//2; y0=225
for ref,lab,name,col in PZ:
    sh=Image.new('RGBA',(cw+40,ch+40),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([20,26,cw+20,ch+26],26,fill=(0,0,0,120)); im.paste(sh.filter(ImageFilter.GaussianBlur(10)),(x-20,y0-20),sh.filter(ImageFilter.GaussianBlur(10)))
    d.rounded_rectangle([x,y0,x+cw,y0+ch],26,fill=(255,255,255),outline=col if ref=='323' else None,width=6)
    w=Image.open(os.path.join(ROOT,f'public/assets/disponibles/{ref}.webp')).convert('RGB'); s=min((cw-40)/w.width,(ch-96)/w.height); w=w.resize((int(w.width*s),int(w.height*s)),Image.LANCZOS)
    im.paste(w,(x+(cw-w.width)//2,y0+44))
    f=F(BLK,24); tw=d.textlength(lab,font=f); d.rounded_rectangle([x+cw/2-tw/2-16,y0-18,x+cw/2+tw/2+16,y0+20],20,fill=col); d.text((x+cw/2-tw/2,y0-14),lab,font=f,fill=NAVY)
    ct(y0+ch-46,name,F(BLK,30),NAVY,x+cw/2)
    x+=cw+gap
# cuántos quedan
libres=100-len(pag)-len(res)
ct(560,f'¡Quedan {libres} números!' if libres<100 else '¡Todos los números disponibles!',F(BLK,64),WHITE)
# tablero
cs,g=80,7; gx=(W-10*cs-9*g)//2; gy=660
for n in range(100):
    r,c=divmod(n,10); x=gx+c*(cs+g); y=gy+r*(cs+g); t=f'{n:02d}'; f=F(BLK,38); w=d.textlength(t,font=f)
    if n in pag:
        d.rounded_rectangle([x,y,x+cs,y+cs],14,fill=RED); d.text((x+(cs-w)/2,y+17),t,font=f,fill=(255,200,195)); d.line([(x+12,y+cs-12),(x+cs-12,y+12)],fill=WHITE,width=5)
    elif n in res:
        d.rounded_rectangle([x,y,x+cs,y+cs],14,fill=YEL); d.text((x+(cs-w)/2,y+17),t,font=f,fill=NAVY)
    else:
        d.rounded_rectangle([x,y,x+cs,y+cs],14,fill=(255,255,255)); d.text((x+(cs-w)/2,y+17),t,font=f,fill=NAVY)
yl=gy+10*(cs+g)+14
items=[((255,255,255),'Disponible'),(YEL,'Reservado'),(RED,'Vendido')]
fx=F(BLD,32); tot=sum(48+d.textlength(t,font=fx)+40 for _,t in items)-40; x=(W-tot)/2
for c,t in items:
    d.rounded_rectangle([x,yl+2,x+34,yl+36],8,fill=c); d.text((x+46,yl),t,font=fx,fill=WHITE); x+=48+d.textlength(t,font=fx)+40
ct(yl+70,'Pagá por SINPE Móvil',F(BLD,44),WHITE)
ct(yl+122,'8640-0835',F(BLK,100),GOLD)
ct(yl+240,'Mandá el comprobante por WhatsApp con tu número',F(MED,32),MUT)
ct(yl+282,'Juega con los 3 primeros premios de la Lotería Nacional',F(MED,28),(160,168,184))
out=os.path.join(ROOT,'social/reels/rifa-tablero.png'); im.save(out); print('ok',out,'libres',libres,'alto usado',yl+320)
