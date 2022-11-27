from random import randint
from typing import Tuple
import ctypes

import numpy as np

from .RandomizerType import RandomizerType

from .SamplingMethod import SamplingMethod
from .SamplingApproach import SamplingApproach
from .IterationMethod import IterationMethod

from .Sampler import Sampler


class RandeerSampler(Sampler):
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

    def get_sampling_function(self, *args, **kwargs):
        raise NotImplementedError('Sampling function getter is not defined for randeer sampler, please use only the sample function')

    def sample(
        self, n: int, min_: int, max_: int, excluded: Tuple[int],
        sampling_method: SamplingMethod, sampling_approach: SamplingApproach, iteration_method: IterationMethod, single_init: bool, using_objects: bool, *args, **kwargs
    ):
        if sampling_approach == SamplingApproach.DEFAULT:
            if sampling_method == SamplingMethod.LOOPING:
                if using_objects:
                    if iteration_method == IterationMethod.PYTHON:
                        for _ in range(n):
                            _ = self.sample_default_by_looping_using_objects(min_, max_, excluded)
                        return
                    if single_init:
                        return self.sample_default_n_by_looping_without_init_using_objects(n, min_, max_, excluded)
                    return self.sample_default_n_by_looping_with_init_using_objects(n, min_, max_, excluded)
                if iteration_method == IterationMethod.PYTHON:
                    for _ in range(n):
                        _ = self.sample_default_by_looping(min_, max_, excluded)
                    return
                if single_init:
                    return self.sample_default_n_by_looping_without_init(n, min_, max_, excluded)
                return self.sample_default_n_by_looping_with_init(n, min_, max_, excluded)
            raise ValueError(f'Sampling method {sampling_method.value} is not supported for approach {sampling_approach.value}')
        if sampling_approach == SamplingApproach.LCG:
            if sampling_method == SamplingMethod.LOOPING:
                if using_objects:
                    raise ValueError('Cannot use objects when sampling with lcg randomizer')
                if iteration_method == IterationMethod.PYTHON:
                    for _ in range(n):
                        _ = self.sample_lcg_by_looping(min_, max_, excluded)
                    return
                if single_init:
                    return self.sample_lcg_n_by_looping_without_init(n, min_, max_, excluded)
                return self.sample_lcg_n_by_looping_with_init(n, min_, max_, excluded)
            raise ValueError(f'Sampling method {sampling_method.value} is not supported for approach {sampling_approach.value}')
        raise ValueError(f'Sampling approach {sampling_approach.value} is not supported')

    def seed(self, seed: int):
        return self.lib.seed(seed)
