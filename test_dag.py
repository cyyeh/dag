import pytest
from dag import DAG

def test_add_vertex():
    dag = DAG()
    dag.add_vertex('A')
    assert 'A' in dag.graph
    assert dag.graph['A'] == []

def test_add_edge():
    dag = DAG()
    dag.add_edge('A', 'B')
    assert 'A' in dag.graph
    assert 'B' in dag.graph
    assert 'B' in dag.graph['A']

def test_has_cycle():
    dag = DAG()
    dag.add_edge('A', 'B')
    dag.add_edge('B', 'C')
    assert not dag.has_cycle()
    dag.add_edge('C', 'A')
    assert dag.has_cycle()

def test_topological_sort():
    dag = DAG()
    dag.add_edge('A', 'B')
    dag.add_edge('B', 'C')
    dag.add_edge('A', 'C')
    assert dag.topological_sort() in [['A', 'B', 'C'], ['A', 'C', 'B']]

if __name__ == "__main__":
    pytest.main()
