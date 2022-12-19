from enum import Enum


class SamplingMethod(Enum):
    LOOPING = 'looping'
    SHIFTING = 'shifting'
    CONSTRAINED_SHIFTING = 'constrained-shifting'
