from itertools import product
from typing import Tuple


class Parameter:
    def __init__(self, min_: int, max_: int, excluded: Tuple[int]):
        assert min_ < max_, 'Min value must be less than max'
        assert all(min_ <= item <= max_ for item in excluded), 'Each excluded value must be in the interval between min and max'

        self.min_ = min_
        self.max_ = max_
        self.excluded = excluded

    def __str__(self):
        return f'{self.min_} {self.max_} {self.excluded}'


class ParameterGrid:
    def __init__(self, parameters: Tuple[Parameter]):
        self.parameters = parameters

    @staticmethod
    def from_range(mins: Tuple[int], maxs: Tuple[int], excluded: Tuple[Tuple[int]]):
        parameters = []
        for min_, max_, excluded_ in product(mins, maxs, excluded):
            parameters.append(Parameter(min_, max_, excluded_))

        return ParameterGrid(parameters)

    def __iter__(self):
        return iter(self.parameters)
