import pytest
from dfg import DataFlowGraph


def test_simple_linear_flow():
    """Test a simple linear flow of operations"""
    dfg = DataFlowGraph()
    
    # Create linear pipeline: double -> add 10 -> to string
    dfg.add_operation(1, lambda x: x * 2)
    dfg.add_operation(2, lambda x: x + 10)
    dfg.add_operation(3, lambda x: str(x))
    
    dfg.add_edge(1, 2)
    dfg.add_edge(2, 3)
    
    results = dfg.process_data(5, start_node=1)
    print(results)
    assert results[3] == "20"  # 5 -> 10 -> 20 -> "20"


def test_diamond_shape_flow():
    """Test a diamond-shaped graph with parallel paths"""
    dfg = DataFlowGraph()
    
    # Create diamond-shaped graph
    dfg.add_operation(1, lambda x: x * 2)      # 5 -> 10
    dfg.add_operation(2, lambda x: x + 5)      # 10 -> 15
    dfg.add_operation(3, lambda x: x ** 2)     # 10 -> 100
    dfg.add_operation(4, lambda x: str(x))     # Last processed result -> string
    
    dfg.add_edge(1, 2)
    dfg.add_edge(1, 3)
    dfg.add_edge(2, 4)
    dfg.add_edge(3, 4)
    
    results = dfg.process_data(5, start_node=1)
    # Note: Current implementation will take the last processed input
    assert results[4] in ["15", "100"]


def test_single_node():
    """Test processing a graph with a single node"""
    dfg = DataFlowGraph()
    dfg.add_operation(1, lambda x: x * 2)
    results = dfg.process_data(5, start_node=1)
    assert results[1] == 10


def test_error_propagation():
    """Test that errors in operations are properly propagated"""
    dfg = DataFlowGraph()
    
    def failing_operation(x):
        raise ValueError("Operation failed")
    
    dfg.add_operation(1, lambda x: x * 2)
    dfg.add_operation(2, failing_operation)
    
    dfg.add_edge(1, 2)
    
    with pytest.raises(ValueError, match="Operation failed"):
        dfg.process_data(5, start_node=1)


def test_invalid_start_node():
    """Test processing with an invalid start node"""
    dfg = DataFlowGraph()
    dfg.add_operation(1, lambda x: x * 2)
    
    with pytest.raises(KeyError):
        dfg.process_data(5, start_node=2)  # Node 2 doesn't exist


def test_cycle_detection():
    """Test that cycles are properly detected"""
    dfg = DataFlowGraph()
    
    dfg.add_operation(1, lambda x: x * 2)
    dfg.add_operation(2, lambda x: x + 1)
    
    dfg.add_edge(1, 2)
    dfg.add_edge(2, 1)  # Creates a cycle
    
    with pytest.raises(ValueError, match="Graph has at least one cycle"):
        dfg.process_data(5, start_node=1)


def test_multiple_paths_same_result():
    """Test that different valid topological sorts produce the same result"""
    dfg = DataFlowGraph()
    
    # Create a graph where nodes 2 and 3 can be processed in any order
    dfg.add_operation(1, lambda x: x * 2)          # 5 -> 10
    dfg.add_operation(2, lambda x: x + 1)          # 10 -> 11
    dfg.add_operation(3, lambda x: x * 3)          # 10 -> 30
    dfg.add_operation(4, lambda x: str(x))         # Last processed -> string
    
    dfg.add_edge(1, 2)
    dfg.add_edge(1, 3)
    
    # Run multiple times to potentially get different topological sorts
    results1 = dfg.process_data(5, start_node=1)
    results2 = dfg.process_data(5, start_node=1)
    
    # Results should be consistent across runs
    assert results1 == results2


def test_operation_type_checking():
    """Test that operations must be callable"""
    dfg = DataFlowGraph()
    
    with pytest.raises((TypeError, AttributeError)):
        dfg.add_operation(1, "not a function")


if __name__ == '__main__':
    pytest.main()
