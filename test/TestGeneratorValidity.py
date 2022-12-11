from functools import wraps
from abc import abstractmethod
from unittest import TestCase

SAMPLED_AN_EXCLUDED_VALUE_MESSAGE = "Sampled an excluded value"


def skip_if_abstract(test):
    @wraps(test)
    def _skip_if_abstract(self, *args, **kwargs):
        if self.abstract:
            return self.skipTest("Should not execute abstract tests")
        return test(self, *args, **kwargs)
    return _skip_if_abstract


class TestGeneratorValidity(TestCase):
    abstract = True

    # @abstractmethod
    # def sample(self, min_: int, max_: int, excluded: tuple[int]) -> int:
    #     pass

    def __init__(self, *args, **kwargs):
        self.sampler = None
        self.sample = None

        super().__init__(*args, **kwargs)

    def run_tests(self, min_: int, max_: int, excluded: tuple[int], n: int = 1000):
        n_allowed_values = max_ - min_ + 1 - len(excluded)
        sampled_values = set()

        for _ in range(n):
            sampled_value = self.sample(min_, max_, excluded)
            self.assertNotIn(sampled_value, excluded, SAMPLED_AN_EXCLUDED_VALUE_MESSAGE)  # Make sure that excluded values are not generated
            sampled_values.add(sampled_value)

        assert len(sampled_values) == n_allowed_values  # Make sure that the every allowed value has been generated at least once

    @skip_if_abstract
    def test_contigent_interval(self):
        min_ = 1
        max_ = 5
        excluded = (2, 3)

        self.run_tests(min_, max_, excluded)

    @skip_if_abstract
    def test_one_hole_interval(self):
        min_ = 1
        max_ = 5
        excluded = (2, 4)

        self.run_tests(min_, max_, excluded)

    @skip_if_abstract
    def test_two_holes_interval(self):
        min_ = 1
        max_ = 6
        excluded = (2, 4, 5)

        self.run_tests(min_, max_, excluded)
