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

    def has_cycle(self):
        # visited is a dictionary that keeps track of the vertices that have been visited
        visited = {vertex: False for vertex in self.graph}
        # rec_stack is a dictionary that keeps track of the vertices that are currently in the recursion stack
        rec_stack = {vertex: False for vertex in self.graph}

        for vertex in self.graph:
            if not visited[vertex]:
                if self._has_cycle_util(vertex, visited, rec_stack):
                    return True
        return False

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

    def topological_sort(self):
        visited = {vertex: False for vertex in self.graph}
        stack = []

        for vertex in self.graph:
            if not visited[vertex]:
                self._topological_sort_util(vertex, visited, stack)

        return stack

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
