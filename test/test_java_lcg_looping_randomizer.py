from unittest import TestCase

from errand import RandeerSampler, RANDEER_LIBRARY_PATH, RandomizerType


class TestJavaLcgLoopingLemmatizer(TestCase):
    def setUp(self):
        self.adapter = RandeerSampler(RANDEER_LIBRARY_PATH)

    def test_in_interval_excluding_task(self):
        min_ = 1
        max_ = 5
        excluded = (2, 4)

        randomizer_id = 17
        seed = 17

        self.adapter.init(randomizer_id, seed, RandomizerType.JAVA_LOOPING)
        self.adapter.init_in_interval_excluding_task(randomizer_id, min_, max_, excluded)

        self.assertEqual(tuple(self.adapter.next(randomizer_id) for _ in range(10)), (1, 1, 1, 1, 5, 5, 1, 3, 3, 3))

    def test_in_interval_excluding_task_using_another_seed(self):
        min_ = 1
        max_ = 5
        excluded = (2, 4)

        randomizer_id = 19
        seed = 19

        self.adapter.init(randomizer_id, seed, RandomizerType.JAVA_LOOPING)
        self.adapter.init_in_interval_excluding_task(randomizer_id, min_, max_, excluded)

        self.assertEqual(tuple(self.adapter.next(randomizer_id) for _ in range(10)), (5, 1, 1, 3, 1, 3, 3, 1, 1, 5))

    def test_randomizer_recreation(self):
        min_ = 1
        max_ = 5
        excluded = (2, 4)

        randomizer_id = 13
        seed = 17

        self.adapter.init(randomizer_id, seed, RandomizerType.JAVA_LOOPING)
        self.adapter.init_in_interval_excluding_task(randomizer_id, min_, max_, excluded)

        self.assertEqual(tuple(self.adapter.next(randomizer_id) for _ in range(10)), (1, 1, 1, 1, 5, 5, 1, 3, 3, 3))
