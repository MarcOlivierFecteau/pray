#!/usr/bin/env python3

import math
import random
import sys
from typing import TextIO

from vec3 import Vector3, Point3, Color
from ray import Ray
from objects import Interval, HitRecord, HittableList


def linear_to_gamma(linear_component: float):
    if linear_component > 0:
        return math.sqrt(linear_component)
    return 0.0


def write_color(out: TextIO, color: Color):
    """
    Write a single pixel's value to an output following the P3 PPM format.

    Args:
        out: An output stream.
        color (Color): The RGB component values ([0, 1]).
    """
    r = linear_to_gamma(color.x)
    g = linear_to_gamma(color.y)
    b = linear_to_gamma(color.z)

    intensity = Interval(0.0, 0.999)
    r = int(256 * intensity.clamp(r))
    g = int(256 * intensity.clamp(g))
    b = int(256 * intensity.clamp(b))
    out.write(f"{r} {g} {b}\n")


class Camera:
    aspect_ratio = 1.0  # image_width / image_height
    image_width: int = 100  # px
    samples_per_pixel: int = 10  # Random samples for each pixel
    max_depth = 10  # Maximum number of ray bounces into scene

    __image_height: int  # px
    __center: Point3
    __pixel00_location: Point3
    __pixel_delta_u: Vector3
    __pixel_delta_v: Vector3
    __pixel_samples_scale: float  # Color scale factor for a sum of pizel samples

    def __init__(self):
        pass

    def __ray_color(self, ray: Ray, depth: int, world: HittableList):
        if depth <= 0:  # No more light is gathered
            return Color.zero()

        record = HitRecord()
        hit_anything, record = world.hit(ray, Interval(0.001, math.inf), record)
        if hit_anything:
            ret: bool
            scattered: Ray
            attenuation: Color
            ret, scattered, attenuation = record.material.scatter(ray, record)  # type: ignore
            if ret:
                return attenuation * self.__ray_color(scattered, depth - 1, world)
            return Color.zero()

        direction = ray.direction.unit
        a = 0.5 * (direction.y + 1.0)
        return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)

    def __initialize(self):
        self.__image_height = int(self.image_width / self.aspect_ratio)
        if self.__image_height < 1:
            self.__image_height = 1

        self.__pixel_samples_scale = 1 / self.samples_per_pixel

        self.__center = Point3.zero()

        # Determine viewport dimensions
        focal_length = 1.0  # m
        viewport_height = 2.0
        viewport_width = viewport_height * (self.image_width / self.__image_height)

        # Calculate the vectors across the horizontal and down the vertical viewport edges
        viewport_u = Vector3(viewport_width, 0, 0)
        viewport_v = Vector3(0, -viewport_height, 0)

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.__pixel_delta_u = viewport_u / self.image_width
        self.__pixel_delta_v = viewport_v / self.__image_height

        # Calculate the location of the upper left pixel
        viewport_upper_left = (
            self.__center
            - Vector3(0, 0, focal_length)
            - viewport_u / 2
            - viewport_v / 2
        )
        self.__pixel00_location = viewport_upper_left + 0.5 * (
            self.__pixel_delta_u + self.__pixel_delta_v
        )

    def __sample_square(self):
        """
        Returns the vector to a random point in the [(-0.5, -0.5), (0.5, 0.5)] unit square.
        """
        return Vector3(random.random() - 0.5, random.random() - 0.5, 0)

    def __get_ray(self, i: int, j: int):
        """
        Construct a camera ray originating from the origin and directed at a randomly sampled
        point around the pixel location (i, j).
        """
        offset = self.__sample_square()
        pixel_sample = (
            self.__pixel00_location
            + ((i + offset.x) * self.__pixel_delta_u)
            + ((j + offset.x) * self.__pixel_delta_v)
        )
        ray_origin = self.__center
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)

    def render(self, world: HittableList):
        self.__initialize()

        sys.stdout.write(f"P3\n{self.image_width} {self.__image_height}\n255\n")
        for i in range(self.__image_height):
            sys.stderr.write(f"\rScanlines remaining: {self.__image_height - i}")
            sys.stderr.flush()
            for j in range(self.image_width):
                pixel_color = Color(0, 0, 0)
                for _ in range(self.samples_per_pixel):
                    ray = self.__get_ray(j, i)
                    pixel_color += self.__ray_color(ray, self.max_depth, world)
                write_color(sys.stdout, self.__pixel_samples_scale * pixel_color)

        sys.stderr.write("\nDone.\n")
