from pygame.math import Vector2


def transform_segment(seg, angle=0., translation=None, pivot=None):
    translation = translation or Vector2(0, 0)
    pivot = pivot or Vector2(0, 0)
    start = transform_vector(seg['start'], angle, translation, pivot)
    end = transform_vector(seg['end'], angle, translation, pivot)
    return {'start': start, 'end': end, 'color': seg.get('color', None)}


def transform_vector(vec, angle, translation, pivot):
    return rotate_vector(vec + translation, angle, pivot)


def rotate_vector(vector, angle, pivot):
    return (vector - pivot).rotate(angle) + pivot


def translate_vector(v, dv):
    return v + dv


def seg_to_vec(seg):
    seg['start'] = Vector2(seg['start'])
    seg['end'] = Vector2(seg['end'])
    return seg
