# Shared graph class for the Campus Navigation System.
# Copy this class into each module file so every module runs independently.

class CampusGraph:
    def __init__(self):
        self.locations = [
            "Main Gate", "Admin Block", "Library", "CSE Department",
            "Cafeteria", "Auditorium", "Sports Ground", "Hostel"
        ]
        self.matrix = [[0] * len(self.locations) for _ in self.locations]
        self.adj = [[] for _ in self.locations]
        # Illustrative distances in metres; replace with your real campus data.
        edges = [
            (0, 1, 120), (0, 4, 180), (1, 2, 90), (1, 3, 140),
            (2, 3, 70), (2, 5, 160), (3, 4, 100), (3, 5, 130),
            (4, 6, 210), (5, 6, 190), (5, 7, 240), (6, 7, 150)
        ]
        for u, v, distance in edges:
            self.matrix[u][v] = self.matrix[v][u] = distance
            self.adj[u].append((v, distance))
            self.adj[v].append((u, distance))

    def show_locations(self):
        print("\nCAMPUS LOCATIONS")
        for i, name in enumerate(self.locations, 1):
            print(f"{i}. {name}")

    def choose_location(self, prompt):
        self.show_locations()
        while True:
            try:
                value = int(input(prompt))
                if 1 <= value <= len(self.locations):
                    return value - 1
                print(f"Choose a number from 1 to {len(self.locations)}.")
            except ValueError:
                print("Invalid input. Enter a whole number.")

    def show_matrix(self):
        print("\nADJACENCY MATRIX (metres; 0 = no direct path)")
        print(" " * 19 + "".join(f"{i+1:>5}" for i in range(len(self.locations))))
        for i, row in enumerate(self.matrix):
            print(f"{self.locations[i]:<19}" + "".join(f"{x:>5}" for x in row))

    def show_adjacency_list(self):
        print("\nADJACENCY LIST")
        for i, edges in enumerate(self.adj):
            neighbours = ", ".join(
                f"{self.locations[v]} ({w} m)" for v, w in edges
            )
            print(f"{self.locations[i]} -> {neighbours}")

    def show_connections(self):
        print("\nDIRECT PATHWAYS")
        for u, edges in enumerate(self.adj):
            for v, w in edges:
                if u < v:
                    print(f"{self.locations[u]} <-> {self.locations[v]}: {w} m")

from collections import deque
import heapq

def bfs(campus, start):
    visited = [False] * len(campus.locations)
    order = []
    queue = deque([start])
    visited[start] = True
    while queue:
        u = queue.popleft()
        order.append(u)
        for v, _ in campus.adj[u]:
            if not visited[v]:
                visited[v] = True
                queue.append(v)
    return order

def dfs(campus, start):
    visited = [False] * len(campus.locations)
    order = []
    stack = [start]
    while stack:
        u = stack.pop()
        if visited[u]:
            continue
        visited[u] = True
        order.append(u)
        for v, _ in reversed(campus.adj[u]):
            if not visited[v]:
                stack.append(v)
    return order

def dijkstra(campus, source, destination):
    n = len(campus.locations)
    distances = [float("inf")] * n
    parent = [None] * n
    distances[source] = 0
    pq = [(0, source)]
    while pq:
        distance, u = heapq.heappop(pq)
        if distance != distances[u]:
            continue
        if u == destination:
            break
        for v, weight in campus.adj[u]:
            candidate = distance + weight
            if candidate < distances[v]:
                distances[v] = candidate
                parent[v] = u
                heapq.heappush(pq, (candidate, v))
    if distances[destination] == float("inf"):
        print("No route exists.")
        return
    route, current = [], destination
    while current is not None:
        route.append(current)
        current = parent[current]
    route.reverse()
    print("Route: " + " -> ".join(campus.locations[i] for i in route))
    print(f"Total distance: {distances[destination]} metres")

def main():
    campus = CampusGraph()
    while True:
        print("\nMODULE 4: COMPLETE CAMPUS NAVIGATOR")
        print("1. Find shortest route")
        print("2. BFS traversal")
        print("3. DFS traversal")
        print("4. Show adjacency list")
        print("5. Show adjacency matrix")
        print("6. Show direct pathways")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        elif choice == "1":
            source = campus.choose_location("Source location number: ")
            destination = campus.choose_location("Destination location number: ")
            if source == destination:
                print(f"Already at {campus.locations[source]}. Distance: 0 metres.")
            else:
                dijkstra(campus, source, destination)
        elif choice in ("2", "3"):
            start = campus.choose_location("Start location number: ")
            order = bfs(campus, start) if choice == "2" else dfs(campus, start)
            label = "BFS" if choice == "2" else "DFS"
            print(label + " order: " + " -> ".join(campus.locations[i] for i in order))
        elif choice == "4":
            campus.show_adjacency_list()
        elif choice == "5":
            campus.show_matrix()
        elif choice == "6":
            campus.show_connections()
        else:
            print("Invalid choice. Enter a number from 0 to 6.")

if __name__ == "__main__":
    main()
