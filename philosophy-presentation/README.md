# Philosophy and Its Role in Education and Society

An academic research-seminar presentation by **Kaudilyar. R**,
Department of Computer Science and Engineering.

This repository holds the finished deck, its source images and diagrams, the
generator code that produced them, speaker notes for every slide, and a
companion document of anticipated audience questions.

## Deliverables

| File | What it is |
|---|---|
| `deck/Philosophy_Education_Society_Kaudilyar_R.pptx` | The editable presentation, 20 slides, 16:9, with speaker notes on every slide |
| `deck/Philosophy_Education_Society_Kaudilyar_R.pdf` | Print/share copy rendered from the PPTX |
| `deck/Speaker_Notes.docx` | All speaker notes as a readable script |
| `deck/Audience_QA_and_References.docx` | 11 anticipated questions with short sourced answers, plus the full APA 7th reference list |
| `deck/preview_montage.png` | Contact sheet of all 20 slides |

## Slide plan

1. Title and central claim
2. Abstract and structure of the argument
3. Why philosophy arises, and why it persists
4. What philosophy is
5. The five classical branches
6. Philosophy and education: the relationship
7. The role of philosophy in education
8. Five major educational philosophies compared
9. Classroom applications of each tradition
10. Philosophy and society: from persons to institutions
11. Justice, equality, freedom and responsibility
12. Philosophy in research and knowledge development
13. Philosophy, publication and research ethics
14. Examples of ethical and unethical research practice
15. Philosophy in everyday life
16. Implications for education and society
17. Limitations and areas for further study
18. Conclusion and key takeaways
19. References: journal articles and standards
20. References: books, and questions for discussion

## Visual design

* 16:9 widescreen, off-white ground, navy and charcoal type with restrained
  orange accents.
* Every major statement carries an adjacent visual. Statements sit on the left
  as icon-led cards; the supporting diagram or photograph sits on the right.
* 13 purpose-built vector infographics: branch taxonomy, educational-philosophies
  comparison table, philosophy/education bridge, research workflow with
  ontology/epistemology/axiology lens, research-ethics pillars, ethical-versus-
  unethical comparison, and a conclusion map.
* 20 photographs, all under public domain, CC0, CC BY or CC BY-SA licences,
  each credited on the slide and in `assets/photo_manifest.json`.
* The same design tokens are reused throughout, so colours and iconography stay
  consistent from slide to slide.

## Research integrity

* **No primary data were collected.** This is a conceptual synthesis. No
  experiment, survey or intervention was performed, and no effect sizes or
  statistics of the author's own are reported.
* Every factual claim is attributed. Journal articles and DOIs were verified
  against the Crossref REST API; books were verified against the Open Library
  editions API; standards documents were retrieved from the issuing bodies.
* No reference, DOI, publisher, year or quotation was invented. The verified
  list is in `src/refs.py`.
* Limitations are stated explicitly on slide 17, including the predominantly
  Western scope of the philosophical traditions presented.

## Rebuilding

```
pip install python-pptx matplotlib pillow cairosvg requests python-docx

cd src
python3 diagrams.py        # -> ../assets/diagrams/*.png
python3 gen_icons.py       # -> ../assets/icons/*.png
python3 build_pptx.py      # -> ../out/*.pptx
python3 build_docs.py      # -> ../out/Speaker_Notes.docx, Audience_QA_and_References.docx
```

Rendering the deck for visual QA requires LibreOffice:

```
export LD_LIBRARY_PATH=/usr/lib/libreoffice/program:$LD_LIBRARY_PATH
soffice --headless --convert-to pdf --outdir out out/*.pptx
pdftoppm -r 100 -png out/*.pdf out/slides/s
python3 src/qa_slides.py
```

`src/qa_slides.py` checks the rendered slides for text or graphics colliding
with the page edge. `src/svglib.py` records layout overflow warnings while the
diagrams are being generated.

## Source layout

```
src/svglib.py        SVG primitives, text metrics, icons, layout QA helpers
src/diagrams.py      the 13 infographics
src/gen_icons.py     icon PNG set
src/deck_lib.py      PPTX primitives, palette, fit-to-box image helpers
src/build_pptx.py    the 20 slides and their speaker notes
src/build_docs.py    the .docx companions
src/refs.py          verified APA 7th reference list
src/qa_content.py    anticipated audience questions
assets/photos/       20 licensed photographs
assets/diagrams/     generated infographics
assets/icons/        generated icon set
assets/photo_manifest.json   image attributions and licences
```

## Image credits

Photographs are from Wikimedia Commons and are reproduced under their stated
licences. Attribution for each image appears on the slide where it is used and
in `assets/photo_manifest.json`, which records the file title, author, licence
and source page. The infographics and icons are original vector work generated
by the scripts in `src/`.

## Citation style

APA 7th edition throughout. The reference list distinguishes journal articles,
books, and standards or institutional sources.
