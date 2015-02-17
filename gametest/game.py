import pygame
import pygame.gfxdraw
import yaml
import math


class FirstPerson(object):
    def __init__(self, level, player, surface):
        self.level = level
        self.running = True
        self.surface = surface
        self.dim = self.surface.get_size()
        self.fps_clock = pygame.time.Clock()
        self.mouse_pos = (0, 0)
        self.player_polygons = player
        self.player_pos = (0, 0)
        self.player_angle = 0

    def run(self):
        while self.running:
            self.main_loop()

    def main_loop(self):
        self.handle_input()
        self.update()
        self.render_frame()

    def update(self):
        self.player_angle = (self.player_angle + 0.01) % (2. * math.pi)

    def render_frame(self):
        self.surface.fill((255, 255, 255))
        for seg in self.level:
            self.draw_segment(self.surface, seg)
        self.draw_player()
        self.fps_clock.tick(60)
        pygame.display.update()

    def draw_player(self):
        for seg in self.player_polygons:
            self.draw_segment(self.surface, seg,
                              translation=(self.dim[0]/2,
                                           self.dim[1]/2))

    def draw_segment(self, screen, seg, angle=0., translation=(0., 0.)):
        start = self.translate_vector(seg['start'], translation)
        end = self.translate_vector(seg['end'], translation)
        start = self.rotate_vector(start, angle)
        end = self.rotate_vector(end, angle)
        pygame.draw.aaline(screen, seg.get('color', (255, 85, 85)), start, end)

    def rotate_vector(self, vector, angle, pivot=None):
        p1, p2 = pivot or (self.dim[0]/2, self.dim[1]/2)
        v1, v2 = vector
        return [(v1-p1) * math.cos(angle) + (v2-p2) * math.sin(angle) + p1,
                -(v1-p1) * math.sin(angle) + (v2-p2) * math.cos(angle) + p2]

    def translate_vector(self, v, dv):
        return [c + dc for c, dc in zip(v, dv)]

    def handle_input(self):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                print("quit")
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

if __name__ == "__main__":
    with open('level.yaml', 'r') as f:
        lvl = yaml.load(f)
    with open('player.yaml', 'r') as f:
        player = yaml.load(f)
    surface = pygame.display.set_mode((640, 360))
    demo = FirstPerson(lvl, player, surface)
    demo.run()
