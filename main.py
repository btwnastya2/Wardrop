from tranport_network import Transport_network
from for_solution import Solution
network = Transport_network(10)
network.choose_pairs([(8,5),(1,9)]) #типо L пар вершин
network.choose_pairs({(8,5): 100,(1,9): 30, (2,9): 10})
network.get_pairs_and_routs() #находим между ними маршруты
network.generate_flow_on_routs()

mat = network.build_C_matrix()
network.set_delay_functions(1,20,1,20)

print(network.dict_flows_on_routs)
print(network.dict_delayed_funcs)

s = Solution(network)
res = s.optimize('trust-constr')
# for i, (route, var) in enumerate(res.vars.items()):
#         print(var)