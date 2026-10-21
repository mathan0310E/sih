# Naan Mudhalvan Generative AI Laboratory Record Manual

## Goal
A traditional Indian engineering college practical record manual for
**SKP Engineering College, Tiruvannamalai - 606 611**, Department of AI & DS,
course "Naan Mudhalvan - Generative Artificial Intelligence", delivered as an
editable `.docx` and a print-ready A4 `.pdf` (currently 107 pages).

## Reference documents
1. `NM LAB MANUAL CS.pdf` (98 pages, Letter, Word 2019) is the layout
   reference. It was **not** attached to the conversation; it was recovered from
   `https://github.com/mathan0310E/sih` (branch `main`, repo root). Its front
   matter is cover (college / address / DEPARTMENT OF / programme / course code /
   REGULATION / dot-leader Name, Register Number, Department, Year-Semester,
   Subject), a CERTIFICATE page with the same dot-leader fields plus
   "Certified that this is the bonafide record ..." and four signature blocks, a
   bordered INDEX table, then `Exp. no: NN  <title>` + `Date:` on every
   experiment page, and a final `CONCLUSION` page.
2. The GenAI syllabus arrived as **two screenshots**, not text. They are stored
   as `ref/img0.jpg` and `ref/img1.jpg`; read them with OCR, since the model has
   no vision. img0 = topics 1-8, img1 = topics 9-15. They are topic
   *descriptions*, so the experiment list in `content.py` is the transcription of
   those 15 topics in order.
3. The Skill Wallet program page (pasted as text) supplies the onboarding tasks
   and learning journey now recorded in `programme.py`.

## Build
```
pip install python-docx pillow pymupdf
python3 assemble.py                       # -> output/NM_LAB_MANUAL_GenAI.docx
export LD_LIBRARY_PATH=/usr/lib/libreoffice/program:$LD_LIBRARY_PATH
soffice --headless --convert-to pdf --outdir output output/NM_LAB_MANUAL_GenAI.docx
```
LibreOffice **requires** `LD_LIBRARY_PATH=/usr/lib/libreoffice/program` here,
otherwise `libreglo.so` is not found.

## Source files
- `build_manual.py` - docx primitives: A4 page border, footer PAGE field,
  fixed-layout bordered tables, shaded monospace code blocks, screenshot
  placeholder boxes, `real_figure()` for authentic captures,
  `borderless_table()` for signature blocks.
- `content.py` - college details, experiments 1-10, appendices, `EXPERIMENTS`.
- `content2.py` - experiments 11-15 (`E11_15`).
- `detailed.py` - `D["01"] ... D["15"]`, the exhaustive step-by-step guides
  (142 steps total). Each step is a dict with `title`, `action`, optional
  `command` lines, `observe` and `note`.
- `programme.py` - the verified Skill Wallet onboarding tasks, learning journey
  text and the link index (`TASKS`, `JOURNEY`, `LINK_INDEX`,
  `VERIFICATION_NOTES`).
- `assemble.py` - page assembly. One Word section plus page breaks, so footer
  page numbers run continuously.
- `shots/` - authentic screenshots captured with headless Chromium from the
  live program pages.

## Conventions and constraints
- Body Times New Roman 12 pt, code Courier New 9 pt. Liberation Serif / Mono
  substitute at PDF conversion time and are metric compatible.
- Text width is 16.2 cm. **Every** table `widths` list must sum to 16.2.
- No line, in code blocks or command blocks, may exceed 80 characters.
- Experiment headings use an em dash: `Exp. no: 07 \u2014 <title>`.
- Screenshots for the 15 experiments are always the placeholder text
  "Paste actual experiment screenshot here."; outputs are headed **Expected
  Output** and each experiment states the result was not produced by an actual
  run. Never fabricate a screenshot or a console transcript.
- The programme section may use authentic screenshots (`real_figure`), but the
  captions say they were captured before sign-in.
- Experiments must not be renamed, reordered or extended beyond the 15 supplied
  topics.

## Verified external facts
Checked against official sources, not memory:
- `https://ai.google.dev/gemini-api/docs` and
  `https://googleapis.github.io/python-genai/`: `genai.Client`,
  `client.models.generate_content`,
  `types.GenerateContentConfig(system_instruction=..., temperature=...,
  max_output_tokens=...)`, `client.chats.create`, `chat.send_message`,
  `AutomaticFunctionCallingConfig(maximum_remote_calls=...)`,
  `response.automatic_function_calling_history`. `gemini-2.0-flash` is listed.
- Learning path titles and activity counts, read from the public path pages:
  `/paths/118` "Beginner: Introduction to Generative AI" (4 activities),
  `/paths/1951` "Generative AI Leader Certification" (5 activities, GAIL),
  `/paths/183` "Advanced: Generative AI for Developers" (12 activities).
- All 19 programme links return HTTP 200.
- Known discrepancy recorded in `programme.py`: the program page reuses the
  playlist `PLHzNxijLRang` (titled "Beginner: Introduction to Generative AI")
  for both the Beginner Lab and the GAIL path. This is flagged to the student,
  not silently propagated.
- Learning path activity *names* are behind a sign-in wall, so they are not
  quoted anywhere.

## Environment (container resets wipe OS packages)
The workspace files survive a container reset, but `/usr/bin/python3`,
`/usr/bin/python3.13`, LibreOffice, poppler and every pip package are lost.
Run `./setup_env.sh` after a reset. It:
1. apt-installs `python3-torch`, `python3-torchvision`, `python3-docx`,
   `python3-numpy/scipy/matplotlib/pil/sklearn/pandas/pytest/sentencepiece/nltk`,
   `libreoffice-writer`, `poppler-utils`.
2. `uv pip install --python /usr/bin/python3.13 --target
   /usr/local/lib/python3.13/dist-packages transformers datasets peft
   sentence_transformers accelerate google-genai`.
3. Deletes the `numpy*`, `torch*`, `nvidia*`, `triton*`, `cuda*`,
   `cusparselt*` wheels that uv drops into that target, because they shadow the
   Debian builds and make `import torchvision` segfault (same crash signature
   as `libnuma`/`libucs`).

Notes:
- Debian Python is `/usr/bin/python3.13` (the path `/usr/bin/python3` is the
  same). `/usr/local/bin/python3` is a different, package-less interpreter.
- LibreOffice needs `LD_LIBRARY_PATH=/usr/lib/libreoffice/program` before
  `soffice --headless --convert-to pdf`, otherwise `libreglo.so` is not found.
- `CAP_SYS_NICE` is absent, so `ulimit -n 4096` fails in non-interactive shells.

## Figure provenance
`assemble.py` has a `REAL_FIGURES` map (exp -> (png, caption)). Only figures
genuinely produced by running a program in `runs/NN/` are inserted; every other
experiment keeps the "Paste actual experiment screenshot here." placeholder.
Never add an entry without a real `runs/NN/*.png`.

## QA loop used
1. `python3 assemble.py`
2. LibreOffice -> PDF
3. `pdftotext -layout`, then assert: each required section heading appears 15
   times, 142 `Step N:` headings, 15 `Exp. no:`, no blank pages, a `Page N`
   footer on every page except the cover, 15 figure placeholders.
4. `pdftotext -bbox`, then assert no word leaves the text frame. Footer page
   numbers are the only expected exception.
5. `pdfimages -list` to confirm the authentic screenshots really embedded.
