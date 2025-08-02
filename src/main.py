#!/usr/bin/env python3

from vec3 import Vector3, Point3, Color
from objects import HittableList, Sphere, Lambertian, Metal
from camera import Camera


if __name__ == "__main__":
    world = HittableList()

    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left = Metal(Color(0.8, 0.8, 0.8))
    material_right = Metal(Color(0.8, 0.6, 0.2))

    world.add(Sphere(Point3(0.0, -100.5, -1.0), 100.0, material_ground))  # Ground
    world.add(Sphere(Point3(0.0, 0.0, -1.2), 0.5, material_center))
    world.add(Sphere(Point3(-1.0, 0.0, -1.0), 0.5, material_left))
    world.add(Sphere(Point3(1.0, 0.0, -1.0), 0.5, material_right))

    cam = Camera()

    cam.aspect_ratio = 16 / 9
    cam.image_width = 400
    cam.samples_per_pixel = 100
    cam.max_depth = 50

    cam.render(world)
