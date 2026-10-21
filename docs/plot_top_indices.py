"""Draws the AAindex indices with the highest stability-selection scores (the scores saved in test.py).

Run from the repository root with Python 3:
    uv run --no-project --with matplotlib python docs/plot_top_indices.py
"""
import ast
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

TOP = 20
indices = open("total_indices_list.txt").read().split()
scores = ast.literal_eval(re.search(r"scores = (\[.*?\])", open("test.py").read(), re.S).group(1))
assert len(indices) == len(scores)
descriptions = {}
for line in open("list_of_indices.txt"):
    m = re.match(r"([A-Z]{4}\d{6}) (.+)", line.strip())
    if m:
        descriptions[m.group(1)] = m.group(2)
top = sorted(zip(indices, scores), key=lambda x: x[1], reverse=True)[:TOP][::-1]
fig, ax = plt.subplots(figsize=(11, 7))
ax.barh([f"{a}  {descriptions.get(a, '')[:70]}" for a, _ in top], [s for _, s in top], color="#4c8bb5")
ax.set_xlabel("Selection score (fraction of resamplings that selected the index)")
ax.set_title(f"The {TOP} AAindex indices with the highest stability-selection scores")
ax.tick_params(axis="y", labelsize=8)
fig.tight_layout()
fig.savefig("docs/top_indices.png", dpi=110)
print("wrote docs/top_indices.png")
