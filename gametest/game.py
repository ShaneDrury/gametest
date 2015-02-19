import pygame
import pygame.gfxdraw
from pygame.rect import Rect
import yaml

from gametest.lib.level import Level
from gametest.lib.math import seg_to_vec, reflect_seg, transform_segment
from gametest.lib.player import Player
from gametest.lib.sector import RectSector
from gametest.lib.view import View3D


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
        player_poly = [transform_segment(seg, angle=90) for seg in player_poly]
        # player_poly = [reflect_seg(seg) for seg in player_poly]
    surface = pygame.display.set_mode((200, 100))
    player = Player(player_poly)
    level = Level(level_poly)
    demo = FirstPerson(level, player, surface)
    demo.run()
