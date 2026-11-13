"""Draw figures/title_coding.png from review/query_analysis.csv.
Usage: python code/figures/title_coding_chart.py review/query_analysis.csv figures/title_coding.png"""
import csv, sys, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
order = ["MED-v1","MED-v2","MED-v5","MED-v3","MED-v4","TECH-v1","TECH-v2","TECH-v3","TECH-v4","TECH-v5","TECH-v6","TECH-v7"]
rows = sorted(rows, key=lambda r: order.index(r["id"]))
labels = [r["id"] for r in rows]; y = range(len(rows))
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=200)
left = [0]*len(rows)
styles = [("P", "P - title clearly on topic", "#222222", ""), ("I", "I - maybe / indirect", "#9a9a9a", ""), ("N", "N - off topic", "white", "////")]
for key, name, col, hatch in styles:
    vals = [int(r[key]) for r in rows]
    ax.barh(y, vals, left=left, color=col, edgecolor="white" if col != "white" else "#555555", linewidth=1, hatch=hatch, height=0.62, label=name)
    left = [a+b for a, b in zip(left, vals)]
for i, r in enumerate(rows):
    ax.text(31, i, f'{int(r["total_hits"]):,} hits', va="center", fontsize=7.5, color="#444444")
ax.set_yticks(list(y)); ax.set_yticklabels(labels); ax.invert_yaxis()
ax.set_xlim(0, 40); ax.set_xticks([0, 10, 20, 30]); ax.set_xlabel("Records exported (first 30 per query)")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.axhline(4.5, color="#888888", lw=0.6, ls=":")
ax.legend(loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=3, frameon=False, fontsize=7.5)
fig.tight_layout(); fig.savefig(sys.argv[2])
