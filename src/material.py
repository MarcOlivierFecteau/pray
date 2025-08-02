#!/usr/bin/env python3

import math
import random
from abc import ABC, abstractmethod
from typing import Final
from vec3 import Vector3, Point3
from color import Color
from ray import Ray
from hittable import HitRecord


class Material(ABC):
    @abstractmethod
    def scatter(self, ray: Ray, record: HitRecord) -> tuple[bool, Ray, Color]:
        return (False, Ray(Point3.zero(), Vector3.zero()), Color.zero())


class Lambertian(Material):
    albedo: Color

    def __init__(self, albedo: Color):
        self.albedo = albedo

    def __repr__(self):
        return f"Lambertian({self.albedo.r}, {self.albedo.g}, {self.albedo.b})"

    def scatter(self, ray: Ray, record: HitRecord):
        scatter_direction = record.normal + Vector3.random_unit()

        # Catch degenerate scatter direction
        if scatter_direction.near_zero():
            scatter_direction = record.normal

        scattered = Ray(record.p, scatter_direction)
        attenuation = self.albedo
        return (True, scattered, attenuation)


class Metal(Material):
    albedo: Color
    fuzz: float

    def __init__(self, albedo: Color, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz

    def scatter(self, ray: Ray, record: HitRecord):
        reflected = Vector3.reflect(ray.direction, record.normal).unit
        reflected += self.fuzz * Vector3.random_unit()
        scattered = Ray(record.p, reflected)
        attenuation = self.albedo
        atop_surface = scattered.direction @ record.normal > 0
        return (atop_surface, scattered, attenuation)


class Dielectric(Material):
    refraction_index: float  # In vacuum or air, or the ratio of the material's refractive index over the refractive index of the enclosing media

    def __init__(self, refraction_index: float):
        self.refraction_index = refraction_index

    def reflectance(self, cosine: float, refraction_index: float):
        """
        Uses Schlick's approximation for reflectance.
        """
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 **= 2
        return r0 + (1 - r0) * math.pow(1 - cosine, 5)

    def scatter(self, ray: Ray, record: HitRecord):
        attenuation: Final[Color] = Color.one()
        refraction_index = (
            1.0 / self.refraction_index if record.front_face else self.refraction_index
        )
        cos_theta = min(-ray.direction.unit @ record.normal, 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta**2)
        cannot_refract = refraction_index * sin_theta > 1.0
        direction: Vector3
        if (
            cannot_refract
            or self.reflectance(cos_theta, refraction_index) > random.random()
        ):
            direction = Vector3.reflect(ray.direction.unit, record.normal)
        else:
            direction = Vector3.refract(
                ray.direction.unit, record.normal, refraction_index
            )
        scattered = Ray(record.p, direction)
        return (True, scattered, attenuation)
