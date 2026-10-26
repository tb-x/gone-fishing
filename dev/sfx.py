"""Judge the ElevenLabs sound-effect takes silently, and turn the chosen ones into the game's clips.

The takes (3 per sound, made with ElevenLabs Sound Effects on the Creator plan) are in dev/sfx-takes/<key>/<n>/.
Nothing is ever played: each take is decoded and measured (level, background noise, when it starts, how long it
lasts, how many separate hits it has). The chosen take is trimmed, faded and levelled into assets/sfx/<key>.mp3,
and dev/audition/sfx.html lets the user listen to the picks and every take.

Use (from the fishing folder, with the Kokoro venv, which has numpy and an ffmpeg):
    ../_tools/kokoro/venv/Scripts/python dev/sfx.py            measure every take, pick, write clips and the page
    ../_tools/kokoro/venv/Scripts/python dev/sfx.py --report   just print the measurements
"""
import json
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
import numpy as np

HERE = Path(__file__).resolve().parent
GAME = HERE.parent
TAKES = HERE / 'sfx-takes'
OUT = GAME / 'assets' / 'sfx'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100
HOP = int(SR * 0.01)   # 10 ms frames

# key: (what it is, the prompt's length in s, kind) - kind 'hit' wants one short event, 'long' a sustained sound
SOUNDS = {
    'stretch': ('rubber slingshot band stretching', 1.0, 'long'),
    'twang': ('slingshot band released', 0.7, 'hit'),
    'whoosh': ('line whizzing through the air', 1.0, 'long'),
    'plop': ('float plopping into the pond', 0.5, 'hit'),
    'splash': ('fish splashing at the surface', 1.5, 'long'),
    'plunk': ('bobber yanked under, a gulp', 0.7, 'hit'),
    'nibble': ('tiny bubble pop', 0.5, 'hit'),
    'bell': ('brass bite bell, one ring', 1.2, 'hit'),
    'strike': ('rod whip zing', 0.6, 'hit'),
    'click': ('one reel ratchet click', 0.5, 'hit'),
    'creak': ('taut line and rod creaking', 1.0, 'long'),
    'snap': ('line snapping', 0.7, 'hit'),
    'spit': ('bubbles blown out underwater', 1.0, 'long'),
    'pop': ('cartoon pop', 0.5, 'hit'),
    'boot': ('soggy boot squelch', 1.0, 'hit'),
    'catch': ('cheerful xylophone jingle', 2.0, 'long'),
    'duck': ('duck quack', 1.0, 'hit'),
    'frog': ('frog croak', 1.0, 'hit'),
    'bird': ('songbird chirp', 1.5, 'long'),
    'buzz': ('dragonfly buzzing past', 1.0, 'long'),
}
# A take chosen by ear overrides the measured pick: {'bell': 2}
CHOSEN = {'stretch': 3, 'twang': 3, 'plop': 3, 'spit': 3, 'bird': 2}   # by the measurements' meaning: one creak, a ringing twang, one burst, one chirp
LEVEL = {'click': 0.6, 'nibble': 0.7, 'stretch': 0.7, 'creak': 0.7, 'duck': 0.6, 'frog': 0.6, 'bird': 0.55, 'buzz': 0.55}   # relative loudness, 1 = full


