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
    filename = os.path.join(dirname, 'views', 'char_bg.png')
    config = pyglet.gl.Config(sample_buffers=1, samples=4)
    window = pyglet.window.Window(
        config=config,
        resizable=False,
        style='borderless'	, width=480, height=640)
    image = pyglet.image.load(filename)

    class Data():
        lmx = -1
        lmy = -1

    self = Data()

    @window.event
    def on_key_release(symbol, modifiers):
        print(symbol)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        print(x, y, button)
        self.lmx, self.lmy = win32api.GetCursorPos()

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if self.lmx > -1:
            mx, my = win32api.GetCursorPos()
            dx = mx - self.lmx
            self.lmx = mx
            dy = my - self.lmy
            self.lmy = my
            # print(dx, dy)
            cur = window.get_location()
            window.set_location(cur[0]+dx, cur[1]+dy)
        pass

    @window.event
    def on_draw():
        window.clear()
        image.blit(0, 0)
    pyglet.app.run()
    pass

if __name__ == '__main__':
    main()
