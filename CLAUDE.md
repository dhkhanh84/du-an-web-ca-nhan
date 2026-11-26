# Project notes for Claude

## Video production defaults (stickman-video-director, mode B)

- **Narration voice: Google Gemini `Algieba`** on `gemini-2.5-flash-preview-tts`, no style/direction prompt, native speed.
  User's explicit preference (2026-11-15): use Algieba for all future videos, whatever the narration language,
  unless the user asks for a different voice in that request.
  This replaces the skill's per-style default voices (e.g. B1's Bodi, which `gemini-2.5-flash-preview-tts` does not offer).
- **Narration route: Gemini API** (`gemini-2.5-flash-preview-tts`, Algieba). The Tier-1 limit is
  100 requests/day, so group 2–3 scenes per request and split at the pauses (`tts_pairs.py` pattern in
  video/wonders-of-planet-earth).
- **Alternative route that works (tested 2026-11-26): Agent Platform (Vertex AI) generateContent.**
  `POST https://aiplatform.googleapis.com/v1/publishers/google/models/gemini-2.5-flash-tts:generateContent`
  with the same body as the Gemini API (voice Algieba), header `x-goog-api-key` (network secret for host
  `aiplatform.googleapis.com`; the key is bound to a service account with `roles/aiplatform.user`).
  Returns raw PCM 24 kHz in `inlineData`. Cloud Text-to-Speech (`texttospeech.googleapis.com`) does NOT work
  with API keys for Gemini voices (403), so do not use `tools/tts_cloud.py`. Its daily quota is not yet known.
- Other settings used so far. These are not user rules, so reconfirm them when needed:
  - Images: `gemini-2.5-flash-image`.
  - Caption timing: `gemini-4-hydrogen`. It is text-only, so it cannot make images or audio.
    Send audio to it one paragraph at a time, because requests over ~30 s get a 502 from the proxy.
    Then snap word times to pauses measured with ffmpeg `silencedetect`.
  - Vietnamese scene text: Patrick Hand (OFL), because B1's Caveat lacks Vietnamese glyphs.
- Renderer pitfall: if a caption is too wide for one line, `autopilot.mjs preview/render` prints
  "B captions allow at most one line" but then hangs instead of exiting. Pre-check caption widths
  (Noto Sans at `captionSize`, max ~1040 px) and wrap every render call in `timeout`.
- Ask before every paid Gemini call. The API key is stored as an environment network secret
  (header `x-goog-api-key`); scripts can use a placeholder `GEMINI_API_KEY`.
- Past projects live in `video/` (each has `checkpoint.json`).
