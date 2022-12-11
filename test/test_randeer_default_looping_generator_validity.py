from errand import RandeerSampler, RANDEER_LIBRARY_PATH

try:
    from TestGeneratorValidity import TestGeneratorValidity  # works for 'python -m unittest discover ...' command
except ModuleNotFoundError:
    from .TestGeneratorValidity import TestGeneratorValidity  # works for 'python -m unittest test ...' command


class TestRandeerDefaultLoopingGeneratorValidity(TestGeneratorValidity):
    abstract = False

    def setUp(self):
        self.sampler = sampler = RandeerSampler(path = RANDEER_LIBRARY_PATH, seed = 17)
        self.sample = sampler.sample_default_by_looping
