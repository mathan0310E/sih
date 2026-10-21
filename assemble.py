#!/usr/bin/env python3
"""Assemble the Naan Mudhalvan Generative AI laboratory record manual.

Run:  python3 assemble.py
Output: output/NM_LAB_MANUAL_GenAI.docx
"""
import os
import content as C
import programme as PROG
from build_manual import (new_doc, page_break, set_border, footer_page_number,
                          P, rich, bullets, numbered, section_head, code_block,
                          data_table, screenshot_area, real_figure,
                          borderless_table, _style, no_space, SERIF, MONO)
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm

CENTER = WD_ALIGN_PARAGRAPH.CENTER
JUST = WD_ALIGN_PARAGRAPH.JUSTIFY

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT, exist_ok=True)
DOCX = os.path.join(OUT, "NM_LAB_MANUAL_GenAI.docx")
SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots")


def dotted_line(doc, label, width=52, size=12, before=4, after=4):
    p = P(doc, "", before=before, after=after)
    _style(p.add_run(label + " "), size)
    _style(p.add_run("." * width), size)
    return p


def blank_field(doc, label, size=12, before=4, after=4, tail=""):
    p = P(doc, "", before=before, after=after)
    _style(p.add_run(label + " "), size)
    _style(p.add_run("_" * 38 + tail), size)
    return p


# ------------------------------------------------------------------ cover
def dot_fill(doc, label, size=12, before=5, after=5, used=0):
    """A 'Name : ......' line with dot leaders, as in the reference cover."""
    p = P(doc, "", before=before, after=after)
    _style(p.add_run(label), size, bold=True)
    n = max(30, 92 - used - len(label))
    _style(p.add_run("." * n), size)
    return p


def cover(doc):
    P(doc, "", after=2)
    P(doc, C.COLLEGE["name"], 24, bold=True, align=CENTER, after=2)
    P(doc, C.COLLEGE["address"], 13, align=CENTER, after=18)
    P(doc, "DEPARTMENT OF", 14, bold=True, align=CENTER, after=2)
    P(doc, "ARTIFICIAL INTELLIGENCE AND DATA SCIENCE", 14, bold=True,
      align=CENTER, after=18)
    P(doc, "B.Tech. \u2013 ARTIFICIAL INTELLIGENCE AND DATA SCIENCE", 13,
      align=CENTER, after=16)
    P(doc, C.COLLEGE["course"], 14, bold=True, align=CENTER, after=10)
    P(doc, "REGULATION - ____________", 12, align=CENTER, after=16)
    P(doc, "LABORATORY RECORD", 12, bold=True, align=CENTER, after=20)

    dot_fill(doc, "Name : ", used=7)
    dot_fill(doc, "Register Number : ", used=18)
    dot_fill(doc, "Department : ", used=13)
    dot_fill(doc, "Year / Semester : ", used=18)
    dot_fill(doc, "Subject : ", used=10)
    P(doc, "", after=14)
    P(doc, "Academic Year : 20______ \u2013 20______", 12, align=CENTER, after=4)


