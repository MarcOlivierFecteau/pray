#!/usr/bin/env python3

from typing import Final

from vec3 import Vector3, Point3, Color
from objects import HittableList, Sphere, Lambertian, Metal, Dielectric
from camera import Camera


if __name__ == "__main__":
    world = HittableList()

    material_ground: Final[Lambertian] = Lambertian(Color(0.8, 0.8, 0.0))
    material_center: Final[Lambertian] = Lambertian(Color(0.1, 0.2, 0.5))
    material_left: Final[Dielectric] = Dielectric(1.5)
    material_bubble: Final[Dielectric] = Dielectric(1.0 / 1.5)
    material_right: Final[Metal] = Metal(Color(0.8, 0.6, 0.2), 0.9)

    world.add(Sphere(Point3(0.0, -100.5, -1.0), 100.0, material_ground))  # Ground
    world.add(Sphere(Point3(0.0, 0.0, -1.2), 0.5, material_center))
    world.add(Sphere(Point3(-1.0, 0.0, -1.0), 0.5, material_left))
    world.add(Sphere(Point3(-1.0, 0.0, -1.0), 0.4, material_bubble))
    world.add(Sphere(Point3(1.0, 0.0, -1.0), 0.5, material_right))

    cam = Camera()

    cam.aspect_ratio = 16 / 9
    cam.image_width = 400
    cam.samples_per_pixel = 100
    cam.max_depth = 50
    cam.vertical_fov = 20.0
    cam.lookfrom = Point3(-2, 2, 1)
    cam.lookat = Point3(0, 0, -1)
    cam.up_direction = Vector3(0, 1, 0)

    cam.render(world)
