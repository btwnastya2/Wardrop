import pandas as pd
import networkx as nx

df = pd.read_excel('graph.xlsx', header=None)
pairs = list(zip(df.iloc[:, 0], df.iloc[:, 1]))
vertexes = set()
for i,j in pairs:
    vertexes.add(i)
    vertexes.add(j)

print(pairs)
print(vertexes)

G = nx.DiGraph()
G.add_edges_from(pairs)

from tranport_network import Transport_network
from for_solution import Solution
from graph import Graph
# g_1 = Graph(26, G)

network = Transport_network(G, 10)
# network.graph = g_1
# network.choose_pairs([(8,5),(1,9)]) #типо L пар вершин
network.choose_pairs({(1,26): 100})
network.get_pairs_and_routs() #находим между ними маршруты
network.generate_flow_on_routs()

mat = network.build_C_matrix()
network.set_delay_functions(10,100,1,20)

print(network.dict_flows_on_routs)
print(network.dict_delayed_funcs)

s = Solution(network)
res = s.optimize()
print(res.message)