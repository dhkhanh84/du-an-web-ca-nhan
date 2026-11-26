# Narrate scenes with Gemini TTS (gemini-2.5-flash-tts, voice Algieba) through Agent Platform / Vertex AI.
# One scene per request, resumable (skips existing WAVs).
#   LANGV=vi python3 tts_vertex.py [chapter ...]     -> audio/vi/scenes/<code>.wav
#   python3 tts_vertex.py [chapter ...]              -> audio/scenes/<code>.wav
# Auth: network secret for aiplatform.googleapis.com (header x-goog-api-key, key bound to a service account).
import json, subprocess, base64, wave, os, sys, time
URL = 'https://aiplatform.googleapis.com/v1/publishers/google/models/gemini-2.5-flash-tts:generateContent'
d = json.load(open('scenes.json'))['scenes']; OUT = 'audio/scenes'
if os.environ.get('LANGV') == 'vi':
    from vi_script import VI
    d = [dict(s, narration=VI[s['code']][1]) for s in d]; OUT = 'audio/vi/scenes'
os.makedirs(OUT, exist_ok=True)
chs = sys.argv[1:]
todo = [s for s in d if (not chs or s['code'].split('.')[0] in chs) and not os.path.exists(f"{OUT}/{s['code'].replace('.', '-')}.wav")]
print(len(todo), 'scenes to read', flush=True)
for s in todo:
    out = f"{OUT}/{s['code'].replace('.', '-')}.wav"; jf = f"/tmp/vx_{s['code']}.json"
    json.dump({"contents": [{"role": "user", "parts": [{"text": s['narration']}]}], "generationConfig": {"responseModalities": ["AUDIO"],
               "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Algieba"}}}}}, open(jf, 'w'))
    ok = False
    for attempt in range(6):
        r = subprocess.run(['curl', '-sS', '--max-time', '170', '-X', 'POST', URL, '-H', 'Content-Type: application/json',
                            '-H', 'x-goog-api-key: GEMINI_API_KEY', '-d', '@' + jf], capture_output=True, text=True)
        try: resp = json.loads(r.stdout)
        except Exception: print(s['code'], 'bad response', r.stdout[:120], r.stderr[:120], flush=True); time.sleep(15); continue
        if 'error' in resp:
            e = resp['error']; msg = e.get('status', '') + ' ' + e.get('message', '')[:200]
            if e.get('code') == 429:
                if 'day' in msg.lower(): print(s['code'], 'DAILY QUOTA HIT - stopping', msg, flush=True); sys.exit(2)
                print(s['code'], 'rate-limited, waiting 30s', flush=True); time.sleep(30); continue
            print(s['code'], 'error', msg, flush=True); time.sleep(10); continue
        try:
            pcm = base64.b64decode(resp['candidates'][0]['content']['parts'][0]['inlineData']['data'])
        except Exception as ex: print(s['code'], 'no audio', str(ex)[:80], flush=True); time.sleep(10); continue
        w = wave.open(out, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm); w.close()
        print(s['code'], 'ok', round(len(pcm) / 48000, 1), flush=True); ok = True; break
    if not ok: print(s['code'], 'FAILED', flush=True)
    time.sleep(1.5)
print('DONE', flush=True)
