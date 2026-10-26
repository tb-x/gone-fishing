"""Pre-render the game's spoken lines as mp3 clips with Kokoro (a local, free text-to-speech model).

Kokoro-82M is Apache 2.0 (checked 2026-10-24 on huggingface.co/hexgrad/Kokoro-82M); it runs here through
kokoro-onnx (MIT), set up once in ../_tools/kokoro/ for What Should Frank Do? (see what-to-do/dev/voices.py
for the setup). Nothing is sent anywhere and nothing of the tool is committed.

Use (from the fishing folder):
    ../_tools/kokoro/venv/Scripts/python dev/voices.py --audition   candidate voices -> dev/audition/index.html
    ../_tools/kokoro/venv/Scripts/python dev/voices.py              render every line with VOICE -> assets/voice/
    ../_tools/kokoro/venv/Scripts/python dev/voices.py --force      render them all again

Clips are assets/voice/<key>.mp3, listed with their text, voice and date in assets/voice/clips.json.
"""
import datetime
import json
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from kokoro_onnx import Kokoro

HERE = Path(__file__).resolve().parent
GAME = HERE.parent
KOKORO = GAME.parent / '_tools' / 'kokoro' / 'models'
OUT = GAME / 'assets' / 'voice'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SR = 24000

# The coach's voice, picked by ear on the audition page (2026-10-26).
VOICE = {'voice': 'bf_emma', 'speed': 0.9}
# The child on the jetty, if the user wants them to cheer too (a woman's voice raised in pitch, like Frank's kids).
KID = None

SENTENCE_PAUSE = 0.4   # seconds between sentences, a little slower than Kokoro's default for young listeners
CLAUSE_PAUSE = 0.18


# ======== the lines ========

ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty', 6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'}


def words(n):
    if n < 20:
        return ONES[n]
    t, o = divmod(n, 10)
    return TENS[t] + ('-' + ONES[o] if o else '')


SIZES = range(12, 96)   # every size a fish in the pond can be (the boot is 24-30)

LINES = {
    'throw': 'Grab the bait, pull it back, and let go!',
    'wind': 'Got it! Wind the reel round and round!',
    'soon-float': 'Too soon! Wait till the bobber goes right under.',
    'soon-bell': 'Too soon! Wait for the bell.',
    'late-float': 'Tap when the bobber goes under!',
    'late-bell': 'Tap when the bell rings!',
    'worm-ate': 'It ate your worm! Reel in for a new one.',
    'worm-nibbled': 'It nibbled up your worm! Reel in for a new one.',
    'snap-tip': 'Snap! The line broke. Stop winding when the fish pulls!',
    'snap': 'Snap!',
    'boot': 'An old boot! Ha ha!',
    'fish-roach': 'A roach!', 'fish-perch': 'A perch!', 'fish-carp': 'A carp!', 'fish-pike': 'A pike!', 'fish-catfish': 'A catfish!',
    'now': 'Now!',
    'new': 'A new one for your book!',
    'biggest': 'Your biggest one yet!',
    'letgo': 'Bye-bye, fish! Off you swim!',
    'lure-tip': 'Wind the reel to make the spinner swim!',
    'waiting': 'Shh. Wait for a fish to find it.',
    **{f'cm-{n}': f'{words(n).capitalize()} centimetres!' for n in SIZES},
}
KID_LINES = {'kid-got': 'I got one!', 'kid-wow': 'Wow! Look at that!', 'kid-whee': 'Wheee!'}


# ======== rendering ========

_kokoro = None


def kokoro():
    global _kokoro
    if _kokoro is None:
        _kokoro = Kokoro(str(KOKORO / 'kokoro-v1.0.onnx'), str(KOKORO / 'voices-v1.0.bin'))
    return _kokoro


def ffmpeg(samples, args):
    cmd = [FFMPEG, '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', 'pipe:0', *args]
    return subprocess.run(cmd, input=samples.astype(np.float32).tobytes(), capture_output=True, check=True).stdout


