# Reel navideño "opciones de regalo": 3–4 relojes disponibles en un solo video.
# Gancho (titulo) -> una tarjeta por reloj con precio -> cierre con todos + "te conseguimos cualquier modelo".
# La voz se genera por partes, así cada reloj aparece justo cuando se nombra.
# uso: python3 social/engine/make_regalos.py social/engine/specs/<slug>.json
# spec: {"titulo":"3 regalos para él","sub":"por menos de ₡50.000","voz_intro":"...",
#        "items":[{"ref","name","price","oferta"(o null),"say"}, ...]}
import sys, os, json, math, subprocess, random, time
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
ENG=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,ENG)
import make_reel as R
W,H,FPS=R.W,R.H,R.FPS; ROOT=R.ROOT
RED=(190,28,48); GOLD=R.GOLD; WHITE=R.WHITE; MUT=R.MUTED; BG=R.BG; GREEN=(24,92,58)
F_B,F_X,F_M=R.F_B,R.F_X,R.F_M; font=R.font; fmt=R.fmt; ease=R.ease
CIERRE="¿Buscás otro modelo? Te lo conseguimos. Escribinos al ochenta y seis cuarenta, cero ocho treinta y cinco, o entrá a tico taim ce erre punto com."

def tts(txt,out):
    env=dict(os.environ,NO_PROXY='',no_proxy='')
    for k in range(5):
        p=subprocess.run(['python3',os.path.join(ENG,'tts.py'),txt,out,'es-CR-JuanNeural','+12%'],env=env,capture_output=True)
        if p.returncode==0 and os.path.exists(out) and os.path.getsize(out)>1000: return R.dur(out)
        time.sleep(4)
    sys.exit('fallo la voz: '+p.stderr.decode()[-300:])

def ctext(d,y,t,f,c,a=255): R.ctext(d,y,t,f,c,a)
def wrap(d,t,f,maxw):
    ls=[];cur=''
    for w in t.split():
        c2=(cur+' '+w).strip()
        if d.textlength(c2,font=f)>maxw and cur: ls.append(cur);cur=w
        else: cur=c2
    return ls+[cur]

