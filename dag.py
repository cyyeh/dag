from collections import deque
from typing import Dict, List, Literal


class DAG:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex not in self.graph:
            self.add_vertex(from_vertex)
        if to_vertex not in self.graph:
            self.add_vertex(to_vertex)
        self.graph[from_vertex].append(to_vertex)

    def _has_cycle_util(self, vertex, visited, rec_stack):
        """
        A utility function to detect a cycle in a directed graph using DFS.

        Args:
            vertex: The current vertex being explored.
            visited: A dictionary that tracks whether each vertex has been visited.
            rec_stack: A dictionary that tracks the vertices currently in the recursion stack.

        Returns:
            bool: True if a cycle is detected, False otherwise.
        """
        visited[vertex] = True
        rec_stack[vertex] = True

        for neighbor in self.graph[vertex]:
            if not visited[neighbor]:
                if self._has_cycle_util(neighbor, visited, rec_stack):
                    return True
            elif rec_stack[neighbor]:
                return True

        rec_stack[vertex] = False
        return False

    def _has_cycle_recursive(self):
        # visited is a dictionary that keeps track of the vertices that have been visited
        visited = {vertex: False for vertex in self.graph}
        # rec_stack is a dictionary that keeps track of the vertices that are currently in the recursion stack
        rec_stack = {vertex: False for vertex in self.graph}

        for vertex in self.graph:
            if not visited[vertex]:
                if self._has_cycle_util(vertex, visited, rec_stack):
                    return True
        return False

    def _has_cycle_iterative(self) -> bool:
        try:
            self.topological_sort('iterative')
            return False
        except ValueError:
            return True

    def _topological_sort_util(self, vertex, visited, stack):
        """
        A utility function to perform a topological sort on a directed graph using DFS.

        Args:
            vertex: The current vertex being explored.
            visited: A dictionary that tracks whether each vertex has been visited.
            stack: A list that stores the vertices in topologically sorted order.

        This function marks the current vertex as visited, recursively visits all its unvisited neighbors,
        and then adds the current vertex to the stack, ensuring that all its dependencies are added before it.
        """
        visited[vertex] = True
        for neighbor in self.graph[vertex]:
            if not visited[neighbor]:
                self._topological_sort_util(neighbor, visited, stack)
        stack.insert(0, vertex)

    def _topological_sort_recursive(self):
        visited = {vertex: False for vertex in self.graph}
        stack = []

        for vertex in self.graph:
            if not visited[vertex]:
                self._topological_sort_util(vertex, visited, stack)

        return stack

    def _topological_sort_iterative(self) -> List[int]:
        # Initialize tracking dictionaries
        in_degree = {vertex: 0 for vertex in self.graph}

        # Calculate in-degrees of all vertices
        for vertex in self.graph:
            for neighbor in self.graph[vertex]:
                in_degree[neighbor] += 1

        # Collect all vertices with in-degree 0
        zero_in_degree = deque([v for v in self.graph if in_degree[v] == 0])
        topological_order = []

        while zero_in_degree:
            vertex = zero_in_degree.popleft()
            topological_order.append(vertex)

            # Decrease the in-degree of all neighbors
            for neighbor in self.graph[vertex]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    zero_in_degree.append(neighbor)

        if len(topological_order) != len(self.graph):
            raise ValueError("Graph has at least one cycle")

        return topological_order

    def has_cycle(self, type: Literal['iterative', 'recursive'] = 'iterative') -> bool:
        if type == 'iterative':
            return self._has_cycle_iterative()
        else:
            return self._has_cycle_recursive()

    def topological_sort(self, type: Literal['iterative', 'recursive'] = 'iterative') -> List[int]:
        if type == 'iterative':
            return self._topological_sort_iterative()
        else:
            return self._topological_sort_recursive()

    def draw(self, filename='dag_graph.jpeg'):
        import networkx as nx
        import matplotlib.pyplot as plt

        """
        Draws the DAG and saves it as a JPEG image.

        Args:
            filename: The name of the file where the image will be saved.

        This function creates a networkx DiGraph from the internal graph representation
        and uses matplotlib to save it as a JPEG image.
        """
        G = nx.DiGraph(self.graph)
        pos = nx.spring_layout(G)  # positions for all nodes
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=500,
            node_color='lightblue',
            font_size=10,
            font_weight='bold',
            arrowsize=10,
        )
        plt.title("Directed Acyclic Graph (DAG)")
        plt.savefig(filename, format='jpeg')
        plt.close()
