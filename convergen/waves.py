# waves.py

import math


def generate_wave_points(width, height, params, offset=0, scale=1.0):
    points = []

    for x in range(width):
        t = x / width * params["wave_frequency_visual"] * 20
        noise = (1 - params["wave_regularidade"]) * math.sin(x * 0.01)
        y = math.sin(t + offset + noise)
        y *= params["wave_amplitude_visual"] * 200 * scale
        y += height // 2
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


def draw_main_waves(ctx, width, height, params, color):
    for offset, scale in [(0.0, 1.0), (1.2, 0.7), (2.4, 0.4)]:
        points = generate_wave_points(width, height, params, offset, scale)
        draw_glow_line(ctx, points, color, params["wave_thickness"])
