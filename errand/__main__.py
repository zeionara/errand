import os
import time
from enum import Enum

from random import randint
from typing import Tuple

import ctypes

from click import group, argument

import numpy as np

RANDEER_LIBRARY_PATH = os.environ.get('RANDEER_LIBRARY_PATH', '/usr/lib/librandeer.so')
# RANDEER_LIBRARY_PATH = os.environ.get('RANDEER_LIBRARY_PATH', '/usr/lib/libmeager.so')


class RandomizerType(Enum):
    DEFAULT_LOOPING = 0


class RandeerAdapter:
    def __init__(self, path: str):
        lib = ctypes.cdll.LoadLibrary(path)
        lib.sample.argtypes = [ctypes.c_int64]
        lib.seed.argtypes = [ctypes.c_int64]
        lib.sample_by_looping.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_by_looping_randomizer.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_by_looping_lcg.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_n_by_looping_without_init.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_n_by_looping_with_init.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]

        lib.init.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64]
        lib.init_in_interval_excluding_task.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.next.argtypes = [ctypes.c_int64]

        self.lib = lib

    def init(self, id_: int, seed: int, type_: RandomizerType):
        return self.lib.init(id_, seed, type_.value)

    def init_in_interval_excluding_task(self, id_: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.init_in_interval_excluding_task(id_, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def next(self, id_: int):
        return self.lib.next(id_)

    def seed(self, seed: int):
        return self.lib.seed(seed)

    def sample_by_looping(self, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_by_looping(min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_by_looping_randomizer(self, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_by_looping_randomizer(min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_by_looping_lcg(self, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_by_looping_lcg(min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_n_by_looping_without_init(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_n_by_looping_without_init(n, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_n_by_looping_with_init(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_n_by_looping_with_init(n, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_by_looping_python(self, min_: int, max_: int, excluded: Tuple[int]):
        while True:
            number = randint(min_, max_)
            if number not in excluded:
                return number


class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, sample: callable, n_samples: int, label: str):
        start_time = time.time()

        for _ in range(n_samples):
            sample()

        print(f'{label:100s} Sampled {n_samples} samples in {time.time() - start_time} seconds')


@group()
def main():
    pass


@main.command()
@argument('number', type = int, default = 17)
def randomize(number: int):
    randeer = RandeerAdapter(RANDEER_LIBRARY_PATH)
    evaluator = Evaluator()

    min_ = 10
    max_ = 20
    excluded = (11, 12, 13, 14, 15, 16, 17, 18, 19)
    n = 100000

    randomizer_id = 17
    seed = 17

    randeer.seed(seed)

    # for _ in range(10):
    #     print(randeer.sample_by_looping(100, 150, (110, 130)))
    #     print(randeer.sample_by_looping_lcg(100, 150, (110, 130)))

    randeer.init(randomizer_id, seed, RandomizerType.DEFAULT_LOOPING)
    randeer.init_in_interval_excluding_task(randomizer_id, min_, max_, excluded)

    evaluator.evaluate(lambda: randeer.sample_by_looping(min_, max_, excluded), n, 'looping in python, generation in c++')
    evaluator.evaluate(lambda: randeer.sample_by_looping_randomizer(min_, max_, excluded), n, 'looping randomizer in python, generation in c++')
    evaluator.evaluate(lambda: randeer.next(randomizer_id), n, 'looping contextualized randomizer in python, generation in c++')
    evaluator.evaluate(lambda: randeer.sample_by_looping_lcg(min_, max_, excluded), n, 'looping in python, generation in c++ using custom function')
    evaluator.evaluate(lambda: randeer.sample_by_looping_python(min_, max_, excluded), n, 'looping in python, generation in python')
    evaluator.evaluate(lambda: randeer.sample_n_by_looping_without_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ without init')
    evaluator.evaluate(lambda: randeer.sample_n_by_looping_with_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ with init')

    # for _ in range(100):
    #     print(randeer.sample_by_looping(10, 20, (12, 13)))


if __name__ == '__main__':
    main()
