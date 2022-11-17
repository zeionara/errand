import os
import time

from random import randint
from typing import Tuple

import ctypes

from click import group, argument

import numpy as np

RANDEER_LIBRARY_PATH = os.environ.get('RANDEER_LIBRARY_PATH', '/usr/lib/librandeer.so')


class RandeerAdapter:
    def __init__(self, path: str):
        lib = ctypes.cdll.LoadLibrary(path)
        lib.sample.argtypes = [ctypes.c_int64]
        lib.sample_by_looping.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_n_by_looping.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]

        self.lib = lib

    def sample_by_looping(self, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_by_looping(min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_n_by_looping(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_n_by_looping(n, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_by_looping_python(self, min_: int, max_: int, excluded: Tuple[int]):
        while True:
            number = randint(min_, max_)
            if number not in excluded:
                return number


class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, sample: callable, n_samples: int):
        start_time = time.time()

        for _ in range(n_samples):
            sample()

        print(f'Sampled {n_samples} samples in {time.time() - start_time} seconds')


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

    evaluator.evaluate(lambda: randeer.sample_by_looping(min_, max_, excluded), n)
    evaluator.evaluate(lambda: randeer.sample_by_looping_python(min_, max_, excluded), n)
    evaluator.evaluate(lambda: randeer.sample_n_by_looping(n, min_, max_, excluded), 1)

    # for _ in range(100):
    #     print(randeer.sample_by_looping(10, 20, (12, 13)))


if __name__ == '__main__':
    main()
