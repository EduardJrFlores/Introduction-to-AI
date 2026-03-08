"""
Genetic Algorithm — Example 2: Travelling Salesman Problem (TSP)
Run:  python example2.py
Req:  pip install matplotlib
"""

import tkinter as tk
from tkinter import scrolledtext
import random, math
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ── Theme ────────────────────────────────────────────────────
BG, PANEL, BORDER = "#0d1117", "#161b22", "#21262d"
GREEN, BLUE, ORANGE, MUTED, FG2 = "#10b981", "#3b82f6", "#f0883e", "#6b7280", "#c9d1d9"

# ── Parameters ───────────────────────────────────────────────
POP_SIZE = 80
GENS     = 400
MUT_RATE = 0.03
N_CITIES = 10

# ── Fixed cities (seeded for reproducibility) ────────────────
rng = random.Random(42)
CITIES = [(rng.uniform(5, 95), rng.uniform(5, 95)) for _ in range(N_CITIES)]
NAMES  = [f"C{i}" for i in range(N_CITIES)]

# ── Algorithm ────────────────────────────────────────────────
def dist(a, b):
    return math.hypot(CITIES[a][0]-CITIES[b][0], CITIES[a][1]-CITIES[b][1])

def route_len(route):
    n = len(route)
    return sum(dist(route[i], route[(i+1)%n]) for i in range(n))

def order_crossover(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [-1] * n
    child[a:b] = p1[a:b]
    fill = [x for x in p2 if x not in child]
    fi = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = fill[fi]; fi += 1
    return child

def swap_mutate(route):
    r = route[:]
    if random.random() < MUT_RATE:
        i, j = random.sample(range(len(r)), 2)
        r[i], r[j] = r[j], r[i]
    return r

def ga_tsp():
    population = [random.sample(range(N_CITIES), N_CITIES) for _ in range(POP_SIZE)]
    history = []; best_route = None; best_dist = float('inf')
    for _ in range(GENS):
        population.sort(key=route_len)
        d = route_len(population[0])
        if d < best_dist: best_dist = d; best_route = population[0][:]
        history.append(best_dist)
        elite_n = max(2, POP_SIZE // 10)
        new_pop = population[:elite_n]
        pool = population[:20]
        while len(new_pop) < POP_SIZE:
            p1 = random.choice(pool); p2 = random.choice(pool)
            new_pop.append(swap_mutate(order_crossover(p1, p2)))
        population = new_pop[:POP_SIZE]
    return best_route, best_dist, history

# ── Drawing ──────────────────────────────────────────────────
def draw_route(ax, route, title, color=GREEN):
    ax.clear(); ax.set_facecolor(BG)
    if route:
        n = len(route)
        for i in range(n):
            a, b = route[i], route[(i+1)%n]
            x1,y1 = CITIES[a]; x2,y2 = CITIES[b]
            ax.annotate("", xy=(x2,y2), xytext=(x1,y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5))
    for i, (x, y) in enumerate(CITIES):
        ax.scatter(x, y, s=180, color=ORANGE, zorder=5,
                   edgecolors="#fbbf24", linewidths=1.5)
        ax.text(x+1.5, y+1.5, NAMES[i], color=FG2, fontsize=9, fontweight="bold")
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    d = f"  (dist={route_len(route):.1f})" if route else ""
    ax.set_title(f"{title}{d}", color=FG2, fontsize=9)

def draw_convergence(ax, history):
    ax.clear(); ax.set_facecolor(BG)
    if history:
        ax.plot(history, color=ORANGE, lw=1.8)
        ax.fill_between(range(len(history)), history, alpha=0.15, color=ORANGE)
    ax.set_title("Best Distance vs Generation", color=FG2, fontsize=9)
    ax.set_xlabel("Generation", color=MUTED, fontsize=8)
    ax.set_ylabel("Route Distance", color=MUTED, fontsize=8)
    ax.tick_params(colors=FG2, labelsize=7)
    for sp in ax.spines.values(): sp.set_edgecolor(BORDER)

# ── UI ───────────────────────────────────────────────────────
root = tk.Tk()
root.title("Genetic Algorithm — Example 2: Travelling Salesman Problem")
root.geometry("1060x700"); root.configure(bg=BG)

hf = tk.Frame(root, bg=BG); hf.pack(fill="x", padx=20, pady=(16,8))
tk.Label(hf, text="GENETIC ALGORITHM", fg=GREEN, bg=BG,
         font=("Courier New",16,"bold")).pack(side="left")
tk.Label(hf, text="  Example 2 · Travelling Salesman Problem (TSP)", fg=MUTED, bg=BG,
         font=("Courier New",11)).pack(side="left")

dc = tk.Frame(root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
dc.pack(fill="x", padx=20, pady=(0,10))
tk.Label(dc, text="ALGORITHM", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,2))
tk.Label(dc,
    text=(f"Find the shortest route visiting all {N_CITIES} cities exactly once and returning to start.\n"
          f"Population: {POP_SIZE}   Generations: {GENS}   Mutation: swap two cities  ({MUT_RATE:.0%} rate)\n"
          "Crossover: Order Crossover (OX) — preserves relative order of cities from each parent."),
    fg=FG2, bg=PANEL, font=("Courier New",10), justify="left"
).pack(anchor="w", padx=12, pady=(0,10))

cf = tk.Frame(root, bg=BG); cf.pack(fill="both", expand=True, padx=20, pady=(0,16))
left  = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
right = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
left.pack(side="left", fill="both", expand=True, padx=(0,8))
right.pack(side="left", fill="both", expand=True)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(9, 3.8), facecolor=BG)
fig.tight_layout(pad=2)
canvas = FigureCanvasTkAgg(fig, master=left)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)