def render(text, cfg):
    """Speak `text` with a voice setting {voice, speed, pitch}; British voices (bf_/bm_) speak British English."""
    lang = 'en-gb' if cfg['voice'][0] == 'b' else 'en-us'
    samples, sr = kokoro().create(text, voice=cfg['voice'], speed=cfg.get('speed', 1.0), lang=lang,
                                  sentence_pause=SENTENCE_PAUSE, clause_pause=CLAUSE_PAUSE)
    assert sr == SR
    p = cfg.get('pitch', 1.0)
    if abs(p - 1) > 1e-3:   # raise pitch and formants together (asetrate), then put the length back (atempo)
        raw = ffmpeg(samples, ['-af', f'asetrate={SR * p:.0f},aresample={SR},atempo={1 / p:.5f}', '-f', 'f32le', 'pipe:1'])
        samples = np.frombuffer(raw, dtype=np.float32)
    pad = np.zeros(int(SR * 0.05), dtype=np.float32)
    return np.concatenate([pad, samples, pad])


LOUDNESS = 0.11   # target RMS of the voiced parts, so every line is about as loud as the others


def save_mp3(samples, path):
    peak = float(np.max(np.abs(samples))) or 1.0
    frames = samples[: len(samples) // 480 * 480].reshape(-1, 480)   # 20 ms frames
    rms = np.sqrt((frames ** 2).mean(axis=1))
    voiced = rms[rms > 0.15 * rms.max()] if rms.size else rms
    level = float(np.sqrt((voiced ** 2).mean())) if voiced.size else peak
    samples = samples * min(0.89 / peak, LOUDNESS / level)          # even loudness, never clipping
    loud = np.where(rms > 0.015 * rms.max())[0]                      # trim the silence Kokoro leaves around a line (gently: soft 'sh' and 's' starts stay)
    if loud.size:
        samples = samples[max(0, loud[0] * 480 - int(SR * 0.06)): min(len(samples), (loud[-1] + 1) * 480 + int(SR * 0.12))]
    ffmpeg(samples, ['-codec:a', 'libmp3lame', '-b:a', '64k', '-y', str(path)])


def median_pitch(samples):
    """Rough speaking pitch in Hz (autocorrelation over voiced 40 ms frames)."""
    n, hop, out = int(SR * 0.04), int(SR * 0.02), []
    lo, hi = int(SR / 500), int(SR / 80)
    for i in range(0, len(samples) - n, hop):
        f = samples[i:i + n] - np.mean(samples[i:i + n])
        if np.sqrt(np.mean(f * f)) < 0.02:
            continue
        ac = np.correlate(f, f, 'full')[n - 1:]
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] > 0.45 * ac[0]:
            out.append(SR / lag)
    return float(np.median(out)) if out else 0.0


# ======== commands ========

def describe(cfg):
    return f"{cfg['voice']} speed {cfg.get('speed', 1.0)}" + (f" pitch x{cfg['pitch']}" if cfg.get('pitch', 1.0) != 1.0 else '')


