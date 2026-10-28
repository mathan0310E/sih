"""Build the academic presentation: Philosophy and Its Role in Education and Society.

Design: 16:9 widescreen, off-white ground, navy/charcoal type with restrained
orange accents. Every major statement carries an adjacent visual (diagram or
licensed photograph). Speaker notes are attached to every slide.

All citations are drawn from refs.py, which was verified against Crossref and
Open Library. No findings, statistics or quotations are invented.
"""
import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

from svglib import wrap as wrap_pts

# ---------------------------------------------------------------- palette
NAVY = RGBColor(0x0F, 0x2D, 0x52)
NAVY_D = RGBColor(0x0A, 0x1E, 0x38)
NAVY_L = RGBColor(0x1C, 0x4B, 0x7D)
CHAR = RGBColor(0x33, 0x3A, 0x42)
ORANGE = RGBColor(0xC2, 0x5E, 0x1A)
AMBER = RGBColor(0xE8, 0xA3, 0x3D)
TEAL = RGBColor(0x16, 0x6B, 0x67)
PURPLE = RGBColor(0x5B, 0x4B, 0x8A)
GREEN = RGBColor(0x2E, 0x6B, 0x4F)
GREY = RGBColor(0x5F, 0x6B, 0x7A)
GREY_L = RGBColor(0x8A, 0x94, 0xA2)
BORDER = RGBColor(0xD5, 0xDA, 0xE1)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
OFF = RGBColor(0xFA, 0xF9, 0xF6)
TINT = RGBColor(0xEE, 0xF3, 0xF9)

FONT = "Calibri"
FONT_H = "Calibri"

# ---------------------------------------------------------------- geometry
SW, SH = 13.3333, 7.5
ML, MR = 0.62, 0.62
CW = SW - ML - MR                     # 12.0933
TITLE_Y = 0.40
RULE_Y = 1.04
BODY_TOP = 1.30
BODY_BOT = 6.92
BODY_H = BODY_BOT - BODY_TOP

# two-column split
LCOL_W = 5.90
RCOL_X = ML + 6.23                    # 6.85
RCOL_W = CW - 6.23                    # 5.8633

ASSETS = "/workspace/project/assets"
DIAG = os.path.join(ASSETS, "diagrams")
PHOTO = os.path.join(ASSETS, "photos")
ICON = os.path.join(ASSETS, "icons")
OUTDIR = "/workspace/project/out"

FITLOG = []


# ---------------------------------------------------------------- helpers
PALETTE = {"navy": NAVY, "navy_d": NAVY_D, "navy_l": NAVY_L, "orange": ORANGE,
           "amber": AMBER, "teal": TEAL, "purple": PURPLE, "green": GREEN,
           "crimson": RGBColor(0x9E, 0x2B, 0x2B), "grey": GREY, "char": CHAR,
           "white": WHITE}


def C(name):
    """Resolve a palette name to an RGBColor."""
    if isinstance(name, RGBColor):
        return name
    return PALETTE[name]


