from typing import Tuple

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame, MultiIndex

from .Experiment import Experiment
from .ParameterGrid import ParameterGrid
from .Unit import Unit


class Evaluator:
    def __init__(self, experiments: Tuple[Experiment], n_repetitions: int = 1, seeds: Tuple[int] = None):
        self.experiments = experiments
        self.n_repetitions = n_repetitions
        self.seeds = seeds

    def visualize(self, x: Tuple[int], y: Tuple[float], label: Tuple[str], unit: Unit, xlabels: Tuple[str]):
        sns.set_style('darkgrid')

        plot = sns.lmplot(DataFrame({'x': x, 'y': y, 'experiment label': label}), x = 'x', y = 'y', hue = 'experiment label', order = 3, ci = 95)

        plt.tight_layout()
        plt.xticks(rotation = 10)

        plot.set(xlabel = 'parameters', ylabel = f'execution time ({unit.value})', title = 'Random number generation time')
        plot.fig.set_size_inches(16, 8)
        # plot.set(yscale = 'log')
        # plot.set(xticklabels = xlabels)
        plot.set(xticks = range(len(xlabels)))
        plot.set_xticklabels(xlabels)

        min_y = min(y)
        max_y = max(y)
        inc_y = (max_y - min_y) / 20
        yticks = np.arange(min_y, max_y + inc_y, inc_y)
        plot.set(yticks = yticks)

        sns.move_legend(plot, 'upper right')
        # sns.move_legend(plot, 'upper left', bbox_to_anchor = (1, 1))

        return plot

    def evaluate(self, n: int, grid: ParameterGrid, unit: Unit = Unit.SECOND):
        column_names = []
        data = []

        x = []
        y = []
        label = []
        xlabels = []

        is_first_experiment = True
        for experiment in self.experiments:
            # print(experiment.label)
            means = []
            stds = []
            results = []
            # x = []
            for parameter in grid:
                result = experiment.run(n, parameter.min_, parameter.max_, parameter.excluded, self.n_repetitions, self.seeds, unit)
                means.append(np.mean(result))
                stds.append(np.std(result))
                results.append(result)
                for _ in range(self.n_repetitions if self.seeds is None else len(self.seeds) * self.n_repetitions):
                    x.append(parameter.id)
                if is_first_experiment:
                    xlabels.append(str(parameter))

            if is_first_experiment:
                is_first_experiment = False

            column_names.append((experiment.label, 'mean'))
            data.append(means)

            column_names.append((experiment.label, 'std'))
            data.append(stds)

            y.extend(n_value := np.reshape(np.array(results), (-1, )).tolist())
            label.extend([experiment.label for _ in range(len(n_value))])

        return DataFrame(zip(*data), columns = MultiIndex.from_tuples(column_names)), self.visualize(x, y, label, unit, xlabels)
