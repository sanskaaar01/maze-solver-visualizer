# 🚀 Maze Solver Visualizer (BFS vs Dijkstra)

## 📌 Overview

This project is an interactive **maze solver and algorithm visualizer** built using Python and Tkinter.

It demonstrates how **Breadth-First Search (BFS)** and **Dijkstra’s Algorithm** behave on a maze modeled as a graph, including real-time visualization, animation, and performance comparison.

---

## 🎯 Features

* 🧩 Random maze generation (always solvable)
* 🖱 Click to select **Start** and **End** points
* 🔵 BFS shortest path visualization (minimum steps)
* 🟠 Dijkstra shortest path visualization (minimum cost)
* 🎬 Animated path traversal
* ⚖️ Algorithm comparison:

  * Steps
  * Cost
  * Execution time
* 🎨 Weighted maze (different traversal costs)
* 🧹 Clear path and regenerate maze functionality

---

## 🧠 Concepts Used

* Graph representation (grid → graph)
* Breadth-First Search (BFS)
* Dijkstra’s Algorithm
* Priority Queue (Min Heap)
* Algorithm analysis (time, cost, path length)
* Path reconstruction using parent tracking

---

## ⚔️ BFS vs Dijkstra

| Feature         | BFS                   | Dijkstra              |
| --------------- | --------------------- | --------------------- |
| Graph Type      | Unweighted            | Weighted              |
| Goal            | Shortest path (steps) | Minimum cost path     |
| Data Structure  | Queue                 | Priority Queue (Heap) |
| Time Complexity | O(V + E)              | O((V + E) log V)      |

👉 In some cases, both may produce the same path due to maze structure.
👉 In weighted scenarios, Dijkstra may choose a longer but cheaper path.

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

1. Click on any open cell → set **Start (Green)**
2. Click another cell → set **End (Red)**
3. Choose:

   * **Solve BFS**
   * **Solve Dijkstra**
   * **Compare Both**
4. View:

   * Animated path
   * Stats (steps, cost, time)

---

## 📊 Sample Output

```
BFS → Steps: 45 | Cost: 180 | Time: 0.0002s  
Dijkstra → Steps: 60 | Cost: 120 | Time: 0.0005s  

⚡ Faster: BFS  
📏 Shorter Path: BFS  
💰 Cheaper Path: Dijkstra  
```

---

## 📷 Screenshot

(Add your screenshot in `/screenshots/app.png`)

---

## 💡 Learning Outcome

This project helps in understanding:

* Difference between **unweighted and weighted shortest path algorithms**
* Trade-offs between **speed vs optimal cost**
* Practical use of **graphs and priority queues**

---

## 🔧 Tech Stack

* Python
* Tkinter (GUI)
* Heapq (Priority Queue)

---

## 🚀 Future Improvements

* Step-by-step exploration visualization (BFS wave)
* Adjustable maze size
* Speed control for animation
* Export results as report

---

## 👨‍💻 Author

**Sanskar Bhosle**
