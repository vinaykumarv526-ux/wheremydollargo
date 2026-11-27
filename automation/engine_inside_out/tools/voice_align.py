"""Voiceover and word alignment generator for 2D Flat Architectural Explainer.
Uses edge-tts (en-US-ChristopherNeural or en-US-GuyNeural) at 1.0x speed.
Generates:
  - data/narration.wav (24 kHz or 48 kHz mono/stereo)
  - data/lines.json ({ lines: [ { i, text, start, end } ] })
  - data/words.json ([ { w, line, s, e } ])
"""
import asyncio, json, os, re, subprocess, sys
from pathlib import Path
import numpy as np
from scipy.io import wavfile
import edge_tts

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
DATA_DIR = ROOT / 'data'
DATA_DIR.mkdir(parents=True, exist_ok=True)

script_path = ROOT / 'script.json'
if not script_path.exists():
    print(f"Error: {script_path} not found")
    sys.exit(1)

script = json.loads(script_path.read_text(encoding='utf-8'))
lines = script.get('lines', [])
voice = script.get('voice', 'en-US-ChristopherNeural')
lead_silence = float(script.get('lead', 0.40))
outro_silence = float(script.get('outro', 0.80))

norm = lambda w: re.sub(r'[^a-z0-9]+', '', w.lower())

async def synthesize_all():
    print(f"Synthesizing voiceover with voice: {voice}...")
    line_audios = []
    
    for idx, item in enumerate(lines):
        text = item['text']
        tmp_mp3 = DATA_DIR / f'line_{idx}.mp3'
        tmp_wav = DATA_DIR / f'line_{idx}.wav'
        
        comm = edge_tts.Communicate(text, voice)
        await comm.save(str(tmp_mp3))
        
        # Convert to 48kHz mono wav
        subprocess.run(
            ['ffmpeg', '-v', 'error', '-y', '-i', str(tmp_mp3), '-ar', '48000', '-ac', '1', str(tmp_wav)],
            check=True
        )
        if tmp_mp3.exists(): tmp_mp3.unlink()
        
        sr, audio_data = wavfile.read(str(tmp_wav))
        # Trim leading and trailing quiet silence
        abs_a = np.abs(audio_data)
        thr = max(100, int(0.015 * abs_a.max()))
        idx_sig = np.where(abs_a > thr)[0]
        if len(idx_sig) > 0:
            a_start = max(0, idx_sig[0] - int(0.02 * sr))
            a_end = min(len(audio_data), idx_sig[-1] + int(0.04 * sr))
            trimmed = audio_data[a_start:a_end]
        else:
            trimmed = audio_data
            
        line_audios.append(trimmed)
        if tmp_wav.exists(): tmp_wav.unlink()

    # Assemble full narration track with lead and natural pauses
    SR = 48000
    combined = [np.zeros(int(lead_silence * SR), dtype=np.int16)]
    current_time = lead_silence
    line_meta = []
    words_meta = []

    for idx, (item, audio) in enumerate(zip(lines, line_audios)):
        dur = len(audio) / SR
        start_t = round(current_time, 3)
        end_t = round(current_time + dur, 3)
        line_meta.append({
            'i': idx,
            'text': item['text'],
            'start': start_t,
            'end': end_t
        })
        combined.append(audio)
        
        # Word-level distribution within line duration
        tokens = [w for w in item['text'].split() if norm(w)]
        weights = [len(norm(w)) + 2.0 + (2.0 if w.endswith(',') else 3.5 if re.search(r'[.?!]$', w) else 0) for w in tokens]
        tot = sum(weights) or 1.0
        cur_w_t = start_t
        
        for w, wt in zip(tokens, weights):
            w_dur = dur * (wt / tot)
            speak_dur = w_dur * 0.90
            words_meta.append({
                'w': w,
                'line': idx,
                's': round(cur_w_t, 3),
                'e': round(cur_w_t + speak_dur, 3)
            })
            cur_w_t += w_dur

        # Inter-line gap
        gap = float(item.get('gap', 0.28))
        combined.append(np.zeros(int(gap * SR), dtype=np.int16))
        current_time = end_t + gap

    combined.append(np.zeros(int(outro_silence * SR), dtype=np.int16))
    full_audio = np.concatenate(combined)
    
    out_narration = DATA_DIR / 'narration.wav'
    wavfile.write(str(out_narration), SR, full_audio)
    
    (DATA_DIR / 'lines.json').write_text(json.dumps({'lines': line_meta}, indent=2), encoding='utf-8')
    (DATA_DIR / 'words.json').write_text(json.dumps(words_meta, indent=2), encoding='utf-8')
    
    total_dur = len(full_audio) / SR
    print(f"Narration generated: {out_narration} ({total_dur:.2f}s, {len(line_meta)} lines, {len(words_meta)} words)")

if __name__ == '__main__':
    asyncio.run(synthesize_all())
