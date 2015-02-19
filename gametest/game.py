import pygame

import pygame.gfxdraw
from pygame.math import Vector2
from pygame.rect import Rect
import yaml

from gametest.lib.level import Level
from gametest.lib.entity import Entity

from gametest.lib.math import transform_segment, seg_to_vec, reflect_seg
from gametest.lib.player import Player


class View3D(Entity):
    def __init__(self, sector, level):
        self.level = level.polygons
        self.angle = 0
        self.pos = Vector2(0, 0)
        self.sector = sector

    def update(self, parent):
        self.angle = parent.entities['player'].angle
        self.pos = parent.entities['player'].pos

    def handle_event(self, event):
        pass

    def draw(self):
        # for x, y in iter_scan(self.sector.rect):
        #     pass
        return self.level


def iter_scan(rect):
    min_x, min_y = rect.bottomleft
    max_x, max_y = rect.topright
    for y in range(min_y, max_y + 1, -1):
        for x in range(min_x, max_x + 1):
            yield (x, y)


class Sector(object):
    """
    A section of a surface.
    """
    def transform(self, poly):
        pass


class RectSector(Sector):
    def __init__(self, rect):
        self.rect = rect

    def transform(self, poly):
        return [transform_segment(
            seg,
            translation=(self.rect.left + self.rect.width/2,
                         self.rect.top + self.rect.height/2))
                for seg in poly]


class FirstPerson(object):
    def __init__(self, level, player, surface):
        self.running = True
        self.surface = surface
        self.dim = self.surface.get_size()
        self.fps_clock = pygame.time.Clock()
        right_sector = RectSector(Rect(self.dim[0]/2, 0, self.dim[0]/2, self.dim[1]))
        self.sectors = {
            RectSector(Rect(0, 0, self.dim[0]/2, self.dim[1])):
                ['player', 'level'],  # TODO: ref obj directly?
            right_sector:
                ['view_3d']
        }
        view_3d = View3D(right_sector, level)
        self.entities = {'player': player, 'level': level,
                         'view_3d': view_3d}
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
        for sector, entities in self.sectors.items():
            for e in entities:
                entity = self.entities[e]
                poly = sector.transform(entity.draw())
                self.draw_poly(self.surface, poly)
        self.fps_clock.tick(60)
        pygame.display.update()

    def draw_poly(self, surface, poly):
        for seg in poly:
            color = seg.get('color', (255, 85, 85))
            pygame.draw.line(surface, color, seg['start'], seg['end'])

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
    surface = pygame.display.set_mode((1280, 480))
    player = Player(player_poly)
    level = Level(level_poly)
    demo = FirstPerson(level, player, surface)
    demo.run()
