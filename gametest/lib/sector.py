from gametest.lib.math import transform_segment


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


def iter_scan(rect):
    min_x, min_y = rect.bottomleft
    max_x, max_y = rect.topright
    for y in range(min_y, max_y + 1, -1):
        for x in range(min_x, max_x + 1):
            yield (x, y)