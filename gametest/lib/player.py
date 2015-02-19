import math
import pygame
from pygame.math import Vector2
from gametest.lib.entity import Entity
from gametest.lib.math import transform_segment


class Player(Entity):
    def __init__(self, polygons):
        self.polygons = polygons
        self.pos = Vector2(50, 50)
        self.angle = 0
        self.angle_vel = 0
        self.handling_input = False
        self.d_angle = 1
        self.max_angle_vel = 2
        self.vel = Vector2(0, 0)
        self.max_vel = 2
        self.d_vel = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.handling_input = True
            if event.key == pygame.K_LEFT:
                if abs(self.angle_vel) <= self.max_angle_vel:
                    self.angle_vel += self.d_angle
            elif event.key == pygame.K_RIGHT:
                if abs(self.angle_vel) <= self.max_angle_vel:
                    self.angle_vel -= self.d_angle
            elif event.key == pygame.K_a:
                if abs(self.vel.x) <= self.max_vel:
                    self.vel.x -= self.d_vel
            elif event.key == pygame.K_d:
                if abs(self.vel.x) <= self.max_vel:
                    self.vel.x += self.d_vel
            elif event.key == pygame.K_w:
                if abs(self.vel.y) <= self.max_vel:
                    self.vel.y -= self.d_vel
            elif event.key == pygame.K_s:
                if abs(self.vel.y) <= self.max_vel:
                    self.vel.y += self.d_vel
        elif event.type != pygame.KEYDOWN:
            self.handling_input = False

    def update(self, parent):
        if not self.handling_input:
            if self.angle_vel != 0.0:
                self.angle_vel += math.copysign(self.d_angle, -self.angle_vel)
            if self.vel.x != 0.0:
                self.vel.x += math.copysign(self.d_vel, -self.vel.x)
            if self.vel.y != 0.0:
                self.vel.y += math.copysign(self.d_vel, -self.vel.y)
        self.angle += self.angle_vel
        self.pos += self.vel.rotate(-self.angle)

    def draw(self):
        return [transform_segment(seg) for seg in self.polygons]
