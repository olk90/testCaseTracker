# Code in this file is derived from https://gist.github.com/mgalgs/8c1dd50fe3c19a1719fb2ecd012c4edd

from collections import namedtuple

import traceback
import Xlib
import Xlib.display as d
import pyscreenshot as pss

display = d.Display()
root = display.screen().root
NET_ACTIVE_WINDOW = display.intern_atom("_NET_ACTIVE_WINDOW")

Geometry = namedtuple("Geometry", "x y width height")


def get_active_window():
    window_id = root.get_full_property(NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
    try:
        return display.create_resource_object("window", window_id)
    except Xlib.error.XError:
        traceback.print_exc()


def get_geometry(window):
    geometry = window.get_geometry()
    (x, y) = geometry.x, geometry.y
    while True:
        parent = window.query_tree().parent
        pg = parent.get_geometry()
        x += pg.x
        y += pg.y
        if parent.id == root.id:
            break
        window = parent
    return Geometry(x, y, pg.width, pg.height)


def get_bbox(window):
    geometry = get_geometry(window)
    wpx = geometry.x
    wpy = geometry.y
    ww = geometry.width
    wh = geometry.height
    return wpx, wpy, ww, wh


def xlib_screenshot():
    im = pss.grab(backend="pil")
    window = get_active_window()
    wpx, wpy, ww, wh = get_bbox(window)
    return im, ww, wh
