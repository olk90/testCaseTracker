import os

from io import BytesIO
from docx import Document
from docx.shared import Cm

import pyscreenshot as pss
from PIL import ImageDraw

from pynput.mouse import Listener as MouseListener, Button


def on_click(x, y, button, pressed):
    if button == Button.left and pressed:
        im = pss.grab(backend="pil")

        draw = ImageDraw.Draw(im)
        offset = 32
        draw.rectangle((x - offset, y - offset, x + offset, y + offset), outline="red", width=5)

        im_bytes = BytesIO()
        im.save(im_bytes, format="png")
        im_bytes.seek(0)

        directory = os.path.expanduser("~")
        filename = "screenshots.docx"
        file_path = os.path.join(directory, filename)

        if os.path.exists(file_path):
            doc = Document(file_path)
        else:
            doc = Document()

        page_width = doc.sections[0].page_width.cm - doc.sections[0].left_margin.cm - doc.sections[0].right_margin.cm
        paragraph = doc.add_paragraph()
        run = paragraph.add_run()
        run.add_picture(im_bytes, width=Cm(page_width))

        doc.save(file_path)


if __name__ == '__main__':
    print("Press Ctrl+C to exit")
    try:
        with MouseListener(on_click=on_click) as ml:
            ml.join()
    except KeyboardInterrupt:
        print("\n Good bye!")
