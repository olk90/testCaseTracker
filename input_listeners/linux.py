import evdev


def get_mouse_event_device():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        capabilities = device.capabilities(verbose=True)
        if evdev.ecodes.EV_REL in capabilities and evdev.ecodes.EV_KEY in capabilities:
            # Check if the device has relative motion events and key events (mouse-like)
            if evdev.ecodes.REL_X in capabilities[evdev.ecodes.EV_REL] and \
                    evdev.ecodes.REL_Y in capabilities[evdev.ecodes.EV_REL] and \
                    evdev.ecodes.BTN_LEFT in capabilities[evdev.ecodes.EV_KEY]:
                return device
    return None


def on_click(x, y, event):
    if event.type == evdev.ecodes.EV_KEY and event.code == evdev.ecodes.BTN_MIDDLE and event.value == 1:
        print("Middle button clicked")


def attach_listener():
    mouse = get_mouse_event_device()
    if mouse:
        device = evdev.InputDevice(mouse)
    else:
        raise Exception("BOOOOOOM!")

    for event in device.read_loop():
        on_click(0, 0, event)
