import pygame
import pygame.gfxdraw
import yaml


class FirstPerson(object):
    def __init__(self, level):
        self.level = level
        self.running = True
        self.screen = pygame.display.set_mode((640, 360))
        self.fps_clock = pygame.time.Clock()
        self.mouse_pos = (0, 0)

    def run(self):
        while self.running:
            self.main_loop()

    def main_loop(self):
        self.handle_input()
        self.update()
        self.render_frame()

    def update(self):
        pass

    def render_frame(self):
        self.screen.fill((255, 255, 255))
        for seg in self.level:
            pygame.draw.aaline(self.screen, seg['color'], seg['start'],
                               seg['end'])
        self.fps_clock.tick(60)
        pygame.display.update()

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
    demo = FirstPerson(lvl)
    demo.run()