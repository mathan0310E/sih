# Naan Mudhalvan Generative AI Laboratory Record Manual

## Goal
Produce a traditional Indian engineering college practical record manual for
**SKP Engineering College, Tiruvannamalai - 606 611**, Department of AI & DS,
course "Naan Mudhalvan - Generative Artificial Intelligence", as an editable
`.docx` plus a print-ready `.pdf` (A4).

## Layout reference
`NM LAB MANUAL CS.pdf` (98 pages, Letter, Word 2019) is the formatting
reference. It was **not** attached to the conversation; it was obtained from
`https://github.com/mathan0310E/sih` (branch `main`, repo root). Its front
matter is: cover (college name / address / DEPARTMENT OF / programme /
course code / REGULATION / dot-leader Name, Register Number, Department,
Year-Semester, Subject) then a CERTIFICATE page with the same dot-leader
fields plus "Certified that this is the bonafide record ..." and
Staff-In-Charge / Head of the Department / Internal Examiner / External
Examiner signature blocks, then an INDEX table, then `Exp. no: NN  <title>` +
`Date:` on every experiment page, ending with a `CONCLUSION` page.

## Build
```
pip install python-docx
python3 assemble.py                     # -> output/NM_LAB_MANUAL_GenAI.docx
export LD_LIBRARY_PATH=/usr/lib/libreoffice/program:$LD_LIBRARY_PATH
soffice --headless --convert-to pdf --outdir output output/NM_LAB_MANUAL_GenAI.docx
```
LibreOffice **requires** `LD_LIBRARY_PATH=/usr/lib/libreoffice/program` on this
image, otherwise `libreglo.so` is not found.

## Source files
- `build_manual.py` - docx primitives (A4 page border, footer PAGE field,
  fixed-layout bordered tables, shaded monospace code blocks, screenshot boxes).
- `content.py` - college details, experiments 1-10, appendices, `EXPERIMENTS`.
- `content2.py` - experiments 11-15 (`E11_15`).
- `assemble.py` - page assembly (cover, certificate, index, experiments,
  appendices). Single Word section + page breaks so page numbers are continuous.

## Conventions and constraints
- Body font Times New Roman 12 pt; code Courier New 9 pt. Liberation Serif /
  Liberation Mono substitute at PDF conversion time (metric compatible).
- Text width is 16.2 cm; **every** table `widths` list must sum to 16.2.
- Longest code line is 80 characters so code blocks never wrap.
- Screenshots are always the placeholder "Paste actual experiment screenshot
  here."; outputs are labelled "Expected Output" and every experiment states
  that results were not produced by an actual run.
- Experiment list/order comes from the supplied syllabus (two attached images,
  15 topics) and must not be renamed, reordered or extended.
- API facts were checked against https://ai.google.dev/gemini-api/docs and
  https://googleapis.github.io/python-genai/ (`client.chats.create`,
  `chat.send_message`, `automatic_function_calling_history`,
  `types.AutomaticFunctionCallingConfig(maximum_remote_calls=...)`,
  `types.GenerateContentConfig(system_instruction=..., temperature=...)`).

## QA loop used
1. `python3 assemble.py`
2. LibreOffice -> PDF
3. `pdftotext -layout` then assert: 15 x each section heading, no blank pages,
   `Page N` footer on every page but the cover, 15 figure captions.
4. `pdftotext -bbox` then assert no word leaves the text frame (footers are the
   only exception, by design).
