from pygame.math import Vector2
from gametest.lib.entity import Entity
from gametest.lib.math import transform_segment


class Level(Entity):
    def __init__(self, polygons):
        self.polygons = polygons
        self.angle = 0
        self.pos = Vector2(0, 0)

    def update(self, parent):
        self.angle = parent.entities['player'].angle
        self.pos = parent.entities['player'].pos

    def handle_event(self, event):
        pass

    def draw(self):
        return [transform_segment(seg,
                                  translation=-self.pos,
                                  angle=self.angle)
                for seg in self.polygons]
