from enum import Enum


class Unit(Enum):
    SECOND = 'second'
    MILLISECOND = 'millisecond'
    MICROSECOND = 'microsecond'

    @property
    def scaling_coefficient(self):
        if self == Unit.SECOND:
            return 1
        if self == Unit.MILLISECOND:
            return 1000
        if self == Unit.MICROSECOND:
            return 1000000
        raise ValueError(f'Unknown scaling coefficient for value {self.value}')
