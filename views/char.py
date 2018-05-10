import pyglet
import sys
import os
import os
dirname = os.path.dirname(__file__)


def main():
    import pyglet
    import sys
    import os
    import win32api
    dirname = os.path.dirname(__file__)
    pyglet.resource.path = ['./res']
    pyglet.resource.reindex()

    class Button():
        sp_up = None
        sp_down = None
        width = 0
        height = 0
        x = 0
        y = 0

        def __init__(self, up, down, on_up=None):
            self.sp_up = up
            self.sp_down = down
            self.width = up.width
            self.height = up.height
            self.up()

        def set_pos(self, x, y):
            set_pos(self.sp_up, x, y)
            set_pos(self.sp_down, x, y)
            self.x = x
            self.y = y

        def is_in(self, x, y):
            # print(x,y,self.x,self.y)
            if x > self.x and x < (self.x + self.width):
                if y > self.y and y < (self.y + self.height):
                    return True

        def up(self):
            self.sp_down.visible = False
            self.sp_up.visible = True
            pass

        def down(self):
            self.sp_down.visible = True
            self.sp_up.visible = False
            pass

    class Marionette():
        lmx = -1
        lmy = -1
        main_batch = pyglet.graphics.Batch()
        window = None

        def __init__(self):
            pass

        def new_window(self):
            config = pyglet.gl.Config(sample_buffers=1, samples=4)
            window = pyglet.window.Window(
                config=config,
                resizable=False,
                style='borderless', width=480, height=640)
            self.window = window
            return window

        def new_sprite(self, filename, batch=None):
            img = pyglet.resource.image(filename)
            b = self.main_batch
            if batch:
                b = batch
            sp = pyglet.sprite.Sprite(img=img, batch=b)
            return sp
        buttons = []

        def add_button(self, button, callback):
            self.buttons.append([button, callback])
            pass

        def button_down(self, x, y):
            for a in self.buttons:
                if a[0].is_in(x, y):
                    a[0].down()

        def button_up(self, x, y):
            for a in self.buttons:
                if a[0].is_in(x, y):
                    a[0].up()
                    a[1]()

    def set_pos(sp, x=None, y=None):
        if x:
            sp.x = x
        if y:
            sp.y = win.height - y - sp.height


    m = Marionette()
    win = m.new_window()

    bg = m.new_sprite('char_bg.png')
    set_pos(bg, 0, 0)

    sp = m.new_sprite('sp1_up.png')
    sp1_down = m.new_sprite('sp1_down.png')
    btn = Button(sp, sp1_down)
    btn.set_pos(250, 200)

    def on_btn():
        print('on button')
    m.add_button(btn, on_btn)

    @win.event
    def on_key_release(symbol, modifiers):
        print(symbol)

    @win.event
    def on_mouse_release(x, y, button, modifiers):
        m.button_up(x, win.height - y)

    @win.event
    def on_mouse_press(x, y, button, modifiers):
        # print(x, y, button)
        m.lmx, m.lmy = win32api.GetCursorPos()
        m.button_down(x, win.height - y)

    @win.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if m.lmx > -1:
            mx, my = win32api.GetCursorPos()
            dx = mx - m.lmx
            m.lmx = mx
            dy = my - m.lmy
            m.lmy = my
            # print(dx, dy)
            cur = win.get_location()
            win.set_location(cur[0] + dx, cur[1] + dy)
        pass

    @win.event
    def on_draw():
        win.clear()
        m.main_batch.draw()

        # batch = pyglet.graphics.Batch()
        # vertex_list = batch.add(2, pyglet.gl.GL_LINES, None,
        #                         ('v2i', (10, 15, 30, 35)),
        #                         ('c3B', (0, 0, 255, 0, 255, 0))
        #                         )
    pyglet.app.run()
    pass

if __name__ == '__main__':
    main()
