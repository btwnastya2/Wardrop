import sympy as sp
import numpy as np
from scipy.optimize import minimize



class Solution:
    def __init__(self, tr_network):
        self.tr_network = tr_network
        self.vars = {i: j['flow'] for i,j in self.tr_network.dict_flows_on_routs.items()}

    def build_Func(self):
        d = self.tr_network.get_timef_on_rout_integrate()
        print('cловарь интегралов')
        print(d)
        return sum(d[i].subs(self.tr_network.rho, self.tr_network.get_flow_on_edge(i)) for i in self.tr_network.dict_edges if i in d.keys())

    def preparing_func(self):
        f_sym = self.build_Func()
        v = [j for i,j in sorted(self.vars.items(), key=lambda x: x[0])]
        print(f'Порядок переменных:{v}')
        f_num = sp.lambdify(v, f_sym, 'numpy')

        return lambda x: f_num(*x)

    def get_feasible_initial_point(self):
        s = len(self.vars.keys())  # общее количество маршрутов
        x0 = np.zeros(s)

        for goal, routs_idx in self.tr_network.dict_pairs_num_routs.items():
            chi = self.tr_network.pairs_start_finish[goal]  # общий поток для этой пары

            if len(routs_idx) > 0:
                # равномерно распределяем общий поток по маршрутам этой пары
                x0[routs_idx] = chi / len(routs_idx)

        return x0

    def optimize(self, method_use):
        n_vars = len(self.vars)
        constr = []
        b = [(0, None) for _ in range(n_vars)]

        for goal, routs_idx in self.tr_network.dict_pairs_num_routs.items():
            ch = self.tr_network.pairs_start_finish[goal]
            def eq_constraint(X, indices=routs_idx, demand=ch):
                return np.sum(X[indices]) - demand

            constr.append({'type': 'eq', 'fun': eq_constraint})

        func = self.preparing_func()

        res = minimize(
            fun=func,
            x0=self.get_feasible_initial_point(),
            bounds=b,
            constraints=constr,
            method=method_use
        )

        print("Статус оптимизации:", res.success)
        print("Значение целевой функции:", res.fun)
        print("Оптимальные значения переменных:")
        for i, val in enumerate(res.x):
            print(f"  x[{i}] = {val:.6f}")

        for i in self.vars.keys():
            print(self.tr_network.time_on_rout(i, res.x))

        return res





