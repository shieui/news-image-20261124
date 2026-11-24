#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page to entry.png.

Build-time script only. It runs here, on this machine, with Pillow.
The graded entrypoint (main.py) never imports Pillow: it only copies
the PNG this script produces.

Layout is fixed to a measured vertical budget (1024 px tall):
masthead 32-190, lead 198-472, middle row 488-690, bottom row
706-906, also-today 918-942, footer 956. Every block's copy is kept
short enough to fit its slot at the sizes used.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 229)
INK = (24, 24, 22)
RED = (178, 34, 34)
DARK_BLUE = (31, 58, 95)
TEAL = (14, 110, 105)
GREY = (92, 88, 80)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped paragraph; returns y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, color=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=color)


def kicker(draw, x, y, text, color=RED):
    draw.text((x, y), text, font=font(SANS_B, 20), fill=color)


def headline(draw, x, y, text, max_w, size=27, leading=33):
    return para(draw, x, y, text, font(SERIF_B, size), max_w, leading)


def draw_jets_scene(draw, x0, y0, x1, y1):
    """Stylised scene: jets over the sea near an island, for the lead art."""
    sky = (196, 222, 235)
    sea = (146, 184, 205)
    deep = (96, 140, 168)
    draw.rectangle([x0, y0, x1, y1], fill=sky)
    draw.ellipse([x1 - 78, y0 + 18, x1 - 22, y0 + 74], fill=(224, 178, 74))
    for cx, cy, s in [(x0 + 60, y0 + 42, 26), (x0 + 150, y0 + 26, 20),
                      (x0 + 260, y0 + 58, 18)]:
        draw.ellipse([cx - s, cy - s // 2, cx + s, cy + s // 2],
                     fill=(240, 244, 246))
    horizon = y0 + (y1 - y0) * 2 // 3
    draw.rectangle([x0, horizon, x1, y1], fill=sea)
    for wy in range(horizon + 14, y1 - 6, 22):
        for wx in range(x0 + 8, x1 - 20, 44):
            draw.arc([wx, wy, wx + 34, wy + 14], 180, 360, fill=deep, width=2)
    draw.polygon([(x0 + 30, y1), (x0 + 95, horizon + 26), (x0 + 175, horizon + 26),
                  (x0 + 235, y1)], fill=(88, 104, 78))
    draw.rectangle([x0 + 118, horizon - 6, x0 + 128, horizon + 26], fill=(245, 245, 240))
    draw.rectangle([x0 + 114, horizon - 14, x0 + 132, horizon - 6], fill=RED)
    for jx, jy, s in [(x0 + 210, y0 + 58, 1.0), (x0 + 300, y0 + 96, 0.8)]:
        pts = [(jx, jy), (jx - 34 * s, jy + 12 * s), (jx - 20 * s, jy + 2 * s),
               (jx - 30 * s, jy - 8 * s)]
        draw.polygon(pts, fill=(38, 44, 58))
        draw.line([(jx - 34 * s, jy + 8 * s), (jx - 88 * s, jy + 20 * s)],
                  fill=(255, 255, 255), width=3)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def story_row(draw, y_rule, stories):
    """One row of three stories. Each story: (kicker, colour, headline, deck).
    Returns the y of the divider below the row."""
    cols = [(44, 300), (362, 300), (680, 300)]
    for (cx, cw), (kick, colour, head, deck) in zip(cols, stories):
        draw.rectangle([cx, y_rule, cx + cw, y_rule + 3], fill=colour)
        kicker(draw, cx, y_rule + 8, kick, colour)
        y = headline(draw, cx, y_rule + 36, head, cw)
        para(draw, cx, y + 6, deck, font(SANS, 18), cw, 23)
    return y_rule + 202


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([10, 10, 1013, 1013], outline=RED, width=2)
    d.rectangle([18, 18, 1005, 1005], outline=INK, width=1)

    # masthead
    centred(d, 512, 32, "T H E   W O R L D   I N   O N E   D A Y",
            font(SANS_B, 27), GREY)
    size = 60
    while True:
        fnt = font(SERIF_B, size)
        if d.textlength("TUESDAY 24 NOVEMBER 2026", font=fnt) <= 936:
            break
        size -= 2
    centred(d, 512, 68, "TUESDAY 24 NOVEMBER 2026", fnt)
    d.rectangle([44, 146, 980, 149], fill=RED)
    d.rectangle([44, 154, 980, 155], fill=INK)
    centred(d, 512, 164, "Six stories that defined the day  \u2022  From every region, every field",
            font(SANS, 22), GREY)

    # ---- lead story ----
    kicker(d, 44, 198, "LEAD STORY  \u2022  KOREA")
    y = headline(d, 44, 226, "Russian jets spark shelter alert on Korean island",
                 536, size=40, leading=45)
    para(d, 44, y + 8,
         "Russian warplanes entered South Korea's air defence zone near "
         "Ulleung on Tuesday; Seoul scrambled jets. A shelter alert "
         "wrongly warned of a breach, then wrongly blamed North Korea. "
         "It was lifted in minutes.",
         font(SANS, 19), 536, 25)
    draw_jets_scene(d, 600, 206, 980, 414)
    para(d, 600, 422, "Russian warplanes neared Ulleung; Seoul scrambled jets.",
         font(SERIF, 17), 380, 21, color=GREY)

    d.line([(44, 472), (980, 472)], fill=INK, width=2)

    # ---- middle row ----
    story_row(d, 488, [
        ("SECURITY  \u2022  EUROPE", DARK_BLUE,
         "NATO vows to defend space after Russia warning",
         "Allies say Moscow may launch a nuclear satellite within weeks."),
        ("POLITICS  \u2022  USA", RED,
         "Democrats clinch biggest House majority since 1992",
         "Final count: at least 258 seats \u2014 power to block Trump's agenda."),
        ("WAR  \u2022  UKRAINE", RED,
         "Russian strikes kill at least 15 in Kyiv region",
         "Overnight missiles hit towns around the capital, Ukraine says."),
    ])
    d.line([(44, 690), (980, 690)], fill=INK, width=2)

    # ---- bottom row ----
    story_row(d, 706, [
        ("SPORT  \u2022  WORLD CUP", DARK_BLUE,
         "Four hosts for the 2031 Women's World Cup",
         "US, Mexico, Costa Rica, Jamaica host 2031; UK gets 2035."),
        ("DISASTER  \u2022  AFRICA", TEAL,
         "Fire engulfs six hotels on Zanzibar",
         "Blaze sweeps resorts on the island; 180 tourists evacuated."),
        ("POLITICS  \u2022  USA", RED,
         "Trump halts Iowa explosives detonation",
         "Planned detonation paused pending a court ruling."),
    ])
    d.line([(44, 906), (980, 906)], fill=RED, width=2)

    # ---- also today, one line ----
    label = "ALSO TODAY:  "
    d.text((44, 918), label, font=font(SANS_B, 18), fill=RED)
    lx = 44 + d.textlength(label, font=font(SANS_B, 18))
    d.text((lx, 918),
           "Jimmy Gomez resigns  \u2022  Magnitude 4.1 quake in Pakistan  "
           "\u2022  Amtrak derails; five hurt",
           font=font(SANS, 18), fill=INK)

    centred(d, 512, 956, "All stories as reported on Tuesday 24 November 2026  \u2022  One day, one page.",
            font(SERIF, 16), GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