def _cname(color):
    """Reverse-map an RGBColor to its icon-file colour name."""
    for n, v in PALETTE.items():
        if v == color:
            return n
    raise KeyError(f"no icon colour named for {color}")


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def rect(slide, x, y, w, h, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
    return s


def line_h(slide, x, y, w, color=BORDER, lw=0.75):
    return rect(slide, x, y, w, 0.011, fill=color)


def estimate_lines(text, size_pt, width_in):
    """Number of wrapped lines for text at size_pt inside width_in inches."""
    return len(wrap_pts(text, size_pt, width_in * 72.0))


def fits(text, size_pt, width_in, height_in, lh=1.24):
    return estimate_lines(text, size_pt, width_in) * size_pt * lh <= height_in * 72.0


def autosize(text, width_in, height_in, start, minimum=9.0, lh=1.24):
    """Largest size (<= start, >= minimum) at which text fits the box."""
    s = start
    while s > minimum and not fits(text, s, width_in, height_in, lh):
        s -= 0.5
    if not fits(text, s, width_in, height_in, lh):
        FITLOG.append(f"text still overflows at {s}pt: {text[:70]!r}")
    return s


def textbox(slide, x, y, w, h, wrap=True, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf


def para(tf, runs, size=13, color=CHAR, bold=False, align=PP_ALIGN.LEFT,
         space_after=0, space_before=0, first=False, line_spacing=1.06,
         bullet=None, bullet_color=None, indent=0.0, font=FONT):
    """Add a paragraph. `runs` is a str or list of (text, bold, color) tuples."""
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(space_before)
    p.line_spacing = line_spacing
    if indent:
        p.paragraph_format if False else None
        pPr = p._pPr if p._pPr is not None else p._p.get_or_add_pPr()
        pPr.set("marL", str(int(indent * 914400)))
        pPr.set("indent", str(int(-indent * 914400)))
    if bullet:
        r = p.add_run()
        r.text = bullet
        r.font.size = Pt(size)
        r.font.bold = True
        r.font.color.rgb = bullet_color or ORANGE
        r.font.name = font
        r2 = p.add_run()
        r2.text = "  "
        r2.font.size = Pt(size)
        r2.font.name = font
    if isinstance(runs, str):
        runs = [(runs, bold, color)]
    for t, b, c in runs:
        r = p.add_run()
        r.text = t
        r.font.size = Pt(size)
        r.font.bold = b
        r.font.color.rgb = c
        r.font.name = font
    return p


def pic_cover(slide, path, x, y, w, h):
    """Insert image cropped to fill the box exactly (centre-weighted)."""
    with Image.open(path) as im:
        iw, ih = im.size
    box_ar = w / h
    img_ar = iw / ih
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    if img_ar > box_ar:
        frac = (1 - box_ar / img_ar) / 2
        pic.crop_left = frac
        pic.crop_right = frac
    elif img_ar < box_ar:
        frac = (1 - img_ar / box_ar) / 2
        pic.crop_top = frac
        pic.crop_bottom = frac
    return pic


def pic_fit(slide, path, x, y, w, h, halign="center", valign="middle"):
    """Insert image scaled to fit inside the box, preserving aspect ratio."""
    with Image.open(path) as im:
        iw, ih = im.size
    ar = iw / ih
    if ar > w / h:
        dw, dh = w, w / ar
    else:
        dh, dw = h, h * ar
    dx = x + (w - dw) / 2 if halign == "center" else (x if halign == "left" else x + w - dw)
    dy = y + (h - dh) / 2 if valign == "middle" else (y if valign == "top" else y + h - dh)
    return slide.shapes.add_picture(path, Inches(dx), Inches(dy), Inches(dw), Inches(dh))


def icon(slide, name, color, x, y, size):
    """Insert an icon; `color` may be a palette name or an RGBColor."""
    p = os.path.join(ICON, f"{name}_{_cname(C(color))}.png")
    return slide.shapes.add_picture(p, Inches(x), Inches(y), Inches(size), Inches(size))


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def photo_credit(slide, key, x, y, w, text_size=7.2):
    """Attribution line for a licensed photograph, taken from the manifest."""
    import json
    man = _MANIFEST()
    m = man.get(key)
    if not m:
        return
    txt = f"Image: {m['title'].replace('File:', '')} — {m['artist'] or 'unknown'} ({m['lic']}), via Wikimedia Commons"
    tf = textbox(slide, x, y, w, 0.24)
    para(tf, txt, size=text_size, color=GREY_L, first=True, line_spacing=1.0)


_MAN = None


def _MANIFEST():
    global _MAN
    if _MAN is None:
        import json
        _MAN = json.load(open(os.path.join(ASSETS, "photo_manifest.json")))
    return _MAN


# ---------------------------------------------------------------- chrome
def slide_frame(slide, kicker, title, number, total=18):
    rect(slide, 0, 0, SW, SH, fill=WHITE)
    # left accent spine
    rect(slide, 0, 0, 0.105, SH, fill=ORANGE)
    # kicker
    tf = textbox(slide, ML, TITLE_Y - 0.01, CW, 0.24)
    para(tf, kicker.upper(), size=9.6, color=ORANGE, bold=True, first=True)
    # title
    tsize = 25 if len(title) <= 58 else (22.5 if len(title) <= 76 else 20.5)
    tf2 = textbox(slide, ML, TITLE_Y + 0.21, CW - 1.2, 0.62)
    para(tf2, title, size=tsize, color=NAVY, bold=True, first=True, line_spacing=1.0,
         font=FONT_H)
    line_h(slide, ML, RULE_Y, CW)
    # footer
    tf3 = textbox(slide, ML, SH - 0.40, CW - 1.0, 0.24)
    para(tf3, "Philosophy and Its Role in Education and Society", size=8.2,
         color=GREY_L, first=True)
    tf4 = textbox(slide, SW - MR - 0.9, SH - 0.40, 0.9, 0.24)
    para(tf4, f"{number} / {total}", size=8.6, color=GREY, bold=True, first=True,
         align=PP_ALIGN.RIGHT)


def statement_card(slide, x, y, w, h, icon_name, icon_color, heading, body,
                   accent, hsize=13.5, bsize=11.2):
    """Rounded card: accent bar, icon, bold heading, explanatory body."""
    rect(slide, x, y, w, h, fill=TINT, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(slide, x, y + 0.10, 0.055, h - 0.20, fill=C(accent))
    icon(slide, icon_name, icon_color, x + 0.20, y + 0.15, 0.26)
    tx = x + 0.58
    tw = w - 0.58 - 0.18
    avail_h = h - 0.30
    hs = autosize(heading, tw, avail_h, hsize, 10.5)
    tf = textbox(slide, tx, y + 0.14, tw, 0.30)
    para(tf, heading, size=hs, color=C(accent), bold=True, first=True, line_spacing=1.0)
    hh = estimate_lines(heading, hs, tw) * hs * 1.24 / 72.0
    bs = autosize(body, tw, max(avail_h - hh - 0.03, 0.22), bsize, 8.6)
    tf2 = textbox(slide, tx, y + 0.16 + hh, tw, avail_h - hh)
    para(tf2, body, size=bs, color=CHAR, first=True, line_spacing=1.06)
