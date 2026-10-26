# Gone Fishing!

A calm 3D fishing game for kids around 5, seen from the side like a slice through a pond: the jetty and the
child with the rod at the top, and the water cut open below so you can watch the fish find the bait. Every fish
is caught, admired and let go again.

**This is the proof of concept**: one pond, three ways to fish. The full plan (more places, fly fishing, ice
fishing, crabbing, a sticker book) is in [PLAN.md](PLAN.md).

## How it plays

- Pick your tackle with the three round buttons: **bobber**, **bell and sinker** (bottom fishing) or **spinner**.
- **Throw it like Angry Birds**: a wooden slingshot stands on the end of the jetty with the bait sitting in its
  pouch. Grab the bait and pull it back: it stays right under your finger (as far as the band reaches), and the
  two bands stretch from the prongs into a triangle, back band behind the bait and front band in front, with a
  faint fill that turns from green to yellow to red. The screen holds still while you pull. Let go and it flies
  the other way: the longer the pull, the further; pulling down throws high, pulling straight back throws low and
  fast. A dotted arc with a yellow ring shows where it will land, and the camera follows the bait through the
  air. A tiny pull is called off, and a touch away from the bait just shows the hand pointing at it.
- With the bobber, **drag the worm** up or down (the little ↕ badge) to choose how deep it hangs: deep for carp,
  middle for roach and perch.
- **Watch.** A fish that likes the bait swims over, sniffs it (a "?"), nibbles, then really bites.
- **Bobber**: wait until it goes right under, then tap. **Bell**: wait until it rings and the rod bends, then tap.
  Tapping during the nibbles is too soon and the fish swims off; it comes back later.
- **Fish eat the worm.** Every nibble takes a bite out of it (it gets smaller), and a fish that bites when you
  don't tap swims off with the rest. No fish comes to an empty hook: the hand points at the reel, and reeling in
  (or touching the water to throw again) puts a fresh worm on. The spinner never runs out.
- **The reel is a crank**: put a finger on the big round button and wind it round and round (the yellow knob
  follows your finger, and the ratchet clicks). The faster you wind, the faster the line comes in. A press on its
  own strikes a bite. Space winds it on a computer.
- **Spinner**: wind the reel to make it swim. Pike and perch chase a moving spinner and grab it themselves; if
  you stop, they lose interest.
- **Reeling in a fish**: wind while it rests (the button is green). When the button turns red with a hand, the
  fish is pulling: stop winding! Winding through a pull fills the ring, the line turns red, shivers and creaks,
  and if the ring fills up **the line snaps**. The fish swims off trailing your tackle, shakes the hook out (💨,
  it's fine) and a new hook is tied on (✨).
- **Bigger, stronger fish are harder**: they come in slowly however fast you wind, winding against their pull
  hardly slows them, and the line strains faster. A roach takes about 7 seconds and never snaps the line; a pike
  takes about 20 and always snaps it if you never stop winding.
- The catch card shows the fish, its name and size, and a sticker fills in at the top. Tap the wave button to let
  it go. There's an old boot on the bottom too: land the sinker anywhere near it (or hang a bobber's worm near the
  bottom close by) and it snags.
- Touch the water while the bait is out to reel it straight back into the slingshot. Space works as the reel button on a
  computer.
- Around the pond: a duck family, a frog on a lily pad, a dragonfly, and in the cut-open bank roots, an
  earthworm and two fossils.

## Fish

Roach and perch in the middle water (bobber), carp and catfish on the bottom (bell and sinker), pike and perch
for the spinner, and one old boot.

## Running it

From this folder: `python -m http.server 5234`, then open http://localhost:5234/. Add `?tbxtest` (or `?mute`)
to keep it silent while testing.

## Tuning knobs

At the top of the script in `index.html`:

- `STRIKE_WINDOW`: seconds to tap after the bobber goes under or the bell rings (1.8).
- `THROW_SPEED`, `GRAVITY`: how far a full-strength throw goes and how high it arcs.
- `SLING_REACH`: how far the bait can be pulled out of the slingshot, as a share of the screen's short side
  (0.2); that's a full-strength throw.
