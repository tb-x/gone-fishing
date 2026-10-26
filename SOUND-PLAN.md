# Gone Fishing! — recorded sound plan

Today every sound is synthesized in the browser and the voice is the device's own (`speechSynthesis`). This plan
replaces both with recorded clips, on a budget:

- **Voice: Kokoro**, the free local text-to-speech model already set up for What Should Frank Do?
  (`_tools/kokoro/`, Kokoro-82M, Apache 2.0). Nothing is sent anywhere and it costs nothing, so there can be as
  many lines as we like.
- **Sound effects: ElevenLabs Sound Effects**, on the paid Creator plan. About 10 credits a second of audio.
  The whole set is roughly 600–1,000 credits; **67,307 credits are left this month** (checked 2026-10-26;
  54,595 of 121,902 used, resets around 2026-11-23).
- **No music** for now: the pond's ambience comes from short one-off critter sounds, not a background loop.
  The user found Robot Spy's noise loop a constant hiss.

Every clip falls back to today's synthesized sound or device voice if it can't load, as in Blast Off.

## 1. Voice lines (Kokoro, free)

### Who speaks

One friendly voice coaches the child. Kokoro has British voices, which suit "centimetres" and the game's current
`en-GB` speech. Candidates for the audition page (the user picks by ear; a voice is never chosen unheard):

| Key | Kokoro voice | Feel |
| --- | --- | --- |
| A | `bf_emma` | warm British woman |
| B | `bm_george` | older British man, a "fishing grandad" |
| C | `af_heart` | Frank's narrator, which the user liked |
| D | `bm_fable` | younger British man, lively |

Optional: the child on the jetty could also cheer ("I got one!", "Wheee!"), using a woman's voice raised in pitch
the way Frank's kids are (`af_bella`, pitch ×1.28). That's a second voice in the same audition.

### The lines

These are the game's lines today (✱ = new lines worth adding once speech is recorded):

| Key | Line | When |
| --- | --- | --- |
| `throw` | Grab the bait, pull it back, and let go! | first hint |
| `wind` | Got it! Wind the reel round and round! | first fish hooked |
| `soon-float` | Too soon! Wait till the bobber goes right under. | struck during nibbles |
| `soon-bell` | Too soon! Wait for the bell. | struck during nibbles (bottom rig) |
| `late-float` | Tap when the bobber goes under! | missed a bite |
| `late-bell` | Tap when the bell rings! | missed a bite (bottom rig) |
| `worm-ate` | It ate your worm! Reel in for a new one. | worm stolen |
| `worm-nibbled` | It nibbled up your worm! Reel in for a new one. | worm nibbled away |
| `snap-tip` | Snap! The line broke. Stop winding when the fish pulls! | first snaps |
| `snap` | Snap! | later snaps |
| `boot` | An old boot! Ha ha! | caught the boot |
| `fish-roach` … `fish-catfish` | A roach! / A perch! / A carp! / A pike! / A catfish! | catch card |
| `cm-12` … `cm-95` | Twelve centimetres! … Ninety-five centimetres! | catch card, after the name |
| ✱ `now` | Now! | the moment the bobber goes under (first few times) |
| ✱ `new` | A new one for your book! | first catch of a kind |
| ✱ `biggest` | Your biggest one yet! | a size record |
| ✱ `letgo` | Bye-bye, fish! Off you swim! | tapping Let it go |
| ✱ `lure-tip` | Wind the reel to make the spinner swim! | spinner sitting still |
| ✱ `waiting` | Shh… wait for a fish to find it. | first wait |

Sizes: the catch card says the name, then the size, as two clips played back to back. Recording every size from
12 to 95 is 84 short clips, about 1.3 MB of mp3. That's free with Kokoro, but it's the biggest part of the
download. The alternative is three size words ("A little one!", "A good one!", "A whopper!"), 3 clips instead of
84 (a choice for the user, below).

### How

- `fishing/dev/voices.py`, a cut-down copy of `what-to-do/dev/voices.py`: a table of `key → text`, one voice
  setting, run with `../_tools/kokoro/venv/Scripts/python dev/voices.py`. It writes `assets/voice/<key>.mp3`
  (mono, 64 kbps, trimmed silence) using the ffmpeg that comes with `imageio-ffmpeg` in that venv. A changed
  line gets a new clip, and `--audition` writes `dev/audition/index.html` with the candidate voices reading
  three sample lines.
- Check every clip silently: decode it in the Browser pane with `OfflineAudioContext` (length, peak, no clipped
  ends). Never play it through the speakers. The user then listens on the audition page.

## 2. Sound effects (ElevenLabs, paid Creator plan)

