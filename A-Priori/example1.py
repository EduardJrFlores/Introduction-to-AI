"""
A-Priori — Example 1: Supermarket Basket Analysis
Run:  python example1.py
Req:  pip install matplotlib
"""

import tkinter as tk
from tkinter import scrolledtext
import collections, itertools
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ── Theme ────────────────────────────────────────────────────
BG, PANEL, BORDER = "#0d1117", "#161b22", "#21262d"
GREEN, BLUE, ORANGE, MUTED, FG2 = "#10b981", "#3b82f6", "#f0883e", "#6b7280", "#c9d1d9"

# ── Data ────────────────────────────────────────────────────
TRANSACTIONS = [
    ['milk', 'bread', 'butter'],
    ['milk', 'bread'],
    ['milk', 'butter'],
    ['bread', 'butter'],
    ['milk', 'bread', 'butter', 'eggs'],
    ['bread', 'eggs'],
    ['milk', 'eggs'],
    ['bread', 'butter', 'eggs'],
    ['milk', 'bread', 'eggs'],
    ['butter', 'eggs'],
]
MIN_SUPPORT    = 0.30
MIN_CONFIDENCE = 0.60

# ── Algorithm ────────────────────────────────────────────────
def apriori(transactions, min_sup, min_conf):
    total  = len(transactions)
    txsets = [frozenset(t) for t in transactions]
    def sup(items): return sum(1 for t in txsets if items.issubset(t)) / total

    counts = collections.Counter(i for t in txsets for i in t)
    freq = {}; current = []
    for item, cnt in counts.items():
        s = cnt / total
        if s >= min_sup:
            fs = frozenset([item]); freq[fs] = s; current.append(fs)

    k = 2
    while current:
        cands = set()
        for i in range(len(current)):
            for j in range(i+1, len(current)):
                u = current[i] | current[j]
                if len(u) == k: cands.add(u)
        nxt = {}
        for c in cands:
            s = sup(c)
            if s >= min_sup: nxt[c] = s
        freq.update(nxt); current = list(nxt.keys()); k += 1

    rules = []
    for itemset, isup in freq.items():
        if len(itemset) < 2: continue
        for i in range(1, len(itemset)):
            for ant in map(frozenset, itertools.combinations(itemset, i)):
                cons = itemset - ant
                if not cons: continue
                conf = isup / freq.get(ant, sup(ant))
                if conf >= min_conf:
                    csup = freq.get(cons, sup(cons))
                    rules.append(dict(ant=set(ant), cons=set(cons),
                                      support=isup, confidence=conf,
                                      lift=conf/csup if csup else 0))
    return freq, sorted(rules, key=lambda r: -r['confidence'])

# ── Drawing ──────────────────────────────────────────────────
def draw_charts(ax1, ax2, freq, rules):
    ax1.clear(); ax2.clear()
    for ax in (ax1, ax2): ax.set_facecolor(BG)

    # support bar chart
    singles = {list(k)[0]: v for k, v in freq.items() if len(k)==1}
    items = list(singles.keys()); vals = [singles[i] for i in items]
    colors = [GREEN, BLUE, ORANGE, "#a78bfa"]
    bars = ax1.bar(items, vals, color=colors[:len(items)], width=0.5)
    ax1.axhline(MIN_SUPPORT, color=MUTED, ls="--", lw=1.2, label=f"min_sup={MIN_SUPPORT}")
    ax1.set_ylim(0, 1); ax1.set_facecolor(BG)
    ax1.set_title("Item Support", color=FG2, fontsize=9)
    ax1.tick_params(colors=FG2, labelsize=8)
    for sp in ax1.spines.values(): sp.set_edgecolor(BORDER)
    ax1.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=FG2, fontsize=8)
    for bar, val in zip(bars, vals):
        ax1.text(bar.get_x()+bar.get_width()/2, val+0.02, f"{val:.0%}",
                 ha="center", color=FG2, fontsize=8)

    # confidence & lift bar chart
    top = rules[:6]
    labels = [f"{list(r['ant'])[0]}→{list(r['cons'])[0]}" for r in top]
    confs  = [r['confidence'] for r in top]
    lifts  = [r['lift'] for r in top]
    x = range(len(labels))
    ax2.bar(x, confs, color=GREEN, alpha=0.85, width=0.4, label="Confidence")
    ax2.plot(x, lifts, color=ORANGE, marker="o", lw=2, label="Lift")
    ax2.set_xticks(list(x))
    ax2.set_xticklabels(labels, rotation=30, ha="right", color=FG2, fontsize=8)
    ax2.set_facecolor(BG); ax2.set_title("Top Rules: Confidence & Lift", color=FG2, fontsize=9)
    ax2.tick_params(colors=FG2, labelsize=8)
    for sp in ax2.spines.values(): sp.set_edgecolor(BORDER)
    ax2.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=FG2, fontsize=8)

