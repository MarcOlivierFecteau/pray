#!/usr/bin/env python3

from vec3 import Vector3, Point3


class Ray:
    __origin: Point3
    __direction: Vector3

    def __init__(self, origin: Point3, direction: Vector3):
        assert isinstance(origin, Point3)
        assert isinstance(direction, Vector3)
        self.__origin = origin
        self.__direction = direction

    @property
    def origin(self):
        return self.__origin

    @property
    def direction(self):
        return self.__direction

    def at(self, t: float):
        return self.__origin + t * self.__direction
