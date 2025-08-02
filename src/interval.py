#!/usr/bin/env python3

import math
from typing import Final


class Interval:
    min: float
    max: float

    def __init__(self, min: float | None = None, max: float | None = None):
        self.min = min if isinstance(min, float) else -math.inf
        self.max = max if isinstance(max, float) else math.inf

    def contains(self, x: float):
        return self.min <= x <= self.max

    def surrounds(self, x: float):
        return self.min < x < self.max

    def clamp(self, x: float):
        if x < self.min:
            return self.min
        elif x > self.max:
            return self.max
        else:
            return x


empty: Final[Interval] = Interval(math.inf, -math.inf)
universe: Final[Interval] = Interval(-math.inf, math.inf)
