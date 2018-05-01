gob_bpy = {
    "export":"""
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

def runZRemesher(zpath,v):
    s = scriptZRemesher(v)
    writeZScript(s,zpath)
    runDefScript()
    pass

def runDynaMesh(zpath,v):
    s = scriptDynaMesh(v)
    writeZScript(s,zpath)
    runDefScript()
    pass
    
def main():
    s = runZRemesher(2)
    writeZScript(s)
    runDefScript()

if __name__ == '__main__':
    main()