from typing import Tuple

import numpy as np
from pandas import DataFrame, MultiIndex

from .Experiment import Experiment
from .ParameterGrid import ParameterGrid


class Evaluator:
    def __init__(self, experiments: Tuple[Experiment], n_repetitions: int = 1, seeds: Tuple[int] = None):
        self.experiments = experiments
        self.n_repetitions = n_repetitions
        self.seeds = seeds

    def evaluate(self, n: int, grid: ParameterGrid):
        column_names = []
        data = []

        for experiment in self.experiments:
            # print(experiment.label)
            means = []
            stds = []
            for parameter in grid:
                result = experiment.run(n, parameter.min_, parameter.max_, parameter.excluded, self.n_repetitions, self.seeds)
                means.append(np.mean(result))
                stds.append(np.std(result))

            column_names.append((experiment.label, 'mean'))
            data.append(means)

            column_names.append((experiment.label, 'std'))
            data.append(stds)

        return DataFrame(zip(*data), columns = MultiIndex.from_tuples(column_names))

    # def evaluate(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
    #     for experiment in self.experiments:
    #         result = experiment.run(n, min_, max_, excluded, self.n_repetitions, self.seeds)
    #         print(f'{experiment.label}: {np.mean(result)} +- {np.std(result)}')
