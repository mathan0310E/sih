"""Minimal SVG builder + text metrics for academic infographics.

Rendered with cairosvg at 2x so diagrams stay crisp on a projector.
Text is wrapped using real DejaVu metrics, which are the same metrics
cairosvg uses via fontconfig, so measured widths match rendered widths.
"""
import html
import os
from PIL import ImageFont

FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FAMILY = "DejaVu Sans, Verdana, sans-serif"

# ---- palette -------------------------------------------------------------
NAVY = "#0F2D52"
NAVY_D = "#0A1E38"
NAVY_L = "#1C4B7D"
CHAR = "#333A42"
ORANGE = "#C25E1A"
AMBER = "#E8A33D"
OFF = "#FAF9F6"
PANEL = "#FFFFFF"
BORDER = "#D5DAE1"
GREY = "#5F6B7A"
GREY_L = "#8A94A2"
TEAL = "#166B67"
PURPLE = "#5B4B8A"
GREEN = "#2E6B4F"
CRIMSON = "#9E2B2B"
TINT = "#EEF3F9"

_fc = {}


def font(size, bold=False):
    key = (int(size), bool(bold))
    if key not in _fc:
        _fc[key] = ImageFont.truetype(FONT_B if bold else FONT_R, int(size))
    return _fc[key]


def tw(s, size, bold=False):
    return font(size, bold).getlength(s)


def wrap(s, size, maxw, bold=False):
    lines, cur = [], ""
    for w in str(s).split():
        t = (cur + " " + w).strip()
        if tw(t, size, bold) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(s):
    return html.escape(str(s), quote=True)


# ---- primitives ----------------------------------------------------------
def rect(x, y, w, h, fill="none", stroke=None, rx=0, sw=1.4, op=None):
    a = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" fill="{fill}"'
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{sw}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + "/>"


def circle(cx, cy, r, fill="none", stroke=None, sw=1.4, op=None):
    a = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"'
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{sw}"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + "/>"


def line(x1, y1, x2, y2, stroke=NAVY, sw=1.4, dash=None, cap="round"):
    a = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
         f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"')
    if dash:
        a += f' stroke-dasharray="{dash}"'
    return a + "/>"


def path(d, fill="none", stroke=None, sw=1.4, op=None):
    a = f'<path d="{d}" fill="{fill}"'
    if stroke:
        a += f' stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    if op is not None:
        a += f' opacity="{op}"'
    return a + "/>"


def txt(x, y, s, size, fill=CHAR, bold=False, anchor="start", italic=False, ls=0):
    st = f' font-style="italic"' if italic else ""
    lsp = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAMILY}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}"{st}{lsp}'
            f'{" font-weight=\"bold\"" if bold else ""}>{esc(s)}</text>')


def text_block(x, y, w, s, size, fill=CHAR, bold=False, anchor="start", lh=1.34,
               align_center_x=None, italic=False):
    """Wrapped text. Returns (svg, total_height). anchor 'middle' centers each line."""
    lines = wrap(s, size, w, bold)
    out, cy = [], y
    ax = x + w / 2 if anchor == "middle" else x
    for ln in lines:
        out.append(txt(ax, cy + size * 0.78, ln, size, fill, bold, "middle" if anchor == "middle" else "start", italic))
        cy += size * lh
    return "".join(out), cy - y


def bullets(x, y, w, items, size, fill=CHAR, gap=10, dot=ORANGE, lh=1.3, bold_lead=True):
    """Bulleted list; text before ':' is emphasised. Returns (svg, height)."""
    out, cy = [], y
    for it in items:
        lead, rest = (it.split(":", 1) + [""])[:2] if ":" in it else (None, it)
        cx = x + size * 0.85
        out.append(circle(x + size * 0.32, cy + size * 0.42, size * 0.19, dot))
        if lead and bold_lead:
            s1, h1 = text_block(cx, cy, w - size * 0.9, lead + ":", size, NAVY, True, lh=lh)
            out.append(s1)
            s2, h2 = text_block(cx, cy + h1, w - size * 0.9, rest.strip(), size, fill, False, lh=lh)
            out.append(s2)
            cy += h1 + h2 + gap
        else:
            s1, h1 = text_block(cx, cy, w - size * 0.9, it, size, fill, False, lh=lh)
            out.append(s1)
            cy += h1 + gap
    return "".join(out), cy - y


