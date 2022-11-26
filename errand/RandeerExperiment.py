from typing import Tuple

from .SamplingMethod import SamplingMethod
from .SamplingApproach import SamplingApproach
from .IterationMethod import IterationMethod

from .RandeerSampler import RandeerSampler
from .Experiment import Experiment


class RandeerExperiment(Experiment):
    def __init__(self, label: str, path: str, sampling_method: SamplingMethod, sampling_approach: SamplingApproach, iteration_method: IterationMethod, single_init: bool, using_objects: bool):
        self.sampling_method = sampling_method
        self.sampling_approach = sampling_approach
        self.iteration_method = iteration_method

        self.single_init = single_init
        self.using_objects = using_objects

        super().__init__(RandeerSampler(path), label)

    def sample(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.sampler.sample(n, min_, max_, excluded, self.sampling_method, self.sampling_approach, self.iteration_method, self.single_init, self.using_objects)
