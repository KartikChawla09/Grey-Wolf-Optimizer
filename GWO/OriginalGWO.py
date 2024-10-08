# import numpy as np
# from mealpy.optimizer import Optimizer

# class OriginalGWO(Optimizer):
#     def __init__(self, epoch=10000, pop_size=100, **kwargs):
#         """
#         Args:
#             epoch (int): maximum number of iterations, default = 10000
#             pop_size (int): number of population size, default = 100
#         """
#         super().__init__(**kwargs)
#         self.epoch = self.validator.check_int("epoch", epoch, [1, 100000])
#         self.pop_size = self.validator.check_int("pop_size", pop_size, [10, 10000])
#         self.set_parameters(["epoch", "pop_size"])
#         self.sort_flag = False

#     def evolve(self, epoch):
#         """
#         The main operations (equations) of algorithm. Inherit from Optimizer class

#         Args:
#             epoch (int): The current iteration
#         """
#         a = 2 - 2 * epoch / (self.epoch - 1)  # linearly decreased from 2 to 0
#         pop_new = []
#         for idx in range(0, self.pop_size):
#             r = np.random.rand()
#             A = 2 * a * r - a
#             C = 2 * r
#             l = np.random.uniform(-1, 1)
#             p = 0.5
#             b = 1
#             if np.random.uniform() < p:
#                 if np.abs(A) < 1:
#                     D = np.abs(
#                         C * self.g_best[self.ID_POS] - self.pop[idx][self.ID_POS]
#                     )
#                     pos_new = self.g_best[self.ID_POS] - A * D
#                 else:
#                     # x_rand = pop[np.random.np.random.randint(self.pop_size)]         # select random 1 position in pop
#                     x_rand = self.create_solution(self.problem.lb, self.problem.ub)
#                     D = np.abs(C * x_rand[self.ID_POS] - self.pop[idx][self.ID_POS])
#                     pos_new = x_rand[self.ID_POS] - A * D
#             else:
#                 D1 = np.abs(self.g_best[self.ID_POS] - self.pop[idx][self.ID_POS])
#                 pos_new = (
#                     self.g_best[self.ID_POS]
#                     + np.exp(b * l) * np.cos(2 * np.pi * l) * D1
#                 )
#             pos_new = self.amend_position(pos_new, self.problem.lb, self.problem.ub)
#             pop_new.append([pos_new, None])
#             if self.mode not in self.AVAILABLE_MODES:
#                 target = self.get_target_wrapper(pos_new)
#                 self.pop[idx] = self.get_better_solution(self.pop[idx], [pos_new, target])
#         if self.mode in self.AVAILABLE_MODES:
#             pop_new = self.update_target_wrapper_population(pop_new)
#             print(len(pop_new))
#             self.pop = self.greedy_selection_population(self.pop, pop_new)


import os
import opfunu
import numpy as np
import pandas as pd
from mealpy.optimizer import Optimizer

class OriginalWOA(Optimizer):
    """
    The original version of: Whale Optimization Algorithm (WOA)

    Links:
        1. https://doi.org/10.1016/j.advengsoft.2016.01.008

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.swarm_based.WOA import OriginalWOA
    >>>
    >>> def fitness_function(solution):
    >>>     return np.sum(solution**2)
    >>>
    >>> problem_dict1 = {
    >>>     "fit_func": fitness_function,
    >>>     "lb": [-10, -15, -4, -2, -8],
    >>>     "ub": [10, 15, 12, 8, 20],
    >>>     "minmax": "min",
    >>> }
    >>>
    >>> epoch = 1000
    >>> pop_size = 50
    >>> model = OriginalWOA(epoch, pop_size)
    >>> best_position, best_fitness = model.solve(problem_dict1)
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")

    References
    ~~~~~~~~~~
    [1] Mirjalili, S. and Lewis, A., 2016. The whale optimization algorithm.
    Advances in engineering software, 95, pp.51-67.
    """

    def __init__(self, epoch=10000, pop_size=100, **kwargs):
        """
        Args:
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
        """
        super().__init__(**kwargs)
        self.name = "OriginalWOA"
        self.epoch = self.validator.check_int("epoch", epoch, [1, 100000])
        self.pop_size = self.validator.check_int("pop_size", pop_size, [10, 10000])
        self.set_parameters(["epoch", "pop_size"])
        self.sort_flag = False

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        a = 2 - 2 * epoch / (self.epoch - 1)  # linearly decreased from 2 to 0
        pop_new = []
        for idx in range(0, self.pop_size):
            r = np.random.rand()
            A = 2 * a * r - a
            C = 2 * r
            l = np.random.uniform(-1, 1)
            p = 0.5
            b = 1
            if np.random.uniform() < p:
                if np.abs(A) < 1:
                    D = np.abs(
                        C * self.g_best[self.ID_POS] - self.pop[idx][self.ID_POS]
                    )
                    pos_new = self.g_best[self.ID_POS] - A * D
                else:
                    # x_rand = pop[np.random.np.random.randint(self.pop_size)]         # select random 1 position in pop
                    x_rand = self.create_solution(self.problem.lb, self.problem.ub)
                    D = np.abs(C * x_rand[self.ID_POS] - self.pop[idx][self.ID_POS])
                    pos_new = x_rand[self.ID_POS] - A * D
            else:
                D1 = np.abs(self.g_best[self.ID_POS] - self.pop[idx][self.ID_POS])
                pos_new = (
                    self.g_best[self.ID_POS]
                    + np.exp(b * l) * np.cos(2 * np.pi * l) * D1
                )
            pos_new = self.amend_position(pos_new, self.problem.lb, self.problem.ub)
            pop_new.append([pos_new, None])
            if self.mode not in self.AVAILABLE_MODES:
                target = self.get_target_wrapper(pos_new)
                self.pop[idx] = self.get_better_solution(
                    self.pop[idx], [pos_new, target]
                )
        if self.mode in self.AVAILABLE_MODES:
            pop_new = self.update_target_wrapper_population(pop_new)
            print(len(pop_new))
            self.pop = self.greedy_selection_population(self.pop, pop_new)