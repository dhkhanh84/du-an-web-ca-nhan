import json,subprocess,base64,wave,os,sys,concurrent.futures as cf
d=json.load(open('scenes.json'))['scenes']
URL='https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent'
def job(s):
    out=f"audio/scenes/{s['code'].replace('.','-')}.wav"
    if os.path.exists(out): return s['code'],'exists',None
    jf=f"/tmp/w_{s['code']}.json"; rf=jf+'.resp'
    open(jf,'w').write(json.dumps({"contents":[{"parts":[{"text":s['narration']}]}],"generationConfig":{"responseModalities":["AUDIO"],"speechConfig":{"voiceConfig":{"prebuiltVoiceConfig":{"voiceName":"Algieba"}}}}}))
    r=subprocess.run(['curl','-sS','--max-time','170','-o',rf,'-w','%{http_code}','-X','POST',URL,'-H','Content-Type: application/json','-d','@'+jf],capture_output=True,text=True)
    try:
        d=json.load(open(rf))
        if 'error' in d: return s['code'],'error',d['error'].get('status')+': '+d['error'].get('message','')[:600]
        pcm=base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])
        w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm); w.close()
        return s['code'],'ok',round(len(pcm)/48000,1)
    except Exception as e: return s['code'],'fail',f"HTTP {r.stdout} {str(e)[:60]}"
todo=[s for s in d if not sys.argv[1:] or s['code'].split('.')[0] in sys.argv[1:]]
import time
for s_ in todo:
    for attempt in range(4):
        c,st,info=job(s_)
        if st=='error' and 'RESOURCE_EXHAUSTED' in str(info) and 'per_day' not in str(info).lower() and 'per day' not in str(info).lower():
            print(c,'rate-limited, waiting 40s',flush=True); time.sleep(40); continue
        break
    print(c,st,info,flush=True)
    if st=='error' and ('per day' in str(info).lower() or 'per_day' in str(info).lower()): print('DAILY QUOTA HIT - stopping',flush=True); break
    time.sleep(6.5)
