from typing import Tuple

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
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

        x = []
        y = []
        label = []

        for experiment in self.experiments:
            # print(experiment.label)
            means = []
            stds = []
            results = []
            # x = []
            xlabels = []
            for parameter in grid:
                result = experiment.run(n, parameter.min_, parameter.max_, parameter.excluded, self.n_repetitions, self.seeds)
                means.append(np.mean(result))
                stds.append(np.std(result))
                results.append(result)
                for _ in range(self.n_repetitions if self.seeds is None else len(self.seeds) * self.n_repetitions):
                    x.append(parameter.max_)
                xlabels.append(str(parameter))

            column_names.append((experiment.label, 'mean'))
            data.append(means)

            column_names.append((experiment.label, 'std'))
            data.append(stds)

            # y = np.reshape(np.array(results), (-1, ))
            y.extend(n_value := np.reshape(np.array(results), (-1, )).tolist())
            label.extend([experiment.label for _ in range(len(n_value))])

            # fig, ax = plt.subplots()
            # fig.set_size_inches(11, 6)

            # tmpdf = DataFrame({'x': x, 'y': y})
            # print(tmpdf)

            # plot = sns.regplot(x = x, y = y, order = 3, label = experiment.label)

            # plot = sns.lmplot(x = 'x', y = 'y', data = DataFrame({'x': x, 'y': y}), order = 2)
            # plot = sns.regplot(x = x, y = y, ax = ax)

            # plot.set(xlabel = 'parameters', ylabel = 'execution time (seconds)', title = 'Random number generation time')
            # plot.set_xticklabels(xlabels)
            # plt.xticks(rotation = 10)
            # plt.tight_layout()
            # plot.get_figure().savefig('plot.png')

            # dd

            # print(y.shape)
            # print(len(x))

        sns.set_style('darkgrid')
        # sns.set(rc = {'figure.figsize': (32, 16)})

        plot = sns.lmplot(DataFrame({'x': x, 'y': y, 'experiment label': label}), x = 'x', y = 'y', hue = 'experiment label', order = 3)
        plot.set(xlabel = 'parameters', ylabel = 'execution time (seconds)', title = 'Random number generation time')
        # plot.set_xticklabels(xlabels)
        plt.xticks(rotation = 10)
        plt.tight_layout()
        plot.fig.set_size_inches(16, 8)
        plot.set(yscale = 'log')
        plot.set(xticklabels = xlabels)
        sns.move_legend(plot, 'upper left', bbox_to_anchor = (1, 1))
        plot.savefig('plot.png')

        return DataFrame(zip(*data), columns = MultiIndex.from_tuples(column_names))

    # def evaluate(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
    #     for experiment in self.experiments:
    #         result = experiment.run(n, min_, max_, excluded, self.n_repetitions, self.seeds)
    #         print(f'{experiment.label}: {np.mean(result)} +- {np.std(result)}')
