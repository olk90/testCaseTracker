import pyscreenshot as pss
from PIL import ImageDraw

from pynput.mouse import Listener as MouseListener, Button


def on_click(x, y, button, pressed):
    if button == Button.left and pressed:
        im = pss.grab(backend="pil")

        draw = ImageDraw.Draw(im)
        offset = 32
        draw.rectangle((x - offset, y - offset, x + offset, y + offset), outline="red", width=5)

        im.save("screenshot.png")


if __name__ == '__main__':
    print("Press Ctrl+C to exit")
    try:
        with MouseListener(on_click=on_click) as ml:
            ml.join()
    except KeyboardInterrupt:
        print("\n Good bye!")
