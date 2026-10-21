import numpy as np, torch
from datasets import load_dataset
from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                          TrainingArguments, Trainer)
from peft import LoraConfig, get_peft_model

# ---------------- data ----------------
raw = load_dataset("nyu-mll/glue", "sst2")
tok = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def enc(batch):
    return tok(batch["sentence"], truncation=True, padding="max_length",
               max_length=128)

# Keep the raw split: renaming the label column replaces it.
ds = raw.map(enc, batched=True).rename_column("label", "labels")
ds.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

train_ds = ds["train"].select(range(2000))    # small subset for the lab
eval_ds = ds["validation"].select(range(500))

# ---------------- zero-shot baseline ----------------
from transformers import pipeline
clf = pipeline("sentiment-analysis",
               model="distilbert-base-uncased-finetuned-sst-2-english")
val = raw["validation"].select(range(500))
sentences = val["sentence"]
truth = np.array(val["label"])
preds = np.array([1 if clf(t)[0]["label"] == "POSITIVE" else 0
                  for t in sentences])
print("zero-shot accuracy:", round(float((preds == truth).mean()), 4))

# ---------------- LoRA fine-tuning ----------------
base = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2)

lora = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.1, bias="none",
                  task_type="SEQ_CLS",
                  target_modules=["q_lin", "v_lin"])
model = get_peft_model(base, lora)
model.print_trainable_parameters()

def score(p):
    return {"accuracy": float((p.predictions.argmax(-1) == p.label_ids).mean())}

args = TrainingArguments(output_dir="./lora_sst2", num_train_epochs=2,
                         per_device_train_batch_size=16,
                         per_device_eval_batch_size=32,
                         learning_rate=5e-4, logging_steps=50,
                         eval_strategy="epoch", report_to=[])
trainer = Trainer(model=model, args=args, train_dataset=train_ds,
                  eval_dataset=eval_ds, compute_metrics=score)
trainer.train()
print("fine-tuned metrics:", trainer.evaluate())

model.save_pretrained("./lora_sst2/adapter")   # adapter only, not the base
