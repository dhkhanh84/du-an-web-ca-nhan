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
narr=rd('audio/narration.wav'); LEAD=.15
N=sec(LEAD)+len(narr)+sec(.4); voice=np.zeros(N); voice[sec(LEAD):sec(LEAD)+len(narr)]=narr
amb=np.zeros(N); fx=np.zeros(N)
def fade(n,fi,fo): e=np.ones(n); a,b=sec(fi),sec(fo); e[:a]=np.linspace(0,1,a) if a else 1; e[n-b:]=np.linspace(1,0,b) if b else e[n-b:]; return e
def bed(gen,t0,t1,fi,fo,rms):
    s,e=sec(t0),min(sec(t1),N); x=gen(e-s); x=x/np.sqrt((x**2).mean())*rms; amb[s:e]+=x*fade(e-s,fi,fo)
dB=lambda d:10**(d/20)
bed(site,0,4.3,.05,1.0,dB(-36)); bed(wind,3.6,9.6,.8,.6,dB(-40)); bed(room,9.2,N/SR,.5,.4,dB(-44))
cues=[]
def put(t,x,d,label):
    s=sec(t); x=x*dB(d); fx[s:s+len(x)]+=x[:N-s]; cues.append({"t":round(t,3),"cue":label,"peak_dB":d})
for t,f in((.85,300),(1.22,340),(1.58,285)): put(t,hammer(f),-12,'hammer on plank (near, wood)')
put(3.62,drop(),-16,'hammers dropped on ground')
for t in(4.55,4.95,5.35,5.7): put(t,gravel(),-22,'footstep on gravel (owner walks in)')
put(7.55,flutter(.35),-22,'paper flourish (sketch raised)')
put(8.45,chime(),-22,'light bulb idea chime')
put(9.35,whoosh(.55),-24,'sketch flies to drafting table')
put(9.95,land(),-18,'paper lands on table')
put(10.25,pencil(1.6),-30,'pencil drawing on paper')
for t,f in((12.95,2900),(13.4,3300),(13.85,3700)): put(t,ting(f),-20,'coin pops from drawn line')
for t in(16.35,16.8,17.25): put(t,catch_(),-20,'coin caught in hand')
put(17.75,tap(),-24,'finger taps tablet')
wr('audio/stems/voice_padded.wav',voice); wr('audio/stems/ambience.wav',amb); wr('audio/stems/fx.wav',fx)
wr('audio/master_sample_mix.wav',voice+amb+fx)
json.dump({"lead":LEAD,"source":"original procedural synthesis (make_sfx.py), no third-party audio","cues":cues},open('audio/sound_manifest.json','w'),indent=1)
print(N/SR)

# ---- Parts 3-6 (appended after sample cues so the reviewed opening stays bit-identical)
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
bed(site,28.0,36.0,.6,.15,dB(-38))          # site returns; cut at "Here is the truth"
bed(wind,44.4,N/SR,.8,.5,dB(-42))
put(19.55,rattle(),-22,'owner touches locked iron gate')
put(20.72,thump(),-14,'approval stamp slams on document')
put(20.95,creak(.7,140),-28,'gate swings open')
for t in(22.25,22.75,23.3): put(t,land(),-18,'envelope placed on table')
put(24.55,creak(.5,320),-30,'scale beam creaks')
put(26.45,metal(220,.4),-26,'scale pan settles')
put(28.6,metal(160,.7),-18,'steel beam set onto frame')
put(30.6,flutter(.25),-24,'clipboard page flip')
put(32.3,pour(),-22,'concrete pour into formwork')
put(33.55,ratchet(),-24,'wrench tightens bolt')
put(34.95,tap(),-22,'pen tick against drawing')
put(38.6,creak(.5,260),-30,'model wobbles over the hero')
put(40.05,deflate(),-24,'hero gives up (exhale-like air, synthetic)')
for i,t in enumerate((41.0,41.45,41.9,42.4,42.9,43.4)): put(t,tap(),-22,'hands link into the ring')
put(43.9,chime(),-24,'ring closes')
put(45.0,tap(),-20,'inspection check mark')
put(46.6,jingle_keys(),-20,'keys change hands')
put(48.0,creak(.8,120),-30,'front door opens')
put(52.05,ting(1800)*.7,-24,'comment bubble pops')
wr('audio/stems/ambience.wav',amb); wr('audio/stems/fx.wav',fx)
wr('audio/master_mix.wav',voice+amb+fx)
json.dump({"lead":LEAD,"source":"original procedural synthesis (make_sfx.py), no third-party audio","cues":cues},open('audio/sound_manifest.json','w'),indent=1)
print('full',N/SR)
