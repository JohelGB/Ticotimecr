# Reel de la Rifa Navideña (3 premios) — 1080x1920, voz + música.
# uso: python3 social/engine/make_rifa.py  -> social/reels/reel-rifa-navidad.mp4 / .jpg
import os, subprocess, json, math, random, asyncio
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ENG=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(ENG))
W,H,FPS=1080,1920,30
TMP='/tmp/rifa_reel'; os.makedirs(TMP,exist_ok=True)
BLK='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; BLD='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
MED='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'; SER='/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
GOLD=(232,197,122); GOLD2=(201,154,66); WHITE=(246,242,234); RED=(255,107,94); NAVY=(10,20,38); MUTED=(180,188,202)
FC={}
def F(p,s):
    if (p,s) not in FC: FC[(p,s)]=ImageFont.truetype(p,s)
    return FC[(p,s)]
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def back(x): x=max(0,min(1,x)); c=1.7; return 1+(c+1)*(x-1)**3+c*(x-1)**2
def money(n): return '₡'+f'{n:,}'.replace(',','.')

# ---------- guion: cada escena con su locución ----------
SC=[
 ('hook',  '¿Un Invicta original para Navidad, sin gastar de más?'),
 ('rifa',  'Gran rifa TicoTime: tres relojes, tres ganadores.'),
 ('p3',    'Tercer premio: Invicta Compass.'),
 ('p2',    'Segundo: Invicta Pro Diver Digital.'),
 ('p1',    'Y el primero: ¡el Invicta Bolt Valkir!'),
 ('num',   'Número a solo mil quinientos colones. ¡Solo cien números!'),
 ('fecha', 'Juega el domingo trece de diciembre con la Lotería Nacional.'),
 ('pago',  'Pagá por SINPE al ocho seis cuatro cero, cero ocho tres cinco.'),
]
PZ={'p1':('1.er PREMIO','Invicta Bolt Valkir','Cronógrafo · 52 mm · Acero',62500,'323'),
    'p2':('2.º PREMIO','Invicta Pro Diver Digital','Analógico y digital · 46,5 mm',39500,'313'),
    'p3':('3.er PREMIO','Invicta Specialty Compass','45 mm · Acero · Azul',38500,'347')}
