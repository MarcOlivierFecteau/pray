#!/usr/bin/env python3

from typing import Final
import random

from vec3 import Vector3, Point3
from color import Color
from hittable import HittableList
from material import Lambertian, Metal, Dielectric
from objects import Sphere
from camera import Camera


if __name__ == "__main__":
    world = HittableList()

    ground_material: Final[Lambertian] = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0.0, -1000, 0.0), 1000.0, ground_material))

    for a in range(-3, 3):
        for b in range(-3, 3):
            choose_material = random.random()
            center = Point3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())

            if (center - Point3(4.0, 0.2, 0.0)).mag > 0.9:
                if choose_material < 0.8:  # Diffuse
                    albedo = Color.random() * Color.random()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_material < 0.95:  # Metal
                    albedo = Color.randrange(0.5, 1.0)
                    fuzz = 0.5 * random.random()
                    sphere_material = Metal(albedo, fuzz)
                else:  # Glass
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1: Final[Dielectric] = Dielectric(1.5)
    world.add(Sphere(Point3(0.0, 1.0, 0.0), 1.0, material1))

    material2: Final[Lambertian] = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4.0, 1.0, 0.0), 1.0, material2))

    material3: Final[Metal] = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4.0, 1.0, 0.0), 1.0, material3))

    cam = Camera()

    cam.aspect_ratio = 16 / 9
    cam.image_width = 400
    cam.samples_per_pixel = 10
    cam.max_depth = 50
    cam.vertical_fov = 20.0
    cam.lookfrom = Point3(13, 2, 3)
    cam.lookat = Point3(0, 0, 0)
    cam.up_direction = Vector3(0, 1, 0)
    cam.defocus_angle = 0.6
    cam.focus_distance = 10.0

    cam.render(world)
