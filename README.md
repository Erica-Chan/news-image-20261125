# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Erica-Chan/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Erica-Chan/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image summing up the world's news of Wednesday, 25 November 2026: 54 stories across 10 regions, with 16 code-drawn scenes. The banner lead: the USTR proposes new Section 301 tariffs of 15–35% on 14 economies, with hearings from 25 January 2027. Five more large leads: the Kospi plunges 6.2% as the chip rout returns (Samsung −9.9%, SK Hynix −11.1%); Pakistan's first astronaut, Muhammad Zeeshan Ali, boards Tiangong aboard Shenzhou-24; a Cairo fuel-tanker fire kills at least 31; two tankers hit naval mines in the Strait of Hormuz; and South Africa's High Court sets aside the Phala Phala report, ending the impeachment process against President Ramaphosa. Ten medium cards, each with its own drawn scene and a certainty badge (CONFIRMED / REPORTED): Bangladesh's 36% garment pay rise, Huawei's conviction in a US trade-secrets trial, Champions League night, the killing of a Hamas security chief in Gaza, a deadly Russian strike in Odesa, RSF drone strikes in Sudan, the Pope's lament for COP31, the Solomons' no-foreign-bases treaty, US Q3 GDP revised up to 4.3%, and the Houthi attack on Saudi Arabia's biggest refinery — plus a by-the-numbers panel, a UTC timeline, 38 more stories with certainty dots, a world map with 16 numbered pins, and a date-check box naming stories left out because they happened on earlier days (notably the Hodeidah port strikes of 20–21 November).

The poster is drawn by `compose_poster.py` (PIL; crisp text over flat vector illustrations drawn in code — no photographs, no AI images) from the sourced, dated story list in `stories.json`, and shipped as `entry.png`. `main.ts` (Node 22, standard library only) copies it to `/output/entry.png`, so two runs write identical bytes with no network.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=96p1ekwa&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
