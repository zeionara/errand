from functools import wraps
from unittest import TestCase

SAMPLED_AN_EXCLUDED_VALUE_MESSAGE = "Sampled an excluded value"
SHOULD_NOT_EXECUTE_ABSTRACT_TESTS_MESSAGE = "Should not execute abstract tests"


def skip_if_abstract(test):
    @wraps(test)
    def _skip_if_abstract(self, *args, **kwargs):
        if self.abstract:
            return self.skipTest(SHOULD_NOT_EXECUTE_ABSTRACT_TESTS_MESSAGE)
        return test(self, *args, **kwargs)
    return _skip_if_abstract


class TestGeneratorValidity(TestCase):
    abstract = True

    def __init__(self, *args, **kwargs):
        self.sampler = None
        self.sample = None

        super().__init__(*args, **kwargs)

    def run_tests(self, min_: int, max_: int, excluded: tuple[int], n: int = 1000):
        n_allowed_values = max_ - min_ + 1 - len(set(excluded))
        sampled_values = set()

        for _ in range(n):
            # print('Sampling from', min_, 'to', max_, 'excluding', excluded)
            sampled_value = self.sample(min_, max_, excluded)
            # print('Sampled', sampled_value)
            self.assertNotIn(sampled_value, excluded, SAMPLED_AN_EXCLUDED_VALUE_MESSAGE)  # Make sure that excluded values are not generated
            sampled_values.add(sampled_value)

        # print(sampled_values)

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
        max_ = 7
        excluded = (2, 4, 6)

        self.run_tests(min_, max_, excluded)

    @skip_if_abstract
    def test_mixed_interval(self):
        min_ = 1
        max_ = 15
        excluded = (2, 3, 4, 6, 7, 10)

        self.run_tests(min_, max_, excluded)

    @skip_if_abstract
    def test_unordered(self):
        min_ = 1
        max_ = 15
        excluded = (10, 7, 2, 3, 6, 4)

        self.run_tests(min_, max_, excluded)

    @skip_if_abstract
    def test_repetitions(self):
        min_ = 1
        max_ = 15
        excluded = (2, 3, 3, 3, 4, 6, 6, 7, 10, 10)

        self.run_tests(min_, max_, excluded)

    @skip_if_abstract
    def test_mixed_head_interval(self):
        min_ = 1
        max_ = 15
        excluded = (1, 2, 3, 6, 7, 10)

        self.run_tests(min_, max_, excluded)

    @skip_if_abstract
    def test_mixed_tail_interval(self):
        min_ = 1
        max_ = 15
        excluded = (7, 8, 9, 11, 12, 15)

        self.run_tests(min_, max_, excluded)
