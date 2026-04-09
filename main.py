import tkinter as tk
import random
import time
import heapq
from collections import deque

CELL_SIZE = 25
ROWS, COLS = 21, 21


# ---------------- MAZE GENERATOR ----------------
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]

    def carve(x, y):
        maze[x][y] = 0
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] == 1:
                    maze[x + dx][y + dy] = 0
                    carve(nx, ny)

    carve(0, 0)
    maze[0][0] = 0
    maze[rows-1][cols-1] = 0
    return maze


# ---------------- BFS ----------------
def bfs(maze, start, end):
    queue = deque([start])
    visited = set([start])
    parent = {}

    directions = [(0,1),(1,0),(0,-1),(-1,0)]

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            return path[::-1]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and
                maze[nx][ny] == 0 and (nx, ny) not in visited):
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return []


# ---------------- DIJKSTRA ----------------
def dijkstra(maze, weights, start, end):
    pq = [(0, start)]
    dist = {start: 0}
    parent = {}

    directions = [(0,1),(1,0),(0,-1),(-1,0)]

    while pq:
        cost, (x, y) = heapq.heappop(pq)

        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            return path[::-1]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and
                maze[nx][ny] == 0):

                new_cost = cost + weights[nx][ny]

                if (nx, ny) not in dist or new_cost < dist[(nx, ny)]:
                    dist[(nx, ny)] = new_cost
                    parent[(nx, ny)] = (x, y)
                    heapq.heappush(pq, (new_cost, (nx, ny)))

    return []


# ---------------- GUI ----------------
class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver (Final Project)")

        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()

        self.create_buttons()
        self.create_legend()

        self.result_label = tk.Label(root, text="", font=("Arial", 11), justify="left")
        self.result_label.pack()

        self.reset()
        self.canvas.bind("<Button-1>", self.on_click)

    # ---------- BUTTONS ----------
    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Button(frame, text="Solve BFS", command=self.solve_bfs).pack(side="left", padx=5)
        tk.Button(frame, text="Solve Dijkstra", command=self.solve_dijkstra).pack(side="left", padx=5)
        tk.Button(frame, text="Compare Both", command=self.compare_algorithms).pack(side="left", padx=5)
        tk.Button(frame, text="Clear Path", command=self.clear_path).pack(side="left", padx=5)
        tk.Button(frame, text="New Maze", command=self.reset).pack(side="left", padx=5)

    # ---------- LEGEND ----------
    def create_legend(self):
        tk.Label(
            self.root,
            text="Green=Start  Red=End  Blue=BFS  Orange=Dijkstra",
            font=("Arial", 10)
        ).pack()

    # ---------- RESET ----------
    def reset(self):
        self.maze = generate_maze(ROWS, COLS)

        # 🔥 STRONG WEIGHT VARIATION (FIXED)
        self.weights = []
        for i in range(ROWS):
            row = []
            for j in range(COLS):
                if self.maze[i][j] == 0:
                    if random.random() < 0.7:
                        row.append(1)  # cheap path
                    else:
                        row.append(random.randint(8, 20))  # expensive
                else:
                    row.append(None)
            self.weights.append(row)

        self.start = None
        self.end = None

        self.draw_maze()
        self.result_label.config(text="")

    # ---------- DRAW ----------
    def draw_maze(self):
        self.canvas.delete("all")

        for i in range(ROWS):
            for j in range(COLS):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                if self.maze[i][j] == 1:
                    color = "black"
                else:
                    cost = self.weights[i][j]
                    if cost == 1:
                        color = "#e0f7fa"
                    elif cost < 10:
                        color = "#64b5f6"
                    else:
                        color = "#0d47a1"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # ---------- CLICK ----------
    def on_click(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if self.maze[row][col] == 1:
            return

        if not self.start:
            self.start = (row, col)
            self.color_cell(row, col, "green")
        elif not self.end:
            self.end = (row, col)
            self.color_cell(row, col, "red")

    def color_cell(self, row, col, color):
        x1, y1 = col*CELL_SIZE, row*CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # ---------- BFS ----------
    def solve_bfs(self):
        if not self.start or not self.end:
            return
        path = bfs(self.maze, self.start, self.end)
        self.animate_path(path, "blue")

    # ---------- DIJKSTRA ----------
    def solve_dijkstra(self):
        if not self.start or not self.end:
            return
        path = dijkstra(self.maze, self.weights, self.start, self.end)
        self.animate_path(path, "orange")

    # ---------- COMPARE ----------
    def compare_algorithms(self):
        if not self.start or not self.end:
            return

        # BFS
        t1 = time.time()
        path_bfs = bfs(self.maze, self.start, self.end)
        bfs_time = time.time() - t1
        bfs_steps = len(path_bfs)
        bfs_cost = sum(self.weights[r][c] for r, c in path_bfs)

        # Dijkstra
        t2 = time.time()
        path_dij = dijkstra(self.maze, self.weights, self.start, self.end)
        dij_time = time.time() - t2
        dij_steps = len(path_dij)
        dij_cost = sum(self.weights[r][c] for r, c in path_dij)

        # Animate
        self.animate_path(path_bfs, "blue")
        self.animate_path(path_dij, "orange")

        # Compare
        faster = "BFS" if bfs_time < dij_time else "Dijkstra"
        shorter = "BFS" if bfs_steps < dij_steps else "Dijkstra"
        cheaper = "BFS" if bfs_cost < dij_cost else "Dijkstra"

        result = (
            f"BFS → Steps: {bfs_steps} | Cost: {bfs_cost} | Time: {bfs_time:.6f}s\n"
            f"Dijkstra → Steps: {dij_steps} | Cost: {dij_cost} | Time: {dij_time:.6f}s\n\n"
            f"⚡ Faster: {faster}\n"
            f"📏 Shorter Path: {shorter}\n"
            f"💰 Cheaper Path: {cheaper}"
        )

        self.result_label.config(text=result)

    # ---------- CLEAR ----------
    def clear_path(self):
        self.draw_maze()
        if self.start:
            self.color_cell(*self.start, "green")
        if self.end:
            self.color_cell(*self.end, "red")

    # ---------- ANIMATION ----------
    def animate_path(self, path, color):
        for i, (r, c) in enumerate(path):
            self.root.after(20 * i, lambda r=r, c=c: self.color_cell(r, c, color))


# ---------------- RUN ----------------
root = tk.Tk()
app = MazeApp(root)
root.mainloop()