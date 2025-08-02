#!/usr/bin/env python3

from abc import ABC, abstractmethod
import math

from ray import Ray
from vec3 import Vector3, Point3, Color


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


empty = Interval(math.inf, -math.inf)
universe = Interval(-math.inf, math.inf)


# To remove the 'undefined' warning in HitRecord
class Material(ABC):  # type: ignore
    pass


class HitRecord:
    _p: Point3
    _normal: Vector3
    _t: float
    _front_face: bool
    _material: Material

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

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, material: Material):
        self._material = material

    mat = material

    def set_face_normal(self, ray: Ray, outward_normal: Vector3):
        """
        Sets the hit record normal vector. `outward_normal` must be a unit vector.
        """
        assert math.isclose(outward_normal.mag, 1.0, abs_tol=1e-6)

        self._front_face = ray.direction @ outward_normal < 0
        self._normal = outward_normal if self._front_face else -outward_normal


class Material(ABC):
    @abstractmethod
    def scatter(self, ray: Ray, record: HitRecord) -> tuple[bool, Ray, Color]:
        return (False, Ray(Point3.zero(), Vector3.zero()), Color.zero())


class Lambertian(Material):
    __albedo: Color

    def __init__(self, albedo: Color):
        self.__albedo = albedo

    def scatter(self, ray: Ray, record: HitRecord):
        scatter_direction = record.normal + Vector3.random_unit()

        # Catch degenerate scatter direction
        if scatter_direction.near_zero():
            scatter_direction = record.normal

        scattered = Ray(record.p, scatter_direction)
        attenuation = self.__albedo
        return (True, scattered, attenuation)


class Metal(Material):
    __albedo: Color

    def __init__(self, albedo: Color):
        self.__albedo = albedo

    def scatter(self, ray: Ray, record: HitRecord):
        reflected = Vector3.reflect(ray.direction, record.normal)
        scattered = Ray(record.p, reflected)
        attenuation = self.__albedo
        return (True, scattered, attenuation)


class Hittable(ABC):
    @abstractmethod
    def hit(
        self, ray: Ray, ray_t: Interval, record: HitRecord
    ) -> tuple[bool, HitRecord]:
        return (False, HitRecord())


class Sphere(Hittable):
    __center: Point3
    __radius: float
    __material: Material

    def __init__(self, center: Point3, radius: float, material: Material):
        assert isinstance(center, Point3)
        assert isinstance(radius, float)
        self.__center = center
        self.__radius = max(radius, 0.0)
        self.__material = material

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
        record.material = self.__material  # type: ignore

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
