# renderer.py

import io

import cairo
from background import draw_background, draw_background_waves, draw_particles
from color import BASE_ACCENT, WAVE_COLOR_MOD, apply_wave_color_mod
from PIL import Image
from typography import draw_brand, draw_greek_letter, draw_title
from utils import create_rng
from waves import draw_main_waves

WIDTH = 1024
HEIGHT = 1024


def resolve_wave_color(wave_type):
    color = apply_wave_color_mod(BASE_ACCENT, WAVE_COLOR_MOD.get(wave_type, 0.0))

    if wave_type == "alpha":
        return (color[0] * 0.8, color[1] * 0.85, color[2] * 0.9)

    return color


def write_webp(surface, output):
    png_buffer = io.BytesIO()
    surface.write_to_png(png_buffer)
    png_buffer.seek(0)

    with Image.open(png_buffer) as image:
        image.convert("RGB").save(output, "WEBP", quality=95, method=6)


def draw_cover(params, title, output, seed=None):
    rng = create_rng(seed)
    wave_type = params["type"]
    color = resolve_wave_color(wave_type)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)

    draw_background(ctx, WIDTH, HEIGHT, color, rng, wave_type)
    draw_background_waves(ctx, WIDTH, HEIGHT, color, rng, wave_type)
    draw_particles(ctx, WIDTH, HEIGHT, color, rng, wave_type)
    draw_main_waves(ctx, WIDTH, HEIGHT, params, color)
    draw_greek_letter(ctx, WIDTH, HEIGHT, wave_type, color)
    draw_title(ctx, title, WIDTH, HEIGHT, color)
    draw_brand(ctx, WIDTH, HEIGHT)

    write_webp(surface, output)
