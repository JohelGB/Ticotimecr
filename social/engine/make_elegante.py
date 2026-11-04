# Reel "elegante" (estilo marca de lujo): clip de IA a pantalla completa + textos finos + cierre TicoTime con precio revelado.
# uso: python3 social/engine/make_elegante.py social/engine/specs/<slug>.json
# spec: {"ref","name","line","price","oferta"|null,"clip":"social/fotos/ai_<ref>_x.mp4","feats":[...2-3],"pregunta":"¿Cuánto creés que cuesta?"}
import sys, os, json, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ENG=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(ENG))
W,H,FPS=1080,1920,30
SERIF='/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf'; SERIF_I='/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
SANS='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'; SANSB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
GOLD=(226,190,120); WHITE=(246,242,234); NAVY=(10,20,36)
FC={}
def F(p,s,wght=None):
    k=(p,s,wght)
    if k not in FC:
        f=ImageFont.truetype(p,s)
        if wght:
            try: f.set_variation_by_axes([wght])
            except Exception: pass
        FC[k]=f
    return FC[k]
def fmt(n): return '₡'+f'{n:,}'.replace(',','.')
def ease(x): x=max(0,min(1,x)); return 1-(1-x)**3
def spaced(d,y,txt,f,fill,a,track=6,cx=W/2):
    ws=[d.textlength(c,font=f) for c in txt]; tot=sum(ws)+track*(len(txt)-1); x=cx-tot/2
    for c,w in zip(txt,ws): d.text((x,y),c,font=f,fill=fill+(a,)); x+=w+track
    return tot
def ctext(d,y,txt,f,fill,a):
    w=d.textlength(txt,font=f); d.text(((W-w)/2,y),txt,font=f,fill=fill+(a,))
def money(d,y,n,size,fill,a,italic=False):
    # Lora no tiene el signo ₡: se dibuja con Inter y los números con Lora
    fs=F(SANS,int(size*0.92)); fn=F(SERIF_I if italic else SERIF,size,600); num=f'{n:,}'.replace(',','.')
    w1=d.textlength('₡',font=fs); w2=d.textlength(num,font=fn); x=(W-w1-w2-4)/2
    d.text((x,y+int(size*0.06)),'₡',font=fs,fill=fill+(a,)); d.text((x+w1+4,y),num,font=fn,fill=fill+(a,)); return x,w1+w2+4
