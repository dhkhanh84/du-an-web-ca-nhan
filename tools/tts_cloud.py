#!/usr/bin/env python3
"""Narration via Google Cloud Text-to-Speech (Gemini-TTS, voice Algieba) for future videos.

Why: Cloud TTS has a per-minute quota (150 requests/min for gemini-2.5-flash-tts by default)
instead of the Gemini API's 100 requests/day on Tier 1. Same price per token, same voices.

Auth: the API key is a network secret for texttospeech.googleapis.com (header x-goog-api-key),
injected by the environment proxy; this script sends a placeholder.

Usage:
  python3 tools/tts_cloud.py "Text to read." out.wav            # one clip
  python3 tools/tts_cloud.py --scenes scenes.json audio/scenes  # every scene (resumable)
Scenes JSON: {"scenes": [{"code": "1.1", "narration": "..."}]} -> audio/scenes/1-1.wav
"""
import base64, json, os, subprocess, sys, tempfile, time

URL = 'https://texttospeech.googleapis.com/v1/text:synthesize'
MODEL = os.environ.get('TTS_MODEL', 'gemini-2.5-flash-tts')
VOICE = os.environ.get('TTS_VOICE', 'Algieba')
LANG = os.environ.get('TTS_LANG', 'en-US')
SR = 24000


def synth(text, out, prompt=None):
    body = {"input": {"text": text},
            "voice": {"languageCode": LANG, "name": VOICE, "modelName": MODEL},
            "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": SR}}
    if prompt:
        body["input"]["prompt"] = prompt
    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as f:
        json.dump(body, f); jf = f.name
    for attempt in range(5):
        r = subprocess.run(['curl', '-sS', '--max-time', '180', '-X', 'POST', URL,
                            '-H', 'Content-Type: application/json',
                            '-H', 'x-goog-api-key: GEMINI_API_KEY',  # placeholder; proxy injects the real key
                            '-d', '@' + jf], capture_output=True, text=True)
        try:
            resp = json.loads(r.stdout)
        except Exception:
            print('bad response:', r.stdout[:200], r.stderr[:200], flush=True); time.sleep(10); continue
        if 'audioContent' in resp:
            wav = base64.b64decode(resp['audioContent'])  # LINEAR16 comes back as a WAV file
            open(out, 'wb').write(wav)
            return True
        err = resp.get('error', {})
        print('error', err.get('code'), err.get('status'), err.get('message', '')[:300], flush=True)
        if err.get('code') == 429:
            time.sleep(30); continue
        return False
    return False


if __name__ == '__main__':
    if sys.argv[1:2] == ['--scenes']:
        scenes = json.load(open(sys.argv[2]))['scenes']; outdir = sys.argv[3]
        os.makedirs(outdir, exist_ok=True)
        for s in scenes:
            out = os.path.join(outdir, s['code'].replace('.', '-') + '.wav')
            if os.path.exists(out):
                continue
            ok = synth(s['narration'], out)
            print(s['code'], 'ok' if ok else 'FAILED', flush=True)
            time.sleep(0.5)
    else:
        ok = synth(sys.argv[1], sys.argv[2])
        print('ok' if ok else 'FAILED'); sys.exit(0 if ok else 1)
