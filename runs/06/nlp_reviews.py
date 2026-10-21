from transformers import (pipeline, AutoTokenizer,
                          AutoModelForSeq2SeqLM)

reviews = [
    "The delivery was fast and the product works exactly as described.",
    "The battery drains within an hour, very disappointed.",
    "Excellent build quality for this price range.",
    "Customer support never replied to my email.",
    "Oh great, it broke on the second day. Wonderful quality!",  # sarcasm
    "Easy to install and the instructions were clear.",
    "The colour is different from the website photo.",
    "Good value for money, I would buy it again.",
]

# ---- sentiment classification ----
clf = pipeline("sentiment-analysis",
               model="distilbert-base-uncased-finetuned-sst-2-english")
results = clf(reviews)
for r, out in zip(reviews, results):
    print(f"{out['label']:8s} {out['score']:.3f}  {r[:60]}")

# ---- abstractive summarisation ----
summ_tok = AutoTokenizer.from_pretrained("t5-small")
summ_model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
document = "summarize: " + " ".join(reviews)
enc = summ_tok(document, return_tensors="pt", truncation=True,
                max_length=512)
ids = summ_model.generate(**enc, max_new_tokens=48,
                          min_new_tokens=12, num_beams=4)
print("\nSummary:")
print(summ_tok.decode(ids[0], skip_special_tokens=True))
