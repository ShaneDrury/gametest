from copy import copy
from pygame.math import Vector2


def update_seg(seg, f, *args, **kwargs):
    """
    Apply f to seg
    """
    new_seg = copy(seg)
    new_seg['start'] = f(seg['start'], *args, **kwargs)
    new_seg['end'] = f(seg['end'], *args, **kwargs)
    return new_seg


def transform_segment(seg, angle=0., translation=None, pivot=None):
    translation = translation or Vector2(0, 0)
    pivot = pivot or Vector2(0, 0)
    return update_seg(seg, transform_vector, angle, translation, pivot)


def transform_vector(vec, angle, translation, pivot):
    return rotate_vector(vec + translation, angle, pivot)


def rotate_vector(vector, angle, pivot):
    return (vector - pivot).rotate(angle) + pivot


def translate_vector(v, dv):
    return v + dv


def seg_to_vec(seg):
    return update_seg(seg, Vector2)


def reflect_seg(seg, plane=None):
    plane = plane or Vector2(0, 1)
    return update_seg(seg, lambda s, p: s.reflect(p), plane)