def arrow_defs(colors=(NAVY, GREY_L, ORANGE, TEAL, PURPLE, CRIMSON)):
    d = ['<defs>']
    for i, c in enumerate(colors):
        d.append(f'<marker id="ah{i}" viewBox="0 0 10 10" refX="8" refY="5" '
                 f'markerWidth="6" markerHeight="6" markerUnits="strokeWidth" '
                 f'orient="auto">'
                 f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{c}"/></marker>')
    d.append("</defs>")
    return "".join(d)


def arrow(x1, y1, x2, y2, stroke=NAVY, sw=1.8, mi=0, dash=None):
    a = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
         f'stroke-width="{sw}" stroke-linecap="round" marker-end="url(#ah{mi})"')
    if dash:
        a += f' stroke-dasharray="{dash}"'
    return a + "/>"


def icon(name, cx, cy, s, color=NAVY, sw=1.9):
    """Vector icon drawn in a 24x24 unit box, centred on (cx,cy) with side s."""
    k = s / 24.0
    def X(v): return cx + (v - 12) * k
    def Y(v): return cy + (v - 12) * k
    st = dict(stroke=color, sw=sw * k, fill="none")
    g = []
    if name == "target":
        g = [circle(X(12), Y(12), 9 * k, "none", color, sw * k),
             circle(X(12), Y(12), 5 * k, "none", color, sw * k),
             circle(X(12), Y(12), 1.7 * k, color)]
    elif name == "book":
        g = [path(f"M {X(4)} {Y(5.5)} h {9*k} a {2.5*k} {2.5*k} 0 0 1 {2.5*k} {2.5*k} v {11*k} h {-9*k} a {-2.5*k} {-2.5*k} 0 0 1 {-2.5*k} {-2.5*k} z", "none", color, sw * k),
             line(X(6.5), Y(9), X(6.5), Y(17), color, sw * k)]
    elif name == "people":
        g = [circle(X(9), Y(8.5), 3.1 * k, "none", color, sw * k),
             path(f"M {X(3.6)} {Y(19)} a {5.4*k} {5.4*k} 0 0 1 {10.8*k} 0", "none", color, sw * k),
             circle(X(17), Y(9.5), 2.4 * k, "none", color, sw * k),
             path(f"M {X(13.8)} {Y(18.6)} a {4.2*k} {4.2*k} 0 0 1 {6.6*k} {-2.2*k}", "none", color, sw * k)]
    elif name == "compass":
        g = [circle(X(12), Y(12), 9 * k, "none", color, sw * k),
             path(f"M {X(15.4)} {Y(8.6)} l {-2.6*k} {5.4*k} l {-2.6*k} {-2.2*k} z", color)]
    elif name == "bulb":
        g = [circle(X(12), Y(10), 5.2 * k, "none", color, sw * k),
             line(X(9.8), Y(15.4), X(9.8), Y(18), color, sw * k),
             line(X(14.2), Y(15.4), X(14.2), Y(18), color, sw * k),
             line(X(9.8), Y(18), X(14.2), Y(18), color, sw * k),
             line(X(12), Y(2.4), X(12), Y(4), color, sw * k),
             line(X(4.2), Y(10), X(5.8), Y(10), color, sw * k),
             line(X(18.2), Y(10), X(19.8), Y(10), color, sw * k)]
    elif name == "scales":
        g = [line(X(12), Y(4), X(12), Y(19), color, sw * k),
             line(X(5), Y(6.6), X(19), Y(6.6), color, sw * k),
             path(f"M {X(2.8)} {Y(13.4)} a {4.6*k} {4.6*k} 0 0 0 {9.2*k} 0 z", "none", color, sw * k),
             path(f"M {X(12)} {Y(13.4)} a {4.6*k} {4.6*k} 0 0 0 {9.2*k} 0 z", "none", color, sw * k),
             line(X(8.2), Y(19), X(15.8), Y(19), color, sw * k)]
    elif name == "chat":
        g = [path(f"M {X(3.5)} {Y(6)} h {17*k} v {10*k} h {-10*k} l {-4*k} {3.6*k} v {-3.6*k} h {-3*k} z", "none", color, sw * k)]
    elif name == "search":
        g = [circle(X(10.6), Y(10.6), 6.2 * k, "none", color, sw * k),
             line(X(15.2), Y(15.2), X(20), Y(20), color, sw * k)]
    elif name == "shield":
        g = [path(f"M {X(12)} {Y(3.2)} l {7.4*k} {2.8*k} v {6.2*k} a {8.4*k} {8.4*k} 0 0 1 {-7.4*k} {8.6*k} a {8.4*k} {8.4*k} 0 0 1 {-7.4*k} {-8.6*k} v {-6.2*k} z", "none", color, sw * k),
             path(f"M {X(8.8)} {Y(12)} l {2.4*k} {2.4*k} l {4*k} {-4.6*k}", "none", color, sw * k)]
    elif name == "pen":
        g = [path(f"M {X(4)} {Y(20)} l {1.4*k} {-4.6*k} l {11*k} {-11*k} l {3.2*k} {3.2*k} l {-11*k} {11*k} z", "none", color, sw * k),
             line(X(14.6), Y(6.2), X(17.8), Y(9.4), color, sw * k)]
    elif name == "gear":
        g = [circle(X(12), Y(12), 3.4 * k, "none", color, sw * k)]
        import math as _m
        for i in range(8):
            a = _m.radians(i * 45)
            x1, y1 = 12 + 5.4 * _m.cos(a), 12 + 5.4 * _m.sin(a)
            x2, y2 = 12 + 8.4 * _m.cos(a), 12 + 8.4 * _m.sin(a)
            g.append(line(X(x1), Y(y1), X(x2), Y(y2), color, sw * k))
    elif name == "globe":
        g = [circle(X(12), Y(12), 8.6 * k, "none", color, sw * k),
             path(f"M {X(3.4)} {Y(12)} h {17.2*k}", "none", color, sw * k),
             path(f"M {X(12)} {Y(3.4)} a {5.2*k} {8.6*k} 0 0 1 0 {17.2*k} a {5.2*k} {8.6*k} 0 0 1 0 {-17.2*k} z", "none", color, sw * k)]
    elif name == "heart":
        g = [path(f"M {X(12)} {Y(20)} C {X(2.6)} {Y(12.6)} {X(5.4)} {Y(4)} {X(12)} {Y(8.4)} "
                  f"C {X(18.6)} {Y(4)} {X(21.4)} {Y(12.6)} {X(12)} {Y(20)} z", "none", color, sw * k)]
    elif name == "cap":
        g = [path(f"M {X(2.6)} {Y(9.4)} L {X(12)} {Y(5)} L {X(21.4)} {Y(9.4)} L {X(12)} {Y(13.8)} z", "none", color, sw * k),
             path(f"M {X(6.4)} {Y(11.4)} v {4.4} a {5.6*k} {3.4*k} 0 0 0 {11.2*k} 0 v {-4.4}", "none", color, sw * k)]
    elif name == "grid":
        g = [rect(X(3.5), Y(3.5), 7.2 * k, 7.2 * k, "none", color, sw * k),
             rect(X(13.3), Y(3.5), 7.2 * k, 7.2 * k, "none", color, sw * k),
             rect(X(3.5), Y(13.3), 7.2 * k, 7.2 * k, "none", color, sw * k),
             rect(X(13.3), Y(13.3), 7.2 * k, 7.2 * k, "none", color, sw * k)]
    elif name == "chart":
        g = [line(X(3.6), Y(19.6), X(20.4), Y(19.6), color, sw * k),
             line(X(3.6), Y(19.6), X(3.6), Y(4.4), color, sw * k),
             rect(X(6.6), Y(13), 2.8 * k, 6.6 * k, color),
             rect(X(11), Y(9), 2.8 * k, 10.6 * k, color),
             rect(X(15.4), Y(5.6), 2.8 * k, 14 * k, color)]
    elif name == "quest":
        g = [path(f"M {X(8.4)} {Y(8.6)} a {3.7*k} {3.7*k} 0 1 1 {4.4*k} {3.6*k} v {2.6*k}", "none", color, sw * k * 1.15),
             circle(X(12.8), Y(19), 1.5 * k, color)]
    elif name == "check":
        g = [circle(X(12), Y(12), 8.8 * k, "none", color, sw * k),
             path(f"M {X(8)} {Y(12.4)} l {2.8*k} {2.8*k} l {5.4*k} {-6*k}", "none", color, sw * k)]
    elif name == "handshake":
        g = [path(f"M {X(2.8)} {Y(12)} l {4*k} {-4*k} l {4*k} {3.4*k} l {3*k} {-2.6*k} l {3*k} {2.6*k} l {4.4*k} {-3.4*k}", "none", color, sw * k),
             path(f"M {X(6.4)} {Y(12.6)} l {3.4*k} {3.4*k} l {3.4*k} {-3.4*k}", "none", color, sw * k)]
    else:
        g = [circle(X(12), Y(12), 9 * k, "none", color, sw * k)]
    return "".join(g)


