from functools import lru_cache
from math import cos, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

paper = "#f8f2e5"
ink = "#152c2b"
muted = "#435956"
red = "#983b30"
rule = "#d5cab5"
canvas = Image.new("RGB", (1024, 1024), paper)
draw = ImageDraw.Draw(canvas)
fonts = Path("/System/Library/Fonts/Supplemental")


@lru_cache
def font(name, size):
    return ImageFont.truetype(str(fonts / (name + ".ttf")), size)


def label(x, y, value, size, color=ink, face="Arial Bold"):
    draw.text((x, y), value, fill=color, font=font(face, size), anchor="lt")


def lines(x, y, values, size, width, color=ink, face="Arial Bold"):
    for idx, value in enumerate(values):
        if draw.textlength(value, font=font(face, size)) > width:
            raise ValueError(f"Text exceeds layout: {value}")
        label(x, y + idx * (size + 2), value, size, color, face)


def scene(x, y, kind):
    w, h = 308, 125
    draw.rectangle((x, y, x+w, y+h), fill="#163c43")
    if kind == "storm":
        draw.polygon([(x,y), (x+78,y), (x+110,y+29), (x+94,y+59),
                      (x+120,y+94),(x+105,y+h),(x,y+h)], fill="#738964")
        for offset in range(4):
            points = []
            for i in range(110):
                t = i * .044
                radius = 5 + i * .43
                points.append((x+200 + radius*cos(t+offset*1.57),
                               y+63 + radius*.83*sin(t+offset*1.57)))
            draw.line(points, fill="#b8e5df", width=4)
        draw.ellipse((x+195,y+58,x+205,y+68), fill="#ffcf94")
    elif kind == "bridge":
        for i in range(12):
            left = x + 12 + 25*i
            height = 20 + i*17 % 38
            draw.rectangle((left,y+70-height,left+16,y+75), fill="#436572")
        for level in [87, 103, 116]:
            draw.line((x+5,y+level,x+w-5,y+level), fill="#547885", width=2)
        for start, end in [(18,140),(169,290)]:
            draw.line((x+start,y+77,x+end,y+77), fill="#efca98", width=7)
            for post in [start+14,end-14]:
                draw.line((x+post,y+76,x+post,y+104), fill="#efca98", width=5)
        draw.line((x+145,y+71,x+153,y+83,x+160,y+72), fill="#f08b6f", width=3)
    elif kind == "stocks":
        for level in [26, 57, 88]:
            draw.line((x+13,y+level,x+w-13,y+level), fill="#406566", width=2)
        for i, (value, index) in enumerate([("−5.06%", "NIKKEI"), ("−5.21%", "KOSPI")]):
            start = x + 22 + i*147
            label(start, y+23, value, 29, "#ffb291")
            label(start, y+69, index, 16, "#f9e5ca")
    elif kind == "climate":
        draw.ellipse((x+209,y+18,x+278,y+87), fill="#e4ad68")
        draw.polygon([(x,y+99),(x+64,y+60),(x+110,y+89),(x+154,y+49),
                      (x+224,y+93),(x+w,y+65),(x+w,y+h),(x,y+h)], fill="#557967")
        draw.polygon([(x,y+107),(x+67,y+93),(x+136,y+110),(x+200,y+86),
                      (x+w,y+105),(x+w,y+h),(x,y+h)], fill="#8bad98")
        label(x+21,y+23,"COP31",34,"#f8f2e5","Georgia Bold")
        label(x+22,y+63,"ANTALYA",15,"#d3e5da")


leads = [
    ("EUROPE  /  SECURITY", "bridge", ["Kyiv bridges", "hit by missiles"],
     ["Russia's barrage also", "disrupted power."], "Associated Press"),
    ("SOUTH ASIA  /  WEATHER", "storm", ["Akvan crosses", "India’s coast"],
     ["Storm weakens over", "southern Odisha."], "India Meteorological Department"),
    ("EAST ASIA  /  MARKETS", "stocks", ["AI sell-off hits", "Asian stocks"],
     ["Nikkei and KOSPI", "each shed over 5%."], "BNR · Indonesia ministry"),
    ("TÜRKİYE  /  CLIMATE", "climate", ["COP31 draft omits", "fossil fuels"],
     ["Omission draws criticism", "as talks near deadline."], "Associated Press · Draft"),
]

briefs = [
    ("EUROPE · DIPLOMACY", ["EU and UK agree", "youth mobility deal"], "EU Council · Talks concluded"),
    ("OCEANIA · DIPLOMACY", ["Albanese meets Xi", "in Shenzhen"], "Australian PM"),
    ("ASIA · RIGHTS", ["Myanmar rejects", "Rohingya ruling"], "AP"),
    ("MIDDLE EAST · SECURITY", ["Saudi Arabia reports", "Houthi launches"], "AP"),
    ("CARIBBEAN · SECURITY", ["Haiti police operate", "in Martissant"], "Vant Bèf Info"),
    ("AFRICA · AID", ["$52m for children", "in three crisis zones"], "ECW · Includes South Sudan"),
    ("ASIA · SOUTH AMERICA", ["Philippines and Chile", "sign trade agreement"], "DZRH"),
    ("EUROPE · SECURITY", ["Russian missile", "comes down in Poland"], "AP"),
    ("EUROPE · LABOR", ["Italy strike disrupts", "schools and transit"], "AP"),
    ("MIDDLE EAST · SECURITY", ["Iraqi troops deploy", "south of Baghdad"], "AP"),
    ("NORTH AMERICA · MARKETS", ["U.S. tech shares", "slide at the open"], "AP"),
    ("BRAZIL · CULTURE", ["Brazil marks Black", "Awareness Day"], "Brazil Culture Ministry"),
    ("JAPAN · ECONOMY", ["October inflation", "reaches 2.3%"], "Japan Statistics Bureau"),
    ("SOUTH SUDAN · CLIMATE", ["U.N. reports on first", "drought action plan"], "UN South Sudan"),
    ("SOUTH ASIA · DIPLOMACY", ["ASEAN chief’s visit", "to Pakistan closes"], "ASEAN · Itinerary"),
    ("UNITED STATES · ECONOMY", ["Consumer sentiment", "rises to 51.5"], "Michigan survey · Bloomberg"),
    ("SOUTH AFRICA · HEALTH", ["Measles surveillance", "report released"], "NICD"),
    ("GLOBAL · HEALTH", ["UNAIDS presents", "World AIDS Day report"], "UN Geneva"),
    ("GLOBAL · EDUCATION", ["UNESCO presents", "early education report"], "UNESCO"),
    ("UKRAINE · CHILDREN", ["1,144 children killed", "or hurt through Oct."], "UNICEF · 2026 verified count"),
    ("SPACE · EUROPE / JAPAN", ["Mercury mission", "nears orbit"], "ESA · Insertion due Saturday"),
]

