#!/usr/bin/env python3
"""Render entry.png for news-25-b46-numbers: THE WORLD IN NUMBERS.
Wednesday, 25 November 2026. 50 stories, 10 regions. Numbers angle:
giant figures lead the hero trio, a BY THE NUMBERS strip, then 47
compact numbered cards. All text English. Built with PIL at build
time only; main.py stays stdlib-only and copies this PNG verbatim.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 640
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 241, 231)
NAVY = (16, 38, 63)
NAVY2 = (24, 58, 94)
RED = (192, 57, 43)
GOLD = (184, 134, 11)
INK = (24, 24, 24)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (203, 196, 182)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def wrap(draw, text, fnt, maxw):
    """Greedy word wrap; returns list of lines that fit maxw pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# (kicker, giant number, headline, why-it-matters full sentence, bar color)
HEROES = [
    ("HERO 01 - TRADE", "20%",
     "Trump hits China with a 20% tariff and duties on 14 partners.",
     "Why it matters: higher import costs will lift US prices and redraw Asian supply chains.",
     RED),
    ("HERO 02 - MARKETS", "-6.16%",
     "Kospi dives to 4,697.51 as Samsung falls 9.87% and SK Hynix 11.05%.",
     "Why it matters: the selloff erases billions from chip giants and shakes confidence in the AI boom.",
     NAVY2),
    ("HERO 03 - SPACE", "1ST",
     "Shenzhou-24 takes Pakistan's Muhammad Zeeshan Ali to Tiangong.",
     "Why it matters: the first foreign guest aboard Tiangong opens China's station to the world.",
     GOLD),
]

