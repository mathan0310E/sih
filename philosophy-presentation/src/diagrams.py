"""Diagram / infographic generator for the philosophy research deck.

Geometry is expressed in inches and converted at 200 px per inch, so a
diagram rendered for a 5.30 in slot is 1060 px wide and any text set at
N pt appears at N pt once the image is placed at that size on the slide.
"""
import os

from svglib import (NAVY, NAVY_D, NAVY_L, CHAR, ORANGE, AMBER, OFF, PANEL, BORDER,
                    GREY, GREY_L, TEAL, PURPLE, GREEN, CRIMSON, TINT,
                    rect, circle, line, path, txt, text_block, bullets, arrow_defs,
                    arrow, icon, render, card, wrap, tw, fit)

PPI = 200
OUT = "/workspace/project/assets/diagrams"


def pt(p):
    """Points -> px (1 pt = 1/72 in)."""
    return p * PPI / 72.0


def inch(v):
    """Inches -> px."""
    return v * PPI


M = inch(0.20)
GAP = inch(0.10)
BAND = inch(0.075)

RIGHT_W, RIGHT_H = inch(5.30), inch(4.85)
FULL_W, FULL_H = inch(12.09), inch(3.35)
STRIP_W, STRIP_H = inch(12.09), inch(1.55)
MID_W, MID_H = inch(12.09), inch(3.20)
LOW_W, LOW_H = inch(12.09), inch(3.05)


def head(w, h, title, sub=None, bg=OFF, accent=ORANGE):
    """Standard diagram header: full-bleed accent bar, title, subtitle."""
    o = [rect(0, 0, w, h, bg), rect(0, 0, w, BAND, accent)]
    o.append(txt(M, BAND + pt(15.5), title, pt(14.0), NAVY, True))
    if sub:
        o.append(txt(M, BAND + pt(28.0), sub, pt(9.8), GREY))
    return "".join(o)


HEAD_H = BAND + pt(36.0)


def footer(w, h, note):
    return txt(w - M, h - inch(0.085), note, pt(7.6), GREY_L, False, "end")


def rows_area(h, n, top, bottom_reserve):
    avail = h - top - bottom_reserve
    return (avail - (n - 1) * GAP) / n


# ---------------------------------------------------------------- S2 roadmap
def d_roadmap():
    w, h = RIGHT_W, RIGHT_H
    o = [head(w, h, "How this presentation is organised",
              "Four linked strands, one continuous argument")]
    top = HEAD_H + inch(0.08)
    items = [
        ("bulb", "Foundations", "What philosophy is, and the five classical branches.", NAVY),
        ("cap", "Education", "Philosophy of education, its role, and five major traditions.", ORANGE),
        ("people", "Society", "Justice, equality, freedom and shared responsibility.", TEAL),
        ("shield", "Research ethics", "How philosophy shapes method, publication and integrity.", PURPLE),
    ]
    ch = rows_area(h, 4, top, inch(0.42))
    for i, (ic, t, s, col) in enumerate(items):
        cy = top + i * (ch + GAP)
        o.append(card(M, cy, w - 2 * M, ch, t, s, accent=col, ic=ic, iccolor=col,
                      tsize=pt(11.6), ssize=pt(9.0), pad=inch(0.11), rx=inch(0.07),
                      icsize=inch(0.20)))
    o.append(footer(w, h, "Scope: conceptual synthesis; no primary data collected."))
    return render("s02_roadmap", w, h, "".join(o), OUT, bg=OFF)