def decode(path):
    raw = subprocess.run([FFMPEG, '-v', 'error', '-i', str(path), '-f', 'f32le', '-ac', '1', '-ar', str(SR), 'pipe:1'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def db(x):
    return 20 * np.log10(max(float(x), 1e-6))


def measure(x):
    n = len(x) // HOP
    env = np.sqrt((x[: n * HOP].reshape(n, HOP) ** 2).mean(axis=1))
    peak_env = env.max() if n else 0
    active = env > peak_env * 10 ** (-30 / 20)            # within 30 dB of the loudest moment
    idx = np.where(active)[0]
    on, off = (idx[0], idx[-1]) if idx.size else (0, 0)
    # separate hits: runs above -20 dB, split by gaps of 80 ms or more
    loud = env > peak_env * 10 ** (-20 / 20)
    hits, gap, inside = 0, 99, False
    for v in loud:
        if v:
            if not inside and gap >= 8:
                hits += 1
            inside, gap = True, 0
        else:
            inside = False
            gap += 1
    floor = np.percentile(env, 10) if n else 0
    return {
        'len': len(x) / SR, 'peak': db(np.abs(x).max()), 'rms': db(np.sqrt((env[active] ** 2).mean()) if idx.size else 0),
        'onset': on * HOP / SR, 'active': (off - on + 1) * HOP / SR, 'hits': hits, 'noise': db(floor) - db(peak_env),
        'on': on * HOP, 'off': (off + 1) * HOP,
    }


def score(m, kind, want):
    s = 0.0
    s -= max(0.0, m['noise'] + 45) * 0.15          # background hiss well under the sound
    s -= max(0.0, m['onset'] - 0.08) * 8           # starts straight away
    s -= max(0.0, -18 - m['peak']) * 0.3           # not too quiet
    if kind == 'hit':
        s -= (m['hits'] - 1) * 2.5                 # one event, not several
        s -= max(0.0, m['active'] - want * 1.3) * 3
    else:
        s -= abs(m['active'] - want) * 1.2         # about the length asked for
    return s


def process(x, m, key):
    """Trim to the sound, fade the ends, level it; returns the samples."""
    start = max(0, m['on'] - int(SR * 0.01))
    end = min(len(x), m['off'] + int(SR * 0.06))
    y = x[start:end].copy()
    fi, fo = int(SR * 0.004), min(int(SR * 0.05), len(y) // 3)
    y[:fi] *= np.linspace(0, 1, fi)
    y[-fo:] *= np.linspace(1, 0, fo)
    peak = np.abs(y).max() or 1
    return y * (0.89 * LEVEL.get(key, 1.0) / peak)


def save_mp3(y, path):
    subprocess.run([FFMPEG, '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', 'pipe:0',
                    '-codec:a', 'libmp3lame', '-b:a', '96k', '-y', str(path)], input=y.astype(np.float32).tobytes(), check=True)


def main(report_only=False):
    picks, table = {}, {}
    for key, (what, want, kind) in SOUNDS.items():
        rows = []
        for n in (1, 2, 3):
            files = sorted((TAKES / key / str(n)).glob('*.mp3'))
            if not files:
                continue
            m = measure(decode(files[0]))
            rows.append((n, files[0], m, score(m, kind, want)))
        best = CHOSEN.get(key) or max(rows, key=lambda r: r[3])[0]
        table[key] = rows
        picks[key] = best
        print(f'{key:8s} {what}')
        for n, f, m, s in rows:
            mark = '*' if n == best else ' '
            print(f"  {mark}{n}  {m['len']:.2f}s  peak {m['peak']:6.1f} dB  noise {m['noise']:6.1f} dB  starts {m['onset']:.2f}s"
                  f"  sound {m['active']:.2f}s  hits {m['hits']}  score {s:6.2f}")
    if report_only:
        return
    OUT.mkdir(parents=True, exist_ok=True)
    made = {}
    for key, best in picks.items():
        n, f, m, _ = next(r for r in table[key] if r[0] == best)
        y = process(decode(f), m, key)
        save_mp3(y, OUT / f'{key}.mp3')
        made[key] = {'what': SOUNDS[key][0], 'take': n, 'dur': round(len(y) / SR, 2),
                     'tool': 'ElevenLabs Sound Effects', 'plan': 'Creator (paid)', 'made': '2026-10-26'}
    (OUT / 'clips.json').write_text(json.dumps(made, indent=1) + '\n', encoding='utf-8', newline='\n')
    # the listening page: the pick (trimmed and levelled) and every raw take
    rel = lambda p: p.relative_to(GAME).as_posix()
    rows = ''
    for key, (what, _, _) in SOUNDS.items():
        takes = ''.join(
            f'<td><audio controls preload="none" src="../../{rel(f)}"></audio><br>take {n}{" (picked)" if n == picks[key] else ""}'
            f'<br><small>{m["active"]:.2f}s, {m["hits"]} hit{"s" if m["hits"] != 1 else ""}, noise {m["noise"]:.0f} dB</small></td>'
            for n, f, m, _ in table[key])
        rows += (f'<tr><th>{key}</th><td>{what}</td><td><audio controls preload="none" src="../../assets/sfx/{key}.mp3"></audio>'
                 f'<br><b>in the game</b></td>{takes}</tr>')
    (HERE / 'audition').mkdir(exist_ok=True)
    (HERE / 'audition' / 'sfx.html').write_text(f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gone Fishing sounds</title>
<style>body{{font-family:Verdana,sans-serif;margin:16px}}td,th{{padding:6px;text-align:left;font-size:12px;vertical-align:top}}audio{{width:180px}}
tr:nth-child(even){{background:#f2f6fa}}</style>
<h1>Gone Fishing! sound effects</h1>
<p>ElevenLabs Sound Effects (Creator plan), 3 takes each. The first column is the picked take, trimmed and levelled
as the game would use it; the others are the raw takes. Picked by measuring (one clean hit, little hiss, starts
at once), not by ear, so a better-sounding take may be one of the others: say which. Nothing plays until you press play.</p>
<table>{rows}</table>""", encoding='utf-8', newline='\n')
    print(f'{len(made)} clips in assets/sfx/; listen on dev/audition/sfx.html')


if __name__ == '__main__':
    main(report_only='--report' in sys.argv)
