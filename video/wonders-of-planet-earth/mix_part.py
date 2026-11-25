import json,sys,wave,numpy as np
NAME=sys.argv[1]; SR=24000; rng=np.random.default_rng(3)
tm=json.load(open(f'audio/parts/{NAME}_timing.json'))
w=wave.open(f'audio/parts/{NAME}_voice.wav'); v=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768
N=len(v); fx=np.zeros(N)
def band(x,lo,hi):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X[(f<lo)|(f>hi)]=0; return np.fft.irfft(X,len(x))
def put(t,x,db):
    s=int(t*SR); x=x/np.abs(x).max()*10**(db/20); fx[s:s+len(x)]+=x[:N-s]
def whoosh(d=.6):
    n=int(d*SR); x=rng.standard_normal(n); out=np.zeros(n)
    for i in range(8): sl=slice(i*n//8,(i+1)*n//8); c=300+i*250; out[sl]=band(x,c,c*2)[sl]
    return out*np.hanning(n)**1.5
def chime():
    n=int(1.6*SR); t=np.arange(n)/SR
    return sum(np.sin(2*np.pi*f*t)*np.exp(-t/d) for f,d in((523.3,.8),(784,.6),(1046.5,.35)))
chs=set(tm['chapters'].values())
for s in tm['scene_times']:
    if s['t0'] in chs: put(max(0,s['t0']-1.5),chime(),-24)
    else: put(max(0,s['t0']-0.45),whoosh(),-34)
# ElevenLabs scene effects (sfx_plan.py): one per scene, faded, sitting under the voice
import os, subprocess
if os.path.exists('sfx_plan.py'):
    from sfx_plan import SFX
    LOUD = {'impact', 'eruption', 'thunder', 'meteor', 'crack', 'collapse', 'icecalve', 'avalanche', 'wave', 'pageflip', 'sonar'}
    cache = {}
    def load(k):
        if k not in cache:
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'assets/sfx/{k}.mp3', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
            x = np.frombuffer(raw, np.int16).astype(float) / 32768
            cache[k] = x / max(1e-6, np.sqrt((x ** 2).mean()))   # unit RMS
        return cache[k]
    where = {c: k for k, (p, cs) in SFX.items() for c in cs}
    for sc in tm['scene_times']:
        k = where.get(sc['code'])
        if not k: continue
        x = load(k).copy(); L = min(len(x), int((sc['dur'] + 0.6) * SR))
        x = x[:L]; fi = min(int(0.25 * SR), L // 4); fo = min(int(1.2 * SR), L // 2)
        x[:fi] *= np.linspace(0, 1, fi); x[L - fo:] *= np.linspace(1, 0, fo)
        db = -27 if k in LOUD else -31
        s0 = int(max(0, sc['t0'] - 0.15) * SR); x = x * 10 ** (db / 20)
        fx[s0:s0 + len(x)] += x[:N - s0]
room=band(rng.standard_normal(N),60,400); room=room/np.sqrt((room**2).mean())*10**(-48/20)
mix=v+fx+room
w=wave.open(f'audio/parts/{NAME}_premix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(mix/max(1,np.abs(mix).max()),-1,1)*32767).astype(np.int16).tobytes()); w.close()
print('ok',round(N/SR,1))
