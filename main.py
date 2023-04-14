import pyscreenshot as pss

from pynput.mouse import Listener


def on_click(x, y, button, pressed):
    # capture the entire screen
    im = pss.grab()

    # save the image to a file
    im.save('screenshot.png')


if __name__ == '__main__':
    print("Press Ctrl+C to exit")
    try:
        with Listener(on_click=on_click) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\n Good bye!")
