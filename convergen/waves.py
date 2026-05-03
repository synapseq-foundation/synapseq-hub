# waves.py

import math

import cairo


MAIN_WAVE_VARIATION = {
    "delta": {"phase": 0.30, "frequency": 0.035, "amplitude": 0.050, "center": 14, "noise": 0.08, "width": 0.06, "harmonic": 0.020},
    "theta": {"phase": 0.45, "frequency": 0.050, "amplitude": 0.065, "center": 18, "noise": 0.12, "width": 0.08, "harmonic": 0.028},
    "alpha": {"phase": 0.60, "frequency": 0.065, "amplitude": 0.080, "center": 22, "noise": 0.16, "width": 0.10, "harmonic": 0.035},
    "beta": {"phase": 0.78, "frequency": 0.085, "amplitude": 0.105, "center": 28, "noise": 0.22, "width": 0.12, "harmonic": 0.045},
    "gamma": {"phase": 0.96, "frequency": 0.105, "amplitude": 0.130, "center": 34, "noise": 0.28, "width": 0.14, "harmonic": 0.055},
}


def generate_wave_points(width, height, params, offset=0, scale=1.0, variation=None):
    variation = variation or {}
    points = []
    frequency = params["wave_frequency_visual"] * variation.get("frequency", 1.0)
    amplitude = params["wave_amplitude_visual"] * variation.get("amplitude", 1.0)
    noise_phase = variation.get("noise_phase", 0.0)
    noise_scale = variation.get("noise_scale", 1.0)
    harmonic = variation.get("harmonic", 0.0)
    harmonic_phase = variation.get("harmonic_phase", 0.0)
    center_y = height // 2 + variation.get("center_shift", 0.0)

    for x in range(width):
        t = x / width * frequency * 20
        noise = (1 - params["wave_regularidade"]) * math.sin(x * 0.01 * noise_scale + noise_phase)
        y = math.sin(t + offset + noise)
        y += harmonic * math.sin(t * 2.15 + harmonic_phase)
        y *= amplitude * 200 * scale
        y += center_y
        points.append((x, y))

    return points


def draw_glow_line(ctx, points, color, base_width):
    r, g, b = color

    draw_line(ctx, points, color, base_width + 9, 0.055)
    draw_line(ctx, points, color, base_width + 4, 0.075)
    draw_line(ctx, offset_points(points, 0, 3), (r, g, b), max(base_width * 0.55, 1), 0.22)

    draw_line(ctx, points, (r, g, b), base_width, 0.78)


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


def offset_points(points, dx, dy):
    return [(x + dx, y + dy) for x, y in points]


def wave_variation_for(params, rng):
    limits = MAIN_WAVE_VARIATION[params["type"]]
    return {
        "frequency": 1 + rng.uniform(-limits["frequency"], limits["frequency"]),
        "amplitude": 1 + rng.uniform(-limits["amplitude"], limits["amplitude"]),
        "center_shift": rng.uniform(-limits["center"], limits["center"]),
        "noise_phase": rng.uniform(0, math.tau),
        "noise_scale": 1 + rng.uniform(-limits["noise"], limits["noise"]),
        "harmonic": rng.uniform(limits["harmonic"] * 0.35, limits["harmonic"]),
        "harmonic_phase": rng.uniform(0, math.tau),
        "width": 1 + rng.uniform(-limits["width"], limits["width"]),
        "phase": rng.uniform(-limits["phase"], limits["phase"]),
    }


def draw_main_waves(ctx, width, height, params, color, rng):
    for offset, scale in [(0.0, 1.0), (1.2, 0.7), (2.4, 0.4)]:
        variation = wave_variation_for(params, rng)
        points = generate_wave_points(width, height, params, offset + variation["phase"], scale, variation)
        draw_glow_line(ctx, points, color, params["wave_thickness"] * variation["width"])
