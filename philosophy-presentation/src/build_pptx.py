"""Build the 18-slide academic presentation and its speaker notes."""
import os
import sys

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_lib import (C, NAVY, NAVY_D, NAVY_L, CHAR, ORANGE, AMBER, TEAL, PURPLE,
                      GREEN, GREY, GREY_L, BORDER, WHITE, OFF, TINT, FONT, FONT_H,
                      SW, SH, ML, MR, CW, TITLE_Y, RULE_Y, BODY_TOP, BODY_BOT,
                      BODY_H, LCOL_W, RCOL_X, RCOL_W, DIAG, PHOTO, OUTDIR,
                      blank, rect, line_h, textbox, para, pic_cover, pic_fit,
                      icon, notes, photo_credit, slide_frame, statement_card,
                      estimate_lines, autosize, FITLOG)
import refs

PRS = Presentation()
PRS.slide_width = Inches(SW)
PRS.slide_height = Inches(SH)


# ---------------------------------------------------------------- components
def lead_block(slide, x, y, w, text, size=12.2, color=CHAR, h=0.62):
    tf = textbox(slide, x, y, w, h)
    para(tf, text, size=size, color=color, first=True, line_spacing=1.10)
    return estimate_lines(text, size, w) * size * 1.10 / 72.0


def icon_bullets(slide, x, y, w, h, items, size=11.4, gap=0.13, icon_size=0.24):
    """Each statement gets its own icon and explanation."""
    n = len(items)
    row_h = (h - (n - 1) * gap) / n
    for i, (ic, col, lead, rest) in enumerate(items):
        ry = y + i * (row_h + gap)
        col = C(col)
        icon(slide, ic, col, x, ry + 0.015, icon_size)
        tx = x + icon_size + 0.13
        tw = w - icon_size - 0.13
        avail = row_h - 0.02
        ls = autosize(lead, tw, avail, size, 9.6)
        tf = textbox(slide, tx, ry, tw, 0.30)
        para(tf, lead, size=ls, color=col, bold=True, first=True, line_spacing=1.02)
        hh = estimate_lines(lead, ls, tw) * ls * 1.24 / 72.0
        if rest:
            rs = autosize(rest, tw, max(avail - hh - 0.02, 0.20), size - 0.7, 8.8)
            tf2 = textbox(slide, tx, ry + hh + 0.015, tw, max(avail - hh, 0.22))
            para(tf2, rest, size=rs, color=CHAR, first=True, line_spacing=1.06)


def photo_panel(slide, key, x, y, w, h, caption, cap_size=10.4):
    """Licensed photograph with a caption that ties it to the statement."""
    cap_h = 0.52
    pic_cover(slide, os.path.join(PHOTO, key + ".jpg"), x, y, w, h - cap_h - 0.30)
    rect(slide, x, y + h - cap_h - 0.30, w, cap_h, fill=TINT, line=BORDER)
    tf = textbox(slide, x + 0.14, y + h - cap_h - 0.30 + 0.075, w - 0.28, cap_h - 0.14)
    para(tf, caption, size=cap_size, color=CHAR, first=True, line_spacing=1.05)
    photo_credit(slide, key, x, y + h - 0.26, w)


def diagram(slide, name, x, y, w, h):
    pic_fit(slide, os.path.join(DIAG, name + ".png"), x, y, w, h)


def ref_columns(slide, x, y, w, h, items, size=7.8, cols=2, gap=0.30):
    n = len(items)
    per = -(-n // cols)
    colw = (w - (cols - 1) * gap) / cols
    for i, it in enumerate(items):
        c, r = divmod(i, per)
        cx = x + c * (colw + gap)
        cy = y + r * (h / per)
        row_h = h / per
        s = autosize(it, colw - 0.16, row_h, size, 6.6, lh=1.05)
        tf = textbox(slide, cx, cy, colw, row_h)
        para(tf, "\u25aa  ", size=s, color=ORANGE, bold=True, first=True, line_spacing=1.04)
        p = tf.paragraphs[0]
        r2 = p.add_run()
        r2.text = it
        r2.font.size = Pt(s)
        r2.font.color.rgb = CHAR
        r2.font.name = FONT


# ================================================================ SLIDE 1
def s01():
    s = blank(PRS)
    rect(s, 0, 0, SW, SH, fill=WHITE)
    rect(s, 0, 0, SW, 2.62, fill=NAVY)
    rect(s, 0, 2.62, SW, 0.075, fill=ORANGE)
    # decorative arc motif (philosophical contemplation)
    pic_fit(s, os.path.join(PHOTO, "philosophy_thinking.jpg"), 9.05, 0.30, 3.90, 2.05)

    tf = textbox(s, ML, 0.44, 8.1, 0.30)
    para(tf, "RESEARCH SEMINAR  \u2022  PHILOSOPHY OF EDUCATION", size=10.4,
         color=AMBER, bold=True, first=True)
    tf = textbox(s, ML, 0.80, 8.2, 1.30)
    para(tf, "Philosophy and Its Role in\nEducation and Society", size=33.5,
         color=WHITE, bold=True, first=True, line_spacing=0.98, font=FONT_H)

    tf = textbox(s, ML, 3.02, 5.6, 0.90)
    para(tf, "A conceptual study of the foundations, branches and social "
             "functions of philosophy, and of its application to education "
             "and to responsible research practice.",
         size=12.4, color=CHAR, first=True, line_spacing=1.12)

    line_h(s, ML, 3.96, 5.6)
    rows = [("Presented by", "Kaudilyar. R"),
            ("Department", "Department of Computer Science and Engineering"),
            ("Citation style", "APA 7th edition"),
            ("Format", "Conceptual synthesis \u2014 no primary data collected")]
    tf = textbox(s, ML, 4.12, 6.4, 1.5)
    for i, (k, v) in enumerate(rows):
        para(tf, [(k + "   ", False, GREY), (v, True, NAVY)], size=11.6,
             first=(i == 0), space_after=5.5)

    # thesis band
    rect(s, ML, 5.86, CW, 0.92, fill=TINT, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s, ML, 5.96, 0.055, 0.72, fill=ORANGE)
    icon(s, "bulb", "orange", ML + 0.20, 6.14, 0.30)
    tf = textbox(s, ML + 0.66, 5.99, CW - 0.90, 0.72)
    para(tf, "Central claim", size=10.4, color=ORANGE, bold=True, first=True)
    para(tf, "Philosophy is not a museum of opinions but a working discipline: "
             "it supplies the reasoning by which education justifies its aims and "
             "by which research defends its integrity.",
         size=11.2, color=CHAR, space_before=1.5, line_spacing=1.06)

    notes(s, """Opening (about 45 seconds).

Good morning. My name is Kaudilyar R, from the Department of Computer Science and Engineering. My presentation is titled "Philosophy and Its Role in Education and Society".

Let me be clear at the outset about what this presentation is and what it is not. It is a conceptual study. I am synthesising established scholarship on philosophy, on philosophy of education, and on research ethics. I have not collected primary data, I have not run an experiment, and I will not be reporting effect sizes or statistics of my own. Everything factual I claim is drawn from published, verifiable sources, which I list at the end in APA seventh edition style.

The photograph on the right is a marble bust from the National Archaeological Museum of Greece. I include it deliberately, because the visual conventions of philosophy — the bust, the thinker, the text — can make the subject look like a gallery of dead ideas. The central claim in the panel below says the opposite, and it is the thesis the whole presentation defends: philosophy is a working discipline. It supplies the reasoning by which education justifies its aims, and by which research defends its integrity.

Hold that claim in mind, because each section adds one strand to it.

Transition: Let me first tell you how the argument is organised.""")
    return s


# ================================================================ SLIDE 2
def s02():
    s = blank(PRS)
    slide_frame(s, "Overview", "Abstract and structure of the argument", 2)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "This presentation argues that philosophy performs three connected "
               "functions: it clarifies what we can know, it guides what we should do, "
               "and it disciplines how we inquire. Education and research are the two "
               "domains where those functions have the most visible consequences.",
               size=12.4)
    icon_bullets(s, ML, BODY_TOP + 0.92, LCOL_W, BODY_H - 1.30, [
        ("bulb", "orange", "Foundations and branches",
         "Definition of philosophy; metaphysics, epistemology, ethics, logic and aesthetics."),
        ("cap", "orange", "Education",
         "The philosophy\u2013education relation, its role in schooling, and five major traditions."),
        ("people", "teal", "Society",
         "Justice, equality, freedom and responsibility as publicly argued principles."),
        ("shield", "purple", "Research and ethics",
         "Method, publication and integrity; consent, confidentiality, attribution."),
    ], size=11.6)
    diagram(s, "s02_roadmap", RCOL_X, BODY_TOP - 0.04, RCOL_W, 5.55)
    notes(s, """Overview (about 50 seconds).

This slide is the map. The paragraph on the left states the abstract: philosophy performs three connected functions — it clarifies what we can know, it guides what we should do, and it disciplines how we inquire. Education and research are the two places where those functions show up most clearly.

The diagram on the right shows the four strands. First, foundations: what philosophy is, and the five classical branches. Second, education: how philosophy of education works, what role philosophy plays in schooling, and the five major traditions. Third, society: how justice, equality, freedom and responsibility are argued rather than merely asserted. Fourth, research ethics: how philosophy shapes method, publication and integrity.

Notice the footer on the diagram: this is a conceptual synthesis with no primary data collected. I state that on the visual itself so it is never in doubt.

Transition: Let me begin with the oldest question of all — why human beings philosophise in the first place.""")
    return s


