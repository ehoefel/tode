from textual.color import Color


def get_contrasting_color(color: Color) -> Color:
    import math
    minContrast = 128
    maxContrast = 255
    r, g, b = color.rgb
    y = int(0.299 * r + 0.587 * g + 0.114 * b)
    oy = 255 - y
    dy = oy - y
    if abs(dy) > maxContrast:
        dy = math.copysign(maxContrast, dy)
        oy = y + dy
    elif abs(dy) < minContrast:
        dy = math.copysign(minContrast, dy)
        oy = y + dy
    return Color(int(oy), int(oy), int(oy))