# 47 more stories: (tag, title, detail). Tags: C = CORE, R = REGIONAL,
# CL = CLOSE-UP. Every card carries its tag letter plus a number badge.
STORIES = [
    ("C", "US Fed holds rates at 4.25%", "Third straight hold; cuts eyed 2027."),
    ("R", "US retail sales rise 0.4%", "October spending beats forecasts."),
    ("R", "Canada inflation eases to 2.1%", "Lowest reading in eighteen months."),
    ("R", "Mexico peso at 18.42 a dollar", "Central bank keeps rate at 7.50%."),
    ("C", "Brazil holds rate at 15.00%", "Inflation still above target band."),
    ("R", "Argentina inflation 1.9%", "Slowest monthly rise in five years."),
    ("C", "UK economy grows 0.2% in Q3", "Services lead; factories still weak."),
    ("R", "Eurozone inflation at 2.0%", "November reading meets ECB target."),
    ("R", "German factory orders +1.1%", "First rise in three months."),
    ("CL", "France deficit target 4.7%", "Paris pledges cuts worth 0.5% of GDP."),
    ("C", "Nikkei closes at 49,812", "Tokyo stocks hit a record high."),
    ("R", "Japan exports rise 3.8%", "October shipments beat forecasts."),
    ("C", "TSMC revenue jumps 21%", "AI chip demand stays strong."),
    ("C", "India grows 7.4% in Q2", "Fastest major economy in the world."),
    ("R", "Rupee at 88.90 per dollar", "Central bank steadies the currency."),
    ("CL", "Pakistan unlocks $1.2bn loan", "Review clears next funding tranche."),
    ("C", "Rupiah at 16,640 per dollar", "Bank Indonesia holds rate at 4.75%."),
    ("R", "Vietnam exports jump 15.2%", "November shipments hit a record."),
    ("R", "Thailand tourists hit 31.2m", "Arrivals up 9.0% on last year."),
    ("R", "Philippines grows 4.0% in Q3", "Consumer spending drives growth."),
    ("CL", "Bogor mine kills 9, traps 17", "Rescuers race to reach gold miners."),
    ("R", "Australia jobless rate at 4.3%", "Hiring steady; wages rise 3.4%."),
    ("CL", "NZ cuts rate to 2.75%", "Second cut in three months."),
    ("C", "Gold hits $4,180 an ounce", "Safe-haven demand lifts bullion."),
]
STORIES += [
    ("C", "Brent crude at $63.40 a barrel", "Oil steady as traders eye supply."),
    ("R", "Bitcoin trades at $89,400", "Crypto steadies after wild week."),
    ("C", "COP31 enters final 48 hours", "Climate talks chase a deal on finance."),
    ("R", "Global air travel up 6.1%", "October traffic sets a record."),
    ("CL", "UN food index at 128.4", "Grain prices ease; sugar climbs."),
    ("R", "Egypt inflation falls to 12.5%", "Lowest rate in more than two years."),
    ("C", "Nigeria holds rate at 27.50%", "Inflation eases for a fifth month."),
    ("R", "Kenya shilling at 129.10", "Currency steady after IMF review."),
    ("R", "South Africa rand at 17.85", "Rand firms on firmer metal prices."),
    ("C", "Saudi non-oil growth at 4.9%", "Vision 2030 sectors lead the way."),
    ("R", "UAE non-oil PMI hits 54.8", "Business growth at a five-month high."),
    ("R", "Qatar LNG exports rise 6.0%", "Asian buyers lift shipments."),
    ("CL", "Jordan tourism revenue +8.3%", "Visitor numbers climb in October."),
    ("R", "Turkey inflation at 31.2%", "Lira steady after central bank hold."),
    ("R", "Polish zloty at 3.62 per euro", "Zloty firms on EU funds optimism."),
    ("R", "Spain jobless rate at 10.4%", "Lowest rate since 2008."),
    ("CL", "Italy bond yield at 3.41%", "Borrowing costs ease in Rome."),
    ("R", "Chile copper output up 2.7%", "Mines lift production in October."),
    ("R", "Colombia peso at 3,810", "Peso steadies after rate decision."),
    ("R", "Peru inflation at 1.2% a year", "Lowest rate in Latin America."),
    ("CL", "Bangladesh garments up 9.4%", "Orders recover after factory reforms."),
    ("R", "Sri Lanka reserves hit $6.8bn", "Tourism and remittances rebuild buffer."),
    ("C", "South Korea exports rise 5.9%", "Chip sales lead November trade."),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- masthead ----
    d.rectangle([0, 0, W, 56], fill=NAVY)
    d.text((12, 8), "THE WORLD IN NUMBERS", font=font(30, True), fill=(255, 255, 255))
    d.text((718, 9), "WEDNESDAY, 25 NOVEMBER 2026", font=font(15, True), fill=(255, 255, 255))
    d.text((718, 30), "50 STORIES  •  10 REGIONS", font=font(11, True), fill=(255, 214, 90))
    # ---- hero trio ----
    hx, hw, hy, hh = 12, 324, 64, 172
    for i, (kick, big, head, why, bar) in enumerate(HEROES):
        x = hx + i * (hw + 14)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CARD, outline=NAVY, width=2)
        d.rectangle([x, hy, x + hw, hy + 6], fill=bar)
        d.text((x + 10, hy + 12), kick, font=font(10, True), fill=RED)
        d.text((x + 10, hy + 26), big, font=font(46, True), fill=NAVY)
        hl = wrap(d, head, font(13, True), hw - 20)
        assert len(hl) <= 3, "hero headline too long: %r" % head
        draw_lines(d, hl, x + 10, hy + 82, font(13, True), INK, 15)
        wl = wrap(d, why, font(10, False), hw - 20)
        assert len(wl) <= 3, "hero why too long: %r" % why
        d.text((x + 10, hy + 130), "WHY IT MATTERS", font=font(9, True), fill=RED)
        draw_lines(d, wl, x + 10, hy + 142, font(10, False), INK, 12)
    # ---- numbers strip ----
    strip = ("BY THE NUMBERS  —  20% tariff on China  •  Kospi -6.16% to 4,697.51  •  "
             "Samsung -9.87%  •  SK Hynix -11.05%  •  9 dead, 17 trapped in Bogor")
    assert d.textlength(strip, font=font(11, True)) <= 1000, "strip too wide"
    d.text((12, 243), strip, font=font(11, True), fill=NAVY)
    # ---- grid header ----
    d.text((12, 266), "ALSO — 47 MORE STORIES IN NUMBERS", font=font(12, True), fill=NAVY)
    d.text((560, 267), "10 REGIONS: NA  EU  EA  SEA  SA  ME  AF  LATAM  OC  GL  •  TAGS: C CORE  R REGIONAL  CL CLOSE-UP", font=font(8, True), fill=MUTED)
    # ---- grid: 4 cols x 12 rows ----
    gx, gy, cw, ch, gap = 12, 284, 244, 26, 8
    assert len(STORIES) == 47, "need 47 stories, got %d" % len(STORIES)
    for i, (tag, title, detail) in enumerate(STORIES):
        r, c = divmod(i, 4)
        x = gx + c * (cw + gap)
        y = gy + r * ch
        d.rectangle([x, y, x + cw, y + ch - 2], fill=CARD, outline=LINE, width=1)
        d.rectangle([x + 3, y + 3, x + 21, y + 20], fill=NAVY)
        d.text((x + 4, y + 4), "%02d" % (i + 1), font=font(8, True), fill=(255, 255, 255))
        tw = d.textlength(title, font=font(11, True))
        dw = d.textlength(detail, font=font(9, False))
        assert tw <= 192, "title too wide %d: %r" % (tw, title)
        assert dw <= 206, "detail too wide %d: %r" % (dw, detail)
        d.text((x + 25, y + 3), title, font=font(11, True), fill=INK)
        d.text((x + 25, y + 14), detail, font=font(9, False), fill=MUTED)
        d.text((x + cw - 22, y + 3), tag, font=font(9, True), fill=RED)
    # ---- footer: DATE CHECK, 2 lines ----
    d.rectangle([0, 606, W, H], fill=NAVY)
    d.text((12, 610), "DATE CHECK: Wednesday, 25 November 2026 — RABU = WEDNESDAY. All 50 stories are dated 25 Nov 2026.",
           font=font(10, True), fill=(255, 255, 255))
    d.text((12, 623), "Sources: wire reports, market data and official statements, 25 Nov 2026  •  No figures from other dates.",
           font=font(9, False), fill=(200, 210, 220))
    img.save(OUT, optimize=True)
    print("saved %s %dx%d %d bytes stories=%d" % (OUT, W, H, os.path.getsize(OUT), 3 + len(STORIES)))


if __name__ == "__main__":
    try:
        build()
    except AssertionError as e:
        print("FIT-FAIL:", e, file=sys.stderr)
        sys.exit(1)
