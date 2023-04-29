import pyautogui


def pyautogui_screenshot():
    window = pyautogui.getActiveWindow()
    wpx = window.topleft.x
    wpy = window.topleft.y
    ww = window.width
    wh = window.height
    return pyautogui.screenshot(region=(wpx, wpy, ww, wh)), window.left, window.top