# ================================================================ SLIDE 3
def s03():
    s = blank(PRS)
    slide_frame(s, "Introduction and background", "Why philosophy arises \u2014 and why it persists", 3)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "Philosophy begins wherever human beings refuse to take the world for "
               "granted. The classical traditions locate its origin in wonder; modern "
               "traditions locate it in doubt. Both agree that it is a practice, not a "
               "body of settled answers.", size=12.4)
    icon_bullets(s, ML, BODY_TOP + 0.86, LCOL_W, BODY_H - 1.24, [
        ("quest", "navy", "Origins in wonder",
         "Perplexity at existence, knowledge and value: why is there something rather than nothing?"),
        ("search", "orange", "Method of questioning",
         "Claims are tested by argument; the Socratic elenchus exposes inconsistency rather than asserting doctrine."),
        ("chart", "teal", "Continuity of the discipline",
         "From ancient Athens through the scientific revolution to contemporary ethics of technology."),
        ("globe", "purple", "Cross-cultural reach",
         "Comparable traditions of systematic reflection appear in Indian, Chinese and Islamic thought."),
    ], size=11.4)
    photo_panel(s, "academy", RCOL_X, BODY_TOP - 0.04, RCOL_W, 5.50,
                "Raphael\u2019s School of Athens (1509\u20131511) idealises philosophy as "
                "public, reasoned debate across traditions \u2014 the visual counterpart of "
                "the four stages above.")
    notes(s, """Introduction and background (about 60 seconds).

Why does philosophy arise at all? The strip diagram at the bottom of the slide gives the classical answer in four stages. Philosophy begins in wonder — the refusal to take the world for granted. It becomes questioning — the Socratic practice of testing claims by argument and exposing inconsistency, rather than asserting doctrine. That questioning becomes reasoning — argument and evidence. And reasoning matures into wisdom, which is judgement in practice.

The four statements on the left add the historical dimension. Philosophy begins in wonder, but it does not stay there. Its method of questioning is what distinguishes it from mere opinion: the Socratic elenchus tests a claim by examining whether it is consistent with the other things the speaker believes. And this practice has continuity — from ancient Athens, through the scientific revolution, to today's ethics of artificial intelligence. It is also cross-cultural: comparable traditions of systematic reflection appear in Indian, Chinese and Islamic thought.

The photograph is Raphael's School of Athens, painted between 1509 and 1511. It is worth pausing on why I chose it. Raphael depicts philosophers as a community in reasoned debate, not as isolated sages. That is exactly the four-stage process in the diagram above it, and it is the model of philosophy I am defending throughout.

Transition: If philosophy is a practice, what exactly is the practice?""")
    return s


# ================================================================ SLIDE 4
def s04():
    s = blank(PRS)
    slide_frame(s, "Definition and foundations", "What philosophy is", 4)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "Philosophy is the systematic, rational examination of the most general "
               "questions about reality, knowledge, value and meaning. Its aim is not to "
               "supply final answers but to make our reasons explicit and defensible.",
               size=12.6)
    icon_bullets(s, ML, BODY_TOP + 0.90, LCOL_W, BODY_H - 1.28, [
        ("quest", "navy", "Wonder as origin",
         "Perplexity about what is real, what can be known, and what is worth doing."),
        ("search", "orange", "Rational inquiry as method",
         "Arguments are examined for validity, evidence and coherence; authority alone is insufficient."),
        ("grid", "teal", "Systematic reflection as form",
         "Ideas are organised into coherent positions, and the consequences of each position are traced."),
        ("chat", "purple", "Dialogue as practice",
         "Philosophy is conducted publicly, in criticism and reply, not privately."),
    ], size=11.4)
    diagram(s, "s04_definition", RCOL_X, BODY_TOP - 0.04, RCOL_W, 5.50)
    notes(s, """Definition and foundations (about 60 seconds).

The definition on the left is deliberately careful. Philosophy is the systematic, rational examination of the most general questions about reality, knowledge, value and meaning. Note the emphasis: its aim is not to supply final answers, but to make our reasons explicit and defensible. That distinction matters, because it separates philosophy from ideology.

The panel on the right breaks the word itself down. It comes from two Greek roots: philos, meaning love or attraction, and sophia, meaning wisdom. So philosophy is literally the love of wisdom — an activity of pursuit, not a possession.

The right-hand panel also gives the three foundations. First, wonder as origin: philosophy starts in perplexity about what is real, what can be known, and what is worth doing. Second, rational inquiry as method: arguments are examined for validity, evidence and coherence, and an appeal to authority is not enough. Third, systematic reflection as form: ideas are organised into coherent positions and the consequences of each position are traced out.

The fourth statement on the left adds something the definition alone can miss — dialogue as practice. Philosophy is conducted publicly, in criticism and reply. That is why this presentation ends with discussion questions rather than with a conclusion that closes the matter.

Transition: Within this practice, five classical branches have developed. Each asks a different kind of question.""")
    return s


