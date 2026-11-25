# Narrate the (short) script two scenes per Gemini TTS request, then split each take at the
# pause between the two scenes. 122 scenes -> 67 requests, inside the 100-requests/day limit.
# Resumable: skips scenes whose WAV exists. A pair whose split is ambiguous is re-done one scene
# per request. Usage: python3 tts_pairs.py [chapter ...]
import json, subprocess, base64, wave, os, sys, time
import numpy as np
SR = 24000
URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent'
d = json.load(open('scenes.json'))['scenes']
OUT = 'audio/scenes'; os.makedirs(OUT, exist_ok=True)
def path(s): return f"{OUT}/{s['code'].replace('.', '-')}.wav"
def save(p, x):
    w = wave.open(p, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(x.astype(np.int16).tobytes()); w.close()
def tts(text, tag):
    jf = f'/tmp/tts_{tag}.json'; rf = jf + '.resp'
    json.dump({"contents": [{"parts": [{"text": text}]}], "generationConfig": {"responseModalities": ["AUDIO"],
               "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Algieba"}}}}}, open(jf, 'w'))
    for attempt in range(5):
        r = subprocess.run(['curl', '-sS', '--max-time', '170', '-o', rf, '-w', '%{http_code}', '-X', 'POST', URL,
                            '-H', 'Content-Type: application/json', '-d', '@' + jf], capture_output=True, text=True)
        try: resp = json.load(open(rf))
        except Exception: print(tag, 'bad response HTTP', r.stdout, flush=True); time.sleep(20); continue
        if 'error' in resp:
            msg = resp['error'].get('status', '') + ': ' + json.dumps(resp['error'])[:1500]
            if 'per_day' in msg.lower() or 'per day' in msg.lower() or 'PerDay' in msg:
                print(tag, 'DAILY QUOTA HIT - stopping', flush=True); sys.exit(2)
            if 'RESOURCE_EXHAUSTED' in msg: print(tag, 'rate-limited, waiting 40s', flush=True); time.sleep(40); continue
            print(tag, 'error', msg[:300], flush=True); time.sleep(20); continue
        try:
            pcm = base64.b64decode(resp['candidates'][0]['content']['parts'][0]['inlineData']['data'])
            return np.frombuffer(pcm, np.int16).astype(float)
        except Exception as e: print(tag, 'no audio', str(e)[:80], flush=True); time.sleep(20)
    return None
def pauses(x):
    hop = int(.02 * SR); r = np.array([np.sqrt((x[i:i + hop] ** 2).mean()) for i in range(0, len(x) - hop, hop)]) / 32768
    q = r < 10 ** (-38 / 20); out = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if (j - i) * .02 >= .25: out.append((i * .02, j * .02))
            i = j
        else: i += 1
    return out
def single(s):
    x = tts(s['narration'], s['code'])
    if x is None: print(s['code'], 'FAILED', flush=True); return
    save(path(s), x); print(s['code'], 'ok single', round(len(x) / SR, 1), flush=True); time.sleep(6.5)
chs = sys.argv[1:]
todo = [s for s in d if (not chs or s['code'].split('.')[0] in chs) and not os.path.exists(path(s))]
groups = []
for s in todo:
    g = groups[-1] if groups else None
    if g and len(g) == 1 and g[0]['code'].split('.')[0] == s['code'].split('.')[0] \
            and int(g[0]['code'].split('.')[1]) + 1 == int(s['code'].split('.')[1]): g.append(s)
    else: groups.append([s])
print(len(todo), 'scenes in', len(groups), 'requests', flush=True)
for g in groups:
    if len(g) == 1: single(g[0]); continue
    a, b = g; tag = a['code'] + '+' + b['code']
    x = tts(a['narration'] + '\n\n' + b['narration'], tag)
    if x is None: print(tag, 'FAILED', flush=True); continue
    dur = len(x) / SR; la, lb = len(a['narration']), len(b['narration'])
    est = dur * la / (la + lb)
    cands = [(s0, s1) for s0, s1 in pauses(x) if 1.0 < s0 and s1 < dur - 1.0]
    best = min(cands, key=lambda p: abs((p[0] + p[1]) / 2 - est) - 1.5 * (p[1] - p[0]), default=None)
    ok = best is not None and abs((best[0] + best[1]) / 2 - est) < max(1.5, 0.15 * dur) and best[1] - best[0] >= .3
    if not ok:
        print(tag, 'split ambiguous, redoing one per request', flush=True); time.sleep(6.5)
        single(a); single(b); continue
    cut0 = int((best[0] + 0.12) * SR); cut1 = int(max(best[0] + 0.12, best[1] - 0.08) * SR)
    save(path(a), x[:cut0]); save(path(b), x[cut1:])
    print(tag, 'ok pair', round(dur, 1), 'split at', round(best[0], 2), '-', round(best[1], 2), 'est', round(est, 2), flush=True)
    time.sleep(6.5)
print('DONE', flush=True)
