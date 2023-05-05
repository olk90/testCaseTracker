import argparse
import os
import platform
from io import BytesIO

from docx import Document
from docx.shared import Cm
from pynput.mouse import Listener as MouseListener, Button

from draw.draw_functions import draw_marker
from properties import properties
from screenshots.pyautogui_screenshots import pyautogui_screenshot
from screenshots.xlib_screenshots import xlib_screenshot


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
        is_wayland = os.environ.get("WAYLAND_DISPLAY")
        is_x11 = os.environ.get("DISPLAY")
        if is_wayland:
            raise Exception("Wayland is not yet implemented")
        elif is_x11:
            im, relative_x, relative_y = xlib_screenshot()
            x -= relative_x
            y -= relative_y
        else:
            raise Exception("Unsupported display server")
    elif system == "Windows":
        im, relative_x, relative_y = pyautogui_screenshot()
        x -= relative_x
        y -= relative_y
    else:
        raise Exception("Unsupported operating system: {}".format(system))
    return im, x, y


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


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help="target file to store the screenshots")
    parser.add_argument("-m", "--marker", type=str, choices=["arrow", "rect", "circle", "bullet", "none"],
                        help="Symbol that marks the clicked area. Default is 'none' ('none' is providing no marker at all)")
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