- `GRAB_PX`: how near the bait a finger has to land to grab it (75 px).
- `PULL_MIN`: a pull shorter than this share of a full one is called off.
- `BOOT_REACH`: how near the old boot a sinker has to land to snag it.
- `WORM_BITE`: how much of the worm each nibble eats (0.3, so three nibbles leave a scrap).
- `CAST_X`: where a throw can land; weaker or stronger throws are bent to land just off the jetty or at the reeds.
- `FLOAT_DEPTH`: where the worm hangs under a new bobber.
- `NOTICE_EVERY`, `SENSE`: how often and from how far a fish notices each bait.
- `REEL_SPEED`, `RETRIEVE_SPEED`, `LURE_SPEED`, `LURE_SINK`: how fast things come in and sink.
- `TENSION_UP`, `TENSION_DOWN`: how quickly the line strains when you reel through a pull, and eases off.
- `ESCAPE_COOL`: how long a fish that got away ignores bait.
- `SNAP_SPIT`: after the line snaps, how long the fish swims off with the tackle before it shakes the hook out.
- `CRANK_FULL`: how fast you wind the reel for full speed (7 radians a second, about one turn a second).
- How hard each fish is to reel in is its `fight` (in `SPECIES`) times its size.
- `HINT_AFTER`: idle seconds before the pointing hand shows where to tap.
- `VIEW_W`: how much of the pond fits across a landscape screen.
- `CLIP_VOL`, `VOICE_VOL`: how loud the sound effects and the coach's voice are.
- `CRITTER_EVERY`: seconds between the pond-life sounds (8 to 16).
- `SFX_V`, `VOICE_V`: bump after replacing a file in `assets/sfx/` or `assets/voice/`.
- `SPECIES`: each fish's depth, size, speed, favourite baits, nibbles and how hard it fights.

## Sound

The coach's voice and the sound effects are recorded (see below). If a voice clip can't load, the browser's own
voice says the same words; if an effect can't load, a synthesized version plays instead (Web Audio). Now and then
a duck, the frog, a bird or the dragonfly is heard, from where it is on screen. How it was made is in
[SOUND-PLAN.md](SOUND-PLAN.md).

To change or add a spoken line: edit `LINES` in `dev/voices.py` (and `LINE_TEXT` in `index.html`), then run
`../_tools/kokoro/venv/Scripts/python dev/voices.py` from this folder, and bump `VOICE_V` in `index.html`.
`dev/audition/lines.html` lists every line to listen to.

## Audio credits

- **Spoken lines** (`assets/voice/*.mp3`, 106 clips, listed with their words in `assets/voice/clips.json`): made
  on 2026-10-26 with **Kokoro-82M** v1.0 (Apache 2.0) through kokoro-onnx, run locally, voice `bf_emma` at
  speed 0.9. The coaching tips, the fish names, "Now!", "A new one for your book!", "Your biggest one yet!",
  "Bye-bye, fish! Off you swim!", and every size from "Twelve centimetres!" to "Ninety-five centimetres!".
  No credit is required; it's listed here so we always know where each clip came from.
- **Sound effects** (`assets/sfx/*.mp3`, 20 clips, listed in `assets/sfx/clips.json`): made on 2026-10-26 with
  **ElevenLabs Sound Effects** on the paid **Creator** plan, 3 takes each, the best trimmed and levelled by
  `dev/sfx.py`. Slingshot stretch and twang, line whoosh, plop, splash, bobber gulp, bubble nibble, bite bell, rod
  zing, reel click, line creak, line snap, bubbles, worm pop, soggy boot, catch jingle, duck, frog, bird and
  dragonfly. Paid-plan audio needs no credit line and may be used commercially; it isn't licensed for reuse
  outside this game. `dev/audition/sfx.html` has every pick and every take.
