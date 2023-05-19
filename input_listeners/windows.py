from pynput.mouse import Button, Listener as MouseListener

from draw.draw_functions import draw_marker
from main import get_image, write_to_file
from properties import properties


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


def attach_listener():
    with MouseListener(on_click=on_click) as ml:
        ml.join()
