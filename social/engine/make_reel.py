import sys, os, subprocess, math, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
W,H,FPS=1080,1920,30
ENG=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(ENG))
LOC=os.path.join(ROOT,'public/assets/disponibles'); WEB=os.path.join(ROOT,'social/fotos')
F_B='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; F_X='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'; F_M='/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf'
GOLD=(239,198,80); GOLD2=(213,166,42); WHITE=(245,243,238); MUTED=(170,178,186); BG=(5,8,12)
import glob
def photos_for(ref):
    fs=sorted(glob.glob(f'{WEB}/{ref}_*.jpg')+glob.glob(f'{WEB}/{ref}_*.png')+glob.glob(f'{WEB}/{ref}_*.webp'))
    skip=set(open(f'{WEB}/omitir.txt').read().split()) if os.path.exists(f'{WEB}/omitir.txt') else set()
    fs=[os.path.basename(f) for f in fs if os.path.basename(f) not in skip]
    if os.path.exists(f'{LOC}/{ref}.webp') and len(fs)<2: fs.append('L')
    return fs or ['L']
FC={}
def font(p,s):
    k=(p,s)
    if k not in FC: FC[k]=ImageFont.truetype(p,s)
    return FC[k]
def fmt(n): return '₡'+f'{n:,}'.replace(',','.')
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def ctext(d,y,txt,f,fill,a=255):
    w=d.textlength(txt,font=f); d.text(((W-w)/2,y),txt,font=f,fill=fill+(a,))
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def load(ref,n):
    im=Image.open(f'{LOC}/{ref}.webp' if n=='L' else f'{WEB}/{n}').convert('RGB')
    # recortar bordes blancos
    bgw=Image.new('RGB',im.size,(255,255,255)); bb=ImageChops.difference(im,bgw).convert('L').point(lambda v:255 if v>18 else 0).getbbox()
    if bb:
        pad=int(0.06*max(im.size)); bb=(max(0,bb[0]-pad),max(0,bb[1]-pad),min(im.width,bb[2]+pad),min(im.height,bb[3]+pad)); im=im.crop(bb)
    return im
def card(im,box_w=820,box_h=820):
    s=min(box_w/im.width,box_h/im.height); im=im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(box_w,box_h),im.getpixel((2,2))); c.paste(im,((box_w-im.width)//2,(box_h-im.height)//2))
    return c
def make(spec,r,out):
    ref=spec['ref']; vo=spec['_voz']; D=dur(vo)+1.3
    fin=r['oferta'] or r['price']; ade=25000 if fin>=100000 else 20000 if fin>=50000 else 15000
    photos=[load(ref,n) for n in photos_for(ref)]
    # intro opcional con clip de IA (spec['intro'] = ruta relativa al repo)
    IL=0; IF=[]
    if spec.get('intro'):
        idir=f'/tmp/intro_{ref}'; os.makedirs(idir,exist_ok=True)
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',os.path.join(ROOT,spec['intro']),'-vf','scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30','-q:v','3',f'{idir}/%04d.jpg'],check=True)
        # fotos extra de IA: pantalla completa con acercamiento lento (3.3 s cada una), después del clip
        for j,n in enumerate(spec.get('extra_photos',[])):
            subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',os.path.join(ROOT,n),'-vf',
              'scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z=\'1.12-0.12*on/99\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d=99:s=1080x1920:fps=30',
              '-frames:v','99','-q:v','3',f'{idir}/x{j}_%04d.jpg'],check=True)
        IF=sorted(os.listdir(idir)); IF=[f'{idir}/{f}' for f in IF if not f.startswith('x')]+[f'{idir}/{f}' for f in IF if f.startswith('x')]; IL=len(IF)/FPS
    # segmentos: si hay 1 foto, alternar completa y acercamiento
    segL=3.3; nseg=math.ceil(max(1,D-IL)/segL); segs=[]
    for i in range(nseg):
        if len(photos)==1:
            im=photos[0]
            if i%2==1:
                cw,ch=int(im.width*0.62),int(im.height*0.62); x0=(im.width-cw)//2; y0=(im.height-ch)//2
                im=im.crop((x0,y0,x0+cw,y0+ch))
            segs.append(card(im))
        else: segs.append(card(photos[i%len(photos)]))
    m=Image.new('L',segs[0].size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,segs[0].width-1,segs[0].height-1],radius=56,fill=255)
    segs=[s.convert('RGBA') for s in segs]
    for s in segs: s.putalpha(m)
    # fondo a partir de la primera foto
    b0=photos[0].resize((W,int(W*photos[0].height/photos[0].width))); b0=b0.resize((int(b0.width*H/b0.height*1.0),H)) if b0.height<H else b0
    b0=b0.crop(((b0.width-W)//2,(b0.height-H)//2,(b0.width-W)//2+W,(b0.height-H)//2+H)).filter(ImageFilter.GaussianBlur(45))
    b0=ImageEnhance.Brightness(b0).enhance(0.28).convert('RGBA')
    grad=Image.new('RGBA',(W,H)); gd=ImageDraw.Draw(grad)
    for y in range(H): gd.line([(0,y),(W,y)],fill=BG+(min(235,int(170*abs(y-H*0.42)/(H*0.58))+40),))
    bg=Image.alpha_composite(b0,grad)
    tmp=f'/tmp/reel_{ref}'; os.makedirs(tmp,exist_ok=True)
    N=int(D*FPS); feats=spec['feats']; fstart=2.0; fend=D-4.6; fl=(fend-fstart)/len(feats)
    fT=font(F_B,50); fS=font(F_M,48); fN=font(F_B,56); fF=font(F_B,54); fw=font(F_X,66); fsm=font(F_M,34); fpill=font(F_B,50)
    for i in range(N):
        t=i/FPS
        intro_on=IL>0 and t<IL
        if intro_on:
            fr=Image.open(IF[min(i,len(IF)-1)]).convert('RGBA')
            ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
            for y in range(0,560): od.line([(0,y),(W,y)],fill=(0,0,0,int(200*(1-y/560))))
            for y in range(1250,H): od.line([(0,y),(W,y)],fill=(0,0,0,int(220*(y-1250)/(H-1250))))
            fr=Image.alpha_composite(fr,ov)
        else: fr=bg.copy()
        d=ImageDraw.Draw(fr)
        tp=t-IL
        top=64; tag='OFERTA' if r['oferta'] else 'ENTREGA INMEDIATA'
        tw=d.textlength(tag,font=fT); px=(W-tw)/2-34
        d.rounded_rectangle([px,top,px+tw+68,top+80],radius=40,fill=GOLD2+(255,)); d.text((px+34,top+8),tag,font=fT,fill=BG+(255,))
        bp=(t*112/60)%1; pz=1+0.04*math.exp(-bp*6); ctext(d,top+100-int(70*(pz-1)),fmt(fin),font(F_X,int(140*pz)),GOLD)
        if r['oferta']:
            s2='antes '+fmt(r['price']); w2=d.textlength(s2,font=fS); x2=(W-w2)/2; y2=top+280
            d.text((x2,y2),s2,font=fS,fill=MUTED+(255,)); d.line([(x2-6,y2+33),(x2+w2+6,y2+33)],fill=MUTED+(255,),width=5)
        # foto actual (con cruce entre segmentos)
        k=min(int(max(0,tp)//segL),nseg-1); lt=max(0,tp)-k*segL
        def draw_seg(img,lt,alpha=255,dx=0):
            ein=ease(lt/0.45); z=(0.86+0.14*ein)*(1+0.045*lt/segL)
            ang=2.2*math.sin(2*math.pi*(t)/3.4)
            w2=img.resize((int(img.width*z),int(img.height*z)),Image.BILINEAR)
            ph=(lt%segL)/0.9
            if 0.3<ph<=1.3:
                p=ph-0.3; gl=Image.new('L',w2.size,0); g2=ImageDraw.Draw(gl); gx=int(-w2.width*0.6+p*w2.width*1.8)
                g2.polygon([(gx,0),(gx+90,0),(gx-70,w2.height),(gx-160,w2.height)],fill=110); gl=ImageChops.multiply(gl.filter(ImageFilter.GaussianBlur(25)),w2.split()[3])
                wh=Image.new('RGBA',w2.size,(255,255,255,0)); wh.putalpha(gl); w2=Image.alpha_composite(w2,wh)
            w2=w2.rotate(ang,resample=Image.BILINEAR,expand=True)
            if alpha<255: w2.putalpha(w2.split()[3].point(lambda v:v*alpha//255))
            cy=885+12*math.sin(2*math.pi*t/2.4); x=int((W-w2.width)/2+dx); y=int(cy-w2.height/2)
            return w2,x,y
        layers=[] if intro_on else None
        if layers is None:
          layers=[]
          slide=int((1-ease(lt/0.45))*260) if (k>0 or IL>0) else 0
          layers.append(draw_seg(segs[k],lt,255,slide))
          if k>0 and lt<0.25:
              a=int(255*(1-lt/0.25)); layers.insert(0,draw_seg(segs[k-1],lt+segL,a,-int((lt/0.25)*200)))
        for w2,x,y in layers:
            sh=Image.new('RGBA',(W,H),(0,0,0,0)); s_img=Image.new('RGBA',w2.size,(0,0,0,255)); s_img.putalpha(w2.split()[3].point(lambda v:int(v*0.55)))
            sh.alpha_composite(s_img,(x+12,y+30)); fr=Image.alpha_composite(fr,sh.filter(ImageFilter.GaussianBlur(18))); fr.alpha_composite(w2,(x,y))
        d=ImageDraw.Draw(fr)
        name=spec.get('name',r['name']); fNn=fN if d.textlength(name,font=fN)<W-80 else font(F_B,44)
        ctext(d,1340,name,fNn,WHITE)
        # caracteristicas una por una
        if fstart<=t<fend:
            j=min(int((t-fstart)//fl),len(feats)-1); lt2=t-fstart-j*fl
            a=int(255*min(ease(lt2/0.35),ease((fl-lt2)/0.3))); dy=int((1-ease(lt2/0.35))*40)
            ft=('✓ ' if False else '')+feats[j]; fw2=d.textlength(ft,font=fF); bx=(W-fw2)/2-46
            d.rounded_rectangle([bx,1440+dy,bx+fw2+92,1440+dy+100],radius=50,fill=(16,24,34,a),outline=GOLD+(a,),width=4)
            d.text((bx+46,1440+dy+18),ft,font=fF,fill=WHITE+(a,))
            # puntitos de progreso
            for q in range(len(feats)):
                cx=W/2+(q-(len(feats)-1)/2)*34; col=GOLD if q==j else (90,98,106)
                d.ellipse([cx-7,1568-7,cx+7,1568+7],fill=col+(255,))
        # cierre
        a=int(255*ease((t-(D-4.4))/0.45))
        if a>0:
            p='Apartalo con '+fmt(ade); pw=d.textlength(p,font=fpill); x=(W-pw)/2-44
            d.rounded_rectangle([x,1430,x+pw+88,1530],radius=50,outline=GOLD+(a,),width=4,fill=(16,24,34,a)); d.text((x+44,1444),p,font=fpill,fill=WHITE+(a,))
            d.rounded_rectangle([80,1570,W-80,1730],radius=30,fill=(18,32,25,a),outline=(158,182,164,a),width=3)
            ctext(d,1582,'WhatsApp 8640-0835',fw,(229,242,232),a); ctext(d,1672,'Original · Garantía 3 meses · ticotimecr.com',fsm,MUTED,a)
        fr.convert('RGB').save(f'{tmp}/{i:04d}.jpg',quality=90)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{tmp}/%04d.jpg','-i',spec['_music'],'-i',vo,
      '-filter_complex',f'[1:a]volume=0.22,atrim=0:{D}[m];[2:a]adelay=350|350,volume=1.6[v];[m][v]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={D-0.6}:d=0.6[a]',
      '-map','0:v','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','-t',str(D),out],check=True)
    Image.open(f'{tmp}/{int(1.2*FPS):04d}.jpg').save(out.replace('.mp4','.jpg'),quality=90)
    subprocess.run(['rm','-rf',tmp])
if __name__=='__main__':
    # uso: python3 social/engine/make_reel.py social/engine/specs/<slug>.json
    import time
    sp=json.load(open(sys.argv[1])); slug=os.path.basename(sys.argv[1])[:-5]
    r={'ref':str(sp['ref']),'name':sp['name'],'price':int(sp['price']),'oferta':int(sp['oferta']) if sp.get('oferta') else None}
    sp['ref']=str(sp['ref'])
    fin=r['oferta'] or r['price']; ade=25000 if fin>=100000 else 20000 if fin>=50000 else 15000
    words={15000:'quince mil',20000:'veinte mil',25000:'veinticinco mil'}
    txt=sp['say']+f" Original y con garantía. Apartalo con {words[ade]}, y escribinos al WhatsApp."
    vo=f'/tmp/voz_{slug}.mp3'; env=dict(os.environ,NO_PROXY='',no_proxy='')
    for k in range(5):
        p=subprocess.run(['python3',os.path.join(ENG,'tts.py'),txt,vo,'es-CR-JuanNeural','+14%'],env=env,capture_output=True)
        if p.returncode==0 and os.path.exists(vo) and os.path.getsize(vo)>1000: break
        time.sleep(4)
    else: sys.exit('fallo la voz: '+p.stderr.decode()[-300:])
    mu=f'/tmp/music_{slug}.wav'; subprocess.run(['python3',os.path.join(ENG,'music.py'),mu,str(dur(vo)+3)],check=True)
    sp['_voz']=vo; sp['_music']=mu
    os.makedirs(os.path.join(ROOT,'social/reels'),exist_ok=True)
    out=os.path.join(ROOT,'social/reels',f'reel-{slug}.mp4')
    make(sp,r,out); print('ok',out)
