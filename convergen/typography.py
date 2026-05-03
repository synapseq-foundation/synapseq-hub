# typography.py

import cairo

LETTER_MAP = {
    "delta": "Δ",
    "theta": "Θ",
    "alpha": "Α",
    "beta": "Β",
    "gamma": "Γ",
}


def centered_text_origin(ctx, text, center_x, center_y):
    xbearing, ybearing, width, height, _, _ = ctx.text_extents(text)
    return center_x - width / 2 - xbearing, center_y - height / 2 - ybearing


def draw_text_glow(ctx, text, x, y, size, color):
    r, g, b = color
    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

    for i in range(5, 0, -1):
        ctx.set_font_size(size + i * 2)
        ctx.set_source_rgba(r, g, b, 0.04 * i)
        ctx.move_to(x, y)
        ctx.show_text(text)

    ctx.set_font_size(size)
    ctx.set_source_rgba(r, g, b, 0.95)
    ctx.move_to(x, y)
    ctx.show_text(text)


def draw_greek_letter(ctx, width, height, wave_type, color):
    letter = LETTER_MAP[wave_type]
    size = 260

    ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    x, y = centered_text_origin(ctx, letter, width / 2, height * 0.28)
    draw_text_glow(ctx, letter, x, y, size, color)


def draw_title(ctx, title, width, height, color):
    ctx.select_font_face("Avenir Next", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(64)

    xbearing, _, text_width, _, _, _ = ctx.text_extents(title)
    x = (width - text_width) / 2 - xbearing
    y = height - 140

    r, g, b = color
    gradient = cairo.LinearGradient(x + xbearing, y, x + xbearing + text_width, y)
    gradient.add_color_stop_rgba(0, 0.95, 0.92, 0.88, 0.95)
    gradient.add_color_stop_rgba(0.55, r, g, b, 0.95)
    gradient.add_color_stop_rgba(
        1, min(r * 1.25, 1), min(g * 1.25, 1), min(b * 1.25, 1), 0.95
    )

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