env=dict(os.environ,NO_PROXY='',no_proxy='')
durs=[]
for i,(k,txt) in enumerate(SC):
    mp3=f'{TMP}/v{i}.mp3'
    if not os.path.exists(mp3):
        subprocess.run(['python3',os.path.join(ENG,'tts.py'),txt,mp3,'es-CR-JuanNeural','+22%'],check=True,env=env)
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',mp3]).decode())
    sd=subprocess.run(['ffmpeg','-i',mp3,'-af','silencedetect=n=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True).stderr
    import re as _re
    st=[float(x) for x in _re.findall(r'silence_start: ([\d.]+)',sd)]
    if st and st[-1]>0.5 and d-st[-1]>0.3: d=st[-1]   # se quita el silencio del final
    durs.append(d)
GAP={'hook':0.5,'rifa':0.4,'p3':0.5,'p2':0.5,'p1':0.9,'num':0.7,'fecha':0.6,'pago':2.6}
starts=[]; t=0.25
for (k,_),d in zip(SC,durs): starts.append(t); t+=d+GAP[k]
D=t; N=int(D*FPS)
print('duración',round(D,2), [round(s,2) for s in starts])

# ---------- recursos ----------
def card(ref,w,h):
    im=Image.open(os.path.join(ROOT,f'public/assets/disponibles/{ref}.webp')).convert('RGB')
    c=Image.new('RGBA',(w,h),(255,255,255,255)); s=min((w-60)/im.width,(h-60)/im.height); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    c.paste(im,((w-im.width)//2,(h-im.height)//2))
    m=Image.new('L',(w,h),0); ImageDraw.Draw(m).rounded_rectangle([0,0,w-1,h-1],38,fill=255); c.putalpha(m); return c
CARDS={k:card(v[4],720,880) for k,v in PZ.items()}
SMALL={k:card(v[4],300,370) for k,v in PZ.items()}
logo=Image.open(os.path.join(ROOT,'public/assets/logo.png')).convert('RGBA').resize((190,190),Image.LANCZOS)
# fondo: degradado radial azul + rayos
bg=Image.new('RGB',(W,H),NAVY); px=bg.load()
for y in range(0,H,2):
    for x in range(0,W,2):
        d=math.hypot((x-W/2)/700,(y-H*0.42)/900); f=max(0,1-d)
        c=(int(8+30*f),int(16+44*f),int(30+78*f))
        px[x,y]=c
        if x+1<W: px[x+1,y]=c
        if y+1<H: px[x,y+1]=c;
        if x+1<W and y+1<H: px[x+1,y+1]=c
bg=bg.convert('RGBA')
random.seed(4); FLAKES=[(random.uniform(0,W),random.uniform(0,H),random.uniform(1.5,4.5),random.uniform(40,110),random.uniform(0,6.28)) for _ in range(90)]
glow=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(glow).ellipse([W/2-460,560,W/2+460,1480],fill=(232,197,122,70)); glow=glow.filter(ImageFilter.GaussianBlur(110))

def ctext(d,y,txt,f,fill,a=255,cx=W/2):
    w=d.textlength(txt,font=f); d.text((cx-w/2,y),txt,font=f,fill=fill+(a,))
def gold_text(fr,y,txt,size,a=255,scale=1.0):
    f=F(BLK,int(size*scale)); tmp=Image.new('L',(W,int(size*scale*1.3)),0); dd=ImageDraw.Draw(tmp)
    w=dd.textlength(txt,font=f); dd.text(((W-w)/2,0),txt,font=f,fill=255)
    grad=Image.new('RGBA',tmp.size); gd=ImageDraw.Draw(grad)
    for yy in range(tmp.size[1]):
        k=yy/tmp.size[1]; c=tuple(int(a1+(b1-a1)*k) for a1,b1 in zip((255,243,207),(184,137,47))); gd.line([(0,yy),(W,yy)],fill=c+(255,))
    grad.putalpha(tmp.point(lambda v:v*a//255)); fr.alpha_composite(grad,(0,int(y-size*(scale-1)*0.5)))
def pill(d,cx,y,txt,f,bgc,fg,a):
    w=d.textlength(txt,font=f); d.rounded_rectangle([cx-w/2-30,y,cx+w/2+30,y+f.size*1.6],40,fill=bgc+(a,)); d.text((cx-w/2,y+f.size*0.25),txt,font=f,fill=fg+(a,))

def scene_at(t):
    i=0
    for j,s in enumerate(starts):
        if t>=s: i=j
    return i,t-starts[i]

def frame(n):
    t=n/FPS; fr=bg.copy(); d=ImageDraw.Draw(fr)
    # nieve
    for (x,y,r,v,ph) in FLAKES:
        yy=(y+v*t)%H; xx=x+18*math.sin(t*0.8+ph); d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=(255,255,255,int(60+r*25)))
    i,lt=scene_at(t); k=SC[i][0]; sd=durs[i]+GAP[k]
    fo=1-ease((lt-(sd-0.25))/0.25) if k!='pago' else 1  # salida
    if k=='hook':
        a=int(255*ease(lt/0.4)*fo)
        lg=logo.copy(); lg.putalpha(lg.split()[3].point(lambda v:v*a//255)); fr.alpha_composite(lg,((W-190)//2,330))
        ctext(d,640,'¿Un Invicta para',F(BLK,96),WHITE,a); ctext(d,750,'esta Navidad',F(BLK,96),WHITE,a)
        a2=int(255*ease((lt-0.7)/0.4)*fo); ctext(d,890,'sin gastar de más?',F(BLK,96),RED,a2)
        a3=int(255*ease((lt-1.4)/0.4)*fo); pill(d,W/2,1080,'RIFA NAVIDEÑA TICOTIME',F(BLD,44),(232,197,122),NAVY,a3)
        # mini relojes abajo
        for j,kk in enumerate(['p3','p1','p2']):
            aa=int(255*ease((lt-1.0-j*0.15)/0.5)*fo)
            if aa<=0: continue
            c=SMALL[kk].copy(); c.putalpha(c.split()[3].point(lambda v:v*aa//255)); fr.alpha_composite(c,(int(45+j*345),1300+int(40*(1-ease((lt-1.0-j*0.15)/0.5)))))
    elif k=='rifa':
        s=0.6+0.4*back(lt/0.6); a=int(255*min(1,lt/0.25)*fo)
        fr.alpha_composite(glow)
        gold_text(fr,700,'GRAN',230,a,s); gold_text(fr,930,'RIFA',230,a,s)
        a2=int(255*ease((lt-0.5)/0.4)*fo); ctext(fr and d,1220,'3 relojes Invicta · 3 ganadores',F(SER,58),WHITE,a2)
        ctext(d,1310,'100 % originales',F(BLD,44),GOLD,a2)
    elif k in PZ:
        lab,name,sub,price,ref=PZ[k]
        if k=='p1': fr.alpha_composite(glow)
        e=ease(lt/0.55); a=int(255*e*fo)
        pill(d,W/2,250,lab,F(BLK,64),GOLD if k=='p1' else (216,221,229),NAVY,a)
        c=CARDS[k]; z=1.0+0.05*min(1,lt/sd); cw,ch=int(720*z*(0.85+0.15*e)),int(880*z*(0.85+0.15*e)); c=c.resize((cw,ch),Image.LANCZOS)
        if k=='p1':
            b=Image.new('RGBA',(cw+24,ch+24),(0,0,0,0)); ImageDraw.Draw(b).rounded_rectangle([0,0,cw+23,ch+23],48,fill=GOLD+(255,)); b.alpha_composite(c,(12,12)); c=b; cw+=24; ch+=24
        c.putalpha(c.split()[3].point(lambda v:v*a//255))
        sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([(W-cw)/2+10,420+30,(W+cw)/2+10,420+ch+30],48,fill=(0,0,0,int(110*e*fo))); fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(25)))
        fr.alpha_composite(c,((W-cw)//2,420+int(60*(1-e)))); d=ImageDraw.Draw(fr)
        a2=int(255*ease((lt-0.35)/0.4)*fo)
        ctext(d,1390,name,F(BLK,72),WHITE,a2); ctext(d,1485,sub,F(MED,44),MUTED,a2)
        ctext(d,1570,'Valor '+money(price),F(BLD,52),GOLD,a2)
    elif k=='num':
        a=int(255*ease(lt/0.4)*fo); s=back(lt/0.5)
        ctext(d,520,'NÚMERO A SOLO',F(BLD,60),WHITE,a)
        box=Image.new('RGBA',(W,H),(0,0,0,0)); bd=ImageDraw.Draw(box)
        bw,bh=int(800*max(0.5,s)),int(330*max(0.5,s)); bd.rounded_rectangle([(W-bw)/2,640,(W+bw)/2,640+bh],48,fill=GOLD+(a,))
        fr.alpha_composite(box); d=ImageDraw.Draw(fr)
        ctext(d,640+bh/2-118*max(0.5,s),money(1500),F(BLK,int(210*max(0.5,s))),NAVY,a)
        a2=int(255*ease((lt-0.8)/0.4)*fo); ctext(d,1080,'Del 00 al 99',F(BLK,96),WHITE,a2)
        a3=int(255*ease((lt-1.6)/0.4)*fo); ctext(d,1210,'¡Solo 100 números!',F(BLK,84),RED,a3)
        # mini cuadrícula
        for q in range(100):
            aq=int(255*ease((lt-1.0-q*0.012)/0.3)*fo)
            if aq<=0: continue
            cx=150+(q%10)*87; cy=1360+(q//10)*42
            d.rounded_rectangle([cx-38,cy,cx+38,cy+34],8,outline=GOLD+(aq,),width=2); ctext(d,cy+4,f'{q:02d}',F(BLD,24),WHITE,aq,cx)
    elif k=='fecha':
        a=int(255*ease(lt/0.4)*fo)
        ctext(d,420,'SORTEO',F(BLD,64),GOLD,a)
        # calendario
        cal=Image.new('RGBA',(W,H),(0,0,0,0)); cd=ImageDraw.Draw(cal); s=back(lt/0.5)
        cw,ch=int(520*max(.5,s)),int(560*max(.5,s)); x0=(W-cw)/2; y0=540
        cd.rounded_rectangle([x0,y0,x0+cw,y0+ch],40,fill=(255,255,255,a)); cd.rounded_rectangle([x0,y0,x0+cw,y0+ch*0.24],40,fill=RED+(a,)); cd.rectangle([x0,y0+ch*0.14,x0+cw,y0+ch*0.24],fill=RED+(a,))
        fr.alpha_composite(cal); d=ImageDraw.Draw(fr)
        ctext(d,y0+ch*0.05,'DICIEMBRE',F(BLK,int(56*max(.5,s))),WHITE,a)
        ctext(d,y0+ch*0.27,'13',F(BLK,int(300*max(.5,s))),NAVY,a)
        ctext(d,y0+ch*0.8,'DOMINGO',F(BLD,int(52*max(.5,s))),(90,98,112),a)
        a2=int(255*ease((lt-0.7)/0.4)*fo)
        ctext(d,1190,'Juega con los 3 primeros premios',F(BLD,54),WHITE,a2); ctext(d,1260,'de la Lotería Nacional (JPS)',F(BLD,54),WHITE,a2)
        a3=int(255*ease((lt-1.3)/0.4)*fo); ctext(d,1380,'1.º → Bolt Valkir   ·   2.º → Pro Diver   ·   3.º → Compass',F(MED,36),GOLD,a3)
    elif k=='pago':
        a=int(255*ease(lt/0.4))
        lg=logo.copy(); lg.putalpha(lg.split()[3].point(lambda v:v*a//255)); fr.alpha_composite(lg,((W-190)//2,300)); d=ImageDraw.Draw(fr)
        ctext(d,560,'Pagá por SINPE Móvil',F(BLK,78),WHITE,a)
        s=back((lt-0.3)/0.5); a2=int(255*ease((lt-0.3)/0.4))
        if a2>0: ctext(d,680,'8640-0835',F(BLK,int(170*max(.5,s))),GOLD,a2)
        a3=int(255*ease((lt-1.0)/0.4))
        ctext(d,920,'y mandá el comprobante',F(BLD,58),WHITE,a3); ctext(d,995,'por WhatsApp para apartar tu número',F(BLD,58),WHITE,a3)
        a4=int(255*ease((lt-1.8)/0.4)); pill(d,W/2,1150,'¡Apartá el tuyo antes de que se acaben!',F(BLK,42),RED,WHITE,a4)
        for j,kk in enumerate(['p3','p1','p2']):
            aa=int(255*ease((lt-2.2-j*0.12)/0.5))
            if aa<=0: continue
            c=SMALL[kk].copy(); c.putalpha(c.split()[3].point(lambda v:v*aa//255)); fr.alpha_composite(c,(int(45+j*345),1340))
        d=ImageDraw.Draw(fr); ctext(d,1760,'ticotimecr.com',F(MED,40),MUTED,a3)
    return fr.convert('RGB')

for n in range(N): frame(n).save(f'{TMP}/f_{n:04d}.jpg',quality=90)
# audio: voz en sus tiempos + música
mu=f'{TMP}/mu.wav'; subprocess.run(['python3',os.path.join(ENG,'music.py'),mu,str(D+0.5)],check=True)
inp=[]; flt=[]
for i,s in enumerate(starts):
    inp+=['-i',f'{TMP}/v{i}.mp3']; flt.append(f'[{i+1}:a]adelay={int(s*1000)}|{int(s*1000)},volume=1.6[v{i}]')
mix=''.join(f'[v{i}]' for i in range(len(starts)))
flt.append(f'[{len(starts)+1}:a]volume=0.22[m]'); flt.append(f'{mix}[m]amix=inputs={len(starts)+1}:normalize=0,afade=t=out:st={D-1}:d=1[a]')
out=os.path.join(ROOT,'social/reels/reel-rifa-navidad.mp4')
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{TMP}/f_%04d.jpg',*inp,'-i',mu,'-filter_complex',';'.join(flt),
  '-map','0:v','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(D),out],check=True)
Image.open(f'{TMP}/f_{int(1.9*FPS):04d}.jpg').save(out.replace('.mp4','.jpg'),quality=90)
print('ok',out)
