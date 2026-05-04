# waves.py

import math

import cairo


MAIN_WAVE_VARIATION = {
    "delta": {"phase": 0.24, "frequency": 0.030, "amplitude": 0.045, "center": 12, "width": 0.05, "harmonic": 0.018, "envelope": 0.06, "secondary": 0.34},
    "theta": {"phase": 0.36, "frequency": 0.045, "amplitude": 0.060, "center": 16, "width": 0.06, "harmonic": 0.026, "envelope": 0.11, "secondary": 0.40},
    "alpha": {"phase": 0.48, "frequency": 0.055, "amplitude": 0.070, "center": 18, "width": 0.08, "harmonic": 0.030, "envelope": 0.08, "secondary": 0.36},
    "beta": {"phase": 0.62, "frequency": 0.075, "amplitude": 0.090, "center": 24, "width": 0.10, "harmonic": 0.040, "envelope": 0.07, "secondary": 0.32},
    "gamma": {"phase": 0.76, "frequency": 0.095, "amplitude": 0.110, "center": 30, "width": 0.12, "harmonic": 0.048, "envelope": 0.055, "secondary": 0.28},
}

WAVE_LAYERS = [(0.0, 1.0), (1.2, 0.68), (2.4, 0.38)]


def generate_wave_points(width, height, params, offset=0, scale=1.0, variation=None):
    variation = variation or {}
    points = []
    frequency = params["wave_frequency_visual"] * variation.get("frequency", 1.0)
    amplitude = params["wave_amplitude_visual"] * variation.get("amplitude", 1.0)
    harmonic_2 = variation.get("harmonic_2", 0.0)
    harmonic_3 = variation.get("harmonic_3", 0.0)
    harmonic_phase = variation.get("harmonic_phase", 0.0)
    envelope_depth = variation.get("envelope_depth", 0.0)
    envelope_rate = variation.get("envelope_rate", 0.32)
    envelope_phase = variation.get("envelope_phase", 0.0)
    center_y = height // 2 + variation.get("center_shift", 0.0)

    for x in range(width):
        t = x / width * frequency * 20
        structural_phase = t + offset
        y = math.sin(structural_phase)
        y += harmonic_2 * math.sin(structural_phase * 2.0 + harmonic_phase)
        y += harmonic_3 * math.sin(structural_phase * 3.0 - harmonic_phase * 0.55)

        envelope = 1 + envelope_depth * math.sin(t * envelope_rate + envelope_phase)
        y *= amplitude * 200 * scale * envelope
        y += center_y
        points.append((x, y))

    return points


def draw_signature_wave(ctx, points, secondary_points, color, base_width, variation, intensity):
    r, g, b = color

    draw_line(ctx, points, color, base_width + 7, 0.036 * intensity)
    draw_line(ctx, points, color, base_width + 3, 0.055 * intensity)
    draw_variable_line(
        ctx,
        secondary_points,
        (r, g, b),
        max(base_width * 0.56, 1),
        0.22 * variation["secondary_alpha"] * intensity,
        variation["width_phase"] + 0.8,
        variation["width_depth"] * 0.55,
    )

    draw_variable_line(
        ctx,
        points,
        (r, g, b),
        base_width,
        0.74 * intensity,
        variation["width_phase"],
        variation["width_depth"],
    )


def draw_line(ctx, points, color, width, alpha):
    r, g, b = color
    ctx.new_path()
    ctx.set_source_rgba(r, g, b, alpha)
    ctx.set_line_width(width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(points[0][0], points[0][1])

    for x, y in points[1:]:
        ctx.line_to(x, y)

    ctx.stroke()


def draw_variable_line(ctx, points, color, base_width, alpha, phase, depth):
    r, g, b = color
    step = 7

    ctx.set_source_rgba(r, g, b, alpha)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)

    for i in range(0, len(points) - step, step):
        progress = i / len(points)
        width = base_width * (1 + depth * math.sin(progress * math.tau * 1.35 + phase))

        ctx.new_path()
        ctx.set_line_width(width)
        ctx.move_to(points[i][0], points[i][1])

        for x, y in points[i + 1 : i + step + 1]:
            ctx.line_to(x, y)

        ctx.stroke()


def wave_variation_for(params, rng):
    limits = MAIN_WAVE_VARIATION[params["type"]]
    harmonic = rng.uniform(limits["harmonic"] * 0.70, limits["harmonic"])

    return {
        "frequency": 1 + rng.uniform(-limits["frequency"], limits["frequency"]),
        "amplitude": 1 + rng.uniform(-limits["amplitude"], limits["amplitude"]),
        "center_shift": rng.uniform(-limits["center"], limits["center"]),
        "harmonic_2": harmonic,
        "harmonic_3": harmonic * 0.38,
        "harmonic_phase": rng.uniform(0, math.tau),
        "envelope_depth": rng.uniform(limits["envelope"] * 0.70, limits["envelope"]),
        "envelope_rate": rng.uniform(0.22, 0.42),
        "envelope_phase": rng.uniform(0, math.tau),
        "secondary_alpha": limits["secondary"],
        "secondary_phase": rng.uniform(0.24, 0.42),
        "secondary_shift": rng.uniform(3, 7),
        "width": 1 + rng.uniform(-limits["width"], limits["width"]),
        "width_depth": rng.uniform(0.045, 0.085),
        "width_phase": rng.uniform(0, math.tau),
        "phase": rng.uniform(-limits["phase"], limits["phase"]),
    }


def draw_main_waves(ctx, width, height, params, color, rng):
    for layer_index, (offset, scale) in enumerate(WAVE_LAYERS):
        variation = wave_variation_for(params, rng)
        layer_phase = offset + variation["phase"]
        points = generate_wave_points(width, height, params, layer_phase, scale, variation)
        secondary = generate_wave_points(
            width,
            height,
            params,
            layer_phase + variation["secondary_phase"],
            scale * 0.92,
            variation | {"center_shift": variation["center_shift"] + variation["secondary_shift"]},
        )
        draw_signature_wave(
            ctx,
            points,
            secondary,
            color,
            params["wave_thickness"] * variation["width"],
            variation,
            1 - layer_index * 0.18,
        )
