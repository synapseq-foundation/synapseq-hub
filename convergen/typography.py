# typography.py

import cairo
from utils import mix_colors

LETTER_MAP = {
    "delta": "δ",
    "theta": "θ",
    "alpha": "α",
    "beta": "β",
    "gamma": "γ",
}


def centered_text_origin(ctx, text, center_x, center_y):
    xbearing, ybearing, width, height, _, _ = ctx.text_extents(text)
    return center_x - width / 2 - xbearing, center_y - height / 2 - ybearing


def draw_text_glow(ctx, text, x, y, size, color):
    r, g, b = color
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    for i in range(2, 0, -1):
        ctx.set_font_size(size + i * 2)
        ctx.set_source_rgba(r, g, b, 0.035 * i)
        ctx.move_to(x, y)
        ctx.show_text(text)

    ctx.set_font_size(size)
    ctx.move_to(x + 2, y + 3)
    ctx.set_source_rgba(0.03, 0.025, 0.022, 0.30)
    ctx.show_text(text)

    symbol_color = mix_colors(color, (0.95, 0.88, 0.78), 0.28)
    sr, sg, sb = symbol_color

    ctx.move_to(x, y)
    ctx.text_path(text)
    ctx.set_source_rgba(sr, sg, sb, 0.98)
    ctx.fill_preserve()
    ctx.set_source_rgba(0.98, 0.88, 0.76, 0.18)
    ctx.set_line_width(1.6)
    ctx.stroke()


def draw_greek_letter(ctx, width, height, wave_type, color):
    letter = LETTER_MAP[wave_type]
    size = 286

    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    x, y = centered_text_origin(ctx, letter, width / 2, height * 0.275)
    draw_text_glow(ctx, letter, x, y, size, color)


def draw_title(ctx, title, width, height, color):
    ctx.select_font_face("Avenir Next", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(60)

    xbearing, _, text_width, _, _, _ = ctx.text_extents(title)
    x = (width - text_width) / 2 - xbearing
    y = height - 140

    r, g, b = color
    warm_text = (0.90, 0.84, 0.76)
    accent_text = mix_colors(color, warm_text, 0.34)
    gradient = cairo.LinearGradient(x + xbearing, y, x + xbearing + text_width, y)
    gradient.add_color_stop_rgba(0, *warm_text, 0.94)
    gradient.add_color_stop_rgba(0.58, *accent_text, 0.96)
    gradient.add_color_stop_rgba(
        1, min(r * 1.08, 1), min(g * 1.08, 1), min(b * 1.08, 1), 0.94
    )

    ctx.move_to(x + 1.5, y + 2)
    ctx.text_path(title)
    ctx.set_source_rgba(0.02, 0.018, 0.016, 0.30)
    ctx.fill()

    ctx.move_to(x, y)
    ctx.text_path(title)
    ctx.set_source(gradient)
    ctx.fill()


def draw_brand(ctx, width, height):
    brand = "synapseq.org"

    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgba(0.72, 0.66, 0.60, 0.6)
    ctx.set_font_size(28)

    xbearing, _, text_width, _, _, _ = ctx.text_extents(brand)
    ctx.move_to((width - text_width) / 2 - xbearing, height - 60)
    ctx.show_text(brand)