# ================================================================ SLIDE 5
def s05():
    s = blank(PRS)
    slide_frame(s, "Foundations", "The five classical branches of philosophy", 5)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "Each branch asks a distinctive question, and each supplies a distinctive "
               "test of adequacy. Together they form the working toolkit that the later "
               "sections of this presentation apply to education and research.",
               size=12.2)
    icon_bullets(s, ML, BODY_TOP + 0.82, LCOL_W, BODY_H - 1.20, [
        ("bulb", "navy", "Metaphysics \u2014 what is real?",
         "Reality, existence, mind, causation and time. It underpins any claim about what there is."),
        ("search", "orange", "Epistemology \u2014 what can we know?",
         "Knowledge, belief, truth, justification and evidence. It guides research method."),
        ("scales", "teal", "Ethics \u2014 what ought we to do?",
         "Right action, virtue, duty and consequence. It guides conduct and professional codes."),
        ("gear", "purple", "Logic \u2014 what follows?",
         "Validity, inference and argument structure. It guards reasoning from fallacy."),
        ("heart", "crimson", "Aesthetics \u2014 what is beauty?",
         "Art, taste, judgement, expression and form. It guides criticism and interpretation."),
    ], size=11.0, gap=0.10)
    diagram(s, "s05_branches", RCOL_X, BODY_TOP - 0.04, RCOL_W, 5.50)
    notes(s, """The five classical branches (about 80 seconds).

This is the conceptual toolkit for the rest of the presentation. Five branches, five different questions, five different tests of adequacy.

Metaphysics asks what is real. It deals with reality, existence, being, mind, causation and time. When a researcher claims that something exists — a construct such as intelligence, or a variable such as motivation — that is a metaphysical commitment, and it should be made explicit.

Epistemology asks what can we know, and how. It deals with knowledge, belief, truth, justification and evidence. This branch directly guides research method, and I will return to it on the methodology slide.

Ethics asks what ought we to do. It covers right action, virtue, duty and consequences. It guides conduct and it underlies professional codes of research integrity.

Logic asks what follows from what. It covers validity, inference and the structure of arguments. Its job is to guard reasoning against fallacy — which is a technical matter, not a matter of opinion.

Aesthetics asks what beauty is, and what makes a judgement of taste defensible. It covers art, expression and form, and it guides criticism and interpretation. It matters to education because the arts are part of the curriculum and their value is contested.

Look at the diagram on the right: each column repeats the question, and then lists what the branch covers and what it guides. Notice the visual point — I have given each branch its own icon and its own colour, and those colours stay consistent for the rest of the deck.

Transition: Now let me bring this toolkit to bear on education.""")
    return s


# ================================================================ SLIDE 6
def s06():
    s = blank(PRS)
    slide_frame(s, "Philosophy and education", "The relationship between philosophy and education", 6)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "The relationship runs in both directions. Philosophy clarifies the aims, "
               "values and criteria of education; education tests those aims against "
               "experience and makes them public. Neither can be reduced to the other.",
               size=12.4)
    icon_bullets(s, ML, BODY_TOP + 0.86, LCOL_W, BODY_H - 1.24, [
        ("target", "navy", "Aims",
         "What is education for? Growth, autonomy, citizenship, employability \u2014 each is a value claim."),
        ("book", "orange", "Curriculum",
         "Which knowledge is most worth teaching, and on what grounds is that selection made?"),
        ("people", "teal", "Pedagogy",
         "How should teaching and learning be conducted? Authority, dialogue, discovery or instruction?"),
        ("check", "purple", "Assessment",
         "What counts as genuine educational success, and what does measuring it distort?"),
    ], size=11.2)
    diagram(s, "s06_edu_bridge", RCOL_X, BODY_TOP - 0.04, RCOL_W, 5.50)
    notes(s, """Philosophy and education (about 65 seconds).

The relationship between philosophy and education runs in both directions, and the diagram makes that explicit with two arrows. Philosophy clarifies the aims, values and criteria of education. Education then tests those aims against experience and makes them public. The footer cites Dewey's Democracy and Education of 1916, Peters's Ethics and Education of 1966, and Biesta's Good Education in an Age of Measurement of 2010 — three points across a century where that two-way relation was argued.

The four cards on the right take each element in turn. Aims: what is education for? Growth, autonomy, citizenship, employability — each of these is a value claim, not a neutral description, and philosophy's job is to make the value claim visible. Curriculum: which knowledge is most worth teaching, and on what grounds is that selection made? Pedagogy: how should teaching be conducted — by authority, by dialogue, by discovery, or by direct instruction? Assessment: what counts as genuine educational success, and what does measuring it distort?

That last question is the sharpest. Biesta's argument is that an excessive focus on measurable outcomes can produce a democratic deficit in education, because what is easily measured displaces what is educationally important.

The four statements on the left make the same point in condensed form, so you can read them at a glance.

Transition: If those are the questions, what does philosophy actually do in a school?""")
    return s


# ================================================================ SLIDE 7
def s07():
    s = blank(PRS)
    slide_frame(s, "Philosophy and education", "The role of philosophy in education", 7)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "In practice philosophy performs five tasks in education. It does not tell "
               "teachers what to do; it makes the reasons for what they do available for "
               "examination.", size=12.2)
    icon_bullets(s, ML, BODY_TOP + 0.76, LCOL_W, BODY_H - 1.14, [
        ("target", "navy", "Clarifying aims",
         "Distinguishing what education is for from what it currently measures."),
        ("gear", "orange", "Examining assumptions",
         "Making implicit beliefs about learners, knowledge and authority explicit."),
        ("search", "teal", "Developing critical thinking",
         "Teaching the evaluation of evidence and argument as a curriculum objective, not a by-product."),
        ("scales", "purple", "Grounding moral education",
         "Providing reasoned frameworks for values education rather than assertion."),
        ("people", "crimson", "Framing policy debate",
         "Supplying the normative vocabulary in which competing proposals can be compared."),
    ], size=11.0, gap=0.10)
    photo_panel(s, "classroom", RCOL_X, BODY_TOP - 0.04, RCOL_W, 5.50,
                "A teacher working with pupils in a Jordanian classroom. Philosophy "
                "enters such a room through the aims, assumptions and judgements the "
                "teacher brings \u2014 not as an extra subject.")
    notes(s, """The role of philosophy in education (about 70 seconds).

This slide answers a practical question: what does philosophy actually do in education? I have identified five tasks, and I want to be careful that none of them is overstated.

First, clarifying aims. Philosophy distinguishes what education is for from what it currently measures. Those are not the same thing, and conflating them is a common policy error.

Second, examining assumptions. Every classroom rests on beliefs about learners, about knowledge, and about authority. Philosophy's job is to make those implicit beliefs explicit so they can be examined rather than merely inherited.

Third, developing critical thinking. Siegel's Educating Reason, from 1988, argues that rationality and critical thinking should be a curriculum objective in their own right, not a by-product of teaching subjects.

Fourth, grounding moral education. Noddings's work on an ethics of care, from 1984, is one example of a reasoned framework for values education — the alternative to simply asserting values to students.

Fifth, framing policy debate. Philosophy supplies the normative vocabulary in which competing educational proposals can be compared.

The photograph shows a teacher helping pupils in a classroom in the Zaatari refugee camp in Jordan. I chose it because it shows the ordinary situation that all five of these abstract tasks are about. Philosophy enters that room through the aims, the assumptions and the judgements the teacher brings. It does not enter as an extra subject on the timetable.

Transition: Those judgements cluster into recognisable traditions. Let me compare the five major ones.""")
    return s


