import heapq
import tkinter as tk
from tkinter import messagebox

# Dijkstra's Algorithm
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        #  continue
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous

# Rebuild shortest path from 'previous' dict
def get_shortest_path(previous, start, end):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    if path and path[0] == start:
        return path
    else:
        return []

# Make graph bidirectional by adding reverse edges
def make_bidirectional(graph):
    bidir_graph = {node: [] for node in graph}
    for node, edges in graph.items():
        for neighbor, weight in edges:
            bidir_graph[node].append((neighbor, weight))
            if neighbor not in bidir_graph:
                bidir_graph[neighbor] = []
            if (node, weight) not in bidir_graph[neighbor]:
                bidir_graph[neighbor].append((node, weight))
    return bidir_graph

# Original graph 
graph = {
    'Bangalore': [('Mysore', 145), ('Tumkur', 70), ('Davangere', 265)],
    'Mysore': [('Mandya', 45), ('Chamarajanagar', 60)],
    'Tumkur': [('Chitradurga', 130)],
    'Davangere': [('Hubli', 140)],
    'Mandya': [('Hassan', 100)],
    'Chamarajanagar': [('Hassan', 170)],
    'Chitradurga': [('Bellary', 130)],
    'Hubli': [('Belgaum', 105), ('Hospet', 150)],
    'Hassan': [('Mangalore', 170)],
    'Mangalore': [('Udupi', 60)],
    'Udupi': [('Karwar', 225)],
    'Karwar': [('Belgaum', 170)],
    'Belgaum': [('Bijapur', 205)],
    'Hospet': [('Bellary', 70)],
    'Bellary': [('Raichur', 180)],
    'Raichur': [('Kalaburagi', 160)],
    'Bijapur': [('Kalaburagi', 160)],
    'Kalaburagi': [('Bidar', 115)],
    'Bidar': [],
}

# Make graph bidirectional
graph = make_bidirectional(graph)

# Function called when button is clicked
def find_path():
    start = entry_start.get().strip().title()
    end = entry_end.get().strip().title()

    if start not in graph or end not in graph:
        messagebox.showerror("Oops!", "That capital isn't in the map! 😢")
        return

    distances, previous = dijkstra(graph, start)
    path = get_shortest_path(previous, start, end)

    if not path:
        result_label.config(text="No path found 😢")
    else:
        result_label.config(
            text=f"🚗 Path: {' → '.join(path)}\n📏 Distance: {distances[end]} km"
        )

#  GUI
root = tk.Tk()
root.title("🌸 Karnataka Cities Route Finder")
root.geometry("520x320")
root.configure(bg="#ffe6f0")  

# Fonts
label_font = ("Comic Sans MS", 12, "bold")
entry_font = ("Comic Sans MS", 12)
button_font = ("Comic Sans MS", 12, "bold")

# Labels and inputs
tk.Label(root, text="Start City:", font=label_font, bg="#ffe6f0", fg="#4b0082").grid(row=0, column=0, padx=15, pady=10, sticky="e")
entry_start = tk.Entry(root, font=entry_font, width=30, bg="#fff0f5")
entry_start.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="End City:", font=label_font, bg="#ffe6f0", fg="#4b0082").grid(row=1, column=0, padx=15, pady=10, sticky="e")
entry_end = tk.Entry(root, font=entry_font, width=30, bg="#fff0f5")
entry_end.grid(row=1, column=1, padx=10, pady=10)

# Button
tk.Button(root, text=" - Find Shortest Path -", command=find_path,
          font=button_font, bg="#ff69b4", fg="white", padx=10, pady=6).grid(row=2, columnspan=2, pady=20)

# Result Display
result_label = tk.Label(root, text="", font=("Comic Sans MS", 12, "bold"), fg="#c71585", bg="#ffe6f0", wraplength=460, justify="center")
result_label.grid(row=3, columnspan=2, pady=10)

root.mainloop()
