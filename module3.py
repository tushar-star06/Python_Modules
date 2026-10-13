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

import heapq

def dijkstra(campus, source, destination):
    n = len(campus.locations)
    distances = [float("inf")] * n
    parent = [None] * n
    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)
        if current_distance != distances[current]:
            continue
        if current == destination:
            break
        for neighbour, weight in campus.adj[current]:
            new_distance = current_distance + weight
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                parent[neighbour] = current
                heapq.heappush(priority_queue, (new_distance, neighbour))

    if distances[destination] == float("inf"):
        print("No route exists.")
        return

    route = []
    current = destination
    while current is not None:
        route.append(current)
        current = parent[current]
    route.reverse()

    print("\nSHORTEST ROUTE")
    print(" -> ".join(campus.locations[i] for i in route))
    print(f"Total distance: {distances[destination]} metres")

def main():
    campus = CampusGraph()
    print("\nMODULE 3: DIJKSTRA SHORTEST PATH")
    source = campus.choose_location("Source location number: ")
    destination = campus.choose_location("Destination location number: ")
    if source == destination:
        print(f"Already at {campus.locations[source]}. Distance: 0 metres.")
    else:
        dijkstra(campus, source, destination)

if __name__ == "__main__":
    main()