def svg(w, h, body, bg=None, scale=2):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">')
    if bg:
        head += rect(0, 0, w, h, bg)
    return head + arrow_defs() + body + "</svg>"


def render(name, w, h, body, outdir, bg=None, scale=2):
    import cairosvg
    os.makedirs(outdir, exist_ok=True)
    s = svg(w, h, body, bg, scale)
    p = os.path.join(outdir, name + ".png")
    cairosvg.svg2png(bytestring=s.encode("utf-8"), write_to=p,
                     output_width=int(w * scale), output_height=int(h * scale))
    return p


# ---- layout QA -----------------------------------------------------------
WARN = []


def fit(label, s, w, size, avail, bold=False, pad=0.0):
    """Record a warning if wrapped text is taller than the space allowed."""
    n = 0
    for ln in wrap(s, size, w, bold):
        n += 1
    need = n * size * 1.34 + pad
    if need > avail + 0.6:
        WARN.append(f"OVERFLOW {label}: needs {need:.1f}px, has {avail:.1f}px "
                    f"({n} lines @ {size:.1f}px in {w:.0f}px)")
    return need


def report():
    if WARN:
        print(f"--- layout warnings: {len(WARN)} ---")
        for x in WARN:
            print("   ", x)
    else:
        print("--- layout OK: no overflow detected ---")
    return WARN