# ================================================================ SLIDE 8
def s08():
    s = blank(PRS)
    slide_frame(s, "Educational philosophies", "Five major educational philosophies compared", 8)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "The five traditions below differ not about whether to teach, but about "
               "what reality and knowledge are taken to be \u2014 and therefore about what "
               "teaching should aim at. The comparison is conceptual, not empirical.",
               size=12.0)
    icon_bullets(s, ML, BODY_TOP + 0.72, LCOL_W, BODY_H - 1.10, [
        ("chat", "navy", "Idealism",
         "Reality is mind-dependent. Teacher as exemplar; Socratic dialogue and character formation."),
        ("search", "navy", "Realism",
         "Reality exists independently. Teacher as authority; demonstration and subject mastery."),
        ("gear", "orange", "Pragmatism",
         "Reality is experience; truth is what works in inquiry. Projects and learning by doing."),
        ("heart", "teal", "Naturalism",
         "Nature is the whole of reality. Teacher as facilitator; interest-led, experiential work."),
        ("quest", "purple", "Existentialism",
         "Existence precedes essence; meaning is chosen. Reflection and discussion of dilemmas."),
    ], size=10.8, gap=0.09)
    diagram(s, "s07_edphil", RCOL_X - 0.10, BODY_TOP - 0.10, RCOL_W + 0.20, 5.70)
    notes(s, """Five major educational philosophies (about 90 seconds).

This is the analytical centre of the presentation. The table compares five traditions across four dimensions, and I want to explain the logic of the comparison before the details.

The key point is on the left: these traditions do not disagree about whether to teach. They disagree about what reality and knowledge are taken to be, and therefore about what teaching should aim at. That is why the second column is "reality and knowledge" — it is the foundation, and the other columns follow from it.

Idealism holds that reality is mind-dependent and truth is coherence of ideas. Education aims at self-realisation, and the teacher is an exemplar who works through dialogue and great texts.

Realism holds that reality exists independently of the mind and knowledge mirrors that order. Education aims at understanding the ordered world, and the teacher is an authority presenting organised subject matter.

Pragmatism holds that reality is experience and truth is what works in inquiry. Education aims at growth through solving real problems, and the teacher is a guide while the learner is an active inquirer. Dewey is the central figure here.

Naturalism holds that nature is the whole of reality and development unfolds naturally. Education is child-centred, the teacher is a facilitator, and interference is minimised. Rousseau is the classic reference.

Existentialism holds that existence precedes essence, so meaning must be chosen rather than received. Education aims at authenticity, freedom and personal responsibility, and the teacher provokes rather than instructs.

The footer is important for academic honesty: this is a synthesis of standard accounts, citing Gutek, Curren and Siegel. It is a conceptual comparison, not an empirical study of which tradition works better.

Transition: What do these abstractions look like when a teacher stands in front of a class?""")
    return s


# ================================================================ SLIDE 9
def s09():
    s = blank(PRS)
    slide_frame(s, "Educational philosophies", "Classroom applications of each tradition", 9)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "The same syllabus can be taught in five different ways. Each tradition "
               "produces a recognisable classroom signature, and each carries a risk that "
               "its critics identify.", size=12.2)
    icon_bullets(s, ML, BODY_TOP + 0.76, LCOL_W, BODY_H - 1.14, [
        ("chat", "navy", "Idealism in practice",
         "Seminar questioning that asks pupils to justify beliefs. Risk: neglecting practical skills."),
        ("search", "navy", "Realism in practice",
         "Careful observation, worked examples, mastery of established knowledge. Risk: passivity."),
        ("gear", "orange", "Pragmatism in practice",
         "Projects that solve real problems and test ideas. Risk: fragmenting systematic knowledge."),
        ("heart", "teal", "Naturalism in practice",
         "Interest-led discovery and outdoor, experiential work. Risk: uneven coverage."),
        ("quest", "purple", "Existentialism in practice",
         "Reflective journals and open dilemmas of choice. Risk: underplaying shared knowledge."),
    ], size=10.8, gap=0.09)
    diagram(s, "s08_classroom", RCOL_X, BODY_TOP - 0.04, RCOL_W, 5.50)
    notes(s, """Classroom applications (about 70 seconds).

This slide moves from theory to practice. The point I want to establish is that the same syllabus can be taught in five different ways, and that each tradition produces a recognisable classroom signature.

Idealism shows up as seminar questioning that asks pupils to justify their beliefs. Its risk, which critics point out, is that it can neglect practical skills.

Realism shows up as careful observation, worked examples, and mastery of established knowledge. Its risk is learner passivity.

Pragmatism shows up as projects that solve real problems. Its risk is that inquiry can fragment systematic knowledge, so pupils learn to solve problems without acquiring a coherent body of understanding.

Naturalism shows up as interest-led discovery and outdoor work. Its risk is uneven coverage, because pupils' interests do not map neatly onto a curriculum.

Existentialism shows up as reflective journals and open dilemmas. Its risk is underplaying shared knowledge, which pupils need in order to choose meaningfully in the first place.

The cards on the right restate these compactly. The footer repeats the caution: these are illustrative practices and I am claiming no effect sizes. The risks are the ones identified in the philosophical literature, and they are the reason most real schools blend traditions rather than following one.

Transition: Education sits inside a wider society. Let me widen the frame.""")
    return s


