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

def bfs(campus, start):
    visited = [False] * len(campus.locations)
    order = []
    queue = deque([start])
    visited[start] = True
    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbour, _ in campus.adj[current]:
            if not visited[neighbour]:
                visited[neighbour] = True
                queue.append(neighbour)
    return order

def dfs(campus, start):
    visited = [False] * len(campus.locations)
    order = []
    stack = [start]
    while stack:
        current = stack.pop()
        if visited[current]:
            continue
        visited[current] = True
        order.append(current)
        for neighbour, _ in reversed(campus.adj[current]):
            if not visited[neighbour]:
                stack.append(neighbour)
    return order

def print_order(campus, order):
    print(" -> ".join(campus.locations[i] for i in order))

def main():
    campus = CampusGraph()
    while True:
        print("\nMODULE 2: ADJACENCY LIST, BFS AND DFS")
        print("1. Show adjacency list")
        print("2. Run BFS")
        print("3. Run DFS")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            campus.show_adjacency_list()
        elif choice in ("2", "3"):
            start = campus.choose_location("Start location number: ")
            if choice == "2":
                print("BFS order: ", end="")
                print_order(campus, bfs(campus, start))
            else:
                print("DFS order: ", end="")
                print_order(campus, dfs(campus, start))
        elif choice == "0":
            break
        else:
            print("Invalid choice. Enter 0, 1, 2, or 3.")

if __name__ == "__main__":
    main()
