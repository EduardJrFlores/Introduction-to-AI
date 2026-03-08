"""
Genetic Algorithm — Example 1: Function Optimisation
Maximise  f(x, y) = -(x² + y²) + 10   on [-5, 5]²
Run:  python example1.py
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
POP_SIZE = 60
GENS     = 150
MUT_RATE = 0.05
LO, HI   = -5.0, 5.0

# ── Algorithm ────────────────────────────────────────────────
def fitness(ind):
    return -(ind[0]**2 + ind[1]**2) + 10

def ga_run():
    ri  = lambda: [random.uniform(LO, HI), random.uniform(LO, HI)]
    cx  = lambda p1, p2: ([p1[0], p2[1]], [p2[0], p1[1]])
    mt  = lambda ind: [
        g + random.gauss(0, (HI-LO)*0.1) if random.random() < MUT_RATE else g
        for g in ind
    ]
    population = [ri() for _ in range(POP_SIZE)]
    history = []; best_ind = None; best_sc = -float('inf')

    for _ in range(GENS):
        scored = sorted(population, key=fitness, reverse=True)
        sc = fitness(scored[0])
        if sc > best_sc: best_sc, best_ind = sc, scored[0][:]
        history.append(best_sc)
        elite_n = max(2, POP_SIZE // 10)
        new_pop = scored[:elite_n]
        while len(new_pop) < POP_SIZE:
            p1 = scored[random.randint(0, 14)]
            p2 = scored[random.randint(0, 14)]
            c1, c2 = cx(p1, p2)
            new_pop += [mt(c1), mt(c2)]
        population = new_pop[:POP_SIZE]

    return best_ind, best_sc, history, population

# ── Drawing ──────────────────────────────────────────────────
def draw_initial(ax1, ax2):
    ax1.clear(); ax2.clear()
    for ax in (ax1, ax2): ax.set_facecolor(BG)
    xs = [random.uniform(LO, HI) for _ in range(500)]
    ys = [random.uniform(LO, HI) for _ in range(500)]
    zs = [fitness([x,y]) for x,y in zip(xs, ys)]
    ax1.scatter(xs, ys, c=zs, cmap="RdYlGn", s=12, alpha=0.6)
    ax1.scatter(0, 0, color=ORANGE, s=150, marker="*", zorder=5, label="Optimal (0,0)")
    ax1.set_facecolor(BG)
    ax1.set_title("Search Space f(x,y)\n(green = high fitness)", color=FG2, fontsize=9)
    ax1.set_xlabel("x", color=MUTED, fontsize=8)
    ax1.set_ylabel("y", color=MUTED, fontsize=8)
    ax1.tick_params(colors=FG2, labelsize=7)
    for sp in ax1.spines.values(): sp.set_edgecolor(BORDER)
    ax1.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=FG2, fontsize=8)
    ax2.set_title("Fitness Convergence", color=FG2, fontsize=9)
    ax2.tick_params(colors=FG2, labelsize=7)
    for sp in ax2.spines.values(): sp.set_edgecolor(BORDER)

def draw_result(ax1, ax2, best_ind, history, final_pop):
    ax1.clear(); ax2.clear()
    for ax in (ax1, ax2): ax.set_facecolor(BG)
    px = [ind[0] for ind in final_pop]; py = [ind[1] for ind in final_pop]
    pz = [fitness(ind) for ind in final_pop]
    ax1.scatter(px, py, c=pz, cmap="RdYlGn", s=40, alpha=0.75, zorder=2)
    ax1.scatter(*best_ind, color=BLUE, s=200, zorder=5,
                label=f"Best ({best_ind[0]:.3f}, {best_ind[1]:.3f})")
    ax1.scatter(0, 0, color=ORANGE, s=150, marker="*", zorder=5, label="Optimal (0,0)")
    ax1.set_facecolor(BG)
    ax1.set_title("Final Population + Best Found", color=FG2, fontsize=9)
    ax1.set_xlabel("x", color=MUTED, fontsize=8)
    ax1.set_ylabel("y", color=MUTED, fontsize=8)
    ax1.tick_params(colors=FG2, labelsize=7)
    for sp in ax1.spines.values(): sp.set_edgecolor(BORDER)
    ax1.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=FG2, fontsize=8)

    ax2.plot(history, color=GREEN, lw=1.8)
    ax2.fill_between(range(len(history)), history, alpha=0.15, color=GREEN)
    ax2.axhline(10, color=ORANGE, lw=1.2, ls="--", label="Optimal = 10")
    ax2.set_facecolor(BG)
    ax2.set_title("Fitness Convergence", color=FG2, fontsize=9)
    ax2.set_xlabel("Generation", color=MUTED, fontsize=8)
    ax2.set_ylabel("Best Fitness", color=MUTED, fontsize=8)
    ax2.tick_params(colors=FG2, labelsize=7)
    for sp in ax2.spines.values(): sp.set_edgecolor(BORDER)
    ax2.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=FG2, fontsize=8)

# ── UI ───────────────────────────────────────────────────────
root = tk.Tk()
root.title("Genetic Algorithm — Example 1: Function Optimisation")
root.geometry("980x660"); root.configure(bg=BG)

hf = tk.Frame(root, bg=BG); hf.pack(fill="x", padx=20, pady=(16,8))
tk.Label(hf, text="GENETIC ALGORITHM", fg=GREEN, bg=BG,
         font=("Courier New",16,"bold")).pack(side="left")
tk.Label(hf, text="  Example 1 · Function Optimisation", fg=MUTED, bg=BG,
         font=("Courier New",11)).pack(side="left")

dc = tk.Frame(root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
dc.pack(fill="x", padx=20, pady=(0,10))
tk.Label(dc, text="ALGORITHM", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,2))
tk.Label(dc,
    text=(f"Finds (x,y) ∈ [{LO},{HI}]² that maximises f(x,y) = -(x²+y²)+10.  Optimal: (0,0) → f=10\n"
          f"Population: {POP_SIZE}   Generations: {GENS}   Mutation rate: {MUT_RATE:.0%}   Crossover: single-point\n"
          "Selection: top-15 pool   |   Elitism: top 10% always survive each generation."),
    fg=FG2, bg=PANEL, font=("Courier New",10), justify="left"
).pack(anchor="w", padx=12, pady=(0,10))

cf = tk.Frame(root, bg=BG); cf.pack(fill="both", expand=True, padx=20, pady=(0,16))
left  = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
right = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
left.pack(side="left", fill="both", expand=True, padx=(0,8))
right.pack(side="left", fill="both", expand=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 4), facecolor=BG)
fig.tight_layout(pad=2)
canvas = FigureCanvasTkAgg(fig, master=left)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
draw_initial(ax1, ax2); canvas.draw()

tk.Button(left, text="▶  Run Genetic Algorithm", command=lambda: run(),
          bg="#0d3d2e", fg=GREEN, activebackground=GREEN, activeforeground="white",
          font=("Courier New",11,"bold"), relief="flat", bd=0,
          padx=18, pady=8, cursor="hand2",
          highlightbackground=GREEN, highlightthickness=1).pack(pady=8)

tk.Label(right, text="EVOLUTION LOG", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,4))
out = scrolledtext.ScrolledText(right, bg="#0d1117", fg=FG2,
      font=("Courier New",10), relief="flat", bd=0, wrap="word", height=22)
out.pack(fill="both", expand=True, padx=8, pady=(0,8))
out.tag_config("green", foreground=GREEN)
out.tag_config("head",  foreground=GREEN, font=("Courier New",10,"bold"))
out.insert("end", "Press  ▶ Run  to evolve the population.\n\n")
out.insert("end", f"Objective : maximise f(x,y) = -(x²+y²) + 10\n")
out.insert("end", f"Domain    : x, y ∈ [{LO}, {HI}]\n")
out.insert("end", f"Optimal   : (0, 0)  →  f = 10\n\n")
out.insert("end", "GA Operators:\n")
out.insert("end", "  Selection  : tournament (top-15 pool)\n")
out.insert("end", "  Crossover  : single-point\n")
out.insert("end", "  Mutation   : Gaussian perturbation\n")
out.insert("end", "  Elitism    : top 10% preserved\n")

def run():
    best_ind, best_sc, history, final_pop = ga_run()
    draw_result(ax1, ax2, best_ind, history, final_pop)
    fig.tight_layout(pad=2); canvas.draw()
    out.delete("1.0", "end")
    out.insert("end", "✅  EVOLUTION COMPLETE\n\n", "green")
    out.insert("end", f"Best x     : {best_ind[0]:+.6f}\n")
    out.insert("end", f"Best y     : {best_ind[1]:+.6f}\n")
    out.insert("end", f"Fitness    : {best_sc:.6f}  (optimal = 10)\n")
    out.insert("end", f"Error      : {abs(10 - best_sc):.6f}\n\n")
    out.insert("end", "CONVERGENCE\n", "head")
    out.insert("end", "─"*36 + "\n")
    for cp in [0, GENS//4, GENS//2, 3*GENS//4, GENS-1]:
        out.insert("end", f"  Gen {cp:4d} : {history[cp]:.5f}\n")
    out.insert("end", f"\nImprovement : {history[-1]-history[0]:.5f}\n")
    out.insert("end", f"Accuracy    : {(1 - abs(10-best_sc)/10)*100:.3f}% of optimal\n")

root.mainloop()