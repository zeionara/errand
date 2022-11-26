from abc import ABC, abstractmethod

from typing import Tuple
import time

import numpy as np


from .Sampler import Sampler


class Experiment(ABC):
    def __init__(self, sampler: Sampler, label: str):
        self.sampler = sampler
        self.label = label

    def run_for_one_seed(self, n_repetitions: int, run: callable, seed: int = None):
        measured_times = []

        if seed is not None:
            self.sampler.seed(seed)

        for _ in range(n_repetitions):
            start_time = time.time()

            run()

            measured_times.append(time.time() - start_time)

        return measured_times

    @abstractmethod
    def sample(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        pass

    def run(self, n: int, min_: int, max_: int, excluded: Tuple[int], nRepetitions: int = 1, seeds: Tuple[int] = None):
        if seeds is None:
            return np.array([self.run_for_one_seed(nRepetitions, lambda: self.sample(n, min_, max_, excluded))])
        return np.array(
            [
                self.run_for_one_seed(nRepetitions, lambda: self.sample(n, min_, max_, excluded), seed)
                for seed in seeds
            ]
        )