# ================================================================ SLIDE 10
def s10():
    s = blank(PRS)
    slide_frame(s, "Philosophy and society", "Philosophy and society: from persons to institutions", 10)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "Society is not a natural object that philosophy merely observes. It is "
               "partly constituted by the concepts we use to organise it. Philosophy "
               "supplies and criticises those concepts.", size=12.4)
    icon_bullets(s, ML, BODY_TOP + 0.84, LCOL_W, BODY_H - 1.22, [
        ("quest", "navy", "Persons",
         "Reasoning and choosing agents who can be held responsible for their actions."),
        ("people", "navy", "Communities",
         "Shared norms, trust, dialogue and care \u2014 the informal fabric beneath formal rules."),
        ("grid", "teal", "Institutions",
         "Law, schools, health, media and science: each embodies normative commitments."),
        ("globe", "orange", "State and global order",
         "Rights, justice, legitimacy and peace, and the problem of agreeing on them across cultures."),
    ], size=11.2)
    photo_panel(s, "freedom_press", RCOL_X, BODY_TOP - 0.04, RCOL_W, 2.55,
                "A press conference. Free inquiry and free reporting are social "
                "conditions that philosophy helps to justify and to limit.")
    photo_panel(s, "responsibility", RCOL_X, BODY_TOP + 2.72, RCOL_W, 2.55,
                "Community service in San Diego. Responsibility is exercised in "
                "particular acts, not only discussed in the abstract.")
    notes(s, """Philosophy and society (about 65 seconds).

Now I widen the frame. The claim on this slide is that society is not a natural object which philosophy merely observes. It is partly constituted by the concepts we use to organise it — and philosophy both supplies and criticises those concepts.

The diagram sets out four layers. At the base, persons: reasoning and choosing agents who can be held responsible for their actions. Above them, communities: shared norms, trust, dialogue and care — the informal fabric that lies beneath formal rules. Above them, institutions: law, schools, health, media and science, each of which embodies normative commitments. And at the top, the state and global order: rights, justice, legitimacy and peace — and the difficult problem of agreeing on those across different cultures.

The two photographs give the abstract layers a concrete referent. The first shows a press conference, because free inquiry and free reporting are social conditions that philosophy helps both to justify and to limit. The second shows community service in San Diego, because responsibility is exercised in particular acts rather than only discussed in the abstract.

The four statements on the left restate the layers so the slide can be read without the diagram.

Transition: Four concepts do most of the work in that discussion — justice, equality, freedom and responsibility. Let me take them one at a time.""")
    return s


# ================================================================ SLIDE 11
def s11():
    s = blank(PRS)
    slide_frame(s, "Philosophy and society", "Justice, equality, freedom and responsibility", 11)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "These four concepts are the working vocabulary of public argument. "
               "Philosophy\u2019s contribution is not to settle them once and for all, but "
               "to show what each one commits us to when we use it.", size=12.4)
    icon_bullets(s, ML, BODY_TOP + 0.84, LCOL_W, BODY_H - 1.22, [
        ("scales", "navy", "Justice",
         "Rawls argues for fairness as the first virtue of institutions, tested from behind a veil of ignorance."),
        ("people", "orange", "Equality",
         "Equal moral worth, equal opportunity and equal treatment are distinct demands that can conflict."),
        ("globe", "teal", "Freedom",
         "Negative freedom is non-interference; positive freedom is the real capability to act. Sen argues both matter."),
        ("handshake", "purple", "Responsibility",
         "Rights presuppose duties; a claim of freedom imposes obligations on others as well as entitlements."),
    ], size=11.2)
    photo_panel(s, "justice", RCOL_X, BODY_TOP - 0.04, RCOL_W, 2.55,
                "Lady Justice outside the Civil Court in Melbourne. The scales and the "
                "sword dramatise the demand that judgement be both fair and enforceable.")
    photo_panel(s, "equality", RCOL_X, BODY_TOP + 2.72, RCOL_W, 2.55,
                "The National Equality March, Washington, 2009. Equality is claimed in "
                "public argument, using reasons addressed to those who disagree.")
    notes(s, """Justice, equality, freedom and responsibility (about 75 seconds).

Four concepts do most of the work in public argument, and I want to show what each commits us to.

Justice. Rawls, in A Theory of Justice, argues that justice is the first virtue of social institutions, and proposes that we test principles of justice from behind a veil of ignorance — that is, by asking what rules we would accept if we did not know what position we would occupy in society.

Equality. This is the one where precision matters most, because equal moral worth, equal opportunity and equal treatment are three distinct demands, and they can conflict with each other. Treating everyone identically can perpetuate inequality of outcome.

Freedom. The classical distinction is between negative freedom, which is non-interference, and positive freedom, which is the real capability to act. Amartya Sen's Development as Freedom argues that both matter, and that poverty is a deprivation of capability rather than merely of income.

Responsibility. Rights presuppose duties. A claim of freedom imposes obligations on others as well as conferring entitlements — that is the point of the handshake icon.

The two photographs keep this from floating free of the world. Lady Justice outside the Civil Court in Melbourne dramatises the demand that judgement be both fair and enforceable. The National Equality March of 2009 shows equality being claimed in public argument, addressed to those who disagree. That is precisely the practice philosophy tries to make rigorous.

Transition: The same concepts reappear inside research, where they become questions of method and integrity.""")
    return s


# ================================================================ SLIDE 12
def s12():
    s = blank(PRS)
    slide_frame(s, "Philosophy in research", "Philosophy in research and knowledge development", 12)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "Research is not a neutral procedure that philosophy inspects from "
               "outside. Every methodological choice already contains philosophical "
               "commitments about what exists, what can be known, and whose values count.",
               size=12.0)
    icon_bullets(s, ML, BODY_TOP + 0.80, LCOL_W, BODY_H - 1.18, [
        ("bulb", "navy", "Ontology",
         "What exists to be studied? If constructs are treated as measurable things, that is a metaphysical commitment."),
        ("search", "orange", "Epistemology",
         "How can it be known? Positivist, interpretive and critical paradigms license different methods."),
        ("scales", "teal", "Axiology",
         "Whose values shape the inquiry? Problem selection and framing are never value-free."),
        ("gear", "purple", "Logic",
         "Do the inferences hold? Validity and the avoidance of fallacy are technical requirements."),
        ("chart", "crimson", "Falsifiability",
         "Popper argues that a claim is scientific only if it forbids something \u2014 if evidence could refute it."),
    ], size=10.6, gap=0.09)
    diagram(s, "s11_research_flow", RCOL_X - 0.10, BODY_TOP - 0.10, RCOL_W + 0.20, 5.66)
    notes(s, """Philosophy in research (about 75 seconds).

The claim on this slide is that research is not a neutral procedure which philosophy inspects from outside. Every methodological choice already contains philosophical commitments.

The workflow across the top of the diagram shows eight stages: problem, question, theory and literature, design, data collection, analysis, interpretation, publication. Below it, five philosophical lenses apply to those stages.

Ontology asks what exists to be studied. If a researcher treats a construct such as motivation or intelligence as a measurable thing, that is a metaphysical commitment, and it deserves to be stated.

Epistemology asks how it can be known. Positivist, interpretive and critical paradigms license different methods and different kinds of evidence. Choosing a questionnaire rather than an interview is an epistemological choice.

Axiology asks whose values shape the inquiry. Problem selection and framing are never value-free — the decision to study one question rather than another reflects priorities.

Logic asks whether the inferences hold. Validity and the avoidance of fallacy are technical requirements, not matters of taste.

And falsifiability: Popper argued in The Logic of Scientific Discovery that a claim is scientific only if it forbids something — that is, only if some possible observation could refute it. That is why the later slides on reproducibility matter.

Transition: From method, let me move to publication — the point at which research becomes public and accountable.""")
    return s


