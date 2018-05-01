# win 32 con
# set Blender Foreground
import win32api
import win32con
import win32gui


def window_enum_handler(hwnd, resultList):
    title = win32gui.GetWindowText(hwnd)
    if "Blender" in title and '.blend' in title:
        print("find Blender hwnd", hwnd, title)
        # run in admin mode
        # win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F5, 0)
        # win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F5, 0)
        win32gui.SetForegroundWindow(hwnd)


def setBlenderForeground():
    win32gui.EnumWindows(window_enum_handler, [])

import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")


def callBlender():
    setBlenderForeground()
    shell.SendKeys("{F5}")
#############
import wx

from gui import BlenFloat

from gob import gob_bpy, runZRemesher, runDynaMesh, key_func, zbCloseHole


class BlenFloatView(BlenFloat):

    def __init__(self, p):
        BlenFloat.__init__(self, p)
        pass

    def on_export(self, event):
        print(gob_bpy["export"])
        run_bpy_str(gob_bpy["export"])

    def on_remesh(self, event):
        zsc_path = self.text_zsc.GetValue()
        value = self.text_remesh.GetValue()
        runZRemesher(zsc_path, value)

    def on_dynamesh(self, e):
        zsc_path = self.text_zsc.GetValue()
        v = self.text_dynamesh.GetValue()
        runDynaMesh(zsc_path, v)

    def on_undo(self, e):
        key_func['undo']()

    def on_redo(self, e):
        key_func['redo']()
    
    def on_focus(self,e):
        key_func['focus']()

    def on_close_hole(self, e):
        zsc_path = self.text_zsc.GetValue()
        zbCloseHole(zsc_path)

    def on_run_test_py(self, event):
        with open('test.py', 'r') as t:
            run_bpy_str(t.read())
            t.close()
            pass


def run_bpy_str(bpystr):
    with open('c:/tmp/bpy.py', 'w') as bpy:
        bpy.write(bpystr)
        bpy.close()
        callBlender()
        pass

    def run_py(self, pycode):
        try:
            exec(compile(pycode, '<string>', 'exec'))
        except Exception as e:
            print(e)
            return 'err'

if __name__ == '__main__':
    app = wx.App(False)

    frame = BlenFloatView(None)
    frame.Show(True)
    app.MainLoop()
