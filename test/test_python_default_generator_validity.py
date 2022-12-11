from errand import PythonSampler, SamplingMethod, SamplingApproach

try:
    from TestGeneratorValidity import TestGeneratorValidity  # works for 'python -m unittest discover ...' command
except ModuleNotFoundError:
    from .TestGeneratorValidity import TestGeneratorValidity  # works for 'python -m unittest test ...' command


class TestPythonDefaultGeneratorValidity(TestGeneratorValidity):
    abstract = False

    # def __init__(self, *args, **kwargs):
    #     # self.sampler = None
    #     # self.sample = None
    #     super().__init__(*args, **kwargs)
    #     self.sampler = sampler = PythonSampler(seed = 17)
    #     self.sample = sampler.get_sampling_function(SamplingMethod.LOOPING, SamplingApproach.DEFAULT)

    def setUp(self):
        self.sampler = sampler = PythonSampler(seed = 17)
        self.sample = sampler.get_sampling_function(SamplingMethod.LOOPING, SamplingApproach.DEFAULT)

    # def sample(self, min_: int, max_: int, excluded: tuple[int]) -> int:
    #     return self._sample(min_, max_, excluded)
