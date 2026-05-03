# waves.py

import math


MAIN_WAVE_VARIATION = {
    "delta": {"phase": 0.35, "frequency": 0.04, "amplitude": 0.06, "center": 18, "noise": 0.12, "width": 0.08},
    "theta": {"phase": 0.55, "frequency": 0.06, "amplitude": 0.08, "center": 24, "noise": 0.18, "width": 0.10},
    "alpha": {"phase": 0.75, "frequency": 0.08, "amplitude": 0.10, "center": 30, "noise": 0.24, "width": 0.12},
    "beta": {"phase": 0.95, "frequency": 0.11, "amplitude": 0.14, "center": 38, "noise": 0.32, "width": 0.14},
    "gamma": {"phase": 1.20, "frequency": 0.14, "amplitude": 0.18, "center": 46, "noise": 0.42, "width": 0.16},
}


def generate_wave_points(width, height, params, offset=0, scale=1.0, variation=None):
    variation = variation or {}
    points = []
    frequency = params["wave_frequency_visual"] * variation.get("frequency", 1.0)
    amplitude = params["wave_amplitude_visual"] * variation.get("amplitude", 1.0)
    noise_phase = variation.get("noise_phase", 0.0)
    noise_scale = variation.get("noise_scale", 1.0)
    center_y = height // 2 + variation.get("center_shift", 0.0)

    for x in range(width):
        t = x / width * frequency * 20
        noise = (1 - params["wave_regularidade"]) * math.sin(x * 0.01 * noise_scale + noise_phase)
        y = math.sin(t + offset + noise)
        y *= amplitude * 200 * scale
        y += center_y
        points.append((x, y))

    return points


def draw_glow_line(ctx, points, color, base_width):
    r, g, b = color

    for i in range(4, 0, -1):
        draw_line(ctx, points, color, base_width + i * 4, 0.03 * i)

    draw_line(ctx, points, (r, g, b), base_width, 0.9)


def draw_line(ctx, points, color, width, alpha):
    r, g, b = color
    ctx.new_path()
    ctx.set_source_rgba(r, g, b, alpha)
    ctx.set_line_width(width)
    ctx.move_to(points[0][0], points[0][1])

    for x, y in points[1:]:
        ctx.line_to(x, y)

    ctx.stroke()


def wave_variation_for(params, rng):
    limits = MAIN_WAVE_VARIATION[params["type"]]
    return {
        "frequency": 1 + rng.uniform(-limits["frequency"], limits["frequency"]),
        "amplitude": 1 + rng.uniform(-limits["amplitude"], limits["amplitude"]),
        "center_shift": rng.uniform(-limits["center"], limits["center"]),
        "noise_phase": rng.uniform(0, math.tau),
        "noise_scale": 1 + rng.uniform(-limits["noise"], limits["noise"]),
        "width": 1 + rng.uniform(-limits["width"], limits["width"]),
        "phase": rng.uniform(-limits["phase"], limits["phase"]),
    }


def draw_main_waves(ctx, width, height, params, color, rng):
    for offset, scale in [(0.0, 1.0), (1.2, 0.7), (2.4, 0.4)]:
        variation = wave_variation_for(params, rng)
        points = generate_wave_points(width, height, params, offset + variation["phase"], scale, variation)
        draw_glow_line(ctx, points, color, params["wave_thickness"] * variation["width"])
