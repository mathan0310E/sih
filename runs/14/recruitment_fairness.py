import numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

rng = np.random.default_rng(42)
n = 4000

# Synthetic applicants. 'group' is the protected attribute. Historical bias
# is injected so that group B is selected less often for the same ability.
group = rng.choice(["A", "B"], size=n, p=[0.5, 0.5])
ability = rng.normal(0, 1, n)                       # true, unobserved merit
years_exp = np.clip(rng.normal(4, 2, n), 0, None)
score = ability + 0.3 * years_exp
logit = 1.1 * score + np.where(group == "B", -0.6, 0.0)
hired = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)

df = pd.DataFrame({"group": group, "score": score,
                   "years_exp": years_exp, "hired": hired})
X = df[["score", "years_exp"]].values
y = df["hired"].values
Xtr, Xte, ytr, yte, gtr, gte = train_test_split(
    X, y, group, test_size=0.3, random_state=0)

clf = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
p = clf.predict_proba(Xte)[:, 1]

def metrics(labels, groups, pred):
    out = {"accuracy": accuracy_score(labels, pred)}
    for g in ("A", "B"):
        m = groups == g
        out["sel_" + g] = pred[m].mean()
        pos = labels[m] == 1
        out["tpr_" + g] = pred[m][pos].mean() if pos.any() else 0.0
    out["dpd"] = abs(out["sel_A"] - out["sel_B"])
    out["di"] = (min(out["sel_A"], out["sel_B"]) /
                  max(out["sel_A"], out["sel_B"]))
    out["eod"] = abs(out["tpr_A"] - out["tpr_B"])
    return out

before = metrics(yte, gte, (p >= 0.5).astype(int))
print("Before mitigation:")
for k, v in before.items():
    print(f"  {k:8s} {v:.3f}")

# ---- post-processing: equalise true-positive rate across groups ----
target = min(before["tpr_A"], before["tpr_B"])
thr = {}
for g in ("A", "B"):
    m = gte == g
    pos_probs = p[m][yte[m] == 1]
    thr[g] = (float(np.quantile(pos_probs, 1 - target))
              if target > 0 and pos_probs.size else 0.5)
print("group thresholds:", {k: round(v, 3) for k, v in thr.items()})

pred_adj = np.array([p[i] >= thr[gte[i]] for i in range(len(p))]).astype(int)
after = metrics(yte, gte, pred_adj)
print("\nAfter mitigation:")
for k, v in after.items():
    print(f"  {k:8s} {v:.3f}")

# ---- chart ----
keys = ["sel_A", "sel_B", "tpr_A", "tpr_B"]
x = np.arange(len(keys)); w = 0.35
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(x - w / 2, [before[k] for k in keys], w, label="before")
ax.bar(x + w / 2, [after[k] for k in keys], w, label="after")
ax.set_xticks(x); ax.set_xticklabels(keys); ax.legend()
ax.set_ylabel("rate")
ax.set_title("Fairness metrics before and after mitigation")
plt.savefig("fairness.png", dpi=150, bbox_inches="tight")
