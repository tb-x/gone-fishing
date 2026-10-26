# Gone Fishing! — plan

A calm 3D fishing game for kids around 5, seen from the side as a **cross-section**: the bank, the jetty and the
child with the rod at the top, and the water cut open like an aquarium slice below, so you can *see* the fish, the
bait and what the fish think of it. Each place teaches a different way of fishing. Catch and release: every fish
goes into the sticker book and back into the water.

Folder `fishing/`, repo `gone-fishing` (when published), local port 5234. Single self-contained `index.html`,
three.js 0.160.0 from jsDelivr (import map), everything modelled in code, sound synthesized.

## Why a cross-section

- A 5-year-old can't read a bobber twitch from above. From the side they see the fish swim up, sniff the worm,
  nibble, then take it, and the bobber dips at the same moment. Cause and effect is on screen.
- **Depth is visible**: you see where the throw lands and where the worm hangs, and you set the depth by dragging
  the worm itself. No sliders, no depth numbers.
- Each species lives at its own depth (surface, middle, bottom, in the weeds), so choosing the technique and the
  spot is the whole "skill", and it's learnable by looking.

## The core loop (every technique)

1. **Pick the tackle**: three or four big round buttons with pictures (bobber, bell + sinker, spinner, fly…).
2. **Cast**, like Angry Birds: the bait sits in a slingshot on the jetty end; grab it and pull it back (it stays
   under the finger, the bands stretch into a triangle, the screen holds still), and let go. The pull's length is
   the strength, its angle the aim, a dotted arc shows where it will land, and the camera follows the flight. The rod bends back, flicks, the line arcs out, splash. With a bobber,
   drag the worm up or down to set its depth.
3. **Wait and watch**: fish that like this bait notice it, come closer, sniff, nibble.
4. **Strike**: the bite signal is different for each technique (bobber goes under, bell rings, the rod jerks).
   Tap anywhere. The window is generous (about 1.5 s) and shown with a big "!".
5. **Reel in**: wind the reel button round like a crank; winding speed is reeling speed. The fish fights in
   bursts: while it pulls (it splashes, the rod bends right over, the line goes red, shivers and creaks) stop
   winding, then wind again when it rests. Winding through a pull fills the tension ring; at full the line snaps,
   the fish swims off with the tackle, shakes the hook out, and a new hook is tied on. Strength (fight × size)
   sets how slowly a fish comes in and how fast the line strains.
6. **The catch card**: the fish turns in the air, its name is spoken, its size shows in cm against a ruler (bigger
   than last time = a gold star), it's added to the sticker book, and a "Let it go" button splashes it home.

Fish eat the worm: each nibble takes a bite, and a fish that bites unanswered swims off with it. An empty hook
catches nothing, so you reel in (the hand points at the reel) and a fresh worm pops on. That's the only cost of
a miss: no score is lost and the fish comes back later.

## Fishing techniques

| Technique | How it plays | Bite signal | Catches |
| --- | --- | --- | --- |
| **Float (bobber)** | Tap the water: the bobber floats there, the worm hangs at the tapped depth below it | Bobber bobs (nibble), then plunges under | Roach, perch, rudd, small carp: middle water |
| **Bottom (ledger + bell)** | Tap: the sinker drops to the lake bed below that spot; the rod rests on a stand with a bell | Rod tip taps, bell rings, then the rod bends | Carp, catfish, tench, crayfish, the odd old boot |
| **Lure (spinner)** | Tap to cast; the lure sinks while you wait and swims back while you reel, so reeling speed sets its depth | A predator chases and grabs it: it hooks itself | Perch, pike, zander: they only chase something moving |
| **Fly** (river) | The fly lands on the surface and drifts with the current | A splash and a fish leaping up at it | Trout, grayling |
| **Ice jig** (winter) | Drop the bait down a hole in the ice; tap to jiggle it up and down | The tiny rod tip pulls down | Perch, whitefish, burbot |
| **Crabbing line** (seaside harbour) | A line with a bait bag lowered off the harbour wall, no hook | Crabs grab on and hold; pull slowly or they let go | Crabs (into the bucket and back), starfish |
| **Boat trolling** (sea) | The boat chugs along; pick how deep the lure runs | The rod bends hard | Mackerel, cod, and a very big rare one |
| **Hand net** (rock pool, bonus) | Drag the net through the pool | — | Shrimps, little fish, a hermit crab |