# ------------------------------------------------------- S3 historical chain
def d_chain():
    w, h = STRIP_W, STRIP_H
    o = [head(w, h, "The philosophical impulse across time",
              "A continuous practice: wonder, questioning, reasoning, wisdom")]
    y = HEAD_H + inch(0.06)
    nodes = [("quest", "Wonder", "Perplexity at the world", NAVY),
             ("bulb", "Questioning", "Socratic elenchus", ORANGE),
             ("search", "Reasoning", "Argument and evidence", TEAL),
             ("compass", "Wisdom", "Judgement in practice", PURPLE)]
    n = len(nodes)
    arw = inch(0.22)
    bw = (w - 2 * M - (n - 1) * arw - (n - 1) * GAP) / n
    bh = h - y - inch(0.14)
    x = M
    for i, (ic, t, s, col) in enumerate(nodes):
        o.append(rect(x, y, bw, bh, PANEL, BORDER, rx=inch(0.07)))
        o.append(rect(x, y, bw, inch(0.045), col))
        o.append(icon(ic, x + bw / 2, y + inch(0.24), inch(0.22), col))
        o.append(txt(x + bw / 2, y + inch(0.50), t, pt(12.0), NAVY, True, "middle"))
        tb, th = text_block(x + inch(0.06), y + inch(0.56), bw - inch(0.12), s,
                            pt(8.8), GREY, False, "middle")
        fit(f"chain[{t}]", s, bw - inch(0.12), pt(8.8), bh - inch(0.60))
        o.append(tb)
        if i < n - 1:
            ax = x + bw + inch(0.02)
            o.append(arrow(ax, y + bh / 2, ax + arw - inch(0.04), y + bh / 2, GREY_L, pt(1.6)))
        x += bw + arw + GAP
    return render("s03_chain", w, h, "".join(o), OUT, bg=OFF)


# ------------------------------------------------------- S4 what philosophy is
def d_definition():
    w, h = RIGHT_W, RIGHT_H
    o = [head(w, h, "Philosophy: etymology and core activity",
              "Greek philos (love) + sophia (wisdom)")]
    y = HEAD_H + inch(0.06)
    bh = inch(0.60)
    o.append(rect(M, y, w - 2 * M, bh, TINT, BORDER, rx=inch(0.07)))
    o.append(txt(M + inch(0.14), y + inch(0.26), "philo-", pt(15.0), NAVY, True))
    o.append(txt(M + inch(0.14), y + inch(0.46), "love, attraction", pt(8.6), GREY))
    o.append(txt(w / 2, y + inch(0.28), "+", pt(15.0), ORANGE, True, "middle"))
    o.append(txt(w - M - inch(0.14), y + inch(0.26), "sophia", pt(15.0), NAVY, True, "end"))
    o.append(txt(w - M - inch(0.14), y + inch(0.46), "wisdom, insight", pt(8.6), GREY, False, "end"))
    y += bh + inch(0.14)
    o.append(txt(M, y + pt(9), "Three foundations", pt(10.8), ORANGE, True))
    y += pt(16)
    rows = [("quest", "Wonder", "Philosophy begins in perplexity \u2014 in noticing "
                                "that things could be otherwise.", NAVY),
            ("search", "Rational inquiry", "Claims are examined through argument and "
                                           "counter-argument, not authority alone.", ORANGE),
            ("grid", "Systematic reflection", "Ideas are organised into coherent positions "
                                              "about reality, knowledge and value.", TEAL)]
    ch = rows_area(h, 3, y, inch(0.42))
    for i, (ic, t, s, col) in enumerate(rows):
        cy = y + i * (ch + GAP)
        o.append(card(M, cy, w - 2 * M, ch, t, s, accent=col, ic=ic, iccolor=col,
                      tsize=pt(11.4), ssize=pt(9.2), pad=inch(0.10), rx=inch(0.07),
                      icsize=inch(0.19)))
    o.append(footer(w, h, "Definition synthesised from standard reference works (SEP)."))
    return render("s04_definition", w, h, "".join(o), OUT, bg=OFF)