def main(path):
    sp=json.load(open(path)); slug=os.path.basename(path)[:-5]; tmpa=f'/tmp/rg_{slug}'; os.makedirs(tmpa,exist_ok=True)
    items=sp['items']
    # voz por partes
    parts=[('intro',sp['voz_intro'])]+[(f'i{k}',it['say']) for k,it in enumerate(items)]+[('cierre',CIERRE)]
    durs=[]
    for k,(nm,tx) in enumerate(parts): durs.append(tts(tx,f'{tmpa}/{k:02d}.mp3')+0.35)
    # concatenar voces con silencios
    lst=open(f'{tmpa}/l.txt','w')
    for k in range(len(parts)):
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{tmpa}/{k:02d}.mp3','-af','apad=pad_dur=0.35','-ar','44100','-ac','2',f'{tmpa}/p{k:02d}.wav'],check=True)
        lst.write(f"file '{tmpa}/p{k:02d}.wav'\n")
    lst.close()
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'{tmpa}/l.txt',f'{tmpa}/voz.wav'],check=True)
    durs=[max(d,2.4) for d in durs]; durs[-1]+=1.2
    starts=[sum(durs[:k]) for k in range(len(durs))]; D=sum(durs)
    mu=f'{tmpa}/music.wav'; subprocess.run(['python3',os.path.join(ENG,'music.py'),mu,str(D+2)],check=True)
    # imágenes
    cards=[]
    for it in items:
        im=R.load(str(it['ref']),'L'); c=R.card(im,760,760).convert('RGBA')
        m=Image.new('L',c.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,c.width-1,c.height-1],radius=50,fill=255); c.putalpha(m); cards.append(c)
    thumbs=[]
    for it in items:
        c=R.card(R.load(str(it['ref']),'L'),300,300).convert('RGBA'); m=Image.new('L',c.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,299,299],radius=30,fill=255); c.putalpha(m); thumbs.append(c)
    # fondo navideño
    bg=Image.new('RGBA',(W,H)); gd=ImageDraw.Draw(bg)
    for y in range(H):
        k=max(0,1-abs(y-H*0.45)/(H*0.7)); gd.line([(0,y),(W,y)],fill=(int(8+40*k),int(14+16*k),int(24+22*k),255))
    rnd=random.Random(7); SNOW=[(rnd.uniform(0,W),rnd.uniform(0,H),rnd.uniform(2,6),rnd.uniform(40,110),rnd.uniform(0,6.28)) for _ in range(90)]
    logo=Image.open(os.path.join(ROOT,'public/assets/logo.png')).convert('RGBA').resize((96,96),Image.LANCZOS)
    tmp=f'{tmpa}/fr'; os.makedirs(tmp,exist_ok=True)
    N=int(D*FPS); n=len(items)
    for i in range(N):
        t=i/FPS; fr=bg.copy(); d=ImageDraw.Draw(fr)
        for sx,sy,sr,sv,sp_ in SNOW:
            yy=(sy+sv*t)%H; xx=sx+18*math.sin(t*1.3+sp_); d.ellipse([xx-sr,yy-sr,xx+sr,yy+sr],fill=(255,255,255,int(60+25*sr)))
        fr.alpha_composite(logo,(60,52)); d.text((172,62),'TicoTime',font=font(F_X,46),fill=WHITE+(255,)); d.text((172+d.textlength('TicoTime ',font=font(F_X,46)),62),'CR',font=font(F_X,46),fill=GOLD+(255,))
        d.text((174,114),'Regalos de Navidad',font=font(F_M,28),fill=MUT+(255,))
        seg=max(k for k in range(len(starts)) if starts[k]<=t); lt=t-starts[seg]
        if seg==0:   # gancho
            a=int(255*ease(lt/0.4)); z=0.9+0.1*ease(lt/0.4)
            f=font(F_X,int(96*z)); ls=wrap(d,sp['titulo'],f,W-140); y=560
            hh=len(ls)*112+60; d.rounded_rectangle([50,y-30,W-50,y-30+hh],radius=50,fill=RED+(a,))
            for q,l in enumerate(ls): ctext(d,y+q*112,l,f,WHITE,a)
            if sp.get('sub'): ctext(d,y+hh+20,sp['sub'],font(F_X,64),GOLD,a)
            # vista previa de los relojes abajo
            tw=n*220+(n-1)*24; x0=(W-tw)//2
            for k,th in enumerate(thumbs):
                aa=ease((lt-0.3-0.15*k)/0.4)
                if aa<=0: continue
                s2=th.resize((220,220),Image.LANCZOS); s2.putalpha(s2.split()[3].point(lambda v:int(v*aa)))
                fr.alpha_composite(s2,(x0+k*244,1240+int((1-aa)*60)))
        elif seg<=n:  # cada reloj
            it=items[seg-1]; c=cards[seg-1]; e=ease(lt/0.45)
            z=(0.88+0.12*e)*(1+0.03*lt/durs[seg]); ang=1.8*math.sin(2*math.pi*t/3.4)
            w2=c.resize((int(c.width*z),int(c.height*z)),Image.BILINEAR).rotate(ang,resample=Image.BILINEAR,expand=True)
            x=int((W-w2.width)/2+(1-e)*300); y=int(860-w2.height/2+10*math.sin(t*2.6))
            sh=Image.new('RGBA',(W,H),(0,0,0,0)); s_img=Image.new('RGBA',w2.size,(0,0,0,255)); s_img.putalpha(w2.split()[3].point(lambda v:int(v*0.5)))
            sh.alpha_composite(s_img,(x+12,y+28)); fr=Image.alpha_composite(fr,sh.filter(ImageFilter.GaussianBlur(18))); fr.alpha_composite(w2,(x,y)); d=ImageDraw.Draw(fr)
            lab=f'OPCIÓN {seg}'; f=font(F_X,44); tw=d.textlength(lab,font=f)
            d.rounded_rectangle([(W-tw)/2-36,200,(W+tw)/2+36,272],radius=36,fill=RED+(255,)); ctext(d,210,lab,f,WHITE)
            fin=it.get('oferta') or it['price']
            ctext(d,1300,it['name'],font(F_B,56) if d.textlength(it['name'],font=font(F_B,56))<W-80 else font(F_B,44),WHITE)
            ctext(d,1390,fmt(fin),font(F_X,120),GOLD)
            if it.get('oferta'):
                s2='antes '+fmt(it['price']); f2=font(F_M,44); w_=d.textlength(s2,font=f2); x2=(W-w_)/2
                d.text((x2,1535),s2,font=f2,fill=MUT+(255,)); d.line([(x2-6,1563),(x2+w_+6,1563)],fill=MUT+(255,),width=5)
            ctext(d,1610,f"Ref. {it['ref']} · Entrega inmediata",font(F_M,38),MUT)
            # puntos de progreso
            for q in range(n):
                cx=W/2+(q-(n-1)/2)*40; col=GOLD if q==seg-1 else (90,98,106); d.ellipse([cx-9,1700-9,cx+9,1700+9],fill=col+(255,))
        else:        # cierre
            a=int(255*ease(lt/0.45))
            cols=min(n,2) if n==4 else n; rows=math.ceil(n/cols); s=300 if n<=3 else 280; g=30
            gw=cols*s+(cols-1)*g; x0=(W-gw)//2
            tot=110+rows*(s+g+64)+30+430; y0=int(260+(1600-tot)/2)+110
            ctext(d,y0-110,'¿Cuál le regalás?',font(F_X,76),WHITE,a)
            for k,th in enumerate(thumbs):
                r_,c_=divmod(k,cols); th2=th.resize((s,s),Image.LANCZOS); th2.putalpha(th2.split()[3].point(lambda v:v*a//255))
                fr.alpha_composite(th2,(x0+c_*(s+g),y0+r_*(s+g+64)))
                it=items[k]; fin=it.get('oferta') or it['price']
                tx=fmt(fin); f=font(F_X,44); d.text((x0+c_*(s+g)+(s-d.textlength(tx,font=f))/2,y0+r_*(s+g+64)+s+8),tx,font=f,fill=GOLD+(a,))
            yb=y0+rows*(s+g+64)+30
            d.rounded_rectangle([60,yb,W-60,yb+130],radius=40,fill=RED+(a,)); ctext(d,yb+16,'¿Buscás otro modelo?',font(F_X,52),WHITE,a); ctext(d,yb+76,'¡Te lo conseguimos!',font(F_B,40),(255,224,160),a)
            d.rounded_rectangle([80,yb+170,W-80,yb+340],radius=30,fill=(18,32,25,a),outline=(158,182,164,a),width=3)
            ctext(d,yb+184,'WhatsApp 8640-0835',font(F_X,66),(229,242,232),a); ctext(d,yb+270,'ticotimecr.com',font(F_B,46),GOLD,a)
            ctext(d,yb+380,'Originales · Garantía 3 meses · Apartá y pagá en tractos',font(F_M,32),MUT,a)
        fr.convert('RGB').save(f'{tmp}/{i:04d}.jpg',quality=90)
    out=os.path.join(ROOT,'social/reels',f'reel-{slug}.mp4')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{tmp}/%04d.jpg','-i',mu,'-i',f'{tmpa}/voz.wav',
      '-filter_complex',f'[1:a]volume=0.2,atrim=0:{D}[m];[2:a]volume=1.6[v];[m][v]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={D-0.6}:d=0.6[a]',
      '-map','0:v','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(D),out],check=True)
    Image.open(f'{tmp}/{int(1.0*FPS):04d}.jpg').save(out.replace('.mp4','.jpg'),quality=90)
    subprocess.run(['rm','-rf',tmpa]); print('ok',out,round(D,1),'s')

if __name__=='__main__': main(sys.argv[1])
