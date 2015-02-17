import math

import pygame
import pygame.gfxdraw
import yaml

from gametest.lib.entity import Entity
from gametest.lib.math import transform_segment, seg_to_vec, reflect_seg


class Level(Entity):
    def __init__(self, polygons):
        self.polygons = polygons
        self.angle = 0

    def update(self, parent):
        self.angle = parent.entities['player'].angle

    def handle_event(self, event):
        pass

    def transform_polygons(self):
        return [transform_segment(seg,
                                  angle=self.angle)
                for seg in self.polygons]


class Player(Entity):
    def __init__(self, polygons):
        self.polygons = polygons
        self.pos = (0, 0)
        self.angle = 0
        self.angle_vel = 0
        self.handling_input = False
        self.d_angle = 1
        self.max_vel = 2

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.handling_input = True
            if event.key == pygame.K_LEFT:
                if abs(self.angle_vel) <= self.max_vel:
                    self.angle_vel += self.d_angle
            elif event.key == pygame.K_RIGHT:
                if abs(self.angle_vel) <= self.max_vel:
                    self.angle_vel -= self.d_angle
        elif event.type != pygame.KEYDOWN:
            self.handling_input = False

    def update(self, parent):
        if not self.handling_input:
            if self.angle_vel != 0.0:
                self.angle_vel += \
                    math.copysign(self.d_angle, -self.angle_vel)
        self.angle = (self.angle + self.angle_vel) % 360

    def transform_polygons(self):
        return [transform_segment(seg)
                for seg in self.polygons]


class FirstPerson(object):
    def __init__(self, level, player, surface):
        self.entities = {'player': player, 'level': level}
        self.running = True
        self.surface = surface
        self.dim = self.surface.get_size()
        self.fps_clock = pygame.time.Clock()
        self.mouse_pos = (0, 0)
        self.keydown = False

    def run(self):
        while self.running:
            self.main_loop()

    def main_loop(self):
        self.handle_input()
        self.update()
        self.render_frame()

    def update(self):
        for e in self.entities.values():
            e.update(self)

    def render_frame(self):
        self.surface.fill((255, 255, 255))
        for e in self.entities.values():
            poly = e.transform_polygons()
            self.draw_poly(self.surface,
                           self.transform_poly(poly))
        self.fps_clock.tick(60)
        pygame.display.update()

    def transform_poly(self, poly):
        return [transform_segment(seg,
                                  translation=(self.dim[0]/2, self.dim[1]/2))
                for seg in poly]

    def draw_poly(self, surface, poly):
        for seg in poly:
            color = seg.get('color', (255, 85, 85))
            pygame.draw.line(surface, color,
                             seg['start'],
                             seg['end'])

    def handle_input(self):
        pygame.event.pump()
        for event in pygame.event.get():
            for e in self.entities.values():
                e.handle_event(event)
            if event.type == pygame.QUIT:
                self.running = False
                print("quit")
                break
            elif event.type == pygame.KEYDOWN:
                self.keydown = True
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type != pygame.KEYDOWN:
                self.keydown = False


if __name__ == "__main__":
    with open('level.yaml', 'r') as f:
        level_poly = [seg_to_vec(seg) for seg in yaml.load(f)]
    with open('player.yaml', 'r') as f:
        player_poly = [seg_to_vec(seg) for seg in yaml.load(f)]
        player_poly = [reflect_seg(seg) for seg in player_poly]
    surface = pygame.display.set_mode((640, 360))
    player = Player(player_poly)
    level = Level(level_poly)
    demo = FirstPerson(level, player, surface)
    demo.run()
