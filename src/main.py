#!/usr/bin/env python3

import math
import sys

from vec3 import Vector3, Point3, Color, write_color
from ray import Ray
from objects import Interval, HitRecord, Hittable, HittableList, Sphere


def ray_color(ray: Ray, world: HittableList):
    record = HitRecord()
    hit_anything, record = world.hit(ray, Interval(0.0, math.inf), record)
    if hit_anything:
        return 0.5 * (record.normal + Vector3.splat(1))

    direction = ray.direction.unit
    a = 0.5 * (direction.y + 1.0)
    return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)


if __name__ == "__main__":
    # Image

    aspect_ratio = 16 / 9
    image_width = 400
    image_height = int(image_width / aspect_ratio)
    if image_height < 1:
        image_height = 1

    # World

    world = HittableList()
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100.0))

    # Camera

    focal_length = 1.0  # mm
    viewport_height = 2.0
    viewport_width = viewport_height * (image_width / image_height)
    camera_center = Point3.zero()

    # Calculate the vectors across the horizontal and down the vertical viewport edges
    viewport_u = Vector3(viewport_width, 0, 0)
    viewport_v = Vector3(0, -viewport_height, 0)

    # Calculate the horizontal and vertical delta vectors from pixel to pixel
    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    # Calculate the location of the upper left pixel
    viewport_upper_left = (
        camera_center - Vector3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
    )
    pixel00_location = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

    # Render

    print(f"P3\n{image_width} {image_height}\n255")

    for i in range(image_height):
        for j in range(image_width):
            pixel_center = (
                pixel00_location
                + (float(j) * pixel_delta_u)
                + (float(i) * pixel_delta_v)
            )
            ray_direction = pixel_center - camera_center
            ray = Ray(camera_center, ray_direction)

            pixel_color = ray_color(ray, world)
            write_color(sys.stdout, pixel_color)
