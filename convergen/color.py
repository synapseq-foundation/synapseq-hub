# color.py

WAVE_COLOR_MOD = {
    "delta": -0.3,
    "theta": -0.1,
    "alpha": 0.0,
    "beta": +0.1,
    "gamma": +0.2,
}

BASE_ACCENT = (0.78, 0.42, 0.26)  # terracotta base


def apply_wave_color_mod(base_rgb, mod):
    r, g, b = base_rgb

    # ajuste simples de luminância
    factor = 1 + mod

    r = max(0, min(1, r * factor))
    g = max(0, min(1, g * factor))
    b = max(0, min(1, b * factor))

    return r, g, b
