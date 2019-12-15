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
    }

    def __init__(self, source: Graph):
        self.graph = source.graph
        self.visited, self.queue = [], deque(tuple(self.graph.keys()))
        while self.queue:
            vertex = self.queue.popleft()
            if vertex not in self.visited:
                self.visited.append(vertex)
            for neighbour in self.graph[vertex]:
                if neighbour not in self.visited:
                    self.visited.append(neighbour)
                    self.queue.appendleft(neighbour)


    def __next__(self):
        try:
            return self.visited.pop(0)
        except IndexError:
            raise StopIteration


if __name__ == '__main__':
    E = {'A': ['B', 'C', 'D'], 'B': ['C'], 'C': ['E', 'G'], 'E': [], 'G': [], 'D': [], 'K': ['O'], 'O': []}
    graph = Graph(E)
    for i in graph:
        print(i)
