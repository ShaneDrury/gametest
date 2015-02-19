import math
from pygame.math import Vector2
from gametest.lib.entity import Entity


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
        to_return = []
        angle = self.angle / 180 * math.pi
        for seg in self.level:
            start = seg['start'] - self.pos
            end = seg['end'] - self.pos
            tz = 
            tz1 = start.x * math.cos(angle) + start.y * math.sin(angle)
            tz2 = end.x * math.cos(angle) + end.y * math.sin(angle)
            tx1 = start.x * math.sin(angle) - start.y * math.cos(angle)
            tx2 = end.x * math.sin(angle) - end.y * math.cos(angle)
            to_return.append({'start': Vector2(-tx1, -tz1),
                              'end': Vector2(-tx2, -tz2)})
        return to_return


def cross(v1, v2):
    return v1.x * v2.y - v1.y * v2.x


def intersect(v1, v2, v3, v4):
    x = cross(v1, v2)
    y = cross(v3, v4)
    det = float(cross(v1-v2, v3-v4))
    x = cross(Vector2(x, v1.x-v2.x), Vector2(y, v3.x-v4.x)) / det
    y = cross(Vector2(y, v1.y-v2.y), Vector2(y, v3.y-v4.y)) / det
    return Vector2(x, y)