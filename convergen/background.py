# background.py

import math

import cairo
from utils import clamp, mix_colors

SYNAPSEQ_BG_TOP = (0.11, 0.09, 0.08)  # #1c1714
SYNAPSEQ_BG_BOTTOM = (0.086, 0.074, 0.066)  # #161311
SYNAPSEQ_TEAL = (15 / 255, 118 / 255, 110 / 255)
SYNAPSEQ_OCHRE = (180 / 255, 83 / 255, 9 / 255)

BACKGROUND_DYNAMICS = {
    "delta": {"blobs": 3, "waves": 2, "grain": 18, "alpha": 0.08},
    "theta": {"blobs": 4, "waves": 3, "grain": 28, "alpha": 0.09},
    "alpha": {"blobs": 5, "waves": 4, "grain": 36, "alpha": 0.10},
    "beta": {"blobs": 6, "waves": 5, "grain": 48, "alpha": 0.11},
    "gamma": {"blobs": 7, "waves": 6, "grain": 64, "alpha": 0.12},
}

BACKGROUND_COMPLEXITY = {
    "delta": 10,
    "theta": 25,
    "alpha": 35,
    "beta": 50,
    "gamma": 70,
}


def draw_background(ctx, width, height, color, rng, wave_type):
    dynamics = BACKGROUND_DYNAMICS[wave_type]

    base = cairo.LinearGradient(0, 0, 0, height)
    base.add_color_stop_rgb(0, *SYNAPSEQ_BG_TOP)
    base.add_color_stop_rgb(1, *SYNAPSEQ_BG_BOTTOM)
    ctx.set_source(base)
    ctx.paint()

    draw_palette_anchors(ctx, width)
    draw_accent_blobs(ctx, width, height, color, rng, dynamics)
    draw_background_grain(ctx, width, height, color, rng, dynamics)


def draw_palette_anchors(ctx, width):
    grad1 = cairo.RadialGradient(140, 90, 40, 140, 90, 560)
    grad1.add_color_stop_rgba(0, *SYNAPSEQ_TEAL, 0.14)
    grad1.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(grad1)
    ctx.paint()

    grad2 = cairo.RadialGradient(width - 130, 120, 35, width - 130, 120, 520)
    grad2.add_color_stop_rgba(0, *SYNAPSEQ_OCHRE, 0.13)
    grad2.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(grad2)
    ctx.paint()


def accent_pool_for(color):
    return [
        color,
        SYNAPSEQ_TEAL,
        SYNAPSEQ_OCHRE,
        mix_colors(color, SYNAPSEQ_OCHRE, 0.35),
    ]


def draw_accent_blobs(ctx, width, height, color, rng, dynamics):
    for _ in range(dynamics["blobs"]):
        cr, cg, cb = rng.choice(accent_pool_for(color))
        cr, cg, cb = mix_colors((cr, cg, cb), color, rng.uniform(0.15, 0.45))

        x = rng.uniform(-width * 0.12, width * 1.12)
        y = rng.uniform(-height * 0.08, height * 0.78)
        inner = rng.uniform(30, 120)
        outer = rng.uniform(360, 760)
        alpha = rng.uniform(dynamics["alpha"] * 0.45, dynamics["alpha"])

        blob = cairo.RadialGradient(x, y, inner, x, y, outer)
        blob.add_color_stop_rgba(
            0, clamp(cr * 1.08), clamp(cg * 1.04), clamp(cb), alpha
        )
        blob.add_color_stop_rgba(0.42, cr, cg, cb, alpha * 0.35)
        blob.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(blob)
        ctx.paint()


def draw_background_grain(ctx, width, height, color, rng, dynamics):
    for _ in range(dynamics["grain"]):
        cr, cg, cb = rng.choice(accent_pool_for(color))
        ctx.new_path()
        ctx.set_source_rgba(cr, cg, cb, rng.uniform(0.008, 0.022))
        ctx.arc(
            rng.uniform(0, width),
            rng.uniform(0, height),
            rng.uniform(18, 90),
            0,
            2 * math.pi,
        )
        ctx.fill()


def draw_particles(ctx, width, height, color, rng, wave_type):
    r, g, b = color
    density = BACKGROUND_COMPLEXITY[wave_type] + BACKGROUND_DYNAMICS[wave_type]["grain"]

    for _ in range(density):
        ctx.new_path()
        ctx.set_source_rgba(r, g, b, rng.uniform(0.02, 0.06))
        ctx.arc(
            rng.uniform(0, width),
            rng.uniform(0, height),
            rng.uniform(0.5, 2.0),
            0,
            2 * math.pi,
        )
        ctx.fill()


def draw_background_waves(ctx, width, height, color, rng, wave_type):
    dynamics = BACKGROUND_DYNAMICS[wave_type]
    r, g, b = color

    for i in range(dynamics["waves"]):
        ctx.new_path()

        offset = rng.uniform(0, math.tau)
        scale = rng.uniform(0.045, 0.15)
        frequency = rng.uniform(5.5, 13.0) + i * 0.35
        center_y = height * rng.uniform(0.32, 0.68)

        ctx.set_source_rgba(r, g, b, rng.uniform(0.022, 0.055))
        ctx.set_line_width(rng.uniform(1.0, 3.0))
        ctx.move_to(0, center_y)

        for x in range(width):
            t = x / width * frequency
            y = math.sin(t + offset) + math.sin(t * 0.37 + offset * 1.7) * 0.35
            ctx.line_to(x, y * height * scale + center_y)

        ctx.stroke()
