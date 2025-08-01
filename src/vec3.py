#!/usr/bin/env python3

from __future__ import annotations
from typing import TypeAlias
import math


class Vector3:
    e: list[float] = []

    def __init__(self, x: float, y: float, z: float):
        self.e = [float(x), float(y), float(z)]

    @property
    def x(self):
        return self.e[0]

    @property
    def y(self):
        return self.e[1]

    @property
    def z(self):
        return self.e[2]

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __getitem__(self, i):
        return self.e[i]

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __add__(self, v: Vector3):
        if not isinstance(v, Vector3):
            raise TypeError
        x = self.x + v.x
        y = self.y + v.y
        z = self.z + v.z
        return Vector3(x, y, z)

    def __sub__(self, v: Vector3):
        if not isinstance(v, Vector3):
            raise TypeError
        x = self.x - v.x
        y = self.y - v.y
        z = self.z - v.z
        return Vector3(x, y, z)

    def __mul__(self, v: Vector3 | float | int):
        if isinstance(v, int):
            v = float(v)
        if isinstance(v, Vector3):
            x = self.x * v.x
            y = self.y * v.y
            z = self.z * v.z
        elif isinstance(v, float):
            x = self.x * v
            y = self.y * v
            z = self.z * v
        else:
            raise TypeError
        return Vector3(x, y, z)

    __rmul__ = __mul__

    def __truediv__(self, v: Vector3 | float | int):
        if isinstance(v, int):
            v = float(v)
        if isinstance(v, Vector3):
            x = self.x / v.x
            y = self.y / v.y
            z = self.z / v.z
        elif isinstance(v, float):
            x = self.x / v
            y = self.y / v
            z = self.z / v
        else:
            raise TypeError
        return Vector3(x, y, z)

    def __matmul__(self, v: Vector3):
        return self.x * v.x + self.y * v.y + self.z * v.z

    @staticmethod
    def zero():
        return Vector3(0, 0, 0)

    @staticmethod
    def one():
        return Vector3(1, 1, 1)

    @staticmethod
    def splat(c: float):
        if isinstance(c, int):
            c = float(c)
        return Vector3(c, c, c)

    @property
    def magnitude_squared(self):
        return self.x**2 + self.y**2 + self.z**2

    @property
    def magnitude(self):
        return math.sqrt(self.magnitude_squared)

    @property
    def unit(self):
        v = Vector3(*self.e)
        return v / v.magnitude

    # Aliases
    mag2 = magnitude_squared
    mag = magnitude
    length = magnitude
    abs = magnitude

    def cross(self, v: Vector3):
        return Vector3(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x,
        )


Color: TypeAlias = Vector3  # Does not eliminate the foot-guns
Point3: TypeAlias = Vector3


def write_color(out, color: Color):
    """
    Write a single pixel's value to an output following the P3 PPM format.

    Args:
        out: An output stream.
        color (Color): The RGB component values ([0, 1]).
    """
    r = int(255.999 * color.x)
    g = int(255.999 * color.y)
    b = int(255.999 * color.z)
    out.write(f"{r} {g} {b}\n")