# ── UI ───────────────────────────────────────────────────────
root = tk.Tk()
root.title("A-Priori — Example 1: Supermarket Basket Analysis")
root.geometry("980x700"); root.configure(bg=BG)

hf = tk.Frame(root, bg=BG); hf.pack(fill="x", padx=20, pady=(16,8))
tk.Label(hf, text="A-PRIORI ALGORITHM", fg=GREEN, bg=BG,
         font=("Courier New",16,"bold")).pack(side="left")
tk.Label(hf, text="  Example 1 · Supermarket Basket Analysis", fg=MUTED, bg=BG,
         font=("Courier New",11)).pack(side="left")

dc = tk.Frame(root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
dc.pack(fill="x", padx=20, pady=(0,8))
tk.Label(dc, text="ALGORITHM", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,2))
tk.Label(dc,
    text=(f"Mines frequent itemsets from {len(TRANSACTIONS)} shopping transactions.\n"
          f"Min Support = {MIN_SUPPORT:.0%}  |  Min Confidence = {MIN_CONFIDENCE:.0%}\n"
          "Apriori property: infrequent itemsets cannot have frequent supersets → prune candidates early."),
    fg=FG2, bg=PANEL, font=("Courier New",10), justify="left"
).pack(anchor="w", padx=12, pady=(0,10))

# transactions
tf = tk.Frame(root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
tf.pack(fill="x", padx=20, pady=(0,8))
tk.Label(tf, text="TRANSACTION DATABASE", fg=ORANGE, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(8,2))
tr = tk.Frame(tf, bg=PANEL); tr.pack(fill="x", padx=12, pady=(0,8))
for i, t in enumerate(TRANSACTIONS):
    tk.Label(tr, text=f"T{i+1:02d}: {', '.join(t)}", fg=FG2, bg=PANEL,
             font=("Courier New",9)).grid(row=i//2, column=i%2, sticky="w", padx=10, pady=1)

cf = tk.Frame(root, bg=BG); cf.pack(fill="both", expand=True, padx=20, pady=(0,16))
left  = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
right = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
left.pack(side="left", fill="both", expand=True, padx=(0,8))
right.pack(side="left", fill="both", expand=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 3.6), facecolor=BG)
fig.tight_layout(pad=2)
canvas = FigureCanvasTkAgg(fig, master=left)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

tk.Button(left, text="▶  Run Apriori", command=lambda: run(),
          bg="#0d3d2e", fg=GREEN, activebackground=GREEN, activeforeground="white",
          font=("Courier New",11,"bold"), relief="flat", bd=0,
          padx=18, pady=8, cursor="hand2",
          highlightbackground=GREEN, highlightthickness=1).pack(pady=8)

tk.Label(right, text="FREQUENT ITEMSETS & RULES", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,4))
out = scrolledtext.ScrolledText(right, bg="#0d1117", fg=FG2,
      font=("Courier New",10), relief="flat", bd=0, wrap="word", height=18)
out.pack(fill="both", expand=True, padx=8, pady=(0,8))
out.tag_config("green", foreground=GREEN)
out.tag_config("head",  foreground=GREEN, font=("Courier New",10,"bold"))
out.insert("end", "Press  ▶ Run Apriori  to mine the transactions.\n")

def run():
    freq, rules = apriori(TRANSACTIONS, MIN_SUPPORT, MIN_CONFIDENCE)
    draw_charts(ax1, ax2, freq, rules); fig.tight_layout(pad=2); canvas.draw()
    out.delete("1.0", "end")
    out.insert("end", f"✅  MINING COMPLETE\n\n", "green")
    out.insert("end", f"Frequent itemsets : {len(freq)}\n")
    out.insert("end", f"Association rules : {len(rules)}\n\n")
    out.insert("end", "FREQUENT ITEMSETS\n", "head")
    out.insert("end", "─"*38 + "\n")
    for fs, sup in sorted(freq.items(), key=lambda x: -x[1]):
        out.insert("end", f"  {str(set(fs)):<28}  sup={sup:.2f}\n")
    out.insert("end", f"\nASSOCIATION RULES\n", "head")
    out.insert("end", "─"*38 + "\n")
    for r in rules[:8]:
        out.insert("end",
            f"  {r['ant']} → {r['cons']}\n"
            f"    support={r['support']:.2f}  confidence={r['confidence']:.2f}  lift={r['lift']:.2f}\n\n")

root.mainloop()