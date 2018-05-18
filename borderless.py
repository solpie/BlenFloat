"""Make the Emacs window full-screen on Windows
At present, this will only adjust the first Emacs frame found. It could be modified to use
win32api.EnumWindows and win32api.GetClassName / win32api.GetWindowText in order to adjust all
Emacs frames.
"""

import sys
import win32gui
import win32con


def set_borderless(hwnd, off=False):
    """Turn off / on titlebar and border"""

    borderless_style = (win32con.WS_BORDER | win32con.WS_THICKFRAME
                        | win32con.WS_CAPTION | win32con.WS_MAXIMIZE)
    current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    if off:
        style = current_style | borderless_style
    else:
        style = current_style & ~borderless_style

    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
    win32gui.SetWindowPos(hwnd, 0, 0,0,0,0, win32con.SWP_FRAMECHANGED | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_NOOWNERZORDER);
    

def find_title(hwnd, e):
    title = win32gui.GetWindowText(hwnd)
    if 'Marie' in title:
        print('find',title)
        set_borderless(hwnd, False)
        pass


def main():
    win32gui.EnumWindows(find_title, [])


if __name__ == "__main__":
    sys.exit(main())