# ------------------------------------------------------- S5 five branches
def d_branches():
    w, h = FULL_W, FULL_H
    o = [head(w, h, "The five classical branches of philosophy",
              "Each branch asks a distinctive question and supplies a distinctive test of adequacy")]
    y = HEAD_H + inch(0.05)
    data = [("bulb", "Metaphysics", "What is real?", NAVY,
             ["Reality, existence, being", "Mind, causation, time", "Underpins ontology"]),
            ("search", "Epistemology", "What can we know?", ORANGE,
             ["Knowledge, belief, truth", "Justification and evidence", "Guides method"]),
            ("scales", "Ethics", "What ought we to do?", TEAL,
             ["Right action, virtue, duty", "Consequences and character", "Guides conduct"]),
            ("gear", "Logic", "What follows?", PURPLE,
             ["Validity and inference", "Argument structure", "Guards reasoning"]),
            ("art", "Aesthetics", "What is beauty?", CRIMSON,
             ["Art, taste, judgement", "Expression and form", "Guides criticism"])]
    cw = (w - 2 * M - 4 * GAP) / 5.0
    ch = h - y - inch(0.32)
    for i, (ic, name, q, col, bl) in enumerate(data):
        x = M + i * (cw + GAP)
        o.append(rect(x, y, cw, ch, PANEL, BORDER, rx=inch(0.07)))
        o.append(rect(x, y, cw, inch(0.055), col))
        o.append(icon(ic, x + cw / 2, y + inch(0.34), inch(0.28), col))
        o.append(txt(x + cw / 2, y + inch(0.62), name, pt(12.4), NAVY, True, "middle"))
        o.append(rect(x + inch(0.16), y + inch(0.71), cw - inch(0.32), inch(0.008), BORDER))
        o.append(txt(x + cw / 2, y + inch(0.87), q, pt(10.2), col, True, "middle"))
        yy = y + inch(1.00)
        for b in bl:
            o.append(circle(x + inch(0.17), yy + pt(2.6), pt(2.6), col))
            tb, th = text_block(x + inch(0.25), yy - pt(1), cw - inch(0.40), b, pt(8.6), CHAR)
            fit(f"branch[{name}]", b, cw - inch(0.40), pt(8.6), inch(0.34))
            o.append(tb)
            yy += th + inch(0.035)
    o.append(footer(w, h, "Branch taxonomy: standard divisions in Western philosophy "
                          "(Stanford Encyclopedia of Philosophy)."))
    return render("s05_branches", w, h, "".join(o), OUT, bg=OFF)


# ------------------------------------------- S6 philosophy and education
def d_edu_bridge():
    w, h = RIGHT_W, RIGHT_H
    o = [head(w, h, "Philosophy and education: a two-way relation",
              "Philosophy clarifies aims; education tests them in practice")]
    y = HEAD_H + inch(0.06)
    arw = inch(0.42)
    bw, bh = (w - 2 * M - arw) / 2.0, inch(0.62)
    o.append(rect(M, y, bw, bh, NAVY, None, rx=inch(0.07)))
    o.append(txt(M + bw / 2, y + inch(0.25), "PHILOSOPHY", pt(11.6), "#FFFFFF", True, "middle"))
    o.append(txt(M + bw / 2, y + inch(0.45), "aims, values, criteria", pt(8.6), "#C9D6E6", False, "middle"))
    o.append(rect(w - M - bw, y, bw, bh, ORANGE, None, rx=inch(0.07)))
    o.append(txt(w - M - bw / 2, y + inch(0.25), "EDUCATION", pt(11.6), "#FFFFFF", True, "middle"))
    o.append(txt(w - M - bw / 2, y + inch(0.45), "practice, experience", pt(8.6), "#FBE3CC", False, "middle"))
    x1, x2 = M + bw + inch(0.06), w - M - bw - inch(0.06)
    o.append(arrow(x1, y + bh * 0.34, x2, y + bh * 0.34, NAVY, pt(2.0)))
    o.append(arrow(x2, y + bh * 0.70, x1, y + bh * 0.70, ORANGE, pt(2.0)))
    o.append(txt(w / 2, y + bh + inch(0.17), "clarifies   \u2192     \u2190   informs",
                 pt(8.4), GREY, False, "middle"))
    y += bh + inch(0.30)
    rows = [("target", "Aims", "What is education for? Growth, autonomy, citizenship.", NAVY),
            ("book", "Curriculum", "Which knowledge is most worth teaching, and why?", ORANGE),
            ("people", "Pedagogy", "How should teaching and learning be conducted?", TEAL),
            ("check", "Assessment", "What counts as genuine educational success?", PURPLE)]
    ch = rows_area(h, 4, y, inch(0.40))
    for i, (ic, t, s, col) in enumerate(rows):
        cy = y + i * (ch + GAP)
        o.append(card(M, cy, w - 2 * M, ch, t, s, accent=col, ic=ic, iccolor=col,
                      tsize=pt(11.0), ssize=pt(9.0), pad=inch(0.10), rx=inch(0.07),
                      icsize=inch(0.18)))
    o.append(footer(w, h, "After Dewey (1916/1944); Peters (1966); Biesta (2010)."))
    return render("s06_edu_bridge", w, h, "".join(o), OUT, bg=OFF)


