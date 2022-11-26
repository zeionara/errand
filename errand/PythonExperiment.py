from typing import Tuple

from .SamplingMethod import SamplingMethod
from .SamplingApproach import SamplingApproach

from .PythonSampler import PythonSampler
from .Experiment import Experiment


class PythonExperiment(Experiment):
    def __init__(self, label: str, sampling_method: SamplingMethod, sampling_approach: SamplingApproach):
        self.sampling_method = sampling_method
        self.sampling_approach = sampling_approach
        super().__init__(PythonSampler(), label)

    def sample(self, n: int, min_: int, max_: int, excluded: Tuple[int]):
        return self.sampler.sample(n, min_, max_, excluded, self.sampling_method, self.sampling_approach)
