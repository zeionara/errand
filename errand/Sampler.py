from abc import ABC, abstractmethod

from typing import Tuple


class Sampler(ABC):

    @abstractmethod
    def get_sampling_function(self, *args, **kwargs):
        pass

    def sample(
        self, n: int, min_: int, max_: int, excluded: Tuple[int],
        *args, **kwargs
    ):
        sample = self.get_sampling_function(*args, **kwargs)

        for _ in range(n):
            sample(min_, max_, excluded)

    @abstractmethod
    def seed(
        self, seed: int
    ):
        pass
