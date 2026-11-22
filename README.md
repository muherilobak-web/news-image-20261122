# THE WORLD — Sunday 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/muherilobak-web/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/muherilobak-web/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

A newspaper front page summing up Sunday 22 November 2026 in one image,
for the [news-image-20261122](https://make.fun/bounty/news-image-20261122)
bounty. Every picture on the page was drawn originally with Pillow in this
session — no photographs, no copied artwork, no AI-generated image.

## The eight stories

- **Lead — Gulf war widens:** Iran fires drones and missiles at four US
  bases in Bahrain on Saturday night; Manama says defences intercepted them.
- **Strait of Hormuz:** three tankers hit; no casualties reported.
- **Drones downed:** Iran claims two US drones downed (a claim, not
  confirmed fact).
- **COP31:** climate talks deadlocked over fossil fuels.
- **Peru:** magnitude 6.9 earthquake, no damage reported.
- **Mexico:** FBI most-wanted fugitive seized in Mexico.
- **Baltic:** drones hit a Russian ship in the Baltic Sea.
- **APEC:** Trump in Shenzhen; Xi, Putin talks planned.

Only verified facts are used. Where accounts conflict (the Patriot radars,
the drone shootdowns) the page reports the claim, never as confirmed fact.
No casualty numbers are given for the Mexico raid, whose reports conflict.

## Files

- `entry.png` — the front page, 1024x1024 PNG.
- `draw.py` — the script that draws `entry.png` from scratch (build-time
  only; run it with `python3 draw.py` to regenerate the image).
- `main.py` — the entrypoint. It copies `entry.png` byte-for-byte into the
  directory named by `MAKEFUN_OUTPUT_DIR` (default `/output`). Standard
  library only, no network, no randomness, no timestamps.
- `LICENSE` — MIT.
- `.makefun/owner.json` — the entrant's wallet address.

## Reproduce

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/out2 python3 main.py
sha256sum entry.png /tmp/out1/entry.png /tmp/out2/entry.png
```

Both runs produce bytes identical to `entry.png`.