# ------------------------------------ S7 five educational philosophies
def th_h(s, w, size):
    _, hh = text_block(0, 0, w, s, size, CHAR)
    return hh


def d_edphil_table():
    w, h = FULL_W, inch(5.30)
    o = [head(w, h, "Five major educational philosophies compared",
              "Representative emphasis, view of the learner, and classroom signature")]
    y = HEAD_H + inch(0.05)
    inner = w - 2 * M
    cols = [inch(1.55), inch(2.25), inch(2.45), inch(2.55), inner - inch(8.80)]
    heads = ["Tradition", "Reality & knowledge", "Aims of education",
             "Teacher & learner", "Classroom signature"]
    hh = inch(0.36)
    o.append(rect(M, y, sum(cols), hh, NAVY, None, rx=inch(0.045)))
    cx = M
    for i, hd in enumerate(heads):
        o.append(txt(cx + inch(0.09), y + inch(0.235), hd, pt(9.4), "#FFFFFF", True))
        cx += cols[i]
    y += hh + inch(0.035)
    rows = [("Idealism", NAVY, "Reality is mind-dependent; truth is coherence of ideas.",
             "Self-realisation; moral and spiritual growth.",
             "Teacher as exemplar; dialogue around great texts.",
             "Socratic questioning; character formation."),
            ("Realism", NAVY_L, "Reality exists independently; knowledge mirrors that order.",
             "Understanding the ordered world; intellectual discipline.",
             "Teacher as authority; organised subject matter.",
             "Demonstration, observation, mastery of established facts."),
            ("Pragmatism", ORANGE, "Reality is experience; truth is what works in inquiry.",
             "Growth through experience; solving real problems.",
             "Teacher as guide; learner as active inquirer.",
             "Projects, experiments, learning by doing."),
            ("Naturalism", TEAL, "Nature is the whole of reality; development unfolds naturally.",
             "Harmonious, child-centred unfolding of potential.",
             "Teacher as facilitator; minimal interference.",
             "Outdoor and experiential learning led by interest."),
            ("Existentialism", PURPLE, "Existence precedes essence; meaning is chosen.",
             "Authenticity, freedom and personal responsibility.",
             "Teacher as provocateur; learner as chooser.",
             "Reflection, journals, discussion of dilemmas.")]
    rh = rows_area(h, 5, y, inch(0.32))
    for i, (name, col, a, b, c, d) in enumerate(rows):
        ry = y + i * (rh + GAP)
        o.append(rect(M, ry, inner, rh, TINT if i % 2 == 0 else PANEL, None, rx=inch(0.03)))
        o.append(rect(M, ry, inch(0.045), rh, col))
        o.append(txt(M + inch(0.13), ry + rh / 2 + pt(3.5), name, pt(10.2), col, True))
        cx = M + cols[0]
        for j, t in enumerate([a, b, c, d]):
            cw_ = cols[j] - inch(0.18)
            need = th_h(t, cw_, pt(8.4))
            fit(f"table[{name}.{j}]", t, cw_, pt(8.4), rh - inch(0.03))
            tb, _ = text_block(cx + inch(0.09), ry + rh / 2 - need / 2, cw_, t, pt(8.4), CHAR)
            o.append(tb)
            cx += cols[j]
    o.append(footer(w, h, "Synthesis of standard accounts (Gutek, 2014; Curren, 2007; "
                          "Siegel, 2009). A conceptual comparison, not an empirical study."))
    return render("s07_edphil", w, h, "".join(o), OUT, bg=OFF)


