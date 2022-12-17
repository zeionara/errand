from errand import RandeerSampler, RANDEER_LIBRARY_PATH

try:
    from TestGeneratorValidity import TestGeneratorValidity  # works for 'python -m unittest discover ...' command
except ModuleNotFoundError:
    from .TestGeneratorValidity import TestGeneratorValidity  # works for 'python -m unittest test ...' command


class TestRandeerDefaultShiftingUsingObjectsGeneratorValidity(TestGeneratorValidity):
    abstract = False

    def setUp(self):
        self.sampler = RandeerSampler(path = RANDEER_LIBRARY_PATH, seed = 17)
        self.sample = self._sample
        self.seed = 17

    def _sample(self, min_: int, max_: int, excluded: tuple[int]):
        self.seed += 1
        self.sampler.seed(self.seed)
        return self.sampler.sample_default_by_shifting_using_objects(min_, max_, excluded)
