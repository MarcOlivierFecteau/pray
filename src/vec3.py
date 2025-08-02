#!/usr/bin/env python3

from __future__ import annotations
import math
import random
from typing import TypeAlias


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

    @staticmethod
    def random():
        return Vector3(random.random(), random.random(), random.random())

    @staticmethod
    def randrange(min: float, max: float):
        range = max - min
        return Vector3(
            min + range * random.random(),
            min + range * random.random(),
            min + range * random.random(),
        )

    @staticmethod
    def random_unit():
        while True:
            v = Vector3.randrange(-1.0, 1.0)
            if 1e-9 <= v.mag2 <= 1:
                return v.unit

    @staticmethod
    def random_on_hemisphere(normal: Vector3):
        on_unit_sphere = Vector3.random_unit()
        if on_unit_sphere @ normal > 0:
            return on_unit_sphere
        else:
            return -on_unit_sphere

    @staticmethod
    def random_in_unit_disk():
        while True:
            p = Vector3(-1.0 + 2.0 * random.random(), -1.0 + 2.0 * random.random(), 0.0)
            if p.mag2 < 1:
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

    def near_zero(self):
        epsilon = 1e-8
        return abs(self.x) < epsilon and abs(self.y) < epsilon and abs(self.z) < epsilon


Color: TypeAlias = Vector3  # Does not eliminate the foot-guns
Point3: TypeAlias = Vector3
