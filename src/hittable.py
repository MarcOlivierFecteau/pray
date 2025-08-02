#!/usr/bin/env python3

import math
from abc import ABC, abstractmethod
from vec3 import Vector3, Point3
from interval import Interval
from ray import Ray
from material import Material


class HitRecord:
    p: Point3  # m
    normal: Vector3
    t: float
    front_face: bool
    material: Material

    def __init__(self):
        self.p = Point3.splat(math.inf)
        self.normal = Vector3.splat(math.inf)
        self.t = math.inf
        self.front_face = False

    def __repr__(self):
        return f"HitRecord({self.p} {self.normal}, {self.t}, {self.front_face})"

    def set_face_normal(self, ray: Ray, outward_normal: Vector3):
        """
        Sets the hit record normal vector. `outward_normal` must be a unit vector.
        """
        assert math.isclose(outward_normal.mag, 1.0, abs_tol=1e-6)

        self.front_face = ray.direction @ outward_normal < 0.0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable(ABC):
    @abstractmethod
    def hit(
        self, ray: Ray, ray_t: Interval, record: HitRecord
    ) -> tuple[bool, HitRecord]:
        return (False, HitRecord())


class HittableList(Hittable):
    objects: list[Hittable] = []

    def __init__(self):
        pass

    def add(self, object: Hittable):
        self.objects.append(object)

    def clear(self):
        self.objects.clear()

    def hit(self, ray: Ray, ray_t: Interval, record: HitRecord):
        temp_record = HitRecord()
        hit_anything = bool(False)
        closest_so_far = ray_t.max

        for object in self.objects:
            hit, temp_record = object.hit(
                ray, Interval(ray_t.min, closest_so_far), temp_record
            )
            if hit:
                hit_anything = True
                closest_so_far = temp_record.t
                record = temp_record

        return (hit_anything, record)