# ------------------------------------------------------------ certificate
def certificate(doc):
    P(doc, C.COLLEGE["name"], 20, bold=True, align=CENTER, after=2)
    P(doc, C.COLLEGE["address"], 12, align=CENTER, after=4)
    P(doc, "CERTIFICATE", 18, bold=True, align=CENTER, after=16)

    dot_fill(doc, "Name : ", used=7)
    dot_fill(doc, "Department : ", used=13)
    dot_fill(doc, "Subject : ", used=10)
    dot_fill(doc, "Year / Semester : ", used=18)
    dot_fill(doc, "Register No : ", used=14)
    P(doc, "", after=12)

    rich(doc, [
        ("Certified that this is the bonafide record of practical work done by the "
         "aforesaid student", False, False),
    ], 12, align=JUST, after=10)
    rich(doc, [
        ("In the ", False, False),
        ("Generative AI", True, False),
        (" Laboratory during the year 20______ \u2013 20______.", False, False),
    ], 12, align=JUST, after=26)

    t = doc.add_table(rows=1, cols=2)
    t.autofit = True
    for i, label in enumerate(["Staff-In-Charge", "Head of the Department"]):
        cell = t.cell(0, i)
        cell.text = ""
        q = cell.paragraphs[0]
        q.alignment = CENTER
        no_space(q, 16, 2)
        _style(q.add_run(label), 11, bold=True)

    P(doc, "", after=24)
    P(doc, "Submission for the Practical Examination held on "
           ".......................................................",
      12, after=30)

    t2 = doc.add_table(rows=1, cols=2)
    t2.autofit = True
    for i, label in enumerate(["Internal Examiner", "External Examiner"]):
        cell = t2.cell(0, i)
        cell.text = ""
        q = cell.paragraphs[0]
        q.alignment = CENTER
        no_space(q, 16, 2)
        _style(q.add_run(label), 11, bold=True)


# ------------------------------------------------------------------ index
def index_page(doc):
    P(doc, "INDEX", 16, bold=True, align=CENTER, after=10)
    header = ["Exp. No.", "Date of Experiment", "Name of the Experiment",
              "Marks Awarded", "Staff Signature"]
    rows = []
    for e in C.EXPERIMENTS:
        rows.append([e["no"], "", e["title"], "", ""])
    data_table(doc, header, rows, widths=[1.6, 2.8, 7.4, 2.2, 2.2], size=9.5)
    P(doc, "", after=6)
    P(doc, "Signature of the Staff-in-Charge: ______________________     "
           "Signature of the Head of the Department: ______________________",
      10, after=4)


# ------------------------------------------------------- programme pages
def programme_pages(doc):
    """Naan Mudhalvan / Skill Wallet onboarding, before the experiments."""
    page_break(doc)
    P(doc, "NAAN MUDHALVAN PROGRAMME \u2014 STUDENT ONBOARDING AND LEARNING "
           "JOURNEY", 15, bold=True, align=CENTER, after=8)
    P(doc, "This section records the mandatory onboarding tasks and the learning "
           "journey published on the Skill Wallet program page for the Google "
           "Cloud Generative AI (Engineering) program. Every link in this section "
           "was verified and every screenshot was captured from the live page. "
           "Complete the tasks in the order given before starting the "
           "experiments.", 11.5, align=JUST, after=10)

    for t in PROG.TASKS:
        p = P(doc, "", before=8, after=3)
        _style(p.add_run(f"Task {t['no']}: {t['title']}"), 12.5, bold=True)
        p = P(doc, "", before=0, after=4)
        _style(p.add_run("Provider: "), 11, bold=True)
        _style(p.add_run(t["provider"]), 11)

        section_head(doc, "STEPS", 12)
        numbered(doc, t["steps"], 11.5)

        section_head(doc, "LINKS", 12)
        rows = [[name, url] for name, url in t["links"]]
        data_table(doc, ["Resource", "URL"], rows,
                   widths=[5.0, 11.2], size=9.5)

        shot = os.path.join(SHOTS, t["shot"])
        if os.path.exists(shot):
            real_figure(doc, shot, t["caption"], width_cm=14.5)
        if t.get("shot2"):
            shot2 = os.path.join(SHOTS, t["shot2"])
            if os.path.exists(shot2):
                real_figure(doc, shot2,
                            "Fig. P.1b: Digital Application Fundamentals (STEM) "
                            "journey page.", width_cm=14.5)

    page_break(doc)
    P(doc, "LEARNING JOURNEY, CAPSTONE PROJECT AND ASSESSMENT", 14, bold=True,
      align=CENTER, after=8)
    for heading, body in PROG.JOURNEY:
        section_head(doc, heading.upper(), 12)
        P(doc, body, 11.5, align=JUST, after=6)

    section_head(doc, "VERIFICATION NOTES", 12)
    numbered(doc, PROG.VERIFICATION_NOTES, 11)


