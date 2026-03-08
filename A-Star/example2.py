import tkinter as tk
from tkinter import scrolledtext
import math
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BG, PANEL, BORDER = "#0d1117", "#161b22", "#21262d"
GREEN, BLUE, ORANGE, MUTED, FG2 = "#10b981", "#3b82f6", "#f0883e", "#6b7280", "#c9d1d9"

CITY_COORDS = {
    "A": (0.5, 1.0), "B": (2.0, 3.5), "C": (4.5, 2.0),
    "D": (3.8, 4.2), "E": (6.0, 2.8), "F": (5.8, 4.8),
}
GRAPH = {
    "A": [("B", 3.6), ("C", 5.1)],
    "B": [("A", 3.6), ("D", 2.2), ("C", 3.2)],
    "C": [("A", 5.1), ("B", 3.2), ("E", 2.8)],
    "D": [("B", 2.2), ("E", 3.2), ("F", 2.2)],
    "E": [("C", 2.8), ("D", 3.2), ("F", 3.2)],
    "F": [("D", 2.2), ("E", 3.2)],
}
START, GOAL = "A", "F"

def heuristic(node):
    gx, gy = CITY_COORDS[GOAL]
    nx, ny = CITY_COORDS[node]
    return math.hypot(nx - gx, ny - gy)

def astar_graph(graph, start, goal):
    open_set = [(0, start)]
    came_from = {}
    g = {start: 0}
    while open_set:
        open_set.sort(key=lambda x: x[0])
        _, cur = open_set.pop(0)
        if cur == goal:
            path = []
            while cur in came_from:
                path.append(cur); cur = came_from[cur]
            path.append(start)
            return list(reversed(path)), g[goal]
        for nb, cost in graph.get(cur, []):
            tg = g[cur] + cost
            if tg < g.get(nb, float('inf')):
                came_from[nb] = cur; g[nb] = tg
                open_set.append((tg + heuristic(nb), nb))
    return None, float('inf')

def draw_graph(ax, path=None):
    ax.clear(); ax.set_facecolor(BG)
    path_edges = set()
    if path:
        for i in range(len(path)-1):
            a, b = path[i], path[i+1]
            path_edges.add((min(a,b), max(a,b)))
    drawn = set()
    for city, nbrs in GRAPH.items():
        x1, y1 = CITY_COORDS[city]
        for nb, cost in nbrs:
            key = (min(city,nb), max(city,nb))
            if key in drawn: continue
            drawn.add(key)
            x2, y2 = CITY_COORDS[nb]
            on = key in path_edges
            ax.plot([x1,x2],[y1,y2], color=GREEN if on else "#374151",
                    lw=3 if on else 1.4, zorder=1, solid_capstyle="round")
            ax.text((x1+x2)/2, (y1+y2)/2+0.12, str(cost), ha="center",
                    color=GREEN if on else MUTED, fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.1", fc=BG, ec="none"))
    for city, (x, y) in CITY_COORDS.items():
        on = path and city in path
        c = BLUE if city==START else ORANGE if city==GOAL else (GREEN if on else "#1e2530")
        ax.scatter(x, y, s=700, color=c, edgecolors=GREEN if on else "#4b5563",
                   linewidths=2, zorder=3)
        ax.text(x, y, city, ha="center", va="center",
                color="white", fontweight="bold", fontsize=13, zorder=4)
    ax.set_xlim(-0.5, 7); ax.set_ylim(0, 5.5)
    ax.axis("off")
    ax.set_title(f"A* City Road Network  ({START} → {GOAL})", color=FG2, fontsize=10, pad=10)

# GUI
root = tk.Tk()
root.title("A* Search — Example 2: City Road Network")
root.geometry("900x620"); root.configure(bg=BG)

hf = tk.Frame(root, bg=BG); hf.pack(fill="x", padx=20, pady=(16,8))
tk.Label(hf, text="A* SEARCH", fg=GREEN, bg=BG,
         font=("Courier New",16,"bold")).pack(side="left")
tk.Label(hf, text="  Example 2 · City Road Network", fg=MUTED, bg=BG,
         font=("Courier New",11)).pack(side="left")

dc = tk.Frame(root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
dc.pack(fill="x", padx=20, pady=(0,10))
tk.Label(dc, text="ALGORITHM", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,2))
tk.Label(dc,
    text=("A* finds the cheapest route from A → F in a weighted road graph.\n"
          "g(n) = total road distance so far   |   h(n) = Euclidean distance to goal\n"
          "The output table shows g, h and f values at each step of the search."),
    fg=FG2, bg=PANEL, font=("Courier New",10), justify="left"
).pack(anchor="w", padx=12, pady=(0,10))

cf = tk.Frame(root, bg=BG); cf.pack(fill="both", expand=True, padx=20, pady=(0,16))
left  = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
right = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
left.pack(side="left", fill="both", expand=True, padx=(0,8))
right.pack(side="left", fill="both", expand=True)

fig, ax = plt.subplots(figsize=(5.5, 4.5), facecolor=BG)
canvas = FigureCanvasTkAgg(fig, master=left)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
draw_graph(ax); canvas.draw()

tk.Button(left, text="▶  Run A* (City Graph)", command=lambda: run(),
          bg="#0d3d2e", fg=GREEN, activebackground=GREEN, activeforeground="white",
          font=("Courier New",11,"bold"), relief="flat", bd=0,
          padx=18, pady=8, cursor="hand2",
          highlightbackground=GREEN, highlightthickness=1).pack(pady=8)

tk.Label(right, text="STEP-BY-STEP OUTPUT", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,4))
out = scrolledtext.ScrolledText(right, bg="#0d1117", fg=FG2,
      font=("Courier New",10), relief="flat", bd=0, wrap="word", height=22)
out.pack(fill="both", expand=True, padx=8, pady=(0,8))
out.tag_config("green", foreground=GREEN)
out.insert("end", "Press  ▶ Run A* (City Graph)  to find the route.\n\n")
out.insert("end", f"Cities    : {list(CITY_COORDS.keys())}\n")
out.insert("end", f"Start     : {START}\n")
out.insert("end", f"Goal      : {GOAL}\n")
out.insert("end", f"Heuristic : Euclidean distance to {GOAL}\n")

def run():
    path, cost = astar_graph(GRAPH, START, GOAL)
    draw_graph(ax, path); canvas.draw()
    out.delete("1.0", "end")
    if path:
        out.insert("end", "SHORTEST PATH FOUND\n\n", "green")
        out.insert("end", f"Route : {' → '.join(path)}\n")
        out.insert("end", f"Cost  : {cost:.2f}\n\n")
        out.insert("end", "Edge breakdown:\n")
        out.insert("end", f"  {'Edge':<8} {'road':>6} {'g':>6} {'h':>6} {'f':>6}\n")
        out.insert("end", "  " + "─"*34 + "\n")
        running = 0.0
        for i in range(len(path)-1):
            a, b = path[i], path[i+1]
            c = next(w for nb, w in GRAPH[a] if nb == b)
            running += c
            h_val = heuristic(b)
            out.insert("end",
                f"  {a}→{b:<6}  {c:>5.1f}  {running:>5.1f}  {h_val:>5.2f}  {running+h_val:>5.2f}\n")
        out.insert("end", f"\nTotal cost : {cost:.2f}\n")
        out.insert("end", "Admissible heuristic → path is OPTIMAL.\n")
    else:
        out.insert("end", "  No path found.\n")

root.mainloop()