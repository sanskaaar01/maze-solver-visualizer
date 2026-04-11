# 🚀 Maze Solver Visualizer (BFS vs Dijkstra)

## 📌 Overview

This project is an interactive **maze solver and algorithm visualizer** built using Python and Tkinter.

It demonstrates how **Breadth-First Search (BFS)** and **Dijkstra’s Algorithm** behave on the same maze, with real-time visualization, animation, and comparison.

---

## 🎯 Features

* 🧩 Random maze generation (with loops → multiple paths)
* 🖱 Click to set:

  * Start node (Green)
  * End node (Red)
* 🔵 Solve using **BFS** (shortest path in steps)
* 🟠 Solve using **Dijkstra** (minimum cost path)
* ⚔️ **Compare Both (Popup Window)**

  * Side-by-side visualization
  * BFS vs Dijkstra simultaneously
* 🎬 Animated path traversal
* 🎚️ Adjustable animation speed (slider)
* ⚖️ Performance comparison:

  * Steps
  * Cost
  * Execution time

---

## 🧠 Concepts Used

* Graph representation (maze → grid graph)
* Breadth-First Search (BFS)
* Dijkstra’s Algorithm
* Priority Queue (Min Heap using `heapq`)
* Path reconstruction
* Algorithm comparison (time vs cost vs steps)

---

## ⚔️ BFS vs Dijkstra

| Feature        | BFS                   | Dijkstra                |
| -------------- | --------------------- | ----------------------- |
| Graph Type     | Unweighted            | Weighted                |
| Goal           | Shortest path (steps) | Minimum cost path       |
| Data Structure | Queue                 | Priority Queue          |
| Behavior       | Fast, ignores cost    | Optimal, considers cost |

👉 In some cases both may give the same path (due to maze structure).
👉 With weighted paths, Dijkstra may choose a longer but cheaper route.

---

## 🖥️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/sanskaaar01/maze-solver-visualizer.git
cd maze-solver-visualizer
```

### 2. Run the project

```bash
python main.py
```

---

## 🕹️ How to Use

1. Click any open cell → set **Start**
2. Click another cell → set **End**
3. Choose:

   * Solve BFS
   * Solve Dijkstra
   * Compare Both (opens popup)
4. Adjust speed (in popup)
5. Watch animations and compare results

---

## 📊 Sample Output

```
BFS → Steps: 45 | Cost: 180 | Time: 0.00020s  
Dijkstra → Steps: 60 | Cost: 120 | Time: 0.00045s  
```

---

## 💡 Learning Outcome

This project helps understand:

* Difference between **unweighted vs weighted shortest paths**
* Trade-offs between **speed and optimal cost**
* Practical use of **graphs and priority queues**

---

## 🔧 Tech Stack

* Python
* Tkinter (GUI)
* Heapq (Priority Queue)

---

## 🚀 Future Improvements

* Show exploration wave (BFS vs Dijkstra)
* Export results to file
* Adjustable maze size
* Improved UI styling

---

## 👨‍💻 Author

**Sanskar Raje Bhosle**
