# win 32 con
# set Blender Foreground
import win32api
import win32con
import win32gui


# def window_enum_handler(hwnd, resultList):
#     title = win32gui.GetWindowText(hwnd)
#     if "Blender" in title and '.blend' in title:
#         print("find Blender hwnd", hwnd, title)
#         # run in admin mode
#         # win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F5, 0)
#         # win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F5, 0)
#         win32gui.SetForegroundWindow(hwnd)


# def setBlenderForeground():
#     win32gui.EnumWindows(window_enum_handler, [])

import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")


def callBlender(hwnd):
    print('call blender', hwnd)
    win32gui.SetForegroundWindow(hwnd)
    # win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F5, 0)
    # win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F5, 0)
    shell.SendKeys("{F5}")


def find_hwnd(callback):
    win32gui.EnumWindows(callback, [])
    pass
#############
import wx

from gui import BlenFloat

from gob import gob_bpy, runZRemesher, runDynaMesh, key_func, zbCloseHole

class BlenFloatView(BlenFloat):
    def __init__(self, p):
        BlenFloat.__init__(self, p)
        self.on_find_hwnd(None)
        pass

    def init_openl_panel(self):
        self.canvas = myGLCanvas(self, size=(640, 480))
        self.panel = GLPanel(self, canvas=self.canvas)

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.sizer.Add(self.panel, 0, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)

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

    def on_focus(self, e):
        key_func['focus']()

    def on_close_hole(self, e):
        zsc_path = self.text_zsc.GetValue()
        zbCloseHole(zsc_path)
    # Rig tab

    def on_run_test_py(self, event):
        with open('test.py', 'r') as t:
            run_bpy_str(t.read())
            t.close()
            pass
        pass

    def on_hide_SHA(self, event):
        run_bpy_by_filename('bpys/rig_hide_cs.py')

    def on_rig_match_def_armature(self, event):
        run_bpy_by_filename_func_stack(
            'bpys/rig_match_def_armature.py', ['# func_1#'])
        pass

    def on_rename_fuse(self, event):
        run_bpy_by_filename('bpys/rig_rename_fuse.py')
        pass

    def on_rig_set_constraints(self, event):
        run_bpy_by_filename('bpys/rig_set_constraints.py')

    def on_rig_clear_all_constraints(self, event):
        run_bpy_by_filename('bpys/rig_clear_all_constraints.py')
    # char tab

    def on_char_open(self, event):
        with open('views/char.py', 'r') as f:
            s = f.read()
            run_py(s)
        pass
    # settig tab
    title_hwnd_map = {}
    hwnd = -1

    def on_find_hwnd(self, event):
        self.combobox_hwnd.Clear()
        self.hwnd = -1

        def set_combobox(hwnd, e):
            title = win32gui.GetWindowText(hwnd)
            if "Blender" in title and '.blend' in title:
                print("find Blender hwnd", hwnd, title)
                self.title_hwnd_map[title] = hwnd
                if self.hwnd < 0:
                    self.hwnd = hwnd
                self.combobox_hwnd.Append(title)
                self.combobox_hwnd.Selection = 0
                # hwnds.append([hwnd, title])
        find_hwnd(set_combobox)
        pass

    def on_select_hwnd(self, event):
        t = self.combobox_hwnd.GetValue()
        self.hwnd = self.title_hwnd_map[t]
        print(self.title_hwnd_map[t], t)


def run_bpy_by_filename(filename):
    with open(filename, 'r') as f:
        run_bpy_str(f.read())
        f.close()
    pass


def run_bpy_by_filename_func_stack(filename, func_stack):
    with open(filename, 'r') as f:
        s = f.read()
        for uncomment in func_stack:
            s = s.replace(uncomment, '')
            print(uncomment, s)
        run_bpy_str(s)
        f.close()
    pass


def run_bpy_str(bpystr):
    with open('c:/tmp/bpy.py', 'w') as bpy:
        bpy.write(bpystr)
        bpy.close()
        callBlender(frame.hwnd)
    pass

def run_py(pycode):
    try:
        exec(compile(pycode, '<string>', 'exec'))
    except Exception as e:
        print(e)
        return 'err'


def elevate():
    import admin
    if not admin.isUserAdmin():
        admin.runAsAdmin()

frame = None
if __name__ == '__main__':
    elevate()
    app = wx.App(False)

    frame = BlenFloatView(None)
    frame.Show(True)
    app.MainLoop()
