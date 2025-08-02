#!/usr/bin/env python3

from vec3 import Vector3, Point3


class Ray:
    origin: Point3
    direction: Vector3

    def __init__(self, origin: Point3, direction: Vector3):
        assert isinstance(origin, Point3)
        assert isinstance(direction, Vector3)
        self.origin = origin
        self.direction = direction

    def at(self, t: float) -> Point3:
        return self.origin + t * self.direction
