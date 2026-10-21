# ------------------- monitor.py (monitoring report) -------------------
import numpy as np, pandas as pd, matplotlib.pyplot as plt

rng = np.random.default_rng(1)
days = pd.date_range("2026-01-01", periods=7)
log = pd.DataFrame({
    "day": np.repeat(days, 200),
    "latency_ms": np.clip(rng.normal(850, 200, 1400), 200, None),
    "cost_usd": rng.uniform(0.0002, 0.0020, 1400),
    "error": rng.random(1400) < 0.015,
    "quality": np.clip(rng.normal(0.72, 0.10, 1400), 0, 1),
})
report = log.groupby("day").agg(
    requests=("latency_ms", "size"),
    p95_latency_ms=("latency_ms", lambda s: np.percentile(s, 95)),
    cost_usd=("cost_usd", "sum"),
    error_rate=("error", "mean"),
    mean_quality=("quality", "mean")).round(4)
print(report)

fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.plot(report.index, report["mean_quality"], marker="o",
         label="mean quality")
ax1.axhline(0.60, ls="--", color="red", label="alert threshold")
ax1.set_ylabel("mean quality score"); ax1.set_ylim(0, 1)
ax2 = ax1.twinx()
ax2.plot(report.index, report["p95_latency_ms"], marker="s",
         color="gray", label="p95 latency")
ax2.set_ylabel("p95 latency (ms)")
ax1.set_title("Monitoring report: quality and latency")
fig.legend(loc="upper right"); fig.autofmt_xdate()
plt.savefig("monitoring.png", dpi=150, bbox_inches="tight")
