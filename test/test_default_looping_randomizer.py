from unittest import TestCase

from errand import RandeerAdapter, RANDEER_LIBRARY_PATH, RandomizerType


class TestDefaultLoopingLemmatizer(TestCase):
    def setUp(self):
        self.adapter = RandeerAdapter(RANDEER_LIBRARY_PATH)

    def test_two_numbers(self):
        self.assertEqual(len(set(self.adapter.sample_by_looping_randomizer(1, 5, (2, 4)) for _ in range(100))), 1)

    def test_in_interval_excluding_task(self):
        min_ = 1
        max_ = 5
        excluded = (2, 4)

        randomizer_id = 17

        self.adapter.init(randomizer_id, 17, RandomizerType.DEFAULT_LOOPING)
        self.adapter.init_in_interval_excluding_task(randomizer_id, min_, max_, excluded)

        self.assertEqual(tuple(self.adapter.next(randomizer_id) for _ in range(10)), (1, 3, 5, 3, 5, 5, 1, 3, 1, 5))
