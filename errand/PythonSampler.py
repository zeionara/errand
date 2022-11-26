from random import randint, seed as seed_
from typing import Tuple

from .SamplingMethod import SamplingMethod
from .SamplingApproach import SamplingApproach

from .Sampler import Sampler


class PythonSampler(Sampler):
    lcg_multiplier = 25214903917
    lcg_increment = 11
    lcg_modulus = 281474976710656

    def __init__(self):
        self.last_lcg_state = 17

    def _lcg_randint(self, modulus: int):
        self.last_lcg_state = (self.last_lcg_state * self.lcg_multiplier + self.lcg_increment) % self.lcg_modulus

        return self.last_lcg_state % modulus

    def sample_default_by_looping(self, min_: int, max_: int, excluded: Tuple[int]):
        while True:
            number = randint(min_, max_)
            if number not in excluded:
                return number

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
            raise ValueError(f'Sampling method {sampling_method.value} is not supported for approach {sampling_approach.value}')
        if sampling_approach == SamplingApproach.LCG:
            if sampling_method == SamplingMethod.LOOPING:
                return self.sample_lcg_by_looping
            raise ValueError(f'Sampling method {sampling_method.value} is not supported for approach {sampling_approach.value}')
        raise ValueError(f'Sampling approach {sampling_approach.value} is not supported')

    def seed(self, seed: int):
        self.last_lcg_state = seed
        seed_(seed)
