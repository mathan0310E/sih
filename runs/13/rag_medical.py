import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import (AutoTokenizer, AutoModelForSeq2SeqLM,
                          VisionEncoderDecoderModel, ViTImageProcessor)
from PIL import Image

DOCS = [
    "Hypertension is a sustained elevation of arterial blood pressure. "
    "It is commonly defined as a systolic pressure at or above 140 mmHg "
    "or a diastolic pressure at or above 90 mmHg.",
    "Type 2 diabetes is a metabolic disorder characterised by insulin "
    "resistance and elevated blood glucose. It is managed with diet, "
    "exercise, oral medication and, in some cases, insulin.",
    "Anaemia is a reduction in the haemoglobin concentration or the red "
    "blood cell count, and it commonly results from iron deficiency.",
    "Asthma is a chronic inflammatory disease of the airways that causes "
    "reversible airflow obstruction and wheezing.",
]

embedder = SentenceTransformer("all-MiniLM-L6-v2")
dvec = embedder.encode(DOCS, normalize_embeddings=True)

def retrieve(question, k=2):
    q = embedder.encode([question], normalize_embeddings=True)[0]
    order = np.argsort(-(dvec @ q))[:k]
    return [DOCS[i] for i in order]

QUESTION = "What blood pressure values are used to define hypertension?"
context = "\n".join(retrieve(QUESTION))
print("Retrieved context:\n", context)

# ---- grounded answer with a local seq2seq model ----
gen_tok = AutoTokenizer.from_pretrained("google/flan-t5-base")
gen_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
prompt = ("Answer the question using only the context below. If the "
          "answer is not in the context, reply exactly: Not in context.\n\n"
          f"Context:\n{context}\n\nQuestion: {QUESTION}\nAnswer:")
enc = gen_tok(prompt, return_tensors="pt", truncation=True,
              max_length=512)
gen_ids = gen_model.generate(**enc, max_new_tokens=64)
print("Answer:", gen_tok.decode(gen_ids[0], skip_special_tokens=True))

# ---- image captioning ----
cap_proc = ViTImageProcessor.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning")
cap_model = VisionEncoderDecoderModel.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning")
cap_tok = AutoTokenizer.from_pretrained(
    "nlpconnect/vit-gpt2-image-captioning")
image = Image.open("sample_medical_image.jpg").convert("RGB")
pixels = cap_proc(images=image, return_tensors="pt").pixel_values
cap_ids = cap_model.generate(pixels, max_new_tokens=32)
print("Caption:", cap_tok.decode(cap_ids[0], skip_special_tokens=True))