# ------------------------------------------------------------- experiment
def detailed_procedure(doc, steps):
    """Render the exhaustive step-by-step guide for one experiment."""
    section_head(doc, "DETAILED STEP-BY-STEP PROCEDURE", 13)
    P(doc, "Follow the steps in the order given. Each step states the action to "
           "perform, the exact command or click, what you should observe, and "
           "what to do if the step fails.",
      11, italic=True, align=JUST, after=6)
    for i, s in enumerate(steps, 1):
        p = P(doc, "", before=8, after=2)
        _style(p.add_run(f"Step {i}: {s['title']}"), 11.5, bold=True)
        rich(doc, [("Action: ", True, False), (s["action"], False, False)],
             11.5, align=JUST, after=3)
        if s.get("command"):
            code_block(doc, s["command"])
        if s.get("observe"):
            rich(doc, [("What you should see: ", True, False),
                       (s["observe"], False, False)],
                 11.5, align=JUST, after=3)
        if s.get("note"):
            rich(doc, [("Note: ", True, False), (s["note"], False, False)],
                 11, align=JUST, after=3)


def experiment(doc, e):
    """Render one experiment, starting on a fresh page."""
    page_break(doc)
    # compact heading area
    p = P(doc, "", before=0, after=2)
    _style(p.add_run(f"Exp. no: {e['no']} \u2014 {e['title']}"), 13, bold=True)
    p = P(doc, "", before=0, after=10)
    _style(p.add_run("Date: ______________________"), 12)

    section_head(doc, "AIM", 13)
    P(doc, e["aim"], 12, align=JUST, after=6)

    section_head(doc, "REQUIREMENTS / TOOLS REQUIRED", 13)
    bullets(doc, e["requirements"], 12)

    section_head(doc, "THEORY", 13)
    for t in e["theory"]:
        P(doc, t, 12, align=JUST, after=6)

    section_head(doc, "PROCEDURE", 13)
    numbered(doc, e["procedure"], 12)

    if e.get("detailed"):
        detailed_procedure(doc, e["detailed"])

    if e.get("prompts"):
        section_head(doc, "PROMPTS USED", 13)
        for pr in e["prompts"]:
            P(doc, pr, 11.5, align=JUST, after=5)

    if e.get("code"):
        section_head(doc, "PROGRAM / COMMANDS / PROMPT", 13)
        P(doc, e["code"]["caption"], 11, italic=True, after=4)
        code_block(doc, e["code"]["lines"])
        if e["code"].get("run"):
            P(doc, "How to execute the program:", 12, bold=True, before=6, after=3)
            numbered(doc, e["code"]["run"], 12)

    section_head(doc, "EXPECTED OUTPUT", 13)
    for o in e["output"]:
        P(doc, o, 12, align=JUST, after=4)

    if e.get("figure"):
        screenshot_area(doc, e["figure"])

    section_head(doc, "OBSERVATION AND ANALYSIS", 13)
    obs = e["observation"]
    for t in obs.get("paras", []):
        P(doc, t, 12, align=JUST, after=4)
    if obs.get("table"):
        tb = obs["table"]
        data_table(doc, tb["header"], tb["rows"], widths=tb.get("widths"), size=10)

    if e.get("troubleshooting"):
        section_head(doc, "TROUBLESHOOTING", 13)
        bullets(doc, e["troubleshooting"], 12)

    if e.get("safety"):
        section_head(doc, "RESPONSIBLE AI, PRIVACY AND SAFETY PRECAUTIONS", 13)
        bullets(doc, e["safety"], 12)

    section_head(doc, "RESULT", 13)
    P(doc, e["result"], 12, align=JUST, after=6)

    section_head(doc, "CONCLUSION", 13)
    P(doc, e["conclusion"], 12, align=JUST, after=6)

    section_head(doc, "VIVA-VOCE QUESTIONS", 13)
    numbered(doc, e["viva"], 12)