# ------------------------------------------ S8 classroom application cards
def d_classroom_cards():
    w, h = RIGHT_W, RIGHT_H
    o = [head(w, h, "Translating traditions into classroom practice",
              "Same syllabus, different pedagogy")]
    y = HEAD_H + inch(0.06)
    items = [("chat", "Idealism", "Seminar questioning that asks pupils to justify beliefs.", NAVY),
             ("search", "Realism", "Careful observation, worked examples, subject mastery.", NAVY_L),
             ("gear", "Pragmatism", "Projects that solve real problems and test ideas.", ORANGE),
             ("heart", "Naturalism", "Interest-led discovery and outdoor, experiential work.", TEAL),
             ("quest", "Existentialism", "Reflective journals and open dilemmas of choice.", PURPLE)]
    ch = rows_area(h, 5, y, inch(0.40))
    for i, (ic, t, s, col) in enumerate(items):
        cy = y + i * (ch + GAP)
        o.append(card(M, cy, w - 2 * M, ch, t, s, accent=col, ic=ic, iccolor=col,
                      tsize=pt(11.0), ssize=pt(9.0), pad=inch(0.095), rx=inch(0.07),
                      icsize=inch(0.18)))
    o.append(footer(w, h, "Illustrative practices; no effect sizes are claimed."))
    return render("s08_classroom", w, h, "".join(o), OUT, bg=OFF)


# ---------------------------------------------------- S9 society layers
def d_society():
    w, h = RIGHT_W, RIGHT_H
    o = [head(w, h, "From persons to institutions",
              "Philosophy supplies the normative vocabulary of social life")]
    y = HEAD_H + inch(0.06)
    layers = [("Persons", "Reasoning, choosing, taking responsibility", NAVY, "quest"),
              ("Communities", "Shared norms, trust, dialogue and care", NAVY_L, "people"),
              ("Institutions", "Law, schools, health, media, science", TEAL, "grid"),
              ("State and global order", "Rights, justice, legitimacy, peace", ORANGE, "globe")]
    ch = rows_area(h, 4, y, inch(0.40))
    for i, (t, s, col, ic) in enumerate(layers):
        cy = y + i * (ch + GAP)
        inset = inch(0.11) * i
        bw = w - 2 * M - 2 * inset
        o.append(rect(M + inset, cy, bw, ch, PANEL, BORDER, rx=inch(0.06)))
        o.append(rect(M + inset, cy, inch(0.05), ch, col))
        o.append(icon(ic, M + inset + inch(0.24), cy + ch / 2, inch(0.20), col))
        tx = M + inset + inch(0.40)
        tb, thh = text_block(tx, cy + inch(0.055), bw - inch(0.55), t, pt(11.2), NAVY, True)
        o.append(tb)
        tb2, _ = text_block(tx, cy + inch(0.055) + thh + inch(0.01), bw - inch(0.55), s,
                            pt(8.8), GREY)
        fit(f"society[{t}]", s, bw - inch(0.55), pt(8.8), ch - inch(0.13) - thh)
        o.append(tb2)
    o.append(footer(w, h, "Normative framing after Rawls (1971) and Sen (1999)."))
    return render("s09_society", w, h, "".join(o), OUT, bg=OFF)


