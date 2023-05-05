from PIL import ImageDraw, ImageFont

from properties import properties


def draw_marker(im, x, y):
    if properties.marker == "arrow":
        draw_arrow(im, x, y)
    elif properties.marker == "circle":
        draw_circle(im, x, y)
    elif properties.marker == "bullet":
        draw_bullet(im, x, y)
    elif properties.marker == "rect":
        draw_rect(im, x, y)


def draw_rect(im, x, y):
    draw = ImageDraw.Draw(im)
    draw.rectangle((x - properties.offset, y - properties.offset, x + properties.offset, y + properties.offset),
                   outline="red", width=5)


def draw_arrow(im, x, y):
    draw = ImageDraw.Draw(im)
    start = (x, y)
    corner1 = (x - properties.offset * 2, y + properties.offset)
    center = (x - properties.offset, y + properties.offset)
    corner2 = (x - properties.offset, y + properties.offset * 2)
    draw.polygon([start, corner1, center, corner2], outline="red", fill="red")


def draw_circle(im, x, y):
    draw = ImageDraw.Draw(im)
    draw.ellipse((x - properties.offset, y - properties.offset, x + properties.offset, y + properties.offset),
                 outline="red", width=5)


def draw_bullet(im, x, y):
    draw = ImageDraw.Draw(im)
    draw.ellipse((x - properties.offset, y - properties.offset, x + properties.offset, y + properties.offset),
                 outline="red", fill="red")
    try:
        font = ImageFont.truetype("arial.ttf", size=properties.offset)
    except OSError:
        font = ImageFont.truetype("LiberationSans-Bold.ttf", size=properties.offset)

    draw.text((x, y), "{}".format(properties.screenshots_taken + 1), fill="white", font=font, anchor="mm")
