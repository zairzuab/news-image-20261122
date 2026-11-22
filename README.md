# The World Today — Sunday 22 November 2026, in Pictures

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/zairzuab/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/zairzuab/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A candidate entry for the [make.fun bounty **news-image-20261122**](https://make.fun/bounty/news-image-20261122): sum up 22 November 2026's world news in one image.

## The image

A 1024×1024 newsprint front page, **"THE WORLD TODAY — Sunday 22 November 2026"**, with **40 stories from 7 regions** — a dense front page, following the winning format of the 18 and 19 November editions (whose 9-story picture editions both missed the paid top 50):

- **Lead story — Iran strikes US bases in Bahrain:** the Revolutionary Guard fires missiles and drones at two US Patriot radars; Bahrain reports a fire at a civilian industrial facility, with no casualties.
- **COP31 nears a deal at dawn:** overtime talks in Antalya close in on a deal after 14 days; the draft still splits on fossil fuels and finance.
- **Russia's 400-drone barrage:** missiles hit Lviv; two killed, ten hurt, as Kyiv's defences down most of the wave.
- **M6.8 quake shakes Peru's Andes** — a strong quake strikes the Andes; no damage or casualties reported.
- **Sparta II ablaze after a drone hit** — a Russian merchant ship burns in the Gulf of Finland; Finland says the war is spilling over.
- **Chip stocks plunge 10%** — US stocks slide as the chip index falls and TSMC sinks; Bitcoin drops to a two-year low.
- **The Day in Brief:** 34 more stories — France's fourth weekend of cost-of-living protests, the ECB chief search, the EU–Indonesia trade deal, Hong Kong's Election Committee vote, the Myanmar quake, Al-Shabaab's Somali ambush, the Sinaloa kingpin's capture, the Democrats reclaiming Congress, the Riemann hypothesis claim, and more. Every story was first reported on Sunday 22 November 2026.

## How it runs

`main.ts` (Node 22, standard library only) decodes the image shipped as
base64 text in `entry.png.b64` and writes it to `/output/entry.png`. It is
fully deterministic and needs no network:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`compose.py` is the build script that laid out the front page: masthead,
six procedurally drawn illustration panels (Gulf dusk, Antalya dawn,
Lviv night sky, seismograph, burning ship, markets chart) and the
day-in-brief list. The composed image is 1024×1024 PNG, 162,550 bytes —
inside the 1 MiB gate — and two runs of the script produce identical bytes.

## License

MIT — see [LICENSE](LICENSE).
