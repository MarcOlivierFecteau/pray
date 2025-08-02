#!/usr/bin/env python3

from __future__ import annotations
import math
import random
from typing import TypeAlias


def random_float(min: float = 0.0, max: float = 1.0):
    range = max - min
    return min + range * random.random()


class Vector3:
    components: list[float] = []

    def __init__(self, x: float, y: float, z: float):
        assert [isinstance(e, float) for e in [x, y, z]]
        self.components = [x, y, z]

    @property
    def _(self):
        return self.components

    @property
    def x(self):
        return self.components[0]

    @property
    def y(self):
        return self.components[1]

    @property
    def z(self):
        return self.components[2]

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __getitem__(self, i):
        return self.components[i]

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __add__(self, v: Vector3):
        cls = type(self)
        assert isinstance(v, Vector3)
        return cls(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v: Vector3):
        assert isinstance(v, Vector3)
        return Vector3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, v: Vector3 | float | int):
        cls = type(self)
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
        return cls(x, y, z)

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

    @classmethod
    def zero(cls):
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def one(cls):
        return cls(1.0, 1.0, 1.0)

    @classmethod
    def splat(cls, c: float):
        assert isinstance(c, float)
        return cls(c, c, c)

    @classmethod
    def random(cls):
        return cls(random.random(), random.random(), random.random())

    @classmethod
    def randrange(cls, min: float, max: float):
        return cls(
            random_float(min, max), random_float(min, max), random_float(min, max)
        )

    @staticmethod
    def random_unit():
        while True:
            v = Vector3.randrange(-1.0, 1.0)
            if 1e-9 <= v.mag2 <= 1.0:
                return v.unit

    @staticmethod
    def random_on_hemisphere(normal: Vector3):
        on_unit_sphere = Vector3.random_unit()
        if on_unit_sphere @ normal > 0.0:
            return on_unit_sphere
        else:
            return -on_unit_sphere

    @staticmethod
    def random_in_unit_disk():
        while True:
            p = Vector3(random_float(-1.0, 1.0), random_float(-1.0, 1.0), 0.0)
            if p.mag2 < 1.0:
                return p

    @staticmethod
    def reflect(v: Vector3, normal: Vector3):
        return v - 2 * (v @ normal) * normal

    @staticmethod
    def refract(uv: Vector3, normal: Vector3, etai_over_etat: float):
        cos_theta = min(-uv @ normal, 1.0)
        ray_out_perpendicular = etai_over_etat * (uv + cos_theta * normal)
        ray_out_parallel = -math.sqrt(abs(1.0 - ray_out_perpendicular.mag2)) * normal
        return ray_out_perpendicular + ray_out_parallel

    @property
    def magnitude_squared(self):
        return self.x**2 + self.y**2 + self.z**2

    @property
    def magnitude(self):
        return math.sqrt(self.magnitude_squared)

    @property
    def unit(self):
        v = Vector3(*self.components)
        return v / v.magnitude

    # Aliases
    mag2 = magnitude_squared
    mag = magnitude
    length = magnitude

    def cross(self, v: Vector3):
        return Vector3(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x,
        )

    def near_zero(self):
        epsilon = 1e-8
        return abs(self.x) < epsilon and abs(self.y) < epsilon and abs(self.z) < epsilon


Point3: TypeAlias = Vector3