field = ["#234c63", "#7d4037", "#4d6656", "#46577e"]
thumbs = {}
for _, art, _, _, _ in leads:
    scene(0, 0, art)
    thumbs[art] = canvas.crop((0, 0, 308, 125)).resize((226, 92), Image.Resampling.LANCZOS)
draw.rectangle((0, 0, 1024, 1024), fill=paper)
draw.rectangle((0, 0, 1024, 9), fill=red)
label(34, 21, "WORLD NEWS", 18, red)
label(34, 48, "Friday, 20 November 2026", 54, ink, "Georgia Bold")
draw.line((34, 109, 990, 109), fill=ink, width=2)
for i, (value, context) in enumerate([
    ("3 bridges", "Hit in Kyiv · Reuters"),
    ("−5.21%", "KOSPI close · Indonesia ministry"),
    ("$52 million", "Education in crises · ECW"),
    ("1,144", "Child casualties in Ukraine · UNICEF"),
]):
    x = 34 + i*241
    label(x, 120, value, 23, red, "Georgia Bold")
    label(x, 149, context, 13, muted)
draw.line((34, 173, 990, 173), fill=rule)
for i, (region, art, headline, detail, source) in enumerate(leads):
    x = 34 + i*241
    canvas.paste(thumbs[art], (x, 187))
    label(x, 288, region, 11, field[i])
    lines(x, 308, headline, 22, 226, face="Georgia Bold")
    lines(x, 361, detail, 15, 226, face="Arial")
    label(x, 399, source, 11, muted)

draw.line((34, 423, 990, 423), fill=ink, width=2)
label(34, 434, "REGIONAL DEVELOPMENTS", 17, red)
features = [
    (0, "EU–UK", "BRUSSELS", 0), (1, "AUS–CHN", "SHENZHEN", 0),
    (2, "ICJ", "MYANMAR", 1), (5, "$52m", "3 COUNTRIES", 2),
    (6, "PHL–CHL", "TRADE PACT", 3), (4, "HAITI", "MARTISSANT", 3),
    (3, "GULF", "SAUDI ARABIA", 1), (8, "ITALY", "LABOR ACTION", 0),
]
for i, (index, sign, place, color) in enumerate(features):
    _, headline, source = briefs[index]
    x, y = 34 + i%4*241, 464 + i//4*114
    draw.rectangle((x,y,x+225,y+105), fill="#efe7d7")
    draw.rectangle((x,y,x+225,y+31), fill=field[color])
    label(x+8,y+6,sign,16,paper)
    label(x+85,y+9,place,11,"#f8ead2")
    sx, sy = x+200, y+7
    if index in (0, 1, 6):
        draw.rounded_rectangle((sx-4,sy+4,sx+7,sy+13), radius=3, outline=paper, width=2)
        draw.rounded_rectangle((sx+4,sy+1,sx+15,sy+10), radius=3, outline=paper, width=2)
    elif index == 5:
        draw.rectangle((sx,sy+2,sx+15,sy+14), outline=paper, width=2)
        draw.line((sx+7,sy+2,sx+7,sy+14), fill=paper, width=2)
    else:
        draw.ellipse((sx+2,sy,sx+13,sy+11), outline=paper, width=2)
        draw.line((sx+7,sy+11,sx+7,sy+16), fill=paper, width=2)
    lines(x+8,y+39,headline,18,209)
    label(x+8,y+86,source,11,muted)

draw.line((34, 693, 990, 693), fill=ink, width=2)
label(34, 706, "THE DAY IN BRIEF", 17, red)
regions = [
    ("EUROPE & MIDDLE EAST", [7, 9, 19, 20]),
    ("ASIA & THE AMERICAS", [10, 11, 12, 14, 15]),
    ("AFRICA & GLOBAL", [13, 16, 17, 18]),
]
for col, (region, indices) in enumerate(regions):
    x = 34 + col*322
    label(x, 744, region, 13, field[col])
    for row, index in enumerate(indices):
        _, headline, source = briefs[index]
        y = 769 + row*40
        lines(x, y, [" ".join(headline)], 14, 307)
        label(x,y+17,source,11,muted)
        draw.line((x,y+34,x+292,y+34), fill=rule)

draw.line((34, 981, 990, 981), fill=ink, width=2)
label(34, 993, "REPORTING CUT  ·  20 NOV 2026, 16:45 UTC", 14, muted)
label(682, 993, "25 STORIES  ·  ORIGINAL ILLUSTRATIONS", 13, muted)
canvas.save(Path(__file__).with_name("edition.png"), optimize=True)
