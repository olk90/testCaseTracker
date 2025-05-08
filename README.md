# testCaseTracker

I have moved this repository to https://codeberg.org/olk90/testCaseTracker where I will continue development.

testCaseTracker is a Python script that enables you to capture screenshots and saves them into a Word document. You can
mark the exact location where you clicked with various symbols such as arrow, rectangle, circle or bullet. The script
supports both Windows and Linux operating systems.

## Requirements

* Python 3.10 or above **(might also run on older versions, but this has not been tested!)**
* On Windows, pyautogui is used to take screenshots
* On Linux, xlib is used to take screenshots
    * implementation for Wayland might be added in the future

## Usage

1. Open the command prompt or terminal.
2. Navigate to the directory containing the `main.py` file.
3. Type the following command: python `main.py -f <file_path> -m <marker>`
4. Replace `<file_path>` with the path and name of the Word document you want to create. If the file does not exist, it
   will be created automatically.
5. Optionally, replace `<marker>` with one of the following options: `none`, `arrow`, `rect`, `circle`, `bullet`. This
   option will determine which symbol is used to mark the clicked location.

### Example usage

```
python main.py -f "C:\Users\john\Desktop\screenshots.docx" -m arrow
```

## Instructions:

1. Run the script using the instructions provided above.
2. Click the middle mouse button to take a screenshot. The clicked location will be marked with the chosen symbol.
3. A Word document will be created (if necessary) or updated with the new screenshot.
4. Continue taking screenshots as desired by clicking the middle mouse button.
5. To exit the program, press Ctrl+C or close the terminal.

**Note:** The script only supports middle mouse button clicks. Other mouse buttons and key combinations are not
recognized.

## Troubleshooting

* If you receive an error message related to the display server, make sure you are running the script on a Linux machine
  with an X11 display server or a Windows machine.
* If you receive an error message related to missing packages, make sure you have installed the required Python
  packages.
* If you encounter any other issues, try restarting the script or the terminal.

## Known issues

* It is not yet possible to take the screenshots on any other display than the main display!
* Right now screenshots in an X11 environment are not cropped properly. A fix is in the works.

## Legal Notice

This program uses the following third-party libraries, each with its own license:

- [pyscreenshot](https://github.com/ponty/pyscreenshot/blob/master/LICENSE.txt) (BSD 2-Clause "Simplified" License)

- [pillow](https://github.com/python-pillow/Pillow/blob/main/LICENSE) (PIL Software License)

- [python-docx](https://github.com/python-openxml/python-docx/blob/master/LICENSE) (MIT License)

- [pyautogui](https://github.com/asweigart/pyautogui/blob/master/LICENSE.txt) (BSD-3-Clause License)

- [pynput](https://github.com/moses-palmer/pynput/blob/master/COPYING.LGPL) (LGPL-3.0 License)

- [python-xlib](https://github.com/python-xlib/python-xlib/blob/master/LICENSE) (LGPL-2.1 License)

This program is licensed under the terms of the GNU General Public License version 3 (GPLv3).
Please refer to the LICENSE file for more information.

