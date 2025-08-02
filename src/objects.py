#!/usr/bin/env python3

import math
from vec3 import Point3
from interval import Interval
from ray import Ray
from hittable import HitRecord, Hittable
from material import Material


class Sphere(Hittable):
    center: Point3  # m
    radius: float  # m
    material: Material

    def __init__(self, center: Point3, radius: float, material: Material):
        assert isinstance(center, Point3)
        assert isinstance(radius, float)
        self.center = center
        self.radius = max(radius, 0.0)
        self.material = material

    def hit(self, ray: Ray, ray_t: Interval, record: HitRecord):
        object_center = self.center - ray.origin
        a = ray.direction.mag2
        h = ray.direction @ object_center
        c = object_center.mag2 - self.radius**2

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
        outward_normal = (record.p - self.center) / self.radius
        record.set_face_normal(ray, outward_normal.unit)
        record.material = self.material  # type: ignore

        return (True, record)
