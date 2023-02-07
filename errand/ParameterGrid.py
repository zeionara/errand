import random
import math

from itertools import product
from typing import Tuple


class Parameter:
    def __init__(self, min_: int, max_: int, excluded: Tuple[int], id_ = None):
        assert min_ < max_, 'Min value must be less than max'
        assert all(min_ <= item <= max_ for item in excluded), 'Each excluded value must be in the interval between min and max'

        self.min_ = min_
        self.max_ = max_
        self.excluded = excluded

        self.id = id_

    def __str__(self):
        # return f'min={self.min_} max={self.max_} excluded={",".join(map(str, self.excluded))}'
        return f'min={self.min_} max={self.max_} excluding {len(self.excluded)} values'


class ParameterGrid:
    def __init__(self, parameters: Tuple[Parameter]):
        for i, parameter in enumerate(parameters):
            parameter.id = i
        self.parameters = parameters

    @staticmethod
    def from_range(mins: Tuple[int], maxs: Tuple[int], excluded: Tuple[Tuple[int]]):
        parameters = []
        for min_, max_, excluded_ in product(mins, maxs, excluded):
            parameters.append(Parameter(min_, max_, excluded_))

        return ParameterGrid(parameters)

    @staticmethod
    def from_boundaries(*boundaries: tuple[tuple[int]], continuous_excluded_interval: bool = False):
        parameters = []

        for min_, max_, excluded_fraction in boundaries:
            # print(min_, max_)

            n_items = max_ - min_ + 1

            assert n_items > 0, 'There must be at least one number in the interval to generate'

            n_excluded_items = math.floor(excluded_fraction * n_items)

            # print(n_items, n_excluded_items)

            excluded = []

            if continuous_excluded_interval:
                min_excluded_interval_first_element = min_
                max_excluded_interval_first_element = max_ - n_excluded_items

                excluded_interval_first_element = random.randint(min_excluded_interval_first_element, max_excluded_interval_first_element)

                for i in range(n_excluded_items):
                    excluded.append(excluded_interval_first_element + i)

            else:
                for _ in range(n_excluded_items):
                    while (i := random.randint(min_, max_)) in excluded:
                        pass

                    excluded.append(i)

            parameters.append(Parameter(min_, max_, excluded))

            # print(min_, max_, excluded)

        return ParameterGrid(parameters)

        # dd

        # parameters = []
        # for min_, max_, excluded_ in product(mins, maxs, excluded):
        #     parameters.append(Parameter(min_, max_, excluded_))

        # return ParameterGrid(parameters)

    def __iter__(self):
        return iter(self.parameters)
