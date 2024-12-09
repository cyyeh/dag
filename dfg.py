from dag import DAG


class DataFlowGraph(DAG):
    def __init__(self):
        super().__init__()
        self.node_operations = {}  # Store operation for each node
        
    def add_operation(self, node_id, operation):
        """Add a node with its associated operation"""
        if not callable(operation):
            raise TypeError(f"Operation must be callable, got {type(operation)}")

        self.add_vertex(node_id)
        self.node_operations[node_id] = operation
        
    def process_data(self, input_data, start_node):
        """Process data through the graph starting from a given node"""
        # Validate start node
        if start_node not in self.graph:
            raise KeyError(f"Start node {start_node} not found in graph")

        # Get execution order through topological sort
        execution_order = self.topological_sort('iterative')
        
        # Track intermediate results
        results = {start_node: input_data}
        
        for node in execution_order:
            if node in results:  # If we have input data for this node
                # Get the operation for this node
                operation = self.node_operations[node]
                # Process the data
                result = operation(results[node])
                # Store result for current node
                results[node] = result
                # Store result for downstream nodes
                for neighbor in self.graph[node]:
                    results[neighbor] = result
                    
        return results
    

if __name__ == '__main__':
    # Create a simple data processing pipeline
    dfg = DataFlowGraph()

    # Add operations
    dfg.add_operation(1, lambda x: x * 2)          # Double the input
    dfg.add_operation(2, lambda x: x + 10)         # Add 10
    dfg.add_operation(3, lambda x: str(x))         # Convert to string

    # Add edges to define data flow
    dfg.add_edge(1, 2)  # Output of operation 1 goes to operation 2
    dfg.add_edge(2, 3)  # Output of operation 2 goes to operation 3

    # Process data
    results = dfg.process_data(5, start_node=1)
    print(results)
    # Results would show the data transformation: 5 -> 10 -> 20 -> "20"
