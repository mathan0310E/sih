import numpy as np, pandas as pd

rng = np.random.default_rng(0)
n = 1000

# Synthetic data: 'score' is the model output, 'group' is a protected
# attribute. The label is created with a deliberate disparity so that the
# fairness metric can be demonstrated.
group = rng.choice(["A", "B"], size=n, p=[0.5, 0.5])
score = rng.normal(0.60, 0.15, n) + np.where(group == "A", 0.05, -0.05)
flag = (score >= 0.60).astype(int)      # positive decision = flagged

df = pd.DataFrame({"group": group, "score": score, "flag": flag})

rates = df.groupby("group")["flag"].mean()
print("Selection rate by group:")
print(rates.round(3))

dpd = rates.max() - rates.min()
di = rates.min() / rates.max()
print(f"Demographic parity difference = {dpd:.3f}")
print(f"Disparate impact ratio        = {di:.3f}")
print("Four-fifths rule:", "PASS" if di >= 0.8 else "REVIEW REQUIRED")

# Mitigation: raise the threshold for the advantaged group so that both
# groups have a comparable selection rate (a simple threshold adjustment).
thr = {"A": np.quantile(score[group == "A"], 1 - rates.min()),
       "B": np.quantile(score[group == "B"], 1 - rates.min())}
adj = np.array([score[i] >= thr[group[i]] for i in range(n)])
df["flag_adj"] = adj
print("\nAfter threshold adjustment:")
print(df.groupby("group")["flag_adj"].mean().round(3))
