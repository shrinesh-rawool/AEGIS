from collections import deque
from typing import Dict, List, Set

class LogisticsGraph:
    def __init__(self):
        # State space representation: Adjacency list
        self.adjacency_list: Dict[str, List[str]] = {}
        self.edge_weights: Dict[tuple, float] = {}

    def add_node(self, node: str):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, u: str, v: str, distance_km: float):
        self.add_node(u)
        self.add_node(v)
        self.adjacency_list[u].append(v)
        self.adjacency_list[v].append(u)
        self.edge_weights[(u, v)] = distance_km
        self.edge_weights[(v, u)] = distance_km

    def bfs_shortest_hops(self, start: str, destination: str) -> List[str]:
        """Exp 5: Breadth-First Search for minimum topological hop-count."""
        if start == destination:
            return [start]
            
        visited: Set[str] = {start}
        queue = deque([[start]])

        while queue:
            path = queue.popleft()
            node = path[-1]

            for neighbor in self.adjacency_list.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path) + [neighbor]
                    if neighbor == destination:
                        return new_path
                    queue.append(new_path)
        return []

    def dfs_all_paths(self, start: str, destination: str, max_depth: int = 6) -> List[List[str]]:
        """Exp 4: Depth-First Search with cycle prevention for alternate routes."""
        all_paths: List[List[str]] = []

        def _dfs(current: str, path: List[str], depth: int):
            if depth > max_depth:
                return
            if current == destination:
                all_paths.append(list(path))
                return

            for neighbor in self.adjacency_list.get(current, []):
                if neighbor not in path:  # Prevent cycles
                    path.append(neighbor)
                    _dfs(neighbor, path, depth + 1)
                    path.pop()

        _dfs(start, [start], 0)
        return all_paths