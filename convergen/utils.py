# utils.py

import colorsys
import random


def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
    return int(r * 255), int(g * 255), int(b * 255)


def create_rng(seed=None):
    if seed is None:
        seed = random.randint(0, 999999)
    return random.Random(seed)


def clamp(value):
    return max(0, min(1, value))


def mix_colors(a, b, amount):
    return tuple(a[i] * (1 - amount) + b[i] * amount for i in range(3))
