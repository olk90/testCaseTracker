import pywayland.client as wl
import pywayland.protocol as wp
from PIL import ImageGrab


def get_geometry():
    display = wl.Display()
    registry = wp.Registry(display)
    registry.add_listener(wp.RegistryHandler())
    display.roundtrip()

    manager = registry.bind(wp.WLR_FOREIGN_TOPLEVEL_MANAGEMENT_MANAGER_UNSTABLE_V1, 1)
    manager.add_listener(wp.WlrForeignToplevelManagerUnstableV1Handler())

    active_window = manager.get_active_window()
    if active_window:
        geometry = active_window.get_geometry()
        return geometry


def pil_screenshot():
    geometry = get_geometry()
    box = (1, 1, 1, 1)
    screenshot = ImageGrab.grab(box)
    return screenshot
