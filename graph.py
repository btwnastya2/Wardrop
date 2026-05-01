import networkx as nx
import random
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.graph = self.build_transport_graph()
        # self.graph = g
        self.out_adj = {node: list(self.graph.successors(node)) for node in self.graph.nodes()}
        self.edges = {i:j for i,j in enumerate(self.graph.edges())}

    def build_transport_graph(self, k=2, p=0.3, seed=42):
        random.seed(seed)

        G_undir = nx.connected_watts_strogatz_graph(self.num_vertices, k, p, seed=seed)

        G = nx.DiGraph()

        for u, v in G_undir.edges():
            if random.random() < 0.5:
                G.add_edge(u, v)
            else:
                G.add_edge(v, u)

        # добавим немного случайных рёбер
        extra_edges = int(self.num_vertices * 0.5)
        for _ in range(extra_edges):
            u, v = random.sample(list(G.nodes()), 2)
            if not G.has_edge(u, v) and not G.has_edge(v, u):
                G.add_edge(u, v)

        return G

    def draw_graph(self):
        pos = nx.spring_layout(self.graph, k=5, iterations=50)  # k - расстояние, iterations - точность
        plt.figure(figsize=(8, 6))
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue',
                edge_color='black', arrows=True, arrowsize=20, font_size=10)
        plt.title("Случайный ориентированный граф")
        plt.show()

    def find_all_paths(self, start, end, path=[]):  # DFS
        path = path + [start]
        if start == end:
            return [path]

        if start not in self.out_adj:
            return []

        paths = []
        for node in self.out_adj[start]:
            if node not in path:
                new_paths = self.find_all_paths(node, end, path)
                for i in new_paths:
                    paths.append(i)

        return paths




