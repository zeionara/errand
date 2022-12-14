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
        return f'min={self.min_} max={self.max_} excluded={",".join(map(str, self.excluded))}'


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

    def __iter__(self):
        return iter(self.parameters)
