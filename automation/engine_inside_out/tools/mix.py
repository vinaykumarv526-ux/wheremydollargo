"""2D Flat Architectural Explainer Soundtrack Synthesizer
Generates 48 kHz procedural sound effects (whoosh, pop, slam, ding, slide, etc.)
and a ducked procedural curiosity background score bed. No external samples required.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from scipy import signal
from scipy.io import wavfile

P = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
SR = 48000
rng = np.random.default_rng(42)

cues_file = P / 'data/cues.json'
script_file = P / 'script.json'

if not cues_file.exists():
    print(f"Error: {cues_file} does not exist.")
    sys.exit(1)

cj = json.loads(cues_file.read_text(encoding='utf-8'))
script = json.loads(script_file.read_text(encoding='utf-8')) if script_file.exists() else {}

DUR = float(cj.get('duration', 30.0))
N = int(DUR * SR) + SR // 10

def lp(x, f, o=2):
    b, a = signal.butter(o, min(f, SR / 2 - 100) / (SR / 2), 'low')
    return signal.lfilter(b, a, x)

def hp(x, f, o=2):
    b, a = signal.butter(o, f / (SR / 2), 'high')
    return signal.lfilter(b, a, x)

def bp(x, f0, f1, o=2):
    b, a = signal.butter(o, [f0 / (SR / 2), f1 / (SR / 2)], 'band')
    return signal.lfilter(b, a, x)

def db(x): return 10 ** (x / 20)
def tt(d): return np.arange(int(d * SR)) / SR

def env(n, a=0.005, r=None):
    e = np.ones(n)
    na = max(1, int(a * SR))
    e[:na] = np.linspace(0, 1, na)
    rest = n - na
    e[na:] = np.exp(-np.linspace(0, r or 5, rest)) if rest > 0 else 1
    return e

def sweep(f0, f1, d, shape='exp'):
    t = tt(d)
    f = f0 * (f1 / f0) ** (t / d) if shape == 'exp' else f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)

def noise(d): return rng.standard_normal(int(d * SR))

# Procedural Sound Cues
def whoosh(d=0.36, **_):
    n = noise(d)
    lo, hi = lp(n, 450), lp(n, 2000)
    k = np.sin(np.pi * np.linspace(0, 1, len(n)))
    x = (lo * (1 - k) + hi * k) * (k ** 1.5)
    return x / (np.abs(x).max() + 1e-9) * 0.55

def pop(**_):
    x = sweep(620, 260, 0.10) * env(int(0.10 * SR), 0.002, 6)
    return lp(x, 3200) * 0.75

def slam(**_):
    d = 0.48
    t = tt(d)
    x = np.sin(2 * np.pi * (65 + 55 * np.exp(-t * 22)) * t) * env(len(t), 0.002, 6)
    return np.tanh(1.5 * (x + lp(noise(d), 1100) * env(len(t), 0.001, 10) * 0.5)) * 0.95

def ding(d=0.85, **_):
    t = tt(d)
    x = (np.sin(2 * np.pi * 1760 * t) + 0.35 * np.sin(2 * np.pi * 3520 * t) + 0.12 * np.sin(2 * np.pi * 5280 * t)) * env(len(t), 0.001, 4.5)
    return lp(x, 6000) * 0.55

def slide(d=0.8, **_):
    n = lp(noise(d), 650)
    e = np.sin(np.pi * np.linspace(0, 1, len(n))) ** 2
    return n / (np.abs(n).max() + 1e-9) * e * 0.35 + sweep(280, 110, d) * e * 0.08

def tock(**_):
    d = 0.08
    t = tt(d)
    return (np.sin(2 * np.pi * 440 * t) + 0.25 * np.sin(2 * np.pi * 880 * t)) * env(len(t), 0.001, 9) * 0.35

FX = dict(whoosh=whoosh, pop=pop, slam=slam, ding=ding, slide=slide, tock=tock)
LEVEL = dict(whoosh=-16, pop=-13, slam=-9, ding=-12, slide=-18, tock=-18)

# Procedural Technical Curiosity Bed (100 BPM, soft pad + subtle synth pulse)
def procedural_bed():
    bpm = 104
    beat = 60 / bpm
    bar = beat * 4
    chords = [[220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [261.6, 329.6, 392.0], [196.0, 246.9, 293.7]]
    x = np.zeros(N)
    nb = int(np.ceil(DUR / bar)) + 1
    
    for b in range(nb):
        ch = chords[b % 4]
        st = int(b * bar * SR)
        n = int(bar * SR)
        if st >= N: break
        t = tt(bar)
        e = np.minimum(1, t / 0.35) * np.minimum(1, (bar - t) / 0.35)
        pad = sum(np.sin(2 * np.pi * f / 2 * t) + 0.2 * np.sin(2 * np.pi * f * t) for f in ch) * e * 0.08
        x[st:st + n] += pad[:max(0, min(n, N - st))]
        
        # Soft rhythmic pulse
        for k in range(8):
            f = ch[k % 3] * 1.5
            ps = st + int(k * beat / 2 * SR)
            pn = int(0.35 * SR)
            if ps + pn >= N: continue
            pt = tt(0.35)
            pl = (np.sin(2 * np.pi * f * pt) + 0.2 * np.sin(3 * np.pi * f * pt)) * env(pn, 0.004, 8) * 0.09
            x[ps:ps + pn] += pl

    x = lp(x, 2800)
    fade = np.ones(N)
    fo = int(1.2 * SR)
    fade[-fo:] = np.linspace(1, 0, fo)
    return x / (np.abs(x).max() + 1e-9) * fade

def load_audio(f):
    out = subprocess.run(
        ['ffmpeg', '-v', 'error', '-i', str(f), '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
        capture_output=True, check=True
    ).stdout
    return np.frombuffer(out, dtype=np.float32).reshape(-1, 2).astype(np.float64)

mix = np.zeros((N, 2))

# 1. Voice
vf = P / 'data/narration.wav'
voice = None
if vf.exists():
    v = load_audio(vf)[:N]
    voice = np.zeros((N, 2))
    voice[:len(v)] = v
    rms = np.sqrt(np.mean(voice ** 2) + 1e-12)
    voice *= db(-19) / rms
    mix += voice

# 2. Background Curiosity Bed (ducked under voice)
m = procedural_bed()
m = np.stack([m, m], 1) * db(-24 if voice is not None else -20)
if voice is not None:
    lev = np.abs(voice.mean(1))
    lev = signal.lfilter([1 - 0.9995], [1, -0.9995], lev)
    lev /= (lev.max() + 1e-9)
    # Duck music by 65% when voice is active
    m *= (1 - 0.65 * np.clip(lev * 3.5, 0, 1))[:, None]
mix += m

# 3. Procedural Cues
for c in cj.get('cues', []):
    fn = FX.get(c['type'])
    if not fn: continue
    st = int(c['t'] * SR)
    if st >= N: continue
    kwargs = {}
    if 'dur' in c: kwargs['d'] = float(c['dur'])
    smp = fn(**kwargs)
    gain = float(c.get('gain', 1.0)) * db(LEVEL.get(c['type'], -14))
    smp = np.stack([smp, smp], 1) * gain
    end = min(N, st + len(smp))
    mix[st:end] += smp[:end - st]

# Normalize to avoid clipping
peak = np.abs(mix).max()
if peak > 0.98:
    mix = mix / peak * 0.96

out_wav = P / 'data/mix.wav'
wavfile.write(str(out_wav), SR, (mix * 32767).astype(np.int16))
print(f"Generated soundtrack mix: {out_wav} ({DUR:.2f}s, {len(cj.get('cues', []))} cues)")
