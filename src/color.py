#!/usr/bin/env python3

from __future__ import annotations
import math
from typing import TextIO
from vec3 import Vector3
from interval import Interval


class Color(Vector3):
    color: Vector3

    def __init__(self, x: float, y: float, z: float):
        assert [isinstance(e, float) for e in [x, y, z]]
        assert [0.0 <= e <= 1.0 for e in [x, y, z]]
        self.color = Vector3(x, y, z)

    @staticmethod
    def from_vector(v: Vector3):
        return Color(*v)

    @property
    def _(self):
        return self.color._

    @property
    def r(self):
        return self.color.x

    @property
    def g(self):
        return self.color.y

    @property
    def b(self):
        return self.color.z


def linear_to_gamma(linear_component: float):
    if linear_component > 0.0:
        return math.sqrt(linear_component)
    return 0.0


def write_color(out: TextIO, color: Color):
    """
    Write a single pixel's value to an output following the P3 PPM format.

    Args:
        out: An output stream.
        color (Color): The RGB component values ([0, 1]).
    """
    r = linear_to_gamma(color.r)
    g = linear_to_gamma(color.g)
    b = linear_to_gamma(color.b)

    intensity = Interval(0.0, 0.999)
    r = int(256 * intensity.clamp(r))
    g = int(256 * intensity.clamp(g))
    b = int(256 * intensity.clamp(b))
    out.write(f"{r} {g} {b}\n")