def fade(t,t0,t1,fi=0.5,fo=0.5): return int(255*min(ease((t-t0)/fi),ease((t1-t)/fo))) if t0<=t<=t1 else 0
sp=json.load(open(sys.argv[1])); slug=os.path.basename(sys.argv[1])[:-5]
clip=os.path.join(ROOT,sp['clip']); tmp=f'/tmp/eleg_{slug}'; os.makedirs(tmp,exist_ok=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',clip,'-vf','scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=contrast=1.04:saturation=1.05','-q:v','2',f'{tmp}/c_%04d.jpg'],check=True)
CF=sorted(f for f in os.listdir(tmp) if f.startswith('c_')); CL=len(CF)/FPS
END=4.8; D=CL+END; N=int(D*FPS)
fin=sp['oferta'] or sp['price']
logo=Image.open(os.path.join(ROOT,'public/assets/logo.png')).convert('RGBA').resize((330,330),Image.LANCZOS)
# degradados
top=Image.new('RGBA',(W,H),(0,0,0,0)); td=ImageDraw.Draw(top)
for y in range(520): td.line([(0,y),(W,y)],fill=(0,0,0,int(150*(1-y/520))))
for y in range(1180,H): td.line([(0,y),(W,y)],fill=(0,0,0,int(200*((y-1180)/(H-1180))**1.2)))
feats=sp['feats']; n=len(feats)
for i in range(N):
    t=i/FPS
    if t<CL:
        fr=Image.open(f'{tmp}/{CF[min(i,len(CF)-1)]}').convert('RGBA'); fr=Image.alpha_composite(fr,top)
        if t>CL-0.6:  # fundido a azul marino
            fr=Image.blend(fr,Image.new('RGBA',(W,H),NAVY+(255,)),ease((t-(CL-0.6))/0.6))
    else:
        fr=Image.new('RGBA',(W,H),NAVY+(255,))
        g=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g); gd.ellipse([W/2-520,520,W/2+520,1560],fill=(40,60,95,120)); fr=Image.alpha_composite(fr,g.filter(ImageFilter.GaussianBlur(120)))
    d=ImageDraw.Draw(fr)
    # 1) pregunta arriba
    a=fade(t,0.4,4.2)
    if a: ctext(d,150,sp.get('pregunta','¿Cuánto creés que cuesta?'),F(SERIF_I,58),WHITE,a)
    # 2) nombre
    a=fade(t,3.6,CL-0.7,0.7,0.5)
    if a:
        spaced(d,1440,sp['name'].upper(),F(SERIF,46,500),WHITE,a,track=5)
        d.line([(W/2-70,1515),(W/2+70,1515)],fill=GOLD+(a,),width=2)
        ctext(d,1535,sp['line'],F(SERIF_I,40),(220,214,200),a)
    # 3) características una a una
    if n:
        s0=6.0; L=(CL-0.9-s0)/n
        for j,ft in enumerate(feats):
            a=fade(t,s0+j*L,s0+(j+1)*L-0.1,0.5,0.4)
            if a: spaced(d,1650,'— '+ft.upper(),F(SERIF,34,450),GOLD,a,track=4)
    # 4) cierre
    if t>=CL:
        lt=t-CL
        a=int(255*ease(lt/0.6)); lg=logo.copy(); lg.putalpha(lg.split()[3].point(lambda v:v*a//255)); fr.alpha_composite(lg,(int((W-330)/2),300)); d=ImageDraw.Draw(fr)
        a=int(255*ease((lt-0.5)/0.6))
        spaced(d,700,sp['name'].upper(),F(SERIF,40,500),WHITE,a,track=5)
        a=int(255*ease((lt-1.0)/0.6))
        ctext(d,800,'¿Acertaste?',F(SERIF_I,50),(220,214,200),a)
        money(d,880,fin,120,GOLD,a)
        if sp['oferta']:
            x2,w2=money(d,1082,sp['price'],40,(170,170,170),a,italic=True); d.line([(x2-4,1110),(x2+w2+4,1110)],fill=(170,170,170,a),width=2)
            ctext(d,1042,'antes',F(SERIF_I,30),(170,170,170),a)
        a=int(255*ease((lt-1.6)/0.6))
        d.line([(W/2-90,1175),(W/2+90,1175)],fill=GOLD+(a,),width=2)
        ctext(d,1215,'Escribinos por WhatsApp',F(SERIF_I,50),WHITE,a)
        ctext(d,1290,'8640-0835',F(SERIF,92,600),GOLD,a)
        ctext(d,1430,'Original · Garantía 3 meses · Apartados',F(SANS,34),(200,196,186),a)
        ctext(d,1482,'ticotimecr.com',F(SANS,34),(200,196,186),a)
    fr.convert('RGB').save(f'{tmp}/f_{i:04d}.jpg',quality=92)
mu=f'/tmp/amb_{slug}.wav'; subprocess.run(['python3',os.path.join(ENG,'ambient.py'),mu,str(D+0.5)],check=True)
out=os.path.join(ROOT,'social/reels',f'reel-{slug}.mp4')
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{tmp}/f_%04d.jpg','-i',mu,'-filter_complex',f'[1:a]volume=0.9,afade=t=out:st={D-1.2}:d=1.2[a]','-map','0:v','-map','[a]',
  '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(D),out],check=True)
Image.open(f'{tmp}/f_{int(2.0*FPS):04d}.jpg').save(out.replace('.mp4','.jpg'),quality=90)
subprocess.run(['rm','-rf',tmp]); print('ok',out)
