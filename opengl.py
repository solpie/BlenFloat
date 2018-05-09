from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from wx.glcanvas import GLCanvas
import wx


class myGLCanvas(GLCanvas):
    # Actual draw

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, -5.0, -250.0)
        glTranslate(0.0, 0.0, -self.distance)
        glRotate(self.alpha, 0.0, 0.0, 1.0)
        glRotate(self.beta, 0.0, 1.0, 0.0)
        for b in self.dataBuffers:
            b.bindAll()
            glDrawElements(self.glDisplayType, b.size, GL_UNSIGNED_INT, 0)
            b.unbind()
        self.SwapBuffers()


class GLPanel(wx.Panel):

    def __init__(self, parent, canvas, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.canvas = canvas

        self.button1 = wx.Button(self, label="POINTS")
        self.button2 = wx.Button(self, label="TRIANGLES")

        self.Bind(wx.EVT_BUTTON, self.setPoints, self.button1)
        self.Bind(wx.EVT_BUTTON, self.setTriangles, self.button2)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.button1, flag=wx.BOTTOM, border=5)
        self.sizer.Add(self.button2, flag=wx.BOTTOM, border=5)

        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, flag=wx.ALL | wx.EXPAND, border=5)

        self.SetSizerAndFit(self.border)

    def setPoints(self, evt):
        self.canvas.setDisplayType(GL_POINTS)
        
        #----------------------------------------------------------------------

    def setTriangles(self, evt):
        self.canvas.setDisplayType(GL_TRIANGLES)


class MainWin(wx.Frame):

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, title='OpenGL', *args, **kwargs)

        self.canvas = myGLCanvas(self, size=(640, 480))
        self.panel = GLPanel(self, canvas=self.canvas)

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.sizer.Add(self.panel, 0, wx.EXPAND)
        self.SetSizerAndFit(self.sizer)

        self.Show()
app = wx.App(0)
wx.InitAllImageHandlers()
main_win = MainWin(None)
main_win.Show()
app.MainLoop()
