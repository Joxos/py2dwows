from enum import Enum


class GEAR(Enum):
    REVERSE = -1
    NEUTRAL = 0
    SLOW = 1
    HALF = 2
    FAST = 3
    FULL = 4


def forward_gear(g: GEAR):
    if g.value < 4:
        return GEAR(g.value + 1)
    return g


def backward_gear(g: GEAR):
    if g.value > -1:
        return GEAR(g.value - 1)
    return g