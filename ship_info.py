from enum import Enum, auto
from config import *


class WARSHIPS(Enum):
    MYOKO = auto()


def nmile(meter):
    return round(meter / 1852, round_digits)


warships = {'myoko': {"length": nmile(201.5), "mass": 14980, "max_speed": 34}}