# ------------------------- S11 research workflow with philosophical lens
def d_research_flow():
    w, h = MID_W, MID_H
    o = [head(w, h, "Philosophy inside the research process",
              "Every stage rests on assumptions about reality (ontology), knowledge "
              "(epistemology) and value (axiology)")]
    y = HEAD_H + inch(0.05)
    steps = ["Problem", "Question", "Theory & literature", "Design", "Data collection",
             "Analysis", "Interpretation", "Publication"]
    arw = inch(0.13)
    bw = (w - 2 * M - (len(steps) - 1) * (arw + inch(0.05))) / len(steps)
    bh = inch(0.52)
    x = M
    for i, s in enumerate(steps):
        col = NAVY if i < 3 else (ORANGE if i < 6 else TEAL)
        o.append(rect(x, y, bw, bh, PANEL, col, rx=inch(0.05), sw=pt(0.9)))
        o.append(rect(x, y, bw, inch(0.045), col))
        need = th_h(s, bw - inch(0.08), pt(8.6))
        tb, _ = text_block(x + inch(0.04), y + inch(0.045) + (bh - inch(0.045) - need) / 2,
                           bw - inch(0.08), s, pt(8.6), NAVY, True, "middle")
        fit(f"step[{s}]", s, bw - inch(0.08), pt(8.6), bh - inch(0.045))
        o.append(tb)
        if i < len(steps) - 1:
            ax = x + bw + inch(0.015)
            o.append(arrow(ax, y + bh / 2, ax + arw - inch(0.02), y + bh / 2, GREY_L, pt(1.4)))
        x += bw + arw + inch(0.05)
    y += bh + inch(0.14)
    lens = [("Ontology", "What exists to be studied?", NAVY),
            ("Epistemology", "How can it be known?", ORANGE),
            ("Axiology", "Whose values shape the inquiry?", TEAL),
            ("Logic", "Do the inferences hold?", PURPLE),
            ("Ethics", "Whom does the study affect?", CRIMSON)]
    lw = (w - 2 * M - 4 * GAP) / 5.0
    lh = h - y - inch(0.30)
    for i, (t, s, col) in enumerate(lens):
        lx = M + i * (lw + GAP)
        o.append(rect(lx, y, lw, lh, TINT, BORDER, rx=inch(0.055)))
        o.append(txt(lx + inch(0.10), y + inch(0.20), t, pt(10.2), col, True))
        tb, th = text_block(lx + inch(0.10), y + inch(0.27), lw - inch(0.20), s, pt(8.6), CHAR)
        fit(f"lens[{t}]", s, lw - inch(0.20), pt(8.6), lh - inch(0.33))
        o.append(tb)
    o.append(footer(w, h, "Workflow synthesised from standard research-methods texts; "
                          "lens categories from philosophy of social science."))
    return render("s11_research_flow", w, h, "".join(o), OUT, bg=OFF)


# ------------------------------------------- S12 ethics pillars
def d_ethics_pillars():
    w, h = RIGHT_W, RIGHT_H
    o = [head(w, h, "Four pillars of responsible research",
              "Consent, confidentiality, attribution, integrity")]
    y = HEAD_H + inch(0.06)
    items = [("check", "Informed consent", "Participants are told the purpose, risks and "
                                           "their right to withdraw, and agree freely.", NAVY),
             ("shield", "Confidentiality", "Personal data are protected and anonymity "
                                           "preserved where it was promised.", TEAL),
             ("pen", "Attribution", "Others' words, data and images are credited; "
                                    "plagiarism breaches integrity.", ORANGE),
             ("gear", "Integrity", "No fabrication, falsification or selective reporting; "
                                   "methods and limits are declared.", PURPLE)]
    ch = rows_area(h, 4, y, inch(0.40))
    for i, (ic, t, s, col) in enumerate(items):
        cy = y + i * (ch + GAP)
        o.append(card(M, cy, w - 2 * M, ch, t, s, accent=col, ic=ic, iccolor=col,
                      tsize=pt(11.2), ssize=pt(9.0), pad=inch(0.10), rx=inch(0.07),
                      icsize=inch(0.19)))
    o.append(footer(w, h, "After the Belmont Report (1979); WMA Declaration of Helsinki; "
                          "Singapore Statement (2010)."))
    return render("s12_ethics", w, h, "".join(o), OUT, bg=OFF)


