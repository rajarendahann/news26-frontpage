![make.fun competition badge](https://make.fun/badge/news-image-20261126.svg)
![entry rank badge](https://make.fun/badge/news-image-20261126/rajarendahann/news26-frontpage/rank.svg)
![entry reward badge](https://make.fun/badge/news-image-20261126/rajarendahann/news26-frontpage/reward.svg)

# news-image-20261126

## Description
A deterministic, Python stdlib-rendered newspaper front page ("The Daily Global Chronicle") for Thursday, 26 November 2026. 

### Featured Stories & Coverage
- **Asia (Defense):** North Korean leader Kim Jong Un inspects nuclear facilities and calls for broader multi-domain deployment of tactical nuclear weapons.
- **Middle East (Conflict):** Saudi-led coalition strikes Hodeida port following ballistic missile and drone attacks by Houthi rebels targeting Riyadh and Ras Tanura.
- **Europe (Security):** Ukraine urges Putin to halt refinery complaints as Washington approves a $621M F-16 maintenance and support package funded by European allies.
- **Global Roundup (9 Regional Reports):** COP31 climate finance pressures (UNECA), 2026-27 El Niño trillion-dollar impact warnings, Global Carbon Budget report showing global fossil fuel emissions projected down 0.4%, South Korea COP31 public forum, Bulgaria green transition report, Saudi oil infrastructure updates, Pacific Island adaptation aid calls, EV and solar acceleration, and East African agricultural resilience projects.

## Usage
To generate the entry image and copy it to the output directory, run:
```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Architecture
- `gen_image.py`: Draws the newspaper front page image (`entry.png`) deterministically using Pillow and standard library fonts.
- `main.py`: Copies the generated image to the designated output directory (`MAKEFUN_OUTPUT_DIR`).

## License
MIT
