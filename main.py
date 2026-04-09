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

    # 🔥 add loops
    for _ in range((rows * cols) // 8):
        i = random.randint(1, rows-2)
        j = random.randint(1, cols-2)
        maze[i][j] = 0

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
        self.root.title("Maze Solver (Final Version)")

        self.canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        self.canvas.pack()

        self.create_buttons()

        self.result_label = tk.Label(root, text="", font=("Arial", 11))
        self.result_label.pack()

        self.reset()

        self.canvas.bind("<Button-1>", self.on_click)

    # ---------- BUTTONS ----------
    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Button(frame, text="Solve BFS", command=self.solve_bfs).pack(side="left", padx=5)
        tk.Button(frame, text="Solve Dijkstra", command=self.solve_dijkstra).pack(side="left", padx=5)
        tk.Button(frame, text="Compare Both", command=self.compare_popup).pack(side="left", padx=5)
        tk.Button(frame, text="New Maze", command=self.reset).pack(side="left", padx=5)

    # ---------- RESET ----------
    def reset(self):
        self.maze = generate_maze(ROWS, COLS)

        # strong weights
        self.weights = [[random.choice([1,1,1,1,20,30]) if self.maze[i][j]==0 else None
                         for j in range(COLS)] for i in range(ROWS)]

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
                    color = "#e0f7fa" if cost == 1 else "#0d47a1"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    # ---------- CLICK ----------
    def on_click(self, event):
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE

        if self.maze[row][col] == 1:
            return

        if not self.start:
            self.start = (row, col)
        elif not self.end:
            self.end = (row, col)

        self.draw_maze()
        if self.start:
            self.draw_cell(self.canvas, *self.start, "green")
        if self.end:
            self.draw_cell(self.canvas, *self.end, "red")

    def draw_cell(self, canvas, r, c, color):
        x1, y1 = c*CELL_SIZE, r*CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def animate(self, canvas, path, color):
        for i, (r, c) in enumerate(path):
            self.root.after(20*i, lambda r=r,c=c: self.draw_cell(canvas, r, c, color))

    # ---------- BFS ----------
    def solve_bfs(self):
        if not self.start or not self.end:
            return
        path = bfs(self.maze, self.start, self.end)
        self.animate(self.canvas, path, "blue")

    # ---------- DIJKSTRA ----------
    def solve_dijkstra(self):
        if not self.start or not self.end:
            return
        path = dijkstra(self.maze, self.weights, self.start, self.end)
        self.animate(self.canvas, path, "orange")

    # ---------- POPUP COMPARISON ----------
    def compare_popup(self):
        if not self.start or not self.end:
            return

        popup = tk.Toplevel(self.root)
        popup.title("BFS vs Dijkstra Comparison")

        frame = tk.Frame(popup)
        frame.pack()

        canvas_bfs = tk.Canvas(frame, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        canvas_bfs.pack(side="left")

        canvas_dij = tk.Canvas(frame, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
        canvas_dij.pack(side="right")

        # draw maze on both
        for i in range(ROWS):
            for j in range(COLS):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE

                color = "black" if self.maze[i][j] == 1 else "#e0f7fa"

                canvas_bfs.create_rectangle(x1, y1, x2, y2, fill=color)
                canvas_dij.create_rectangle(x1, y1, x2, y2, fill=color)

        # mark start/end
        for canvas in [canvas_bfs, canvas_dij]:
            self.draw_cell(canvas, *self.start, "green")
            self.draw_cell(canvas, *self.end, "red")

        # BFS
        t1 = time.time()
        path_bfs = bfs(self.maze, self.start, self.end)
        bfs_time = time.time() - t1
        bfs_cost = sum(self.weights[r][c] for r,c in path_bfs)

        # Dijkstra
        t2 = time.time()
        path_dij = dijkstra(self.maze, self.weights, self.start, self.end)
        dij_time = time.time() - t2
        dij_cost = sum(self.weights[r][c] for r,c in path_dij)

        # animate
        for i, (r, c) in enumerate(path_bfs):
            popup.after(20*i, lambda r=r,c=c: self.draw_cell(canvas_bfs, r, c, "blue"))

        for i, (r, c) in enumerate(path_dij):
            popup.after(20*i, lambda r=r,c=c: self.draw_cell(canvas_dij, r, c, "orange"))

        # results
        tk.Label(popup, text=
            f"BFS → Steps:{len(path_bfs)} Cost:{bfs_cost} Time:{bfs_time:.5f}s\n"
            f"Dijkstra → Steps:{len(path_dij)} Cost:{dij_cost} Time:{dij_time:.5f}s",
            font=("Arial", 11)
        ).pack()


# ---------------- RUN ----------------
root = tk.Tk()
app = MazeApp(root)
root.mainloop()