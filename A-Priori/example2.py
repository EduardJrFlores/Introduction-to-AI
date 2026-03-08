"""
A-Priori — Example 2: Movie Co-watching Recommendation
Run:  python example2.py
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
    ['Inception', 'Interstellar', 'Tenet'],
    ['Inception', 'Interstellar'],
    ['The Matrix', 'John Wick'],
    ['Inception', 'The Matrix', 'Interstellar'],
    ['John Wick', 'Mad Max', 'The Matrix'],
    ['Inception', 'Tenet'],
    ['Interstellar', 'Tenet', 'Inception'],
    ['John Wick', 'The Matrix'],
    ['Mad Max', 'John Wick', 'Inception'],
    ['Interstellar', 'Inception', 'Mad Max'],
]
MIN_SUPPORT    = 0.25
MIN_CONFIDENCE = 0.50

MOVIE_COLORS = {
    'Inception': "#3b82f6", 'Interstellar': "#10b981", 'Tenet': "#a78bfa",
    'The Matrix': "#f0883e", 'John Wick': "#f87171", 'Mad Max': "#fbbf24",
}

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
    return freq, sorted(rules, key=lambda r: -r['lift'])

# ── Drawing ──────────────────────────────────────────────────
def draw_charts(ax1, ax2, freq, rules):
    ax1.clear(); ax2.clear()
    for ax in (ax1, ax2): ax.set_facecolor(BG)

    # horizontal support bar
    singles = {list(k)[0]: v for k, v in freq.items() if len(k)==1}
    movies  = list(singles.keys())
    vals    = [singles[m] for m in movies]
    short   = [m[:11] for m in movies]
    colors  = [MOVIE_COLORS.get(m, MUTED) for m in movies]
    bars = ax1.barh(short, vals, color=colors, height=0.5)
    ax1.axvline(MIN_SUPPORT, color=MUTED, ls="--", lw=1.2, label=f"min_sup={MIN_SUPPORT}")
    ax1.set_xlim(0, 1); ax1.set_facecolor(BG)
    ax1.set_title("Movie Support", color=FG2, fontsize=9)
    ax1.tick_params(colors=FG2, labelsize=8)
    for sp in ax1.spines.values(): sp.set_edgecolor(BORDER)
    ax1.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=FG2, fontsize=8)
    for bar, val in zip(bars, vals):
        ax1.text(val+0.01, bar.get_y()+bar.get_height()/2,
                 f"{val:.0%}", va="center", color=FG2, fontsize=8)

    # confidence vs lift scatter
    top = rules[:8]
    for r in top:
        a = list(r['ant'])[0]; c_node = list(r['cons'])[0]
        ax2.scatter(r['confidence'], r['lift'],
                    s=r['support']*600,
                    color=MOVIE_COLORS.get(a, GREEN),
                    alpha=0.85, zorder=3, edgecolors="white", linewidths=0.5)
        ax2.text(r['confidence']+0.01, r['lift']+0.02,
                 f"{a[:6]}→{c_node[:6]}", color=FG2, fontsize=7)
    ax2.axvline(MIN_CONFIDENCE, color=MUTED, ls="--", lw=1, label=f"min_conf={MIN_CONFIDENCE}")
    ax2.axhline(1.0, color=BLUE, ls=":", lw=1, label="lift=1 (chance)")
    ax2.set_facecolor(BG)
    ax2.set_xlabel("Confidence", color=MUTED, fontsize=8)
    ax2.set_ylabel("Lift", color=MUTED, fontsize=8)
    ax2.set_title("Rules: Confidence vs Lift\n(bubble = support)", color=FG2, fontsize=9)
    ax2.tick_params(colors=FG2, labelsize=8)
    for sp in ax2.spines.values(): sp.set_edgecolor(BORDER)
    ax2.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=FG2, fontsize=7)

# ── UI ───────────────────────────────────────────────────────
root = tk.Tk()
root.title("A-Priori — Example 2: Movie Recommendation")
root.geometry("980x700"); root.configure(bg=BG)

hf = tk.Frame(root, bg=BG); hf.pack(fill="x", padx=20, pady=(16,8))
tk.Label(hf, text="A-PRIORI ALGORITHM", fg=GREEN, bg=BG,
         font=("Courier New",16,"bold")).pack(side="left")
tk.Label(hf, text="  Example 2 · Movie Co-watching Recommendation", fg=MUTED, bg=BG,
         font=("Courier New",11)).pack(side="left")

dc = tk.Frame(root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
dc.pack(fill="x", padx=20, pady=(0,8))
tk.Label(dc, text="ALGORITHM", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,2))
tk.Label(dc,
    text=(f"Discovers movies frequently watched together across {len(TRANSACTIONS)} user sessions.\n"
          f"Min Support = {MIN_SUPPORT:.0%}  |  Min Confidence = {MIN_CONFIDENCE:.0%}\n"
          "High Lift (>1) = movies watched together more than by chance → strong recommendation signal."),
    fg=FG2, bg=PANEL, font=("Courier New",10), justify="left"
).pack(anchor="w", padx=12, pady=(0,10))

tf = tk.Frame(root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
tf.pack(fill="x", padx=20, pady=(0,8))
tk.Label(tf, text="VIEWING SESSIONS", fg=ORANGE, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(8,2))
tr = tk.Frame(tf, bg=PANEL); tr.pack(fill="x", padx=12, pady=(0,8))
for i, t in enumerate(TRANSACTIONS):
    tk.Label(tr, text=f"U{i+1:02d}: {', '.join(t)}", fg=FG2, bg=PANEL,
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

tk.Label(right, text="RULES RANKED BY LIFT", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,4))
out = scrolledtext.ScrolledText(right, bg="#0d1117", fg=FG2,
      font=("Courier New",10), relief="flat", bd=0, wrap="word", height=18)
out.pack(fill="both", expand=True, padx=8, pady=(0,8))
out.tag_config("green", foreground=GREEN)
out.tag_config("head",  foreground=GREEN, font=("Courier New",10,"bold"))
out.insert("end", "Press  ▶ Run Apriori  to find movie associations.\n")

def run():
    freq, rules = apriori(TRANSACTIONS, MIN_SUPPORT, MIN_CONFIDENCE)
    draw_charts(ax1, ax2, freq, rules); fig.tight_layout(pad=2); canvas.draw()
    out.delete("1.0", "end")
    out.insert("end", f"✅  MINING COMPLETE\n\n", "green")
    out.insert("end", f"Frequent itemsets : {len(freq)}\n")
    out.insert("end", f"Association rules : {len(rules)}\n\n")
    out.insert("end", "TOP RULES BY LIFT\n", "head")
    out.insert("end", "─"*42 + "\n")
    for r in rules[:8]:
        out.insert("end",
            f"  {r['ant']} → {r['cons']}\n"
            f"    support={r['support']:.2f}  confidence={r['confidence']:.2f}  lift={r['lift']:.2f}\n\n")
    out.insert("end", "INTERPRETATION\n", "head")
    out.insert("end", "─"*42 + "\n")
    for r in rules[:3]:
        a = list(r['ant'])[0]; c = list(r['cons'])[0]
        out.insert("end",
            f"  Viewers who watch '{a}'\n"
            f"  are {r['lift']:.1f}× more likely to also watch '{c}'.\n\n")

root.mainloop()