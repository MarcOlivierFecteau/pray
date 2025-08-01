#!/usr/bin/env python3

from abc import ABC, abstractmethod
import math

from ray import Ray
from vec3 import Vector3, Point3


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


empty = Interval(math.inf, -math.inf)
universe = Interval(-math.inf, math.inf)


class HitRecord:
    _p: Point3
    _normal: Vector3
    _t: float
    _front_face: bool

    def __init__(self):
        self._p = Point3.splat(math.inf)
        self._normal = Vector3.splat(math.inf)
        self._t = math.inf
        self._front_face = False

    def __repr__(self):
        return f"HitRecord({self._p} {self._normal}, {self._t}, {self._front_face})"

    @property
    def p(self):
        return self._p

    @p.setter
    def p(self, point: Point3):
        self._p = point

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, t: float):
        self._t = t

    @property
    def normal(self):
        return self._normal

    def set_face_normal(self, ray: Ray, outward_normal: Vector3):
        """
        Sets the hit record normal vector. `outward_normal` must be a unit vector.
        """
        assert math.isclose(outward_normal.mag, 1.0, abs_tol=1e-6)

        self._front_face = ray.direction @ outward_normal < 0
        self._normal = outward_normal if self._front_face else -outward_normal


class Hittable(ABC):
    @abstractmethod
    def hit(
        self, ray: Ray, ray_t: Interval, record: HitRecord
    ) -> tuple[bool, HitRecord]:
        return (False, HitRecord())


class Sphere(Hittable):
    __center: Point3
    __radius: float

    def __init__(self, center: Point3, radius: float):
        assert isinstance(center, Point3)
        assert isinstance(radius, float)
        self.__center = center
        self.__radius = max(radius, 0.0)

    def hit(self, ray: Ray, ray_t: Interval, record: HitRecord):
        object_center = self.__center - ray.origin
        a = ray.direction.mag2
        h = ray.direction @ object_center
        c = object_center.mag2 - self.__radius**2

        discriminant = h**2 - a * c
        if discriminant < 0:
            return (False, HitRecord())

        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range
        root = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return (False, HitRecord())

        record.t = root
        record.p = ray.at(root)
        outward_normal = (record.p - self.__center) / self.__radius
        record.set_face_normal(ray, outward_normal.unit)

        return (True, record)


class HittableList(Hittable):
    __objects: list[Hittable] = []

    def __init__(self):
        pass

    def add(self, object: Hittable):
        self.__objects.append(object)

    def clear(self):
        self.__objects.clear()

    def hit(self, ray: Ray, ray_t: Interval, record: HitRecord):
        temp_record = HitRecord()
        hit_anything = bool(False)
        closest_so_far = ray_t.max

        for object in self.__objects:
            hit, temp_record = object.hit(
                ray, Interval(ray_t.min, closest_so_far), temp_record
            )
            if hit:
                hit_anything = True
                closest_so_far = temp_record.t
                record = temp_record

        return (hit_anything, record)
