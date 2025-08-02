#!/usr/bin/env python3

import math
import random
import sys
from typing import Final
from vec3 import Vector3, Point3
from color import Color, write_color
from interval import Interval
from hittable import HitRecord, HittableList
from ray import Ray


class Camera:
    aspect_ratio: float = 1.0  # image_width / image_height
    image_width: int = 100  # px
    samples_per_pixel: int = 10  # Random samples for each pixel
    max_depth: int = 10  # Maximum number of ray bounces into scene
    vertical_fov: float = 90.0  # deg
    horizontal_fov: float = 90.0  # deg
    lookfrom: Point3 = Point3.zero()
    lookat: Point3 = Point3(0.0, 0.0, -1.0)
    up_direction: Vector3 = Vector3(0.0, 1.0, 0.0)
    defocus_angle: float = 0.0  # Variation angle of rays through each pixel (deg)
    focus_distance: float = 10.0  # Distance from camera to plane of perfect focus (m)

    image_height: int  # px
    center: Point3
    pixel00_location: Point3
    pixel_delta_u: Vector3
    pixel_delta_v: Vector3
    pixel_samples_scale: float  # Color scale factor for a sum of pizel samples
    u: Vector3
    v: Vector3
    w: Vector3
    defocus_disk_u: Vector3
    defocus_disk_v: Vector3

    def __init__(self):
        pass

    def ray_color(self, ray: Ray, depth: int, world: HittableList):
        if depth <= 0:  # No more light is gathered
            return Color.zero()

        record = HitRecord()
        hit_anything, record = world.hit(ray, Interval(0.001, math.inf), record)
        if hit_anything:
            ret: bool
            scattered: Ray
            attenuation: Color
            ret, scattered, attenuation = record.material.scatter(ray, record)
            if ret:
                return attenuation * self.ray_color(scattered, depth - 1, world)
            return Color.zero()

        direction = ray.direction.unit
        a = 0.5 * (direction.y + 1.0)
        one: Final[Color] = Color.one()
        return (1.0 - a) * one + a * Color(0.5, 0.7, 1.0)

    def initialize(self):
        self.image_height = int(self.image_width / self.aspect_ratio)
        if self.image_height < 1:
            self.image_height = 1

        self.pixel_samples_scale = 1 / self.samples_per_pixel

        self.center = self.lookfrom

        # Determine viewport dimensions
        theta = math.radians(self.vertical_fov)
        h = math.tan(theta / 2)
        viewport_height = 2 * h * self.focus_distance
        viewport_width = viewport_height * (self.image_width / self.image_height)

        # Calculate the basis unit vectors for the camera coordinate frame
        self.w = (self.lookfrom - self.lookat).unit
        self.u = Vector3.cross(self.up_direction, self.w).unit
        self.v = Vector3.cross(self.w, self.u)

        # Calculate the vectors across the horizontal and down the vertical viewport edges
        viewport_u = viewport_width * self.u
        viewport_v = viewport_height * -self.v

        # Calculate the horizontal and vertical delta vectors from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate the location of the upper left pixel
        viewport_upper_left = (
            self.center
            - (self.focus_distance * self.w)
            - viewport_u / 2.0
            - viewport_v / 2.0
        )
        self.pixel00_location = viewport_upper_left + 0.5 * (
            self.pixel_delta_u + self.pixel_delta_v
        )

        # Calculate the camera defocus disk basic vectors
        defocus_radius = self.focus_distance * math.tan(
            math.radians(self.defocus_angle / 2.0)
        )
        self.defocus_disk_u = self.u * defocus_radius
        self.defocus_disk_v = self.v * defocus_radius

    def sample_square(self):
        """
        Returns the vector to a random point in the [(-0.5, -0.5), (0.5, 0.5)] unit square.
        """
        return Vector3(random.random() - 0.5, random.random() - 0.5, 0)

    def defocus_disk_sample(self):
        """
        Returns a random point in the camera defocus disk.
        """
        p = Vector3.random_in_unit_disk()
        return self.center + p.x * self.defocus_disk_u + p.y * self.defocus_disk_v

    def get_ray(self, i: int, j: int):
        """
        Construct a camera ray originating from the defocus disk and directed at a randomly
        sampled point around the pixel location (i, j).
        """
        offset = self.sample_square()
        pixel_sample = (
            self.pixel00_location
            + ((i + offset.x) * self.pixel_delta_u)
            + ((j + offset.x) * self.pixel_delta_v)
        )
        ray_origin = (
            self.center if self.defocus_angle <= 0.0 else self.defocus_disk_sample()
        )
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)

    def render(self, world: HittableList):
        self.initialize()

        sys.stdout.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
        for i in range(self.image_height):
            sys.stderr.write(f"\rScanlines remaining: {self.image_height - i}")
            sys.stderr.flush()
            for j in range(self.image_width):
                pixel_color = Color.zero()
                for _ in range(self.samples_per_pixel):
                    ray = self.get_ray(j, i)
                    pixel_color = pixel_color + self.ray_color(
                        ray, self.max_depth, world
                    )
                write_color(sys.stdout, self.pixel_samples_scale * pixel_color)

        sys.stderr.write("\nDone.\n")