init_route = list(range(N_CITIES)); random.shuffle(init_route)
draw_route(ax1, init_route, "Random Route", MUTED)
draw_route(ax2, None, "GA Best Route")
draw_convergence(ax3, [])
canvas.draw()

tk.Button(left, text="▶  Run Genetic Algorithm (TSP)", command=lambda: run(),
          bg="#0d3d2e", fg=GREEN, activebackground=GREEN, activeforeground="white",
          font=("Courier New",11,"bold"), relief="flat", bd=0,
          padx=18, pady=8, cursor="hand2",
          highlightbackground=GREEN, highlightthickness=1).pack(pady=8)

tk.Label(right, text="EVOLUTION LOG", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,4))
out = scrolledtext.ScrolledText(right, bg="#0d1117", fg=FG2,
      font=("Courier New",10), relief="flat", bd=0, wrap="word", height=24)
out.pack(fill="both", expand=True, padx=8, pady=(0,8))
out.tag_config("green", foreground=GREEN)
out.tag_config("head",  foreground=GREEN, font=("Courier New",10,"bold"))
out.insert("end", "Press  ▶ Run  to evolve routes.\n\n")
out.insert("end", f"Cities : {N_CITIES}\nCoords :\n")
for i, (x, y) in enumerate(CITIES):
    out.insert("end", f"  {NAMES[i]}: ({x:.1f}, {y:.1f})\n")
out.insert("end", f"\nRandom route dist: {route_len(init_route):.2f}\n")

def run():
    best_route, best_dist, history = ga_tsp()
    draw_route(ax1, init_route, "Random Route", MUTED)
    draw_route(ax2, best_route, "GA Best Route")
    draw_convergence(ax3, history)
    fig.tight_layout(pad=2); canvas.draw()
    out.delete("1.0", "end")
    out.insert("end", "✅  TSP SOLVED (near-optimal)\n\n", "green")
    out.insert("end", f"Cities         : {N_CITIES}\n")
    out.insert("end", f"Best distance  : {best_dist:.2f}\n")
    out.insert("end", f"Random route   : {route_len(init_route):.2f}\n")
    imp = route_len(init_route) - best_dist
    out.insert("end", f"Improvement    : {imp:.2f}  ({imp/route_len(init_route)*100:.1f}% shorter)\n\n")
    out.insert("end", "BEST ROUTE\n", "head")
    out.insert("end", "─"*36 + "\n")
    out.insert("end", "  " + " → ".join(NAMES[c] for c in best_route)
               + f" → {NAMES[best_route[0]]}\n\n")
    out.insert("end", "EDGE DISTANCES\n", "head")
    out.insert("end", "─"*36 + "\n")
    n = len(best_route)
    for i in range(n):
        a, b = best_route[i], best_route[(i+1)%n]
        out.insert("end", f"  {NAMES[a]} → {NAMES[b]} : {dist(a,b):.2f}\n")
    out.insert("end", f"\nCONVERGENCE\n", "head")
    out.insert("end", "─"*36 + "\n")
    for cp in [0, GENS//4, GENS//2, 3*GENS//4, GENS-1]:
        out.insert("end", f"  Gen {cp:4d} : {history[cp]:.2f}\n")

root.mainloop()