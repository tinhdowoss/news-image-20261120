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
    ("EUROPE", ["EU and UK meet", "in Brussels"], "EU Council"),
    ("OCEANIA · EAST ASIA", ["Albanese meets Xi", "in Shenzhen"], "Australian PM"),
    ("AFRICA · AID", ["$52m for learning", "in crisis zones"], "ECW · Includes South Sudan"),
    ("MIDDLE EAST", ["Saudi Arabia reports", "new Houthi launches"], "Associated Press"),
    ("CARIBBEAN", ["Haiti operation", "continues in Martissant"], "Vant Bèf Info"),
    ("NORTH AMERICA", ["U.S. tech shares", "slide at the open"], "Associated Press"),
    ("SOUTHEAST ASIA", ["Myanmar rejects", "Rohingya ruling"], "Associated Press"),
    ("TÜRKİYE · CLIMATE", ["COP31 draft omits", "fossil fuels"], "Associated Press · Draft text"),
    ("SPACE SCIENCE", ["Mercury mission", "nears orbit"], "ESA · Insertion due Saturday"),
]

draw.rectangle((0, 0, 1024, 151), fill=ink)
label(40, 27, "WORLD NEWS", 24, "#b2d7ca")
label(40, 62, "Friday, 20 November 2026", 60, paper, "Georgia Bold")
label(42, 165, "THE DAY’S LEADING STORIES", 18, red)
for i, (region, art, headline, detail, source) in enumerate(leads):
    x = 40 + i * 320
    scene(x, 197, art)
    label(x, 335, region, 15, red)
    lines(x, 361, headline, 33, 305, face="Georgia Bold")
    lines(x, 438, detail, 23, 305, face="Arial")
    label(x, 492, source, 14, muted)

draw.line((40, 524, 984, 524), fill=ink, width=2)
label(40, 541, "AROUND THE WORLD", 19, red)
for i, (region, headline, source) in enumerate(briefs):
    x, y = 40 + i%3*320, 579 + i//3*130
    draw.rectangle((x, y, x+307, y+118), fill="#eee8d9")
    label(x+11, y+10, region, 15, red)
    lines(x+11, y+34, headline, 25, 287)
    label(x+11, y+94, source, 15, muted)

draw.line((40, 973, 984, 973), fill=ink, width=2)
label(40, 991, "REPORTING CUT  ·  20 NOV 2026, 15:00 UTC", 15, muted)
label(683, 991, "ORIGINAL EDITORIAL ILLUSTRATIONS", 14, muted)
canvas.save(Path(__file__).with_name("edition.png"), optimize=True)