# ================================================================ SLIDE 13
def s13():
    s = blank(PRS)
    slide_frame(s, "Research, publication and ethics", "Philosophy, publication and research ethics", 13)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "Publication is where research becomes a public claim, and therefore where "
               "ethical obligation becomes most explicit. Four pillars carry almost the "
               "whole burden of responsible practice.", size=12.2)
    icon_bullets(s, ML, BODY_TOP + 0.78, LCOL_W, BODY_H - 1.16, [
        ("check", "navy", "Informed consent",
         "Participants are told the purpose, risks and their right to withdraw, and agree freely."),
        ("shield", "teal", "Confidentiality",
         "Personal data are protected and anonymity preserved where it was promised."),
        ("pen", "orange", "Attribution",
         "Others\u2019 words, data and images are credited; plagiarism is a breach of integrity."),
        ("gear", "purple", "Integrity",
         "No fabrication, falsification or selective reporting; methods and limits are declared."),
        ("people", "crimson", "Peer review and authorship",
         "Authorship reflects real contribution; reviewers declare conflicts of interest."),
    ], size=10.8, gap=0.09)
    diagram(s, "s12_ethics", RCOL_X, BODY_TOP - 0.04, RCOL_W, 5.50)
    notes(s, """Publication and research ethics (about 70 seconds).

Publication is the point at which research becomes a public claim, and that is where ethical obligation becomes most explicit. Four pillars carry most of the burden.

Informed consent: participants are told the purpose, the risks and their right to withdraw, and they agree freely. This is the pillar that the Belmont Report of 1979 and the Declaration of Helsinki were written to secure.

Confidentiality: personal data are protected and anonymity is preserved where it was promised. Breaking that promise is not a technical failure but a breach of trust.

Attribution: other people's words, data and images are credited. Plagiarism is a breach of integrity because it misrepresents whose work is being presented.

Integrity: no fabrication, falsification or selective reporting, and methods and limits are declared. This is where research misconduct is usually classified.

The fifth statement adds peer review and authorship: authorship should reflect real contribution, and reviewers must declare conflicts of interest.

The diagram on the right puts each pillar in its own block with an icon. The footer cites the Belmont Report, the Declaration of Helsinki and the Singapore Statement on Research Integrity of 2010.

Transition: These principles are easier to accept in the abstract than to apply. Let me look at cases where they were violated.""")
    return s


# ================================================================ SLIDE 14
def s14():
    s = blank(PRS)
    slide_frame(s, "Research, publication and ethics", "Examples of ethical and unethical research practice", 14)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "The distinction is not always between good and bad researchers. It is "
               "between practices that protect participants and readers, and practices "
               "that do not \u2014 and the difference is often procedural.", size=11.8)
    icon_bullets(s, ML, BODY_TOP + 0.72, LCOL_W, BODY_H - 1.10, [
        ("scales", "crimson", "Tuskegee syphilis study (1932\u20131972)",
         "Treatment was withheld from participants who were not informed; a direct cause of the Belmont Report."),
        ("people", "crimson", "Milgram obedience study (1963)",
         "Revealed substantial obedience to authority, but caused serious distress and prompted ethical review."),
        ("quest", "crimson", "Stanford prison experiment (1971)",
         "Role assignment produced abusive behaviour; the design has since been criticised on both ethical and methodological grounds."),
        ("pen", "crimson", "Wakefield et al. (1998), retracted 2010",
         "The Lancet retracted the paper; the episode illustrates the cost of publication without adequate scrutiny."),
        ("chart", "orange", "Reproducibility and reporting",
         "Large-scale replication found much lower reproducibility than expected, motivating open-science reform."),
    ], size=10.2, gap=0.08)
    diagram(s, "s13_ethics_compare", RCOL_X - 0.10, BODY_TOP - 0.10, RCOL_W + 0.20, 5.66)
    notes(s, """Examples of ethical and unethical practice (about 85 seconds).

I want to be careful here, because these cases are often told as morality tales and that flattens what they actually teach. The distinction is usually not between good and bad researchers. It is between practices that protect participants and readers, and practices that do not — and the difference is often procedural.

The Tuskegee syphilis study ran from 1932 to 1972. Treatment was withheld from participants who were not informed of the study's purpose. This case is a direct cause of the Belmont Report and of modern institutional review.

Milgram's 1963 obedience study produced important findings about obedience to authority, but it caused serious distress to participants, and it prompted the development of ethical review for research on human subjects.

The Stanford prison experiment in 1971 assigned students to guard and prisoner roles, and produced abusive behaviour. It has since been criticised on ethical and methodological grounds — Zimbardo himself later wrote about it critically.

The Wakefield paper published in The Lancet in 1998 was retracted in 2010. I include it because it illustrates a different failure: not harm to participants, but publication without adequate scrutiny, and the public consequences that followed.

The last statement is the constructive one. Large-scale replication efforts found substantially lower reproducibility than the field expected, and that finding motivated the open-science reforms — preregistration, data sharing, and reporting standards.

The comparison table on the right sets accepted practice against misconduct in five matched pairs, so the contrast is visible at a glance.

Transition: What can we take from all this for education and society?""")
    return s


# ================================================================ SLIDE 15
def s15():
    s = blank(PRS)
    slide_frame(s, "Application", "Philosophy in everyday life", 15)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "Philosophy is not confined to seminars. It is present whenever a person "
               "weighs evidence, asks whether a rule is fair, or decides what they owe to "
               "others \u2014 which is to say, most days.", size=12.2)
    icon_bullets(s, ML, BODY_TOP + 0.80, LCOL_W, BODY_H - 1.18, [
        ("search", "navy", "Evaluating claims",
         "Deciding whether a headline, advertisement or policy claim is supported by evidence."),
        ("scales", "orange", "Making moral decisions",
         "Weighing honesty, loyalty, harm and fairness when they point in different directions."),
        ("chat", "teal", "Disagreeing well",
         "Distinguishing disagreement about facts from disagreement about values."),
        ("gear", "purple", "Professional judgement",
         "Engineers, doctors and teachers apply codes that encode ethical reasoning."),
        ("bulb", "crimson", "Living with uncertainty",
         "Acting reasonably without guarantees, and revising beliefs when evidence changes."),
    ], size=10.8, gap=0.09)
    photo_panel(s, "children_learning", RCOL_X, BODY_TOP - 0.04, RCOL_W, 2.55,
                "Children at school. The habits of questioning and justifying begin "
                "early, long before they are called philosophy.")
    photo_panel(s, "lecture_hall", RCOL_X, BODY_TOP + 2.72, RCOL_W, 2.55,
                "A university teaching space. Formal education is where everyday "
                "reasoning is examined systematically for the first time.")
    notes(s, """Philosophy in everyday life (about 60 seconds).

It would be a failure of this presentation if philosophy came across as something confined to seminars. The claim here is that philosophy is present whenever a person weighs evidence, asks whether a rule is fair, or decides what they owe to others — which is to say, most days.

Evaluating claims: deciding whether a headline, an advertisement or a policy claim is actually supported by evidence. That is applied epistemology.

Making moral decisions: weighing honesty, loyalty, harm and fairness when they point in different directions. That is applied ethics.

Disagreeing well: distinguishing disagreement about facts from disagreement about values. Much public argument goes wrong precisely because the two are confused.

Professional judgement: engineers, doctors and teachers apply codes of conduct that encode ethical reasoning. As a computer science student, I would add that the ethics of artificial intelligence is now a professional requirement, not an optional interest. UNESCO's 2021 Recommendation on the Ethics of Artificial Intelligence is one current example.

Living with uncertainty: acting reasonably without guarantees, and revising beliefs when the evidence changes.

The photographs connect this to education. The first shows children at school, where the habits of questioning and justifying begin long before anyone calls it philosophy. The second shows a university teaching space, where everyday reasoning is examined systematically for the first time.

Transition: Let me draw out the implications for both.""")
    return s