def card(x, y, w, h, title=None, sub=None, fill=PANEL, stroke=BORDER, accent=None,
         tsize=19, ssize=14, pad=16, rx=12, tcolor=NAVY, scolor=GREY, ic=None,
         icsize=26, iccolor=None, icside="left"):
    """Rounded info card with optional left accent bar, icon, title and body."""
    out = [rect(x + 2, y + 3, w, h, "#0F2D52", rx=rx, op=0.06),
           rect(x, y, w, h, fill, stroke, rx=rx, sw=1.2)]
    if accent:
        out.append(path(f"M {x+rx} {y} h {-rx+6} a {rx} {rx} 0 0 0 {-rx} {rx} v {h-2*rx} "
                        f"a {rx} {rx} 0 0 0 {rx} {rx} h {-6+rx} z", accent))
    cy = y + pad
    tx = x + pad
    if ic:
        out.append(icon(ic, x + pad + icsize / 2, cy + icsize / 2, icsize, iccolor or accent or NAVY))
        tx = x + pad + icsize + 12
    tw_ = w - (tx - x) - pad
    th_tot = 0.0
    if title:
        s1, h1 = text_block(tx, cy + 1, tw_, title, tsize, tcolor, True)
        out.append(s1)
        cy += h1 + 3
        th_tot += h1 + 3
    if sub:
        s2, h2 = text_block(tx, cy, tw_, sub, ssize, scolor)
        out.append(s2)
        th_tot += h2
    avail = h - 2 * pad
    if ic and th_tot > avail:
        fit(f"card[{ic}:{(title or sub or '')[:26]}]", sub or "", tw_, ssize, avail)
    elif th_tot > avail:
        fit(f"card[{(title or sub or '')[:30]}]", (title or "") + " " + (sub or ""),
            tw_, ssize, avail)
    return "".join(out)