# ----------------------------- S13 ethical vs unethical comparison
def d_ethics_compare():
    w, h = MID_W, MID_H
    o = [head(w, h, "Ethical and unethical research practice compared",
              "The same activity can be sound or corrupt depending on how it is conducted")]
    y = HEAD_H + inch(0.05)
    cw = (w - 2 * M - inch(0.22)) / 2.0
    ch = h - y - inch(0.30)
    for j, (lbl, col) in enumerate([("ACCEPTED PRACTICE", GREEN), ("MISCONDUCT", CRIMSON)]):
        xx = M + j * (cw + inch(0.22))
        o.append(rect(xx, y, cw, inch(0.34), col, None, rx=inch(0.045)))
        o.append(txt(xx + cw / 2, y + inch(0.225), lbl, pt(10.6), "#FFFFFF", True, "middle"))
    good = ["Seeking ethics approval before data collection",
            "Reporting methods so others can replicate them",
            "Citing sources, data and images accurately",
            "Declaring conflicts of interest and funding",
            "Publishing results whether or not they are favourable"]
    bad = ["Collecting data without informed consent",
           "Fabricating or falsifying data and results",
           "Plagiarism or silent reuse of others' work",
           "Hiding conflicts of interest or funding",
           "Suppressing findings that contradict the hypothesis"]
    yy = y + inch(0.44)
    rh = (ch - inch(0.44)) / 5.0
    for i in range(5):
        for j, (col, items, ic) in enumerate([(GREEN, good, "check"), (CRIMSON, bad, "quest")]):
            xx = M + j * (cw + inch(0.22))
            ry = yy + i * rh
            o.append(rect(xx, ry + inch(0.015), cw, rh - inch(0.03), PANEL, BORDER, rx=inch(0.04)))
            o.append(icon(ic, xx + inch(0.16), ry + rh / 2, inch(0.15), col, pt(1.8)))
            tw_ = cw - inch(0.36)
            need = th_h(items[i], tw_, pt(8.6))
            fit(f"ethics[{j}.{i}]", items[i], tw_, pt(8.6), rh - inch(0.05))
            tb, _ = text_block(xx + inch(0.28), ry + rh / 2 - need / 2, tw_, items[i],
                               pt(8.6), CHAR)
            o.append(tb)
    o.append(footer(w, h, "Categories follow standard research-integrity frameworks "
                          "(Shamoo & Resnik, 2015; ALLEA, 2023)."))
    return render("s13_ethics_compare", w, h, "".join(o), OUT, bg=OFF)


# ---------------------------------------------- S15 implications
def d_implications():
    w, h = LOW_W, LOW_H
    o = [head(w, h, "Implications for education and society",
              "What follows if the argument of this presentation is accepted")]
    y = HEAD_H + inch(0.05)
    cols = [("cap", "For curriculum", NAVY,
             ["Protect philosophy, ethics and logic within the curriculum",
              "Teach reasoning explicitly rather than incidentally",
              "Make research ethics part of every project brief"]),
            ("people", "For pedagogy", ORANGE,
             ["Model argument and respectful disagreement in class",
              "Use dilemma discussion to build moral judgement",
              "Reward questioning, not answer-recall"]),
            ("globe", "For society", TEAL,
             ["Judge public claims by evidence rather than volume",
              "Defend equality and freedom as argued principles",
              "Treat research integrity as an institutional duty"])]
    cw = (w - 2 * M - 2 * inch(0.16)) / 3.0
    ch = h - y - inch(0.30)
    for i, (ic, t, col, bl) in enumerate(cols):
        x = M + i * (cw + inch(0.16))
        o.append(rect(x, y, cw, ch, PANEL, BORDER, rx=inch(0.06)))
        o.append(rect(x, y, cw, inch(0.055), col))
        o.append(icon(ic, x + inch(0.26), y + inch(0.30), inch(0.22), col))
        o.append(txt(x + inch(0.44), y + inch(0.36), t, pt(11.6), NAVY, True))
        yy = y + inch(0.52)
        for b in bl:
            o.append(circle(x + inch(0.19), yy + pt(2.6), pt(2.6), col))
            tb, thh = text_block(x + inch(0.27), yy - pt(1), cw - inch(0.44), b, pt(8.6), CHAR)
            fit(f"implication[{t}]", b, cw - inch(0.44), pt(8.6), inch(0.34))
            o.append(tb)
            yy += thh + inch(0.035)
    o.append(footer(w, h, "These are reasoned proposals, not empirical findings."))
    return render("s15_implications", w, h, "".join(o), OUT, bg=OFF)


