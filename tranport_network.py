
import itertools
from collections import defaultdict
import sympy as sp
from graph import Graph
import numpy as np

class Transport_network:

    def __init__(self, g, num_vertices=10, seed=42):
        self.graph = Graph( num_vertices=num_vertices)
        # self.graph = g
        self.graph.draw_graph()
        self.pairs_start_finish = {} #нужно ручками задавать, ждет {(O_1,D_1): плотоность потока_1,(O_2,D_2):плотность потока_2,...}
        self.pairs_and_routs = {} #словарь пара: маршруты
        self.rng = np.random.RandomState(seed)
        self.dict_flows_on_routs = {} #номер маршрута : {'rout': j, 'flow': X_{}}
        self.dict_edges = {i:j for i,j in enumerate(self.graph.graph.edges())}
        self.dict_edges_reversed = {j:i for i,j in self.dict_edges.items()}
        self.dict_delayed_funcs = {} #руками задавать максимумы и минимумы по коэффициентам
        self.c_matrix = []
        self.arr_flows = [] #потом это нампи массив
        self.dict_pairs_num_routs = defaultdict(list) #пара (O_i,D_i): [номера маршрутов]
        self.rho = sp.symbols('rho', real=True, nonnegative=True)
        self.dict_integrals = {}


    def choose_pairs(self, pairs_dict):
        self.pairs_start_finish = pairs_dict

    def get_pairs_and_routs(self):
        res_dict = {}
        for i in self.pairs_start_finish.keys():
            res_dict[i] = self.graph.find_all_paths(i[0], i[1])
        self.pairs_and_routs = res_dict
        return res_dict

    def generate_flow_on_routs(self):
        dict_flows = {}
        counter = 0
        arr = []
        print(self.pairs_and_routs)
        for i in self.pairs_and_routs.keys():
            for j in self.pairs_and_routs[i]:
                f = self.rng.randint(1, 100)
                dict_flows[counter] = {'rout': j, 'flow': sp.symbols(f'X_{counter}', real=True, nonnegative=True)}
                self.dict_pairs_num_routs[i].append(counter)
                arr.append(dict_flows[counter]['flow'])
                counter += 1
        self.dict_flows_on_routs = dict_flows
        self.arr_flows = np.array(arr)
        return dict_flows

    def build_C_matrix(self):
        p = len(self.dict_edges)  # дуги - строки
        s = len(self.dict_flows_on_routs)  # маршруты - стобцы
        mat = np.zeros((p, s))
        print(self.dict_edges)
        for i, j in self.dict_edges.items():
            for k in range(s):
                if j in set(itertools.pairwise(self.dict_flows_on_routs[k]['rout'])):
                    mat[i, k] = 1
        self.c_matrix = mat
        return mat

    def set_delay_functions(self, a_1, a_2, b_1, b_2):
        a = np.round(self.rng.uniform(a_1, a_2, len(self.dict_edges)))
        b = np.round(self.rng.uniform(b_1, b_2, len(self.dict_edges)))
        self.dict_delayed_funcs = {
            e: a[e] + b[e] * self.rho
            for e in self.dict_edges
        }
        return self.dict_delayed_funcs

    def get_flow_on_edge(self, i):
        print(i, np.sum(self.c_matrix[i,:] * self.arr_flows))
        return np.sum(self.c_matrix[i,:] * self.arr_flows)

    def time_on_rout(self, n, flow_vector):
        edge_flows = self.c_matrix @ flow_vector
        edge_times = np.array([
            float(self.dict_delayed_funcs[i].subs(self.rho, edge_flows[i]))
            for i in self.dict_edges
        ])
        return np.sum(self.c_matrix[:,n] * edge_times)

    def time_from_to(self, O, D):
        return np.sum(np.array([self.time_on_rout(i) for i in self.dict_pairs_num_routs[(O,D)]]))

    def get_timef_on_rout_integrate(self):
        self.dict_integrals = {i : sp.integrate(self.dict_delayed_funcs[i], (self.rho, 0, self.rho)) for i in self.dict_delayed_funcs.keys()}
        return self.dict_integrals
