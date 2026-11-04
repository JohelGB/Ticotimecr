import numpy as np, scipy.io.wavfile as wf, sys
SR=44100; BPM=112; beat=60/BPM; DUR=float(sys.argv[2]) if len(sys.argv)>2 else 9.2
n=int(SR*DUR); t=np.arange(n)/SR; out=np.zeros((n,2))
rng=np.random.default_rng(7)
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR)
    if i>=n: return
    e=min(n,i+len(sig)); s=sig[:e-i]*gain
    out[i:e,0]+=s*(1-pan)/1; out[i:e,1]+=s*(1+pan)/1
def env(L,a=0.005,d=0.2):
    x=np.arange(int(L*SR))/SR; return np.minimum(1,x/a)*np.exp(-x/d)
def kick():
    L=0.35; x=np.arange(int(L*SR))/SR; f=50+90*np.exp(-x*30)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*9)
def hat(open_=False):
    L=0.12 if not open_ else 0.3; x=rng.standard_normal(int(L*SR))
    x=np.diff(np.concatenate([[0],x])); return x*env(L,0.001,0.02 if not open_ else 0.08)
def snare():
    L=0.25; x=np.arange(int(L*SR))/SR
    return (rng.standard_normal(len(x))*0.6+np.sin(2*np.pi*190*x)*0.5)*np.exp(-x*18)
def note(freq,L,shape='saw',d=0.5):
    x=np.arange(int(L*SR))/SR
    if shape=='saw': s=sum(np.sin(2*np.pi*freq*k*x)/k for k in range(1,8))
    else: s=np.sin(2*np.pi*freq*x)+0.3*np.sin(2*np.pi*2*freq*x)
    return s*np.minimum(1,x/0.01)*np.exp(-x/d)
# progresion Am - F - C - G (cada acorde 2 tiempos? 1 compás = 4 tiempos)
chords=[(220,261.6,329.6),(174.6,220,261.6),(130.8,196,261.6),(196,246.9,293.7)]
bass=[110,87.3,65.4,98]
bar=4*beat
nb=int(DUR/bar)+1
for b in range(nb):
    c=chords[b%4]; t0=b*bar
    for f in c: add(note(f,bar,'saw',0.9),t0,0.05,pan=0.2*(f%3-1))
    for k in range(8):
        add(note(bass[b%4],beat/2,'sine',0.18),t0+k*beat/2,0.35)
    for k in range(4):
        add(kick(),t0+k*beat,0.9)
        if k%2==1: add(snare(),t0+k*beat,0.35)
    for k in range(8): add(hat(k%2==1),t0+k*beat/2,0.18,pan=0.3)
    # arpegio
    for k in range(8):
        f=c[k%3]*2; add(note(f,beat/2,'sine',0.12),t0+k*beat/2,0.08,pan=-0.3)
# whoosh/impacto a los 2.5 s y 5.5 s
for st in (2.5,5.5):
    L=0.5; x=rng.standard_normal(int(L*SR))*np.linspace(0,1,int(L*SR))**2
    add(x*np.exp(-np.linspace(0,1,int(L*SR))*1),st-0.45,0.12)
    add(kick(),st,0.6)
# fade
fade=np.ones(n); fl=int(0.6*SR); fade[-fl:]=np.linspace(1,0,fl); fade[:int(0.05*SR)]=np.linspace(0,1,int(0.05*SR))
out*=fade[:,None]; out/=np.max(np.abs(out))*1.12
wf.write(sys.argv[1],SR,(out*32767).astype(np.int16))