# ================================================================ SLIDE 16
def s16():
    s = blank(PRS)
    slide_frame(s, "Discussion", "Implications for education and society", 16)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "If the argument so far is accepted, then three sets of consequences "
               "follow. These are reasoned proposals drawn from the literature, not "
               "empirical findings of my own.", size=12.0)
    icon_bullets(s, ML, BODY_TOP + 0.78, LCOL_W, BODY_H - 1.16, [
        ("cap", "navy", "Curriculum",
         "Protect philosophy, ethics and logic within the curriculum rather than treating them as optional."),
        ("search", "orange", "Teaching reasoning explicitly",
         "Make critical thinking a taught objective, not an incidental by-product."),
        ("shield", "teal", "Research ethics in every project",
         "Introduce consent, confidentiality and attribution at the start of student projects."),
        ("people", "purple", "Pedagogy",
         "Model argument and respectful disagreement; use dilemma discussion to build judgement."),
        ("globe", "crimson", "Public reasoning",
         "Judge public claims by evidence rather than volume; defend equality and freedom as argued principles."),
    ], size=10.8, gap=0.09)
    diagram(s, "s15_implications", RCOL_X - 0.10, BODY_TOP - 0.04, RCOL_W + 0.20, 5.56)
    notes(s, """Implications for education and society (about 70 seconds).

I want to be explicit about the status of what follows. These are reasoned proposals drawn from the literature, not empirical findings of my own. I have not tested them.

For the curriculum: protect philosophy, ethics and logic within the curriculum rather than treating them as optional extras. When timetables are under pressure, these are usually the first subjects to be reduced.

For teaching: make reasoning a taught objective rather than an incidental by-product. Siegel's argument is that critical thinking does not develop reliably just by studying a subject; it has to be taught.

For research training: introduce consent, confidentiality and attribution at the start of student projects, not as a formality at the end.

For pedagogy: model argument and respectful disagreement, and use dilemma discussion to build judgement. This is where the educational traditions on slide eight converge, despite their differences.

For public reasoning: judge public claims by evidence rather than volume, and defend equality and freedom as argued principles rather than slogans.

The diagram groups these into three columns — curriculum, pedagogy and society. The footer again marks them as reasoned proposals rather than findings.

Transition: Before concluding, let me be honest about the limits of this presentation.""")
    return s


# ================================================================ SLIDE 17
def s17():
    s = blank(PRS)
    slide_frame(s, "Limitations", "Limitations and areas for further study", 17)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "An honest account of a conceptual study must state what it cannot "
               "establish. Four limitations bound the claims made in this presentation, "
               "and each points to a direction for further work.", size=12.2)
    icon_bullets(s, ML, BODY_TOP + 0.80, LCOL_W, BODY_H - 1.18, [
        ("quest", "navy", "No primary data",
         "This is a synthesis of published scholarship. No experiment, survey or intervention was conducted."),
        ("globe", "orange", "Cultural scope",
         "The five branches and five traditions are presented from a predominantly Western philosophical tradition."),
        ("people", "teal", "No effectiveness claims",
         "No claim is made that any educational philosophy produces better outcomes; that would require empirical testing."),
        ("grid", "purple", "Selection of traditions",
         "Five traditions were compared; other frameworks and hybrid positions are not represented."),
        ("gear", "crimson", "Further study",
         "A systematic review, or a comparative study of reasoning instruction, would test the proposals on slide 16."),
    ], size=10.8, gap=0.09)
    photo_panel(s, "library", RCOL_X, BODY_TOP - 0.04, RCOL_W, 2.55,
                "Students reading. The synthesis in this presentation rests on the "
                "published record rather than on new data collection.")
    photo_panel(s, "graduation", RCOL_X, BODY_TOP + 2.72, RCOL_W, 2.55,
                "A university commencement. Whether philosophical education changes "
                "graduates\u2019 reasoning is an open empirical question.")
    notes(s, """Limitations and further study (about 65 seconds).

I think it is more useful to state the limits of a presentation than to hope nobody notices them. Four limitations bound what I have claimed.

First, no primary data. This is a synthesis of published scholarship. I conducted no experiment, survey or intervention, so every empirical statement I have made comes from someone else's published work, cited on the reference slides.

Second, cultural scope. The five branches and the five educational traditions are presented from a predominantly Western philosophical tradition. Comparable traditions in Indian, Chinese and Islamic thought exist and are not represented here.

Third, no effectiveness claims. I have not claimed that any educational philosophy produces better outcomes. Making that claim would require empirical testing, and the traditions on slide eight are conceptual frameworks, not interventions with measured effects.

Fourth, selection. Five traditions were compared; other frameworks and hybrid positions are not represented.

The last point is constructive: a systematic review of reasoning instruction, or a comparative study of the kind of dilemma discussion I recommended, would be the natural way to test the proposals I have made.

The photographs make the boundary concrete. The first shows students reading — the published record on which this synthesis rests. The second shows a commencement ceremony — whether philosophical education changes graduates' reasoning is precisely the open empirical question I have not answered.

Transition: Let me close by drawing the argument together.""")
    return s


