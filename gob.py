gob_bpy = {
    "export": """
def main():
    import bpy
    bpy.ops.scene.gob_export()
    print('gob_export')    
main()
"""
}


import win32gui
import win32api
import win32con
import os


def runDefScript():
    hwnd = win32gui.FindWindowEx(0, 0, 0, 'ZBrush')
    # win32gui.GetWindowText() == self.title
    print(hwnd)
    # 0x55
    # U key
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN,
                         win32con.VK_CONTROL, 0)  #
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, 0x55, 0)  #
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 0x55, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN,
                         win32con.VK_MULTIPLY, 0)  #
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_MULTIPLY, 0)


def writeZScript(s, zpath=None):
    if zpath:
        defzsc = os.path.join(zpath, "DefaultZScript.txt")
        print(defzsc)
        with open(defzsc, 'w') as f:
            f.write(s)
            f.close()


def scriptZRemesher(v):
    if int(v) == 0:
        s = '''
    [Loop,1,
    [IPress,Tool:Geometry:ZRemesher]
    [IPress,Tool:GoZ]
    ]
        '''.format(v)
    else:
        s = '''
    [Loop,1,
    [ISet,Tool:Geometry:Target Polygons Count,{0}]
    [IPress,Tool:Geometry:ZRemesher]
    [IPress,Tool:GoZ]
    ]
        '''.format(v)
    # print(s)
    return s


def scriptDynaMesh(v):
    s = '''
[Loop,1,
[ISet,Tool:Geometry:Resolution,{0}]
[IUnPress,Tool:Geometry:DynaMesh]
[IPress,Tool:Geometry:DynaMesh]
[IPress,Tool:GoZ]
]
'''.format(v)
    return s


def runZRemesher(zpath, v):
    s = scriptZRemesher(v)
    writeZScript(s, zpath)
    runDefScript()
    pass


def runDynaMesh(zpath, v):
    s = scriptDynaMesh(v)
    writeZScript(s, zpath)
    runDefScript()
    pass


def zbCloseHole(zpath):
    s = "[Loop,1,[IPress,Tool:Geometry:Close Holes]]"
    defzsc = os.path.join(zpath, "DefaultZScript.txt")
    f = open(defzsc, 'w')
    f.write(s)
    f.close()
    runDefScript()

def zbRun():
    hwnd = win32gui.FindWindowEx(0, 0, 0, 'ZBrush')
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN,win32con.VK_MULTIPLY, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_MULTIPLY, 0)

def main():
    s = runZRemesher(2)
    writeZScript(s)
    runDefScript()

if __name__ == '__main__':
    main()
# send key only


def zbUndo():
    hwnd = win32gui.FindWindowEx(0, 0, 0, 'ZBrush')
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN,	90, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 90, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)


def zbRedo():
    hwnd = win32gui.FindWindowEx(0, 0, 0, 'ZBrush')
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)  #
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_SHIFT, 0)  #
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN,	90, 0)  #
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 	90, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_SHIFT, 0)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)


def zbFocus():
    hwnd = win32gui.FindWindowEx(0, 0, 0, 'ZBrush')
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN,		70, 0)  #
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, 		70, 0)
key_func = {
    "focus": zbFocus,
    "undo": zbUndo,
    "redo": zbRedo
}