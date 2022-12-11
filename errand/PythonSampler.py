from random import randint, seed as seed_
from typing import Tuple

from .SamplingMethod import SamplingMethod
from .SamplingApproach import SamplingApproach

from .Sampler import Sampler


class PythonSampler(Sampler):
    lcg_multiplier = 25214903917
    lcg_increment = 11
    lcg_modulus = 281474976710656

    def __init__(self, seed: int = None):
        if seed is not None:
            self.seed(seed)
        else:
            self.last_lcg_state = 17

    def _lcg_randint(self, modulus: int):
        self.last_lcg_state = (self.last_lcg_state * self.lcg_multiplier + self.lcg_increment) % self.lcg_modulus

        return self.last_lcg_state % modulus

    def sample_default_by_looping(self, min_: int, max_: int, excluded: Tuple[int]):
        while True:
            number = randint(min_, max_)
            if number not in excluded:
                return number

    def sample_default_by_shifting(self, min_: int, max_: int, excluded: Tuple[int]):
        sorted_excluded_values = sorted(set(excluded))
        n_excluded_values = len(sorted_excluded_values)

        min_sampled_value = 0
        max_sampled_value = max_ - min_
        sorted_excluded_values = tuple(value - min_ for value in sorted_excluded_values)
        max_shifted_sampled_value = max_sampled_value - n_excluded_values

        smallest_excluded_value = sorted_excluded_values[0]
        largest_excluded_value = sorted_excluded_values[-1]

        sampled_value = randint(min_sampled_value, max_shifted_sampled_value)

        # print('-- Sampling from', min_sampled_value, max_shifted_sampled_value, 'excluding', excluded)
        # print('-- Sampled value', sampled_value)

        if sampled_value < smallest_excluded_value:
            # print('-- small value')
            return min_ + sampled_value

        if sampled_value > largest_excluded_value - n_excluded_values:
            # print('-- large value')
            return min_ + sampled_value + n_excluded_values

        left_bound = 0
        right_bound = n_excluded_values - 1

        # print('-- Left bound =', left_bound, '; right bound =', right_bound)

        while left_bound + 1 < right_bound:
            middle_point = (left_bound + right_bound) // 2

            if sorted_excluded_values[middle_point] - (middle_point + 1) < sampled_value:
                left_bound = middle_point
            else:
                right_bound = middle_point
            # print('-- Updated left bound =', left_bound, '; right bound =', right_bound)

        return min_ + sampled_value + left_bound + 1

    def sample_lcg_by_looping(self, min_: int, max_: int, excluded: Tuple[int]):
        diff = max_ - min_ + 1
        while True:
            number = min_ + self._lcg_randint(diff)
            if number not in excluded:
                return number

    def get_sampling_function(self, sampling_method: SamplingMethod, sampling_approach: SamplingApproach):
        if sampling_approach == SamplingApproach.DEFAULT:
            if sampling_method == SamplingMethod.LOOPING:
                return self.sample_default_by_looping
            if sampling_method == SamplingMethod.SHIFTING:
                return self.sample_default_by_shifting
            raise ValueError(f'Sampling method {sampling_method.value} is not supported for approach {sampling_approach.value}')
        if sampling_approach == SamplingApproach.LCG:
            if sampling_method == SamplingMethod.LOOPING:
                return self.sample_lcg_by_looping
            raise ValueError(f'Sampling method {sampling_method.value} is not supported for approach {sampling_approach.value}')
        raise ValueError(f'Sampling approach {sampling_approach.value} is not supported')

    def seed(self, seed: int):
        self.last_lcg_state = seed
        seed_(seed)
