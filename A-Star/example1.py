import tkinter as tk
from tkinter import scrolledtext
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BG, PANEL, BORDER = "#0d1117", "#161b22", "#21262d"
GREEN, BLUE, ORANGE, MUTED, FG2 = "#10b981", "#3b82f6", "#f0883e", "#6b7280", "#c9d1d9"

GRID = [
    [0, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
]
START, GOAL = (0, 0), (6, 6)

def astar_grid(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    h = lambda a, b: abs(a[0]-b[0]) + abs(a[1]-b[1])
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
            return list(reversed(path))
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nb = (cur[0]+dr, cur[1]+dc)
            nr, nc = nb
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0:
                tg = g[cur] + 1
                if tg < g.get(nb, float('inf')):
                    came_from[nb] = cur; g[nb] = tg
                    open_set.append((tg + h(nb, goal), nb))
    return None

def draw_grid(ax, path=None):
    path_set = set(map(tuple, path)) if path else set()
    rows, cols = len(GRID), len(GRID[0])
    ax.clear(); ax.set_facecolor(BG)
    for r in range(rows):
        for c in range(cols):
            cell = GRID[r][c]
            color = "#374151" if cell == 1 else "#1e2530"
            if (r,c) in path_set: color = GREEN
            if (r,c) == START:    color = BLUE
            if (r,c) == GOAL:     color = ORANGE
            ax.add_patch(plt.Rectangle([c, rows-1-r], 0.88, 0.88, color=color, linewidth=0))
            label = "S" if (r,c)==START else "G" if (r,c)==GOAL else ("WALL" if cell==1 else "")
            if path and (r,c) in path_set and (r,c) not in (START, GOAL):
                label = str(path.index((r,c)))
            if label:
                ax.text(c+0.44, rows-1-r+0.44, label, ha="center", va="center",
                        color="white", fontsize=9, fontweight="bold")
    ax.set_xlim(0, cols); ax.set_ylim(0, rows)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("A* Grid Maze  (S=Start · G=Goal · Wall)", color=FG2, fontsize=10, pad=10)

#GUI
root = tk.Tk()
root.title("A* Search — Example 1: Grid Maze")
root.geometry("860x620"); root.configure(bg=BG)

hf = tk.Frame(root, bg=BG); hf.pack(fill="x", padx=20, pady=(16,8))
tk.Label(hf, text="A* SEARCH", fg=GREEN, bg=BG,
         font=("Courier New",16,"bold")).pack(side="left")
tk.Label(hf, text="  Example 1 · Grid Maze Pathfinding", fg=MUTED, bg=BG,
         font=("Courier New",11)).pack(side="left")

dc = tk.Frame(root, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
dc.pack(fill="x", padx=20, pady=(0,10))
tk.Label(dc, text="ALGORITHM", fg=GREEN, bg=PANEL,
         font=("Courier New",9,"bold")).pack(anchor="w", padx=12, pady=(10,2))
tk.Label(dc,
    text=("A* evaluates nodes using  f(n) = g(n) + h(n)\n"
          "g(n) = steps taken so far   |   h(n) = Manhattan distance to goal\n"
          "Numbers on path cells show the order each node was added to the solution."),
    fg=FG2, bg=PANEL, font=("Courier New",10), justify="left"
).pack(anchor="w", padx=12, pady=(0,10))

cf = tk.Frame(root, bg=BG); cf.pack(fill="both", expand=True, padx=20, pady=(0,16))
left  = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
right = tk.Frame(cf, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
left.pack(side="left", fill="both", expand=True, padx=(0,8))
right.pack(side="left", fill="both", expand=True)

fig, ax = plt.subplots(figsize=(5, 4.5), facecolor=BG)
canvas = FigureCanvasTkAgg(fig, master=left)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
draw_grid(ax); canvas.draw()

tk.Button(left, text="▶  Run A* (Grid)", command=lambda: run(),
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
out.insert("end", "Press  ▶ Run A* (Grid)  to find the path.\n\n")
out.insert("end", f"Grid size : {len(GRID)} × {len(GRID[0])}\n")
out.insert("end", f"Start     : {START}\n")
out.insert("end", f"Goal      : {GOAL}\n")
out.insert("end", f"Heuristic : Manhattan distance\n")

def run():
    path = astar_grid(GRID, START, GOAL)
    draw_grid(ax, path); canvas.draw()
    out.delete("1.0", "end")
    if path:
        out.insert("end", "PATH FOUND\n\n", "green")
        out.insert("end", f"Total steps  : {len(path)-1}\n")
        out.insert("end", f"Nodes in path: {len(path)}\n\n")
        out.insert("end", "Route (row, col):\n")
        for i, p in enumerate(path):
            tag = "green" if p in (START, GOAL) else ""
            note = "  ← START" if p==START else "  ← GOAL" if p==GOAL else ""
            out.insert("end", f"  Step {i:2d}: {p}{note}\n", tag)
        out.insert("end", "\nf(n) = g(n) + h(n)\n")
        out.insert("end", "Each step costs 1 (uniform grid).\n")
        out.insert("end", "Admissible heuristic → path is OPTIMAL.\n")
    else:
        out.insert("end", "No path found — goal unreachable.\n")

root.mainloop()