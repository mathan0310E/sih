import torch, matplotlib.pyplot as plt
from transformers import AutoTokenizer, AutoModelForCausalLM

torch.manual_seed(0)
name = "gpt2"
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForCausalLM.from_pretrained(name,
                                             output_attentions=True)
model.eval()
print("parameters:", sum(p.numel() for p in model.parameters()) / 1e6, "M")

prompt = "Artificial intelligence will change education because"
ids = tok(prompt, return_tensors="pt")["input_ids"]

# ---- tokenisation ----
for i in ids[0].tolist():
    print(i, repr(tok.decode([i])))

# ---- generation with different sampling settings ----
for temp, top_p in [(0.7, 0.9), (1.0, 0.95)]:
    out = model.generate(ids, max_new_tokens=40, do_sample=True,
                         temperature=temp, top_p=top_p,
                         pad_token_id=tok.eos_token_id)
    print("=" * 70)
    print(f"temperature={temp} top_p={top_p}")
    print(tok.decode(out[0], skip_special_tokens=True))

# ---- attention heat map ----
with torch.no_grad():
    out = model(ids, output_attentions=True)
attn = out.attentions[0][0, 0].cpu()   # layer 0, head 0
fig, ax = plt.subplots(figsize=(5, 5))
im = ax.imshow(attn, cmap="viridis")
ax.set_xlabel("key position"); ax.set_ylabel("query position")
ax.set_title("Layer 0, head 0 attention")
fig.colorbar(im, ax=ax)
plt.savefig("attention.png", dpi=150, bbox_inches="tight")