# ---------------------------------------------- S16 conclusion map
def d_conclusion():
    w, h = FULL_W, inch(3.55)
    o = [head(w, h, "Philosophy as the connective discipline",
              "One practice, three consequences")]
    cy = h / 2 + inch(0.16)
    cx = w / 2 - inch(0.55)
    r = inch(0.72)
    o.append(circle(cx, cy, r + inch(0.08), TINT))
    o.append(circle(cx, cy, r, NAVY))
    tb, _ = text_block(cx - r + inch(0.10), cy - inch(0.22), 2 * r - inch(0.20), "PHILOSOPHY",
                       pt(12.0), "#FFFFFF", True, "middle")
    o.append(tb)
    o.append(txt(cx, cy + inch(0.22), "love of wisdom", pt(8.6), "#C9D6E6", False, "middle"))
    nodes = [("cap", "Education", "Aims, curriculum and pedagogy become deliberate "
                                  "rather than accidental.", NAVY),
             ("people", "Individuals", "Reasoning, autonomy and responsibility become "
                                       "practised habits.", ORANGE),
             ("globe", "Society", "Justice, equality and freedom gain public "
                                  "justification.", TEAL)]
    bw, bh = inch(3.00), inch(0.80)
    x = M
    for i, (ic, t, s, col) in enumerate(nodes):
        y = cy - inch(1.20) + i * (bh + inch(0.18))
        o.append(rect(x, y, bw, bh, PANEL, BORDER, rx=inch(0.06)))
        o.append(rect(x, y, inch(0.05), bh, col))
        o.append(icon(ic, x + inch(0.26), y + bh / 2, inch(0.22), col))
        tb, thh = text_block(x + inch(0.44), y + inch(0.09), bw - inch(0.58), t, pt(11.4), col, True)
        o.append(tb)
        tb2, _ = text_block(x + inch(0.44), y + inch(0.09) + thh, bw - inch(0.58), s, pt(8.6), CHAR)
        fit(f"concl[{t}]", s, bw - inch(0.58), pt(8.6), bh - inch(0.16) - thh)
        o.append(tb2)
        o.append(arrow(x + bw, y + bh / 2, cx - r - inch(0.07), cy + (i - 1) * inch(0.07),
                       GREY_L, pt(1.6)))
    ox = w - M - inch(3.55)
    o.append(rect(ox, cy - inch(1.20), inch(3.55), inch(2.40), TINT, BORDER, rx=inch(0.06)))
    o.append(txt(ox + inch(0.14), cy - inch(1.00), "Key takeaways", pt(11.4), NAVY, True))
    pts = ["Philosophy is a practice of justified questioning, not a set of opinions.",
           "Its branches structure how we ask about reality, knowledge, conduct, reasoning and art.",
           "Education is where these questions become public and consequential.",
           "Research ethics is applied philosophy: consent, confidentiality, attribution, integrity.",
           "A philosophically literate society argues better and trusts more carefully."]
    yy = cy - inch(0.80)
    for p in pts:
        o.append(circle(ox + inch(0.21), yy + pt(2.6), pt(2.6), ORANGE))
        tb, thh = text_block(ox + inch(0.29), yy - pt(1), inch(3.55) - inch(0.45), p, pt(8.6), CHAR)
        fit("takeaway", p, inch(3.55) - inch(0.45), pt(8.6), inch(0.40))
        o.append(tb)
        yy += thh + inch(0.03)
    o.append(arrow(cx + r + inch(0.07), cy, ox - inch(0.04), cy, GREY_L, pt(1.6)))
    return render("s16_conclusion", w, h, "".join(o), OUT, bg=OFF)


ALL = [d_roadmap, d_chain, d_definition, d_branches, d_edu_bridge, d_edphil_table,
       d_classroom_cards, d_society, d_research_flow, d_ethics_pillars,
       d_ethics_compare, d_implications, d_conclusion]

if __name__ == "__main__":
    for fn in ALL:
        print("built", os.path.basename(fn()))
