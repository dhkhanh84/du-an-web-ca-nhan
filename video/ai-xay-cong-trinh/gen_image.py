import json,sys,base64,subprocess,os
REF='/root/.claude/plugins/synced/6885484c-7413-48de-8948-b53451880e01_1ccae8e5-87c7-4a7f-b902-53f9d823848c/stickman-video-director/skills/directing-stickman-videos/assets/b1/character-acting-reference.png'
STYLE=("Match the attached reference's drawing style exactly: slender stick figures (about 4-4.5 heads tall), round hollow head, fine slightly irregular black pen outlines, "
"single-line torso and limbs, small oval hands and feet, black oval eyes, expressive eyebrows and mouth, whole-body acting with weight and hand contact. "
"Hand-drawn colored props with limited warm yellow, red, green and navy marker accents. Plain near-white paper background, no text, no letters, no captions, no logos. "
"Wide 16:9 composition with the main action in the upper two-thirds and empty space along the bottom. Keep the same cast design across images: ")
def gen(name,prompt,model='gemini-2.5-flash-image',refs=()):
    out=f'assets/sample/{name}.png'
    if os.path.exists(out): print('exists',out); return
    parts=[{"text":STYLE+prompt}]
    for r in (REF,)+tuple(refs): parts.append({"inlineData":{"mimeType":"image/png","data":base64.b64encode(open(r,'rb').read()).decode()}})
    open('/tmp/img.json','w').write(json.dumps({"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9"}}}))
    r=subprocess.run(['curl','-sS','-X','POST',f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent','-H','Content-Type: application/json','-d','@/tmp/img.json'],capture_output=True,text=True)
    d=json.loads(r.stdout)
    if 'error' in d: print('ERR',d['error'].get('status'),d['error'].get('message','')[:200]); return
    for p in d['candidates'][0]['content']['parts']:
        i=p.get('inlineData')
        if i: open(out,'wb').write(base64.b64decode(i['data'])); print('saved',out,i['mimeType']); return
    print('no image',json.dumps(d)[:300])
if __name__=='__main__': gen(sys.argv[1],sys.argv[2],refs=sys.argv[3:])
