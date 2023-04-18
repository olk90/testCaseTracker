import argparse
import os
import platform
from io import BytesIO

import pyautogui
import pyscreenshot as pss
from PIL import ImageDraw, ImageFont
from docx import Document
from docx.shared import Cm
from pynput.mouse import Listener as MouseListener, Button


class RuntimeProperties:
    screenshots_taken = 0
    file_path = ""
    marker = "rect"
    offset = 32


properties = RuntimeProperties()


def on_click(x, y, button, pressed):
    if button == Button.middle and pressed:

        im, x, y = get_image(x, y)
        draw_marker(im, x, y)
        write_to_file(im)

        properties.screenshots_taken += 1
        if properties.screenshots_taken == 1:
            print("Took first screenshot")
        else:
            print("Took {} screenshots".format(properties.screenshots_taken))


def get_image(x, y):
    system = platform.system()
    if system == "Linux":
        # TODO This won't work on Wayland.
        im = pss.grab(backend="pil")
    elif system == "Windows":
        im, relative_x, relative_y = pyautogui_screenshot()
        x -= relative_x
        y -= relative_y
    else:
        raise Exception("Unsupported operating system: {}".format(system))
    return im, x, y


def pyautogui_screenshot():
    window = pyautogui.getActiveWindow()
    wpx = window.topleft.x
    wpy = window.topleft.y
    ww = window.width
    wh = window.height
    return pyautogui.screenshot(region=(wpx, wpy, ww, wh)), window.left, window.top


def write_to_file(im):
    im_bytes = BytesIO()
    im.save(im_bytes, format="png")
    im_bytes.seek(0)
    if os.path.exists(properties.file_path):
        doc = Document(properties.file_path)
    else:
        doc = Document()
    page_width = doc.sections[0].page_width.cm - doc.sections[0].left_margin.cm - doc.sections[0].right_margin.cm
    paragraph = doc.add_paragraph()
    run = paragraph.add_run()
    run.add_picture(im_bytes, width=Cm(page_width))
    doc.save(properties.file_path)


def draw_marker(im, x, y):
    if properties.marker == "arrow":
        draw_arrow(im, x, y)
    elif properties.marker == "circle":
        draw_circle(im, x, y)
    elif properties.marker == "bullet":
        draw_bullet(im, x, y)
    else:
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

    draw.text((x, y), "{}".format(properties.screenshots_taken), fill="white", font=font, anchor="mm")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help="target file to store the screenshots")
    parser.add_argument("-m", "--marker", type=str, choices=["arrow", "rect", "circle", "bullet"],
                        help="symbol that marks the clicked")
    args = parser.parse_args()

    if args.marker:
        properties.marker = args.marker

    properties.file_path = args.file

    try:
        print("Use middle click to take a screenshot!")
        with MouseListener(on_click=on_click) as ml:
            ml.join()
    except KeyboardInterrupt:
        print("\n Good bye!")
