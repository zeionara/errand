import os
import time
from enum import Enum

from random import randint
from typing import Tuple

import ctypes

from statistics import mean

from click import group, argument

import numpy as np

RANDEER_LIBRARY_PATH = os.environ.get('RANDEER_LIBRARY_PATH', '/usr/lib/librandeer.so')
# RANDEER_LIBRARY_PATH = os.environ.get('RANDEER_LIBRARY_PATH', '/usr/lib/libmeager.so')


class RandomizerType(Enum):
    DEFAULT_LOOPING = 0
    JAVA_LOOPING = 1


last_lcg_state = 17

lcg_multiplier = 25214903917
lcg_increment = 11
lcg_modulus = 281474976710656


def lcg_randint(modulus: int):
    global last_lcg_state

    last_lcg_state = (last_lcg_state * lcg_multiplier + lcg_increment) % lcg_modulus

    return last_lcg_state % modulus


class RandeerAdapter:
    def __init__(self, path: str):
        lib = ctypes.cdll.LoadLibrary(path)
        lib.sample.argtypes = [ctypes.c_int64]
        lib.seed.argtypes = [ctypes.c_int64]

        lib.sample_default_by_looping.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_default_n_by_looping_without_init.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_default_n_by_looping_with_init.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]

        lib.sample_default_by_looping_using_objects.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_default_n_by_looping_without_init_using_objects.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_default_n_by_looping_with_init_using_objects.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]

        lib.sample_lcg_by_looping.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_lcg_n_by_looping_without_init.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.sample_lcg_n_by_looping_with_init.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]

        # lib.sample_by_looping_randomizer.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        # lib.sample_by_looping_lcg.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]

        lib.init.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64]
        lib.init_in_interval_excluding_task.argtypes = [ctypes.c_int64, ctypes.c_int64, ctypes.c_int64, ctypes.c_void_p, ctypes.c_int64]
        lib.next.argtypes = [ctypes.c_int64]

        self.lib = lib

    # core

    def init(self, id_: int, seed: int, type_: RandomizerType):
        return self.lib.init(id_, seed, type_.value)

    def init_in_interval_excluding_task(self, id_: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.init_in_interval_excluding_task(id_, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def next(self, id_: int):
        return self.lib.next(id_)

    # default looping

    def sample_default_by_looping(self, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_default_by_looping(min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_default_n_by_looping_without_init(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_default_n_by_looping_without_init(n, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_default_n_by_looping_with_init(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_default_n_by_looping_with_init(n, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    # default looping using objects

    def sample_default_by_looping_using_objects(self, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_default_by_looping_using_objects(min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_default_n_by_looping_without_init_using_objects(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_default_n_by_looping_without_init_using_objects(n, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_default_n_by_looping_with_init_using_objects(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_default_n_by_looping_with_init_using_objects(n, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    # lcg looping

    def sample_lcg_by_looping(self, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_lcg_by_looping(min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_lcg_n_by_looping_without_init(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_lcg_n_by_looping_without_init(n, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def sample_lcg_n_by_looping_with_init(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.lib.sample_lcg_n_by_looping_with_init(n, min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    # def sample_by_looping_randomizer(self, min_: int, max_: int, excluded: Tuple[int]):
    #     return self.lib.sample_by_looping_randomizer(min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    # def sample_by_looping_lcg(self, min_: int, max_: int, excluded: Tuple[int]):
    #     return self.lib.sample_by_looping_lcg(min_, max_, np.array(excluded).__array_interface__['data'][0], len(excluded))

    def seed(self, seed: int):
        return self.lib.seed(seed)

    def sample_default_by_looping_python(self, min_: int, max_: int, excluded: Tuple[int]):
        while True:
            number = randint(min_, max_)
            if number not in excluded:
                return number

    def sample_lcg_by_looping_python(self, min_: int, max_: int, excluded: Tuple[int]):
        diff = max_ - min_ + 1
        while True:
            number = min_ + lcg_randint(diff)
            if number not in excluded:
                return number


class Evaluator:
    def __init__(self):
        pass

    def evaluate(self, sample: callable, n_samples: int, label: str, n_measurements: int = 10):
        measured_times = []

        for _ in range(n_measurements):
            start_time = time.time()

            for _ in range(n_samples):
                sample()

            measured_times.append(time.time() - start_time)

        # print(f'{label:100s} Sampled {n_samples} samples in {time.time() - start_time} seconds')
        print(f'{label:100s} Sampled {n_samples} samples in {mean(measured_times):.5f} seconds (averaged over {n_measurements} measurements)')


@group()
def main():
    pass


@main.command()
@argument('seed', type = str, default = "17")
def randomize(seed: int):
    randeer = RandeerAdapter(RANDEER_LIBRARY_PATH)
    evaluator = Evaluator()

    min_ = 10
    max_ = 20
    excluded = (11, 12, 13, 14, 15, 16, 17, 18, 19)
    n = 100000

    # randomizer_id = 17
    # seed = 17

    for seed_ in tuple(int(str_seed.strip()) for str_seed in seed.split(',')):

        randeer.seed(seed_)

        # for _ in range(10):
        #     print(randeer.sample_by_looping(100, 150, (110, 130)))
        #     print(randeer.sample_by_looping_lcg(100, 150, (110, 130)))

        # randeer.init(randomizer_id, seed, RandomizerType.DEFAULT_LOOPING)
        # randeer.init_in_interval_excluding_task(randomizer_id, min_, max_, excluded)

        print('Default')

        evaluator.evaluate(lambda: randeer.sample_default_by_looping_python(min_, max_, excluded), n, 'looping in python, generation in python')
        evaluator.evaluate(lambda: randeer.sample_default_by_looping(min_, max_, excluded), n, 'looping in python, generation in c++')
        evaluator.evaluate(lambda: randeer.sample_default_n_by_looping_with_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ with init')
        evaluator.evaluate(lambda: randeer.sample_default_n_by_looping_without_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ without init')

        print('Default using objects')

        evaluator.evaluate(lambda: randeer.sample_default_by_looping_using_objects(min_, max_, excluded), n, 'looping in python, generation in c++')
        evaluator.evaluate(lambda: randeer.sample_default_n_by_looping_with_init_using_objects(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ with init')
        evaluator.evaluate(lambda: randeer.sample_default_n_by_looping_without_init_using_objects(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ without init')

        print('LCG')

        evaluator.evaluate(lambda: randeer.sample_lcg_by_looping_python(min_, max_, excluded), n, 'looping in python, generation in python')
        evaluator.evaluate(lambda: randeer.sample_lcg_by_looping(min_, max_, excluded), n, 'looping in python, generation in c++')
        evaluator.evaluate(lambda: randeer.sample_lcg_n_by_looping_with_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ with init')
        evaluator.evaluate(lambda: randeer.sample_lcg_n_by_looping_without_init(n, min_, max_, excluded), 1, 'looping in c++, generation in c++ without init')

        # evaluator.evaluate(lambda: randeer.sample_by_looping_randomizer(min_, max_, excluded), n, 'looping randomizer in python, generation in c++')
        # evaluator.evaluate(lambda: randeer.next(randomizer_id), n, 'looping contextualized randomizer in python, generation in c++')
        # evaluator.evaluate(lambda: randeer.sample_by_looping_lcg(min_, max_, excluded), n, 'looping in python, generation in c++ using custom function')

        # for _ in range(100):
        #     print(randeer.sample_by_looping(10, 20, (12, 13)))


if __name__ == '__main__':
    main()
