from errand import PythonSampler, SamplingMethod, SamplingApproach

try:
    from TestGeneratorValidity import TestGeneratorValidity  # works for 'python -m unittest discover ...' command
except ModuleNotFoundError:
    from .TestGeneratorValidity import TestGeneratorValidity  # works for 'python -m unittest test ...' command


class TestPythonDefaultGeneratorValidity(TestGeneratorValidity):
    abstract = False

    def setUp(self):
        self.sampler = sampler = PythonSampler(seed = 17)
        self.sample = sampler.get_sampling_function(SamplingMethod.LOOPING, SamplingApproach.DEFAULT)
