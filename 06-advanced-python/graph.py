from collections import deque


class Graph:
    __slots__ = {'graph'}

    def __init__(self, graph: dict):
        self.graph = graph

    def __iter__(self):
        return GraphIterator(self)


class GraphIterator:
    __slots__ = {
        'graph',
        'visited',
        'queue',
        'non_visited'
    }

    def __init__(self, source: Graph):
        self.graph = source.graph
        self.non_visited = list(self.graph.keys())
        self.visited, self.queue = [], deque(self.non_visited[0])
        while self.non_visited:
            if not self.queue:
                self.queue.append(self.non_visited[0])
            vertex = self.queue.popleft()
            if vertex not in self.visited:
                self.visit_node(vertex)
            for neighbour in self.graph[vertex]:
                if neighbour not in self.visited:
                    self.visit_node(neighbour)
                    self.queue.append(neighbour)

    def visit_node(self, node):
        self.visited.append(node)
        self.non_visited.remove(node)

    def __next__(self):
        try:
            return self.visited.pop(0)
        except IndexError:
            raise StopIteration


if __name__ == '__main__':
    E = {'A': ['B', 'C', 'D'], 'B': ['C'], 'C': ['E', 'G'], 'E': [], 'G': [], 'D': [], 'K': ['O'], 'O': ['I'], 'I': []}
    graph = Graph(E)
    for i in graph:
        print(i)