# ------------------------------------------------------------- appendices
def appendices(doc):
    page_break(doc)
    P(doc, "CONCLUSION", 16, bold=True, align=CENTER, after=10)
    for t in C.CONCLUSION_PAGE:
        P(doc, t, 12, align=JUST, after=8)

    page_break(doc)
    P(doc, "APPENDIX A \u2014 REFERENCES AND OFFICIAL DOCUMENTATION", 14, bold=True,
      align=CENTER, after=10)
    numbered(doc, C.REFERENCES, 11)

    page_break(doc)
    P(doc, "APPENDIX B \u2014 SOFTWARE REQUIREMENTS", 14, bold=True, align=CENTER,
      after=10)
    sr = C.SOFTWARE_REQUIREMENTS
    data_table(doc, sr["header"], sr["rows"], widths=sr["widths"], size=10)
    P(doc, "", after=8)
    P(doc, "A single environment can be created once with the following commands:",
      11, italic=True, after=4)
    code_block(doc, [
        "python3 -m venv .venv",
        "source .venv/bin/activate        # Windows: .venv\\Scripts\\activate",
        "pip install torch torchvision transformers datasets peft \\",
        "            sentence-transformers scikit-learn numpy pandas \\",
        "            matplotlib pytest pillow google-genai",
    ])

    page_break(doc)
    P(doc, "APPENDIX C \u2014 SCREENSHOT CHECKLIST", 14, bold=True, align=CENTER,
      after=6)
    P(doc, "Paste an authentic screenshot for each item below in the corresponding "
           "experiment. Do not reuse a screenshot from a different experiment.",
      11, italic=True, align=JUST, after=8)
    header = ["No.", "Screenshot to be pasted", "Pasted (Yes / No)"]
    rows = [[str(i + 1), s, ""] for i, s in enumerate(C.SCREENSHOT_CHECKLIST)]
    data_table(doc, header, rows, widths=[1.4, 11.8, 3.0], size=10)

    page_break(doc)
    P(doc, "APPENDIX D \u2014 STUDENT SUBMISSION CHECKLIST", 14, bold=True,
      align=CENTER, after=6)
    header = ["No.", "Item", "Completed (Yes / No)"]
    rows = [[str(i + 1), s, ""] for i, s in enumerate(C.SUBMISSION_CHECKLIST)]
    data_table(doc, header, rows, widths=[1.4, 11.8, 3.0], size=10)
    P(doc, "", after=12)
    P(doc, "Declaration: I declare that the practical work recorded in this manual "
           "was carried out by me, that the outputs shown are my own, and that any "
           "assistance taken from tools or references has been acknowledged.",
      11, align=JUST, after=20)
    p = P(doc, "", after=4)
    _style(p.add_run("Signature of the Student: ______________________"), 11)
    P(doc, "Date: ______________________", 11, after=4)

    page_break(doc)
    P(doc, "APPENDIX E \u2014 PROGRAMME LINK INDEX", 14, bold=True, align=CENTER,
      after=6)
    P(doc, "Every link below was opened and returned HTTP 200 when this manual "
           "was prepared. Path titles and activity counts are as published on "
           "the public path pages.", 11, italic=True, align=JUST, after=8)
    data_table(doc, PROG.LINK_INDEX[0], PROG.LINK_INDEX[1:],
               widths=[3.2, 5.6, 7.4], size=8.5)


def main():
    doc = new_doc()
    set_border(doc.sections[0])
    footer_page_number(doc.sections[0])

    cover(doc)
    page_break(doc)
    certificate(doc)
    page_break(doc)
    index_page(doc)
    programme_pages(doc)
    for e in C.EXPERIMENTS:
        experiment(doc, e)
    appendices(doc)

    doc.save(DOCX)
    print("wrote", DOCX)
    print("sections (pages):", len(doc.sections))
    print("paragraphs:", len(doc.paragraphs))
    print("tables:", len(doc.tables))


if __name__ == "__main__":
    main()
