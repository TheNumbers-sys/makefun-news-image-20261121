from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = "#f5f0e5"
INK = "#171715"
RED = "#b52822"
MUTED = "#655f55"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else SANS, size)

def measure(text, f):
    b = d.textbbox((0, 0), text, font=f)
    return b[2] - b[0], b[3] - b[1]

def wrap(text, f, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = word if not line else line + " " + word
        if measure(trial, f)[0] <= max_width:
            line = trial
        else:
            if not line:
                raise ValueError(f"word too wide: {word}")
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def text_block(text, box, size, bold=False, color=INK, leading=4):
    x0, y0, x1, y1 = box
    f = font(size, bold)
    lines = wrap(text, f, x1 - x0)
    heights = [measure(line, f)[1] for line in lines]
    total_h = sum(heights) + leading * (len(lines) - 1)
    if total_h > y1 - y0:
        raise ValueError(f"text block exceeds panel: {text!r}: {total_h}>{y1-y0}")
    y = y0
    for line, lh in zip(lines, heights):
        x = x0
        raw = d.textbbox((0, 0), line, font=f)
        x -= raw[0]
        d.text((x, y), line, font=f, fill=color)
        bbox = d.textbbox((x, y), line, font=f)
        if bbox[0] < x0 or bbox[2] > x1 or bbox[1] < y0 or bbox[3] > y1:
            raise ValueError(f"text outside assigned box: {line!r} {bbox}")
        y += lh + leading

def rule(y, x0=48, x1=976, fill=INK, width=2):
    d.line((x0, y, x1, y), fill=fill, width=width)

d.text((48, 24), "THE WORLD IN ONE DAY", font=font(47, True), fill=INK)
d.rectangle((48, 88, 976, 133), fill=RED)
d.text((68, 94), "SATURDAY 21 NOVEMBER 2026", font=font(29, True), fill=PAPER)

d.text((48, 143), "IRAN STRIKES US", font=font(44, True), fill=INK)
d.text((48, 192), "BASES IN BAHRAIN", font=font(44, True), fill=INK)
lead = "Tehran says it hit two US positions at al-Riffa and Awali; Bahrain reports an industrial fire, no injuries"
text_block(lead, (48, 239, 654, 325), 19, leading=5)

d.rounded_rectangle((690, 151, 976, 323), radius=8, outline=INK, width=2)
d.text((706, 161), "GULF · SCHEMATIC", font=font(14, True), fill=MUTED)
d.polygon([(708, 203), (760, 197), (798, 207), (815, 221), (804, 235), (779, 239),
           (766, 256), (739, 250), (725, 232), (708, 230)], fill="#e7decd", outline=INK)
d.polygon([(832, 193), (860, 186), (884, 192), (899, 204), (920, 199), (948, 211),
           (957, 228), (939, 237), (914, 229), (891, 237), (875, 226), (856, 230),
           (838, 217)], fill="#e7decd", outline=INK)
d.ellipse((845, 246, 855, 256), fill=RED)
d.ellipse((870, 252, 880, 262), fill=RED)
d.text((809, 267), "BAHRAIN", font=font(13, True), fill=INK)
d.line((850, 257, 850, 275), fill=RED, width=2)
d.text((705, 291), "al-Riffa  •  Awali", font=font(15, True), fill=INK)
rule(334, fill=RED, width=4)

d.text((48, 346), "RUSSIAN MISSILE HITS ZELENSKY'S HOMETOWN", font=font(30, True), fill=INK)
text_block("Kryvyi Rih strike kills 2, wounds dozens; missiles also land in Poland",
           (48, 388, 976, 431), 20, leading=4)
rule(446)

stories = [
    ("MEXICO CAPTURES FBI MOST-WANTED CARTEL BOSS",
     'Fausto Isidro Meza Flores, "Chapo Isidro", seized in Sinaloa; at least 11 dead in violence that followed'),
    ("MARKETS SLIDE INTO CORRECTION", "AI sell-off deepens; S&P down 3.7%"),
    ("COP31 TALKS RUN PAST DEADLINE", "Antalya summit in overtime, no deal on fossil fuels"),
    ("TRUMP DEFENDS PUTIN TIES", 'After Shenzhen summit with Xi; Zelensky calls Putin a "killer"'),
    ("DENMARK BACKS US-GREENLAND DEAL 109-0", "Parliament ratifies new security deal; two new US bases"),
    ("NVIDIA HALTS H200 CHIP EXPORTS TO CHINA", "Amid US debate over advanced tech sales"),
]
cols = [(48, 500), (524, 976)]
rows = [(460, 601), (611, 752), (762, 903)]
for i, (title, body) in enumerate(stories):
    col, row = i % 2, i // 2
    x0, x1 = cols[col]
    y0, y1 = rows[row]
    d.rectangle((x0, y0, x1, y1), outline="#aaa18f", width=1)
    text_block(title, (x0 + 13, y0 + 8, x1 - 13, y0 + 66), 24, True, leading=2)
    body_right = x1 - 13
    if i == 1:
        cx0, cy0, cx1, cy1 = x1 - 113, y0 + 76, x1 - 18, y1 - 17
        d.line((cx0, cy0, cx0, cy1, cx1, cy1), fill=INK, width=2)
        pts = [(cx0 + 8, cy0 + 7), (cx0 + 29, cy0 + 12), (cx0 + 48, cy0 + 26),
               (cx0 + 67, cy0 + 31), (cx1 - 5, cy1 - 6)]
        d.line(pts, fill=RED, width=4, joint="curve")
        for px, py in (pts[0], pts[-1]):
            d.ellipse((px - 3, py - 3, px + 3, py + 3), fill=RED)
        body_right = cx0 - 9
    text_block(body, (x0 + 13, y0 + 70, body_right, y1 - 9), 17, leading=3)
    if col == 0:
        d.line((x1 + 12, y0, x1 + 12, y1), fill="#c4bcad", width=1)
    if row < 2:
        d.line((x0, y1 + 5, x1, y1 + 5), fill=RED, width=2)

d.rectangle((48, 920, 976, 972), fill="#e9e1d2")
d.text((62, 935), "ALSO:", font=font(16, True), fill=RED)
text_block("Denmark to expel Russian envoy over a foiled assassination plot",
           (126, 934, 960, 960), 16, leading=2)

assert im.size == (1024, 1024)
im.save("entry.png", format="PNG", optimize=True)
