from functools import lru_cache
from math import cos, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

paper = "#f8f2e5"
ink = "#152c2b"
muted = "#435956"
red = "#983b30"
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
    else:
        for level in [26, 57, 88]:
            draw.line((x+13,y+level,x+w-13,y+level), fill="#406566", width=2)
        for i, (value, index) in enumerate([("−5.06%", "NIKKEI"), ("−5.21%", "KOSPI")]):
            start = x + 22 + i*147
            label(start, y+23, value, 29, "#ffb291")
            label(start, y+69, index, 16, "#f9e5ca")


leads = [
    ("EUROPE  /  SECURITY", "bridge", ["Kyiv bridges", "hit by missiles"],
     ["Russia's barrage also", "disrupted power."], "Associated Press"),
    ("SOUTH ASIA  /  WEATHER", "storm", ["Akvan crosses", "India’s coast"],
     ["Storm weakens over", "southern Odisha."], "India Meteorological Department"),
    ("EAST ASIA  /  MARKETS", "stocks", ["AI sell-off hits", "Asian stocks"],
     ["Japan and South Korea", "each shed over 5%."], "BNR / Indonesia economy ministry"),
]

briefs = [
    ("EUROPE · DIPLOMACY", ["EU and UK meet", "in Brussels"], "EU Council"),
    ("TÜRKİYE · CLIMATE", ["COP31 draft omits", "fossil fuels"], "AP · Draft text"),
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
    ("AUSTRALIA · TECHNOLOGY", ["Audit board spotlights", "AI quality guidance"], "AUASB"),
    ("UNITED STATES · TRAVEL", ["IT breakdowns fuel", "holiday flight worries"], "AP"),
]

draw.rectangle((0, 0, 1024, 114), fill=ink)
label(40, 17, "WORLD NEWS", 20, "#b2d7ca")
label(40, 45, "Friday, 20 November 2026", 55, paper, "Georgia Bold")
for i, (region, art, headline, detail, source) in enumerate(leads):
    x = 40 + i * 320
    scene(x, 130, art)
    label(x, 265, region, 14, red)
    lines(x, 286, headline, 32, 305, face="Georgia Bold")
    lines(x, 355, detail, 20, 305, face="Arial")
    label(x, 400, source, 13, muted)

draw.line((40, 424, 984, 424), fill=ink, width=2)
label(40, 437, "AROUND THE WORLD", 18, red)
for i, (region, headline, source) in enumerate(briefs):
    x, y = 40 + i%4*239, 463 + i//4*85
    draw.rectangle((x, y, x+227, y+78), fill="#eee8d9")
    label(x+9, y+6, region, 11, red)
    lines(x+9, y+22, headline, 19, 210)
    label(x+9, y+64, source, 11, muted)

draw.line((40, 980, 984, 980), fill=ink, width=2)
label(40, 991, "REPORTING CUT  ·  20 NOV 2026, 16:45 UTC", 15, muted)
label(683, 991, "27 STORIES  ·  ORIGINAL ILLUSTRATIONS", 14, muted)
canvas.save(Path(__file__).with_name("edition.png"), optimize=True)
