import math

import pygame
import pygame.gfxdraw
import yaml

from gametest.lib.entity import Entity


class Level(Entity):
    def __init__(self, polygons):
        self.polygons = polygons
        self.angle = 0

    def update(self, parent):
        self.angle = -parent.entities['player'].angle

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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.handling_input = True
            if event.key == pygame.K_LEFT:
                if abs(self.angle_vel) <= pow(2, -3):
                    self.angle_vel += pow(2, -4)
            elif event.key == pygame.K_RIGHT:
                if abs(self.angle_vel) <= pow(2, -3):
                    self.angle_vel -= pow(2, -4)
        elif event.type != pygame.KEYDOWN:
            self.handling_input = False

    def update(self, parent):
        if not self.handling_input:
            if self.angle_vel != 0.0:
                self.angle_vel += \
                    math.copysign(pow(2, -4), -self.angle_vel)
        self.angle = (self.angle + self.angle_vel) % (2. * math.pi)

    def transform_polygons(self):
        return [transform_segment(seg)
                for seg in self.polygons]


def transform_segment(seg, angle=0., translation=(0., 0.), pivot=(0., 0.)):
    start = translate_vector(seg['start'], translation)
    end = translate_vector(seg['end'], translation)
    start = rotate_vector(start, angle, pivot)
    end = rotate_vector(end, angle, pivot)
    return {'start': start, 'end': end, 'color': seg.get('color', None)}


def rotate_vector(vector, angle, pivot):
    p1, p2 = pivot
    v1, v2 = vector
    return [(v1-p1) * math.cos(angle) + (v2-p2) * math.sin(angle) + p1,
            -(v1-p1) * math.sin(angle) + (v2-p2) * math.cos(angle) + p2]


def translate_vector(v, dv):
    return [c + dc for c, dc in zip(v, dv)]


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
            color = seg['color'] or (255, 85, 85)
            pygame.draw.aaline(surface, color,
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
        level_poly = yaml.load(f)
    with open('player.yaml', 'r') as f:
        player_poly = yaml.load(f)
    surface = pygame.display.set_mode((640, 360))
    player = Player(player_poly)
    level = Level(level_poly)
    demo = FirstPerson(level, player, surface)
    demo.run()