def build(force=False):
    if not VOICE:
        sys.exit('Pick the coach voice first: set VOICE in dev/voices.py (listen on dev/audition/index.html)')
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / 'clips.json'
    old = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    todo = {k: (t, VOICE) for k, t in LINES.items()}
    if KID:
        todo.update({k: (t, KID) for k, t in KID_LINES.items()})
    manifest, made = {}, 0
    for key, (text, cfg) in todo.items():
        entry = {'text': text, 'voice': describe(cfg), 'tool': 'Kokoro-82M v1.0 (kokoro-onnx)'}
        prev = old.get(key)
        if not force and prev and all(prev.get(k) == v for k, v in entry.items()) and (OUT / f'{key}.mp3').exists():
            manifest[key] = prev
            continue
        samples = render(text, cfg)
        save_mp3(samples, OUT / f'{key}.mp3')
        manifest[key] = {**entry, 'dur': round(len(samples) / SR, 2), 'made': datetime.date.today().isoformat()}
        made += 1
        print(f'  {key}.mp3  {text}')
    for f in OUT.glob('*.mp3'):
        if f.stem not in manifest:
            f.unlink()
    manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
    # a page to listen to every line
    (HERE / 'audition').mkdir(exist_ok=True)
    rows = ''.join(f'<tr><th>{k}</th><td>{v["text"]}</td><td><audio controls preload="none" src="../../assets/voice/{k}.mp3"></audio></td></tr>'
                   for k, v in manifest.items())
    (HERE / 'audition' / 'lines.html').write_text(f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gone Fishing lines</title>
<style>body{{font-family:Verdana,sans-serif;margin:16px;max-width:860px}}td,th{{padding:6px;text-align:left;font-size:13px}}audio{{width:220px}}</style>
<h1>Every spoken line</h1><p>{describe(VOICE)}, made with Kokoro. Nothing plays until you press play.</p><table>{rows}</table>""",
        encoding='utf-8', newline='\n')
    print(f'{made} new clips, {len(manifest)} in clips.json; listen on dev/audition/lines.html')


# Candidates for the coach, and for the child on the jetty (raised in pitch like Frank's kids).
COACHES = [
    ('bf_emma', 'warm British woman'), ('bf_isabella', 'brighter British woman'), ('bm_george', 'older British man, a fishing grandad'),
    ('bm_lewis', 'gentle British man'), ('bm_fable', 'younger, lively British man'), ('af_heart', "American woman, Frank's narrator"),
]
COACH_SPEED = 0.9
COACH_LINES = ['Grab the bait, pull it back, and let go!', 'Too soon! Wait till the bobber goes right under.', 'A pike! Seventy-two centimetres!']
KIDS = [
    ({'voice': 'af_bella', 'speed': 0.95, 'pitch': 1.28}, "Frank's voice"),
    ({'voice': 'bf_emma', 'speed': 0.95, 'pitch': 1.3}, 'a British child'),
    ({'voice': 'bf_isabella', 'speed': 0.95, 'pitch': 1.3}, 'another British child'),
]
KID_SAMPLE = ['I got one!', 'Wow! Look at that!']


def audition():
    out = HERE / 'audition'
    out.mkdir(exist_ok=True)
    rows = []
    for voice, feel in COACHES:
        cfg = {'voice': voice, 'speed': COACH_SPEED}
        name = f'coach-{voice}.mp3'
        save_mp3(np.concatenate([render(t, cfg) for t in COACH_LINES]), out / name)
        rows.append((voice, feel, name))
        print(f'  {name}')
    kids = []
    for cfg, feel in KIDS:
        samples = np.concatenate([render(t, cfg) for t in KID_SAMPLE])
        name = f"kid-{cfg['voice']}-{cfg['pitch']:.2f}.mp3"
        save_mp3(samples, out / name)
        kids.append((describe(cfg), feel, name, median_pitch(samples)))
        print(f'  {name}')
    coach_rows = ''.join(f'<tr><th>{v}</th><td>{feel}</td><td><audio controls preload="none" src="{n}"></audio></td></tr>' for v, feel, n in rows)
    kid_rows = ''.join(f'<tr><th>{d}</th><td>{feel}</td><td><audio controls preload="none" src="{n}"></audio></td><td>{hz:.0f} Hz</td></tr>' for d, feel, n, hz in kids)
    (out / 'index.html').write_text(f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gone Fishing voices</title>
<style>body{{font-family:Verdana,sans-serif;margin:16px;max-width:760px}}td,th{{padding:8px;text-align:left;font-size:14px}}audio{{width:240px}}</style>
<h1>Gone Fishing! voice audition</h1>
<p>Made locally with Kokoro (free). Nothing plays until you press play.</p>
<h2>The coach</h2><p>Lines: "{'" / "'.join(COACH_LINES)}" (speed {COACH_SPEED})</p><table>{coach_rows}</table>
<h2>The child on the jetty (optional)</h2><p>Lines: "{'" / "'.join(KID_SAMPLE)}". A 5-year-old speaks at about 250-300 Hz.</p><table>{kid_rows}</table>""",
        encoding='utf-8', newline='\n')
    print(f'Listen: {out / "index.html"}')


if __name__ == '__main__':
    args = sys.argv[1:]
    if '--audition' in args:
        audition()
    else:
        build(force='--force' in args)