The POC has the first three; they share the cast/strike/reel code and differ only in the rig, the bite signal and
which fish care.

## Places (one technique introduced per place)

1. **The Pond** (jetty, lily pads, reeds): float. Tutorial-light: a hand points at the water, then at the bobber.
2. **The Lake** (rowing-boat jetty, weed beds, deep middle): bottom rig, then lure.
3. **The River** (flowing water, current lines, stones): fly. Fish face upstream; the fly drifts.
4. **The Frozen Lake** (winter, the cross-section shows ice, snow and the hole): ice jig.
5. **The Harbour** (wall, steps, boats, seaweed): crabbing line.
6. **Out at Sea** (the boat moves, seabed scrolls): trolling.

Each place has its own species list (6–8), times of day (morning mist, sunny, evening glow), and weather
(rain rings on the surface, wind waves). Places unlock by catching any 3 kinds at the previous one, and are always
replayable. No timers, no score, no game over.

## Fish and what they like

Every species is a little table: depth band, size range (cm), speed, which baits it likes, how shy it is, how hard
it fights, how many nibbles before a real bite, and its look (body shape and colours). Behaviour:

- **Wander** in its depth band, turning at the edges and around weeds and rocks.
- **Notice** bait it likes inside its sense range (bigger for smell at the bottom, for flash with lures).
- **Approach**, pause and **sniff** (a little "?" bubble), **nibble** 0–3 times, then **bite** and **turn away**.
- **Spooked** by a splash right on top of it: darts off and comes back later (teaches "cast beside, not on").
- Predators **chase** a moving lure and lose interest when it stops.

## Collection

- **Sticker book**: a page per place, a silhouette per species that fills in when caught, with the biggest size.
- **Rare ones**: one gold or very big fish per place, and a funny junk catch (boot, teapot, rubber duck).

## Controls and screen

- Tap the water to cast; tap anywhere to strike; hold the reel button to reel. Everything else is a big button.
- Portrait: the camera follows the bait along the slice; landscape: the whole slice fits. The tackle buttons sit
  along the bottom (portrait) or the right side (landscape); home top-left, mute top-right, sticker book top-right.
- Minimal reading: names are spoken (`speechSynthesis`) and shown short.

## Sound

Synthesized Web Audio for now, with `speechSynthesis` for the spoken lines. The plan for recorded sound
(free local Kokoro voice lines, ElevenLabs sound effects, critter sounds instead of a background loop) is in
[SOUND-PLAN.md](SOUND-PLAN.md).

## Look

Low-poly and bright, flat-shaded, everything built in code: fish from scaled spheres and fins, layered soil
strata on the cut face of the bank, waving weeds, light shafts and bubbles under water, the surface as a moving
wave strip, the child as a simple round figure on the jetty edge with a hat.

## Build steps

1. **POC** (built 2026-10-26, `index.html`; `window.__gf.step(secs)` runs it without animation frames for tests): the pond cross-section, the child, a bending rod and line, tap-to-cast, float, bottom
   and lure rigs, 6 species with notice/nibble/bite/chase, strike, hold-to-reel fight with a tension ring, the
   catch card with release, a sticker row, synthesized sound. Check it's fun on a phone and a tablet.
2. **Game feel**: tutorial hand, spook-on-splash, better fight (fish pulls the line sideways, jumps for the big
   ones), size records and gold stars, telemetry milestones (`cast`, `bite`, `missed`, `caught`, `escaped`).
3. **Places 2–3** (lake, river) with fly fishing and current.
4. **Places 4–6** (frozen lake, harbour, sea) with ice jig, crabbing and trolling.
5. **Sticker book screen**, weather and time of day.
6. **Ship**: README, manifest, icons, `sw.js` (copy of `blast-off/sw.js` with `PREFIX = 'gone-fishing-'`),
   landing-page entry, `tb-x/gone-fishing` repo with Pages.

## Questions for later

- A crank-style reel (circle your finger on the reel) instead of hold-to-reel? Fun on a tablet, harder for some
  5-year-olds. Try both after the POC.
- Keep fish (bucket, aquarium at home) or always release? The plan says release; the sticker book is the reward.
