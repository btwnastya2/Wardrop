import numpy as np
import itertools
from graph import Graph

rng = np.random.RandomState(42)
G = Graph(10)
routs = G.find_all_paths(8,5)
G.draw_graph()
print(routs)
routs_dict = {i:(routs[i], rng.randint(1,100)) for i in range(len(routs))}
print(routs_dict)

d_edges = {i:j for i,j in enumerate(G.graph.edges())}
print(d_edges)
p = len(d_edges) #дуги - строки
s = len(routs) #маршруты - стобцы
mat = np.zeros((p,s))
for i,j in d_edges.items():
  for k in range(s):
    if j in set(itertools.pairwise(routs_dict[k][0])):
      mat[i,k] = 1
print(mat)