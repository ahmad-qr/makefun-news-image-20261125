#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news summary image (1024x1024).

Renders ten verified stories from Wednesday 25 November 2026 as a
newspaper-style infographic with Pillow and the DejaVu fonts. This script
runs on the build machine only; the entry program (main.py) is stdlib-only
and copies the finished PNG. Story sources: Reuters, RFE/RL, AFP, UNAIDS.
"""
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024
PAPER = (250, 248, 243)
NAVY = (12, 32, 58)
GOLD = (200, 162, 42)
INK = (22, 28, 36)
GREY = (96, 102, 112)
STRIPE = (239, 237, 231)
DIVIDER = (214, 210, 202)

BOLD_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TAG_COLOURS = {
    "WAR": (158, 32, 32),
    "CLIMATE": (176, 74, 28),
    "MIDEAST": (120, 72, 160),
    "SPACE": (30, 80, 160),
    "US": (24, 110, 88),
    "CYBER": (90, 40, 120),
    "MARKETS": (150, 110, 20),
    "ASIA": (24, 110, 88),
    "HEALTH": (176, 74, 28),
}

# (tag, headline, detail) — headlines are kept short so each fits one line.
STORIES = [
    ("WAR", "Zelenskiy confirms Ukraine hit Russian ship",
     "Kyiv claims the Gulf of Finland drone strike; Norway urges caution. (Reuters)"),
    ("WAR", "Russian war dead pass 700,000",
     "New analysis puts Russian soldiers killed in Ukraine near 700,000. (RFE/RL)"),
    ("CLIMATE", "COP31 climate talks collapse",
     "Antalya summit ends with no deal as oil producers block phase-out text. (AFP)"),
    ("MIDEAST", "Houthi drone hits Riyadh's tallest tower",
     "11 wounded in the strike on the Saudi capital, civil defence says. (Reuters)"),
    ("SPACE", "First Pakistani reaches orbit",
     "Shenzhou-24 carries a Pakistani astronaut to China's Tiangong station. (Reuters)"),
    ("US", "Trump gives Giuliani Medal of Freedom",
     "Ex-mayor honoured in a closed Oval Office ceremony on Tuesday. (Reuters)"),
    ("CYBER", "CIA and spy agency hit by breach",
     "Unclassified data exposed in a breach, NYT reports; no classified loss. (Reuters)"),
    ("MARKETS", "AI shares slide as tariff threat grows",
     "Nasdaq falls 1.5%, Nvidia about 6% on reports of new US tariffs. (Reuters)"),
    ("ASIA", "Malaysia to return 6,500 Rohingya",
     "Refugees to be sent back to Myanmar in December, PM Anwar says. (Reuters)"),
    ("HEALTH", "AIDS deaths fall to 20-year low",
     "570,000 deaths in 2025, but HIV funding fell 18%, UNAIDS warns. (UNAIDS)"),
]

HEADER_HEIGHT = 148
ROW_HEIGHT = 83
FOOTER_TOP = 982


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_header(canvas):
    pen = ImageDraw.Draw(canvas)
    pen.rectangle((0, 0, WIDTH, HEADER_HEIGHT), fill=NAVY)
    pen.rectangle((0, HEADER_HEIGHT, WIDTH, HEADER_HEIGHT + 4), fill=GOLD)
    pen.text((30, 22), "THE WORLD TODAY", font=font(BOLD_FONT, 60),
             fill=(255, 255, 255))
    pen.text((30, 100), "WORLD NEWS \u2022 WEDNESDAY 25 NOVEMBER 2026",
             font=font(BOLD_FONT, 25), fill=(216, 180, 86))


def draw_story(canvas, number, top, tag, headline, detail):
    pen = ImageDraw.Draw(canvas)
    if number % 2:
        pen.rectangle((0, top, WIDTH, top + ROW_HEIGHT), fill=STRIPE)
    colour = TAG_COLOURS[tag]
    pen.rectangle((0, top, 10, top + ROW_HEIGHT), fill=colour)
    pen.text((26, top + 14), tag, font=font(BOLD_FONT, 18), fill=colour)
    head = font(BOLD_FONT, 23)
    if pen.textlength(headline, font=head) > 840:
        raise ValueError(f"headline too long for one line: {headline!r}")
    pen.text((148, top + 10), headline, font=head, fill=INK)
    body = font(PLAIN_FONT, 19)
    if pen.textlength(detail, font=body) > 840:
        raise ValueError(f"detail too long for one line: {detail!r}")
    pen.text((148, top + 56), detail, font=body, fill=GREY)
    if number < len(STORIES) - 1:
        pen.line((0, top + ROW_HEIGHT, WIDTH, top + ROW_HEIGHT), fill=DIVIDER)


def draw_footer(canvas):
    pen = ImageDraw.Draw(canvas)
    pen.rectangle((0, FOOTER_TOP, WIDTH, HEIGHT), fill=NAVY)
    small = font(PLAIN_FONT, 17)
    line = "Sources: Reuters \u2022 RFE/RL \u2022 AFP \u2022 UNAIDS"
    width = pen.textlength(line, font=small)
    pen.text(((WIDTH - width) / 2, 998), line, font=small,
             fill=(255, 255, 255))


def main():
    canvas = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw_header(canvas)
    for number, (tag, headline, detail) in enumerate(STORIES):
        top = HEADER_HEIGHT + 4 + number * ROW_HEIGHT
        draw_story(canvas, number, top, tag, headline, detail)
    draw_footer(canvas)
    canvas.save("news.png")
    print(f"saved news.png {canvas.size[0]}x{canvas.size[1]}")


if __name__ == "__main__":
    main()
