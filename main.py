import argparse
import os
import platform
from io import BytesIO

import pyautogui
import pyscreenshot as pss
from PIL import ImageDraw
from docx import Document
from docx.shared import Cm
from pynput.mouse import Listener as MouseListener, Button


class RuntimeProperties:
    screenshots_taken = 0
    file_path = ""


properties = RuntimeProperties()


def take_screenshot():
    window = pyautogui.getActiveWindow()
    wpx = window.topleft.x
    wpy = window.topleft.y
    ww = window.width
    wh = window.height
    return pyautogui.screenshot(region=(wpx, wpy, ww, wh)), window.left, window.top


def on_click(x, y, button, pressed):
    if button == Button.middle and pressed:

        system = platform.system()
        if system == "Linux":
            # TODO This won't work on Wayland.
            im = pss.grab(backend="pil")
        elif system == "Windows":
            im, relative_x, relative_y = take_screenshot()
            x -= relative_x
            y -= relative_y
        else:
            raise Exception("Unsupported operating system: {}".format(system))

        draw = ImageDraw.Draw(im)
        offset = 32
        draw.rectangle((x - offset, y - offset, x + offset, y + offset), outline="red", width=5)

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
        properties.screenshots_taken += 1
        if properties.screenshots_taken == 1:
            print("Took first screenshot")
        else:
            print("Took {} screenshots".format(properties.screenshots_taken))


if __name__ == "__main__":
    print("Use middle click to take a screenshot!")

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True, help="target file to store the screenshots")
    args = parser.parse_args()
    properties.file_path = args.file

    try:
        with MouseListener(on_click=on_click) as ml:
            ml.join()
    except KeyboardInterrupt:
        print("\n Good bye!")
