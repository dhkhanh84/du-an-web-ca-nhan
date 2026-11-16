import os
# Original procedural ambience + Foley for the sample. numpy only. Output: stems + mixed master.
import numpy as np, wave, json
SR=24000; rng=np.random.default_rng(7)
def rd(p):
    w=wave.open(p); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768; return x
def wr(p,x):
    x=np.clip(x,-1,1); w=wave.open(p,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
def band(x,lo,hi):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X[(f<lo)|(f>hi)]=0; return np.fft.irfft(X,len(x))
def env(n,a,d):  # attack/decay seconds
    t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
def norm(x,peak): m=np.abs(x).max(); return x/m*peak if m>0 else x
def sec(s): return int(s*SR)
def hammer(f0):
    n=sec(.25); t=np.arange(n)/SR
    body=np.sin(2*np.pi*f0*t)*env(n,.001,.05)+.5*np.sin(2*np.pi*f0*4.3*t)*env(n,.001,.02)
    click=band(rng.standard_normal(n),1500,8000)*env(n,.0005,.006)
    return norm(body+1.5*click,1)
def drop():
    n=sec(.5); t=np.arange(n)/SR; x=np.sin(2*np.pi*110*t)*env(n,.001,.07)+band(rng.standard_normal(n),300,3000)*env(n,.001,.03)
    h=.35*hammer(260); x[sec(.11):sec(.11)+len(h)]+=h
    return norm(x,1)
def gravel():
    n=sec(.16); g=band(rng.standard_normal(n),900,5000)*(rng.random(n)<.08)*3+band(rng.standard_normal(n),400,2500)*.6
    return norm(g*env(n,.004,.04),1)
def flutter(dur):
    n=sec(dur); am=np.abs(band(rng.standard_normal(n),5,40)); am/=am.max()
    return norm(band(rng.standard_normal(n),1800,7000)*am*np.hanning(n),1)
def whoosh(dur):
    n=sec(dur); x=rng.standard_normal(n); out=np.zeros(n); k=8
    for i in range(k):
        s=slice(i*n//k,(i+1)*n//k); c=600+i*350; out[s]=band(x,c,c*2.2)[s]
    return norm(out*np.hanning(n)**1.5,1)
def land(): n=sec(.12); return norm(band(rng.standard_normal(n),150,1800)*env(n,.002,.025),1)
def pencil(dur):
    n=sec(dur); t=np.arange(n)/SR; am=(np.sin(2*np.pi*3.2*t)>0.1).astype(float); am=np.convolve(am,np.ones(240)/240,'same')
    return norm(band(rng.standard_normal(n),2500,7500)*am*(0.6+0.4*rng.random(n)),1)
def ting(f):
    n=sec(.7); t=np.arange(n)/SR
    x=sum(a*np.sin(2*np.pi*f*r*t)*env(n,.0007,d) for r,a,d in((1,1,.35),(2.76,.5,.18),(5.4,.25,.08)))
    return norm(x,1)
def catch_(): n=sec(.12); return norm(band(rng.standard_normal(n),800,6000)*env(n,.0005,.01),1)*.6+np.pad(ting(3100)[:sec(.12)]*.4,(0,0))
def tap(): n=sec(.06); return norm(band(rng.standard_normal(n),600,4000)*env(n,.0003,.006),1)
def chime():
    n=sec(1.2); t=np.arange(n)/SR; return norm(sum(np.sin(2*np.pi*f*t)*env(n,.003,d) for f,d in((1318.5,.6),(1975.5,.45),(2637,.25))),1)
# --- beds
def site(n):
    x=band(np.cumsum(rng.standard_normal(n))/80,40,900)*.6+band(rng.standard_normal(n),200,1200)*.15
    for t0 in rng.uniform(0,n/SR-.3,10): s=sec(t0); h=hammer(rng.uniform(250,420))*.18; x[s:s+len(h)]+=band(h,100,2500)[:n-s]
    return x
def wind(n):
    am=np.abs(band(rng.standard_normal(n),.1,.8)); am=.4+am/am.max()
    return band(rng.standard_normal(n),150,1400)*am
def room(n): return band(rng.standard_normal(n),60,500)
def metal(f0,dur=.6):
    n=sec(dur); t=np.arange(n)/SR
    x=sum(a*np.sin(2*np.pi*f0*r*t)*env(n,.0008,d) for r,a,d in((1,1,.25),(2.4,.6,.12),(3.9,.4,.06)))
    return norm(x+band(rng.standard_normal(n),800,6000)*env(n,.0005,.01),1)
def rattle():
    n=sec(.5); x=np.zeros(n)
    for t0 in (0,.07,.16,.27):
        m=metal(rng.uniform(700,950),.25)*rng.uniform(.5,1); s=sec(t0); x[s:s+len(m)]+=m[:n-s]
    return norm(x,1)
def thump():
    n=sec(.4); t=np.arange(n)/SR
    return norm(np.sin(2*np.pi*95*t)*env(n,.001,.06)+.6*band(rng.standard_normal(n),200,2500)*env(n,.0005,.015),1)
def creak(dur=.6,f=180):
    n=sec(dur); t=np.arange(n)/SR; fm=f*(1+.25*np.sin(2*np.pi*1.3*t))
    saw=((np.cumsum(fm)/SR)%1)*2-1; pulses=(rng.random(n)<.02)
    return norm(band(saw*(.5+pulses),300,3000)*np.hanning(n),1)
def pour(dur=.9):
    n=sec(dur); am=np.abs(band(rng.standard_normal(n),3,18)); am/=am.max()
    return norm(band(rng.standard_normal(n),80,900)*am*np.hanning(n),1)
def ratchet():
    n=sec(.6); x=np.zeros(n)
    for i in range(7): c=tap()*.8; s=sec(i*.08); x[s:s+len(c)]+=c[:n-s]
    return norm(band(x,1500,8000),1)
def jingle_keys():
    n=sec(.8); x=np.zeros(n)
    for i in range(9):
        m=metal(rng.uniform(2500,4200),.35)*rng.uniform(.3,1); s=sec(rng.uniform(0,.45)); x[s:s+len(m)]+=m[:n-s]
    return norm(x,1)
def deflate(): n=sec(.5); return norm(band(rng.standard_normal(n),200,1500)*np.linspace(1,0,n)**2,1)

def metal(f0,dur=.6):
    n=sec(dur); t=np.arange(n)/SR
    x=sum(a*np.sin(2*np.pi*f0*r*t)*env(n,.0008,d) for r,a,d in((1,1,.25),(2.4,.6,.12),(3.9,.4,.06)))
    return norm(x+band(rng.standard_normal(n),800,6000)*env(n,.0005,.01),1)
def rattle():
    n=sec(.5); x=np.zeros(n)
    for t0 in (0,.07,.16,.27):
        m=metal(rng.uniform(700,950),.25)*rng.uniform(.5,1); s=sec(t0); x[s:s+len(m)]+=m[:n-s]
    return norm(x,1)
def thump():
    n=sec(.4); t=np.arange(n)/SR
    return norm(np.sin(2*np.pi*95*t)*env(n,.001,.06)+.6*band(rng.standard_normal(n),200,2500)*env(n,.0005,.015),1)
def creak(dur=.6,f=180):
    n=sec(dur); t=np.arange(n)/SR; fm=f*(1+.25*np.sin(2*np.pi*1.3*t))
    saw=((np.cumsum(fm)/SR)%1)*2-1; pulses=(rng.random(n)<.02)
    return norm(band(saw*(.5+pulses),300,3000)*np.hanning(n),1)
def pour(dur=.9):
    n=sec(dur); am=np.abs(band(rng.standard_normal(n),3,18)); am/=am.max()
    return norm(band(rng.standard_normal(n),80,900)*am*np.hanning(n),1)
def ratchet():
    n=sec(.6); x=np.zeros(n)
    for i in range(7): c=tap()*.8; s=sec(i*.08); x[s:s+len(c)]+=c[:n-s]
    return norm(band(x,1500,8000),1)
def jingle_keys():
    n=sec(.8); x=np.zeros(n)
    for i in range(9):
        m=metal(rng.uniform(2500,4200),.35)*rng.uniform(.3,1); s=sec(rng.uniform(0,.45)); x[s:s+len(m)]+=m[:n-s]
    return norm(x,1)
def deflate(): n=sec(.5); return norm(band(rng.standard_normal(n),200,1500)*np.linspace(1,0,n)**2,1)


def heartbeat():
    n=sec(.6); t=np.arange(n)/SR; x=np.zeros(n)
    for t0,a in((0,1),(.22,.7)):
        s0=sec(t0); m=sec(.18); tt=np.arange(m)/SR; x[s0:s0+m]+=a*np.sin(2*np.pi*55*tt)*np.exp(-tt/.05)
    return norm(x,1)
narr=rd('audio/narration.wav'); LEAD=.15
N=sec(LEAD)+len(narr)+sec(.3); voice=np.zeros(N); voice[sec(LEAD):sec(LEAD)+len(narr)]=narr
amb=np.zeros(N); fx=np.zeros(N)
def fade(n,fi,fo): e=np.ones(n); a,b=sec(fi),sec(fo); e[:a]=np.linspace(0,1,a); e[n-b:]=np.linspace(1,0,b); return e
def bed(gen,t0,t1,fi,fo,rms):
    s,e=sec(t0),min(sec(t1),N); x=gen(e-s); x=x/np.sqrt((x**2).mean())*rms; amb[s:e]+=x*fade(e-s,fi,fo)
dB=lambda d:10**(d/20)
bed(room,0,N/SR,.3,.3,dB(-44)); bed(wind,51.0,58.3,.8,.8,dB(-38))
cues=[]
def put(t,x,d,label):
    s=sec(t); x=x*dB(d); fx[s:s+len(x)]+=x[:N-s]; cues.append({"t":round(t,3),"cue":label,"peak_dB":d})
put(.15,whoosh(.5),-20,'"1993" slams in')
for t in(.9,1.05,1.25): put(t,tap(),-28,'keyboard taps')
put(1.85,whoosh(.35),-22,'cut to investors')
put(3.0,metal(500,.3),-28,'controller crossed out')
put(5.6,flutter(.3),-26,'job-ads page in apron')
put(9.6,tap(),-24,'lectern mic tap')
put(14.1,pencil(.45),-22,'pen strikes out VISION')
put(15.35,ting(3000),-24,'PERSPECTIVE appears')
put(20.7,whoosh(.6),-24,'expensive workstation')
put(22.5,ting(2600),-22,'price drops: cheap')
put(24.0,ting(3300),-24,'cube becomes controller')
put(25.1,tap(),-24,'controller pop')
put(27.75,whoosh(.4),-22,'lesson 2 title')
for t in(31.0,31.4,31.8,32.3): put(t,tap(),-22,'computer maker named')
put(33.65,thump(),-14,'TOO EXPENSIVE stamp')
for t in(35.2,36.0,36.8): put(t,heartbeat(),-16,'heartbeat under the big bet')
for t in np.linspace(44.8,46.25,9): put(float(t),tap()*.7,-30,'competitors disappear')
put(46.45,chime(),-24,'one survivor left')
put(49.2,metal(900,.4),-30,'gears click')
put(51.15,whoosh(.5),-26,'lesson 3 title, into fog')
put(56.85,land(),-24,'step forward')
for i,t in enumerate((58.45,58.6,58.77,58.95,59.15)): put(t,land()*(1-i*.12),-16,'block tower collapses')
put(60.25,whoosh(.4),-24,'REBUILD')
put(61.6,tap(),-20,'last block placed')
for t in(68.15,68.75,69.4): put(t,tap(),-22,'check mark')
put(70.35,thump(),-22,'NOT ENOUGH')
put(71.4,chime(),-24,'PASSION')
put(75.95,ting(1800)*.7,-24,'comment bubble pops')
os.makedirs('audio/stems',exist_ok=True)
wr('audio/stems/voice_padded.wav',voice); wr('audio/stems/ambience.wav',amb); wr('audio/stems/fx.wav',fx)
mix=voice+amb+fx; pk=np.abs(mix).max(); g=min(1.0,10**(-3.2/20)/pk); print('peak',round(20*np.log10(pk),2),'dBFS -> gain',round(20*np.log10(g),2),'dB')
wr('audio/master_mix.wav',mix*g)
json.dump({"lead":LEAD,"source":"original procedural synthesis (make_sfx.py), no third-party audio, no music","cues":cues},open('audio/sound_manifest.json','w'),indent=1)
print(N/SR)