Short one-shots, 3 takes each (short prompts often come back quiet or with several hits, per Beat Bugs), so the
best take is picked and its level and length fixed in code (`CLIP_TRIM`), not re-recorded.

| Key | Sound | Length | Replaces |
| --- | --- | --- | --- |
| `sfx-stretch` | rubber band stretching, a short creak | 1 s | `stretch` (pitched up per step in code) |
| `sfx-twang` | slingshot band release twang | 0.7 s | `twang` |
| `sfx-whoosh` | fishing line whizzing through the air | 1 s | `whoosh` |
| `sfx-plop` | small float plopping into a pond | 0.5 s | `plop` |
| `sfx-splash` | fish splashing at the surface | 1.5 s | `splash` |
| `sfx-plunk` | bobber yanked under water, a deep gulp | 0.7 s | `plunk` |
| `sfx-nibble` | tiny underwater bubble pop | 0.5 s | `nibble` |
| `sfx-bell` | small brass bite-alarm bell, one ring | 1.2 s | `ding` |
| `sfx-strike` | quick rod whip zing | 0.6 s | `strike` |
| `sfx-click` | one fishing-reel ratchet click | 0.5 s | `tick` |
| `sfx-creak` | taut fishing line and rod creaking | 1 s | `creak` |
| `sfx-snap` | fishing line snapping, a sharp twang | 0.7 s | `snap` |
| `sfx-spit` | bubbles blown out underwater | 1 s | (hook shaken out) |
| `sfx-pop` | cartoon pop, a worm going on the hook | 0.5 s | `pop` |
| `sfx-boot` | soggy boot squelch | 1 s | (boot landed) |
| `sfx-catch` | short cheerful xylophone jingle | 2 s | `fanfare` |
| `sfx-duck` | duck quack | 1 s | new: ducks now and then |
| `sfx-frog` | frog croak | 1 s | new: the frog, when its throat puffs |
| `sfx-bird` | one songbird chirp | 1.5 s | new: now and then |
| `sfx-buzz` | dragonfly wing buzz | 1 s | new: when it darts past |

**Cost**: 20 sounds, about 19 s of audio, × 3 takes ≈ 57 s ≈ **600 credits**, up to about 1,000 with retakes.
Ask first (with this number) before generating, as always.

**Licence** (re-check the terms first; they were last read 2026-10-23): paid-plan output may be used
commercially, needs no credit line, and we own it. No beta features. List every clip in the README's
"Audio credits" with the tool, plan and date. Say there that the audio isn't licensed for reuse.

## 3. In the game

- Load clips like Blast Off: `CLIPS` list, `assets/<name>.mp3?v=ASSET_V`, fetched at start and decoded into the
  game's existing `AudioContext`. `sfx.x()` plays the clip if it's loaded, otherwise today's synthesized
  version. Mute and `?tbxtest` keep everything silent, as now.
- `say(key)` plays the voice clip, or falls back to `speechSynthesis` with the same text. A small queue chains
  "A pike!" + "Seventy-two centimetres!", and a new line cuts off the one playing.
- Critter sounds: at most one every 8–15 s, quiet, panned by where the animal is on screen.
- Tuning knobs: `CLIP_VOL`, `VOICE_VOL`, `CRITTER_EVERY`, `CLIP_TRIM` (per-clip start and end).
- Size: about 0.3 MB of effects, plus 0.2 MB of voice lines (1.5 MB with every size number). The service worker
  caches it all once the game is published.

## 4. Steps

1. **Voice audition** (free): done 2026-10-26, `dev/audition/index.html`. The user picked `bf_emma` (speed 0.9)
   and no child voice for now.
2. **Render the lines** (free): done 2026-10-26. 106 clips (1.65 MB; the 84 sizes are 1.3 MB of it), even
   loudness, silence trimmed. The game plays them with `say(key)` and falls back to the device voice; the
   everyday lines load with the page, and a fish's name and size load when it's hooked. All six ✱ lines are in.
3. **Sound effects**: generated 2026-10-26 (60 takes, about 640 credits), judged silently by `dev/sfx.py`, picks
   trimmed and levelled into `assets/sfx/` (160 KB), all on `dev/audition/sfx.html`. The user listened and kept
   every pick; wired in the same day, each with its synthesized sound as the fallback.
4. **Critter ambience** and the README's audio credits: done 2026-10-26 (a duck, the frog, a bird or the
   dragonfly every 8–16 s, panned to where it is). Tested with sound off and with a silent, never-started
   AudioContext standing in for the real one.

## Choices for the user

- Which voice (after the audition), and whether the child on the jetty speaks too.
- Exact sizes ("Seventy-two centimetres!", 84 clips) or size words ("A whopper!", 3 clips).
- Whether to add the ✱ lines.
- Whether to add the critter sounds.