# ================================================================ SLIDE 18
def s18():
    s = blank(PRS)
    slide_frame(s, "Conclusion", "Conclusion and key takeaways", 18)
    lead_block(s, ML, BODY_TOP, LCOL_W,
               "Philosophy is best understood as the connective discipline. It does not "
               "sit alongside education and research; it supplies the reasoning that "
               "makes both of them defensible.", size=12.4)
    icon_bullets(s, ML, BODY_TOP + 0.82, LCOL_W, BODY_H - 1.20, [
        ("bulb", "navy", "A practice, not a doctrine",
         "Philosophy is justified questioning; it is judged by the quality of its reasons."),
        ("grid", "orange", "Five branches, five tests",
         "Metaphysics, epistemology, ethics, logic and aesthetics each apply a distinct standard."),
        ("cap", "teal", "Education is the proving ground",
         "Aims, curriculum, pedagogy and assessment are where philosophical claims become consequential."),
        ("shield", "purple", "Research ethics is applied philosophy",
         "Consent, confidentiality, attribution and integrity are reasoned obligations, not paperwork."),
        ("globe", "crimson", "A reasoned public sphere",
         "Justice, equality and freedom are argued principles; a philosophically literate society argues better."),
    ], size=10.8, gap=0.09)
    diagram(s, "s16_conclusion", RCOL_X - 0.10, BODY_TOP - 0.10, RCOL_W + 0.20, 5.66)
    notes(s, """Conclusion (about 70 seconds).

Let me draw the argument together.

Philosophy is best understood as the connective discipline. It does not sit alongside education and research as a separate subject; it supplies the reasoning that makes both of them defensible.

Five takeaways. First, philosophy is a practice, not a doctrine — it is justified questioning, and it is judged by the quality of its reasons rather than by the fame of its authorities.

Second, the five branches each apply a distinct standard: metaphysics asks what is real, epistemology what can be known, ethics what ought to be done, logic what follows, and aesthetics what counts as beauty. Those standards are not interchangeable.

Third, education is the proving ground. Aims, curriculum, pedagogy and assessment are where abstract philosophical claims become consequential, because they affect what children actually experience.

Fourth, research ethics is applied philosophy. Consent, confidentiality, attribution and integrity are reasoned obligations, not administrative paperwork.

Fifth, a philosophically literate society argues better. Justice, equality and freedom are argued principles, and a public that can follow those arguments makes better collective decisions.

The diagram shows philosophy at the centre with three consequences radiating from it: education, individuals and society. The right-hand panel repeats the five takeaways as a summary.

That completes the presentation. Thank you — I am happy to take questions.

Transition: I have prepared a short list of the questions I expect, which appears on the final reference slide, and I am glad to take any others.""")
    return s


# ================================================================ SLIDE 19
def s19():
    s = blank(PRS)
    slide_frame(s, "References", "References \u2014 journal articles and standards", 19, total=20)
    lead_block(s, ML, BODY_TOP - 0.04, CW,
               "All sources below are supplementary scholarly literature, verified "
               "against Crossref and Open Library. No primary data were collected for "
               "this presentation.", size=10.4, color=GREY)
    ref_columns(s, ML, BODY_TOP + 0.46, CW, BODY_H - 0.60,
                refs.ARTICLES + refs.STANDARDS, size=7.8, cols=2, gap=0.34)
    notes(s, """References, part one (about 30 seconds).

This slide lists the journal articles and the standards or institutional sources. Every one has been verified: the DOIs resolve through Crossref, and the standards documents were retrieved from the issuing bodies.

The articles include the empirical studies I cited on the ethics slide — Milgram's obedience study, the Lancet retraction of the Wakefield paper, the reproducibility study, and surveys of research misconduct by Fanelli and by Martinson and colleagues. They also include the philosophical literature on educational research, notably Biesta's argument about evidence-based practice, and the open-science reform programme led by Nosek and colleagues.

The standards are the Belmont Report, the Declaration of Helsinki, the Singapore Statement on Research Integrity, the ALLEA European Code of Conduct, the ICMJE recommendations, and UNESCO's Recommendation on the Ethics of Artificial Intelligence.

The note at the top is deliberate: all of these are supplementary scholarly literature. I collected no primary data, so nothing on these slides reports my own findings.

Transition: The book references and the discussion questions follow.""")
    return s


# ================================================================ SLIDE 20
def s20():
    s = blank(PRS)
    slide_frame(s, "References and discussion", "References \u2014 books, and questions for discussion", 20, total=20)
    ref_columns(s, ML, BODY_TOP - 0.06, CW, 4.16, refs.BOOKS, size=7.4, cols=3, gap=0.28)
    y = BODY_TOP + 4.24
    rect(s, ML, y, CW, 1.36, fill=TINT, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s, ML, y + 0.10, 0.055, 1.16, fill=ORANGE)
    icon(s, "chat", "orange", ML + 0.20, y + 0.16, 0.28)
    tf = textbox(s, ML + 0.62, y + 0.12, 3.0, 0.30)
    para(tf, "Questions for discussion", size=11.6, color=ORANGE, bold=True, first=True)
    qs = ["Can education pursue measurable outcomes without distorting its aims?",
          "Should research ethics be taught as procedure or as reasoning?",
          "Is critical thinking a separate subject or an outcome of subject teaching?",
          "What does a society lose when public argument is settled by volume rather than evidence?"]
    tf2 = textbox(s, ML + 0.62, y + 0.46, CW - 0.90, 0.84)
    for i, q in enumerate(qs):
        para(tf2, [(str(i + 1) + ".  ", True, ORANGE), (q, False, CHAR)],
             size=10.2, first=(i == 0), space_after=3.2, line_spacing=1.05)
    notes(s, """References, part two, and discussion questions (about 40 seconds).

The upper part of this slide lists the books, in three columns. The works fall into four groups. The philosophical foundations: Russell's History of Western Philosophy, Kuhn's Structure of Scientific Revolutions, Popper's Logic of Scientific Discovery, Rawls's A Theory of Justice, and Sen's Development as Freedom. The philosophy of education: Dewey, Peters, Hirst, Whitehead, Freire, Noddings, Gutmann, Siegel, Curren, Gutek, hooks and Nussbaum. The research ethics texts: Beauchamp and Childress, and Shamoo and Resnik. And the case-study sources: Jones on the Tuskegee study, Zimbardo on the Stanford prison experiment, Milgram on obedience, and Skloot on Henrietta Lacks.

At the bottom are four questions I would be glad to discuss. The first is the one I find hardest: can education pursue measurable outcomes without distorting its aims? The second asks whether research ethics is best taught as procedure or as reasoning. The third asks whether critical thinking is a separate subject or an outcome of subject teaching. And the fourth asks what a society loses when public argument is settled by volume rather than by evidence.

Thank you for your attention. I am happy to take questions on any part of the presentation, and I have prepared a separate written list of anticipated questions with short, sourced answers if anyone would like it.""")
    return s


# ---------------------------------------------------------------- build
def main():
    for fn in [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10,
               s11, s12, s13, s14, s15, s16, s17, s18, s19, s20]:
        fn()
    os.makedirs(OUTDIR, exist_ok=True)
    out = os.path.join(OUTDIR, "Philosophy_Education_Society_Kaudilyar_R.pptx")
    PRS.save(out)
    print("saved:", out)
    print("slides:", len(PRS.slides.__iter__.__self__._sldIdLst))
    if FITLOG:
        print(f"--- {len(FITLOG)} fit warnings ---")
        for w in FITLOG[:25]:
            print("   ", w)
    else:
        print("--- no fit warnings ---")


if __name__ == "__main__":
    main()
