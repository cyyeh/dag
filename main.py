import random

from dag import DAG


def main():
    # Create a new DAG instance
    dag = DAG()

    num_vertices = 8
    vertices = [f'V{i}' for i in range(num_vertices)]

    # Randomly add edges to form a DAG
    for i in range(num_vertices):
        from_vertex = vertices[i]
        # Ensure we only add edges to vertices with a higher index to maintain acyclic property
        for j in range(i + 1, num_vertices):
            to_vertex = vertices[j]
            # Randomly decide whether to add an edge
            if random.choice([True, False]):
                dag.add_edge(from_vertex, to_vertex)

    assert not dag.has_cycle()

    print(f'Topological sort: {dag.topological_sort()}')

    # Draw the DAG and save it as a JPEG image
    dag.draw('sample_dag.jpeg')

if __name__ == "__main__":
    main()
