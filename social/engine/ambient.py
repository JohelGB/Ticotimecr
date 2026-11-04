# Música suave/elegante (pads + piano suave), sin percusión. uso: python3 ambient.py salida.wav segundos
import numpy as np, scipy.io.wavfile as wf, sys
SR=44100; DUR=float(sys.argv[2]); n=int(SR*DUR); t=np.arange(n)/SR; out=np.zeros((n,2))
rng=np.random.default_rng(3)
def add(sig,st,g=1,pan=0):
    i=int(st*SR)
    if i>=n: return
    e=min(n,i+len(sig)); out[i:e,0]+=sig[:e-i]*g*(1-pan); out[i:e,1]+=sig[:e-i]*g*(1+pan)
def pad(freqs,L):
    x=np.arange(int(L*SR))/SR; s=np.zeros_like(x)
    for f in freqs:
        for det in (-0.6,0.6): s+=np.sin(2*np.pi*(f+det)*x)+0.25*np.sin(2*np.pi*2*(f+det)*x)
    env=np.minimum(1,x/1.2)*np.minimum(1,(L-x)/1.2); return s*env/len(freqs)
def piano(f,L=2.5):
    x=np.arange(int(L*SR))/SR
    return (np.sin(2*np.pi*f*x)+0.4*np.sin(2*np.pi*2*f*x)+0.15*np.sin(2*np.pi*3*f*x))*np.exp(-x*2.2)*np.minimum(1,x/0.005)
ch=[(220,261.6,329.6,392),(174.6,220,261.6,329.6),(196,246.9,293.7,392),(164.8,207.7,246.9,329.6)]  # Am7 Fmaj7 G Em
bar=3.2
for b in range(int(DUR/bar)+1):
    c=ch[b%4]; add(pad(c,bar+1.2),b*bar,0.10)
    for k,f in enumerate([c[0]*2,c[2]*2,c[1]*2,c[3]*2]): add(piano(f),b*bar+k*0.8,0.12,pan=0.3*(k%2*2-1))
# reverb simple
for d,g in ((0.11,0.35),(0.23,0.25),(0.37,0.18)):
    k=int(d*SR); out[k:]+=out[:-k]*g
f=np.ones(n); fl=int(1.5*SR); f[-fl:]=np.linspace(1,0,fl); f[:int(0.8*SR)]=np.linspace(0,1,int(0.8*SR))
out*=f[:,None]; out/=np.max(np.abs(out))*1.15
wf.write(sys.argv[1],SR,(out*32767).astype(np.int16))
