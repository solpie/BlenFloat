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

        def __init__(self, up, down):
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

    # class Bone(Button):
    #     name = ''

    #     def __init__(self, m, name, sp_name):
    #         self.name = name
    #         up = m.new_sprite(sp_name + '_up.png')
    #         down = m.new_sprite(sp_name + '_down.png')
    #         super().__init__(up, down)
    #         m.add_button(self, self.on_select)

    #     def on_select(self, e):
    #         with open('views/select_bone.py') as f:
    #             s = f.read()
    #             s = s.replace('# bone_name#', self.name)
    #             run_bpy_str(s)

    import win32gui
    import win32con

    from views.ui.control import Control, Sprite, EventDispatcher, MouseEvent, view as v
    add_ctrl = v.add_ctrl

    class Marionette():
        lmx = -1
        lmy = -1
        main_batch = pyglet.graphics.Batch()
        window = None

        def __init__(self):
            pass
        # window
        is_topmost = False

        def toggle_topmost(self, *e):
            hwnd = win32gui.GetForegroundWindow()
            act = win32con.HWND_TOPMOST
            if self.is_topmost:
                act = win32con.HWND_NOTOPMOST
                self.set_transparent(hwnd, 1)
            else:
                act = win32con.HWND_TOPMOST
                self.set_transparent(hwnd, 0.85)
            win32gui.SetWindowPos(hwnd, act, 0, 0, 0, 0,
                                  win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
            self.is_topmost = not self.is_topmost
            pass

        def set_transparent(self, hwnd, alpha):
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(
                95, 95, 95), int(alpha * 255), win32con.LWA_ALPHA)
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

    def set_pos(sp, x=None, y=None):
        if x:
            sp.x = x
        if y:
            sp.y = win.height - y - sp.height

    run_bpy_str = globals()['run_bpy_str']
    m = Marionette()
    win = m.new_window()
    # init control

    ##
    mx, my = win32api.GetCursorPos()
    win.set_location(mx - 420, my - 10)

    bg = Sprite('char_bg.png', m.main_batch)
    # set tool bar
    button_pin = Sprite('pin_up.png', m.main_batch).set_pos(10, 580)
    add_ctrl(button_pin, MouseEvent.DOWN, m.toggle_topmost)
    m.toggle_topmost()

    def exit(self, **e):
        win.close()
        pass

    def reload(t=None):
        pyglet.clock.schedule_once(exit, 0.3)
        globals()['frame'].on_char_open()
        pass
    b = Sprite('reload_up.png', m.main_batch).set_pos(420, 580)
    add_ctrl(b, MouseEvent.DOWN, reload)

    # set up bone position
    w_mid = win.width / 2
    # init finger
    def on_finger(*e):
        print('on_finger', e[0].name)
        if not e[0].name:
            return
        with open('views/select_bone.py') as f:
            s = f.read()
            s = s.replace('# bone_name#', e[0].name)
            run_bpy_str(s)

    def new_finger(finger_name, x, y, filename='finger1.png'):
        f = Sprite(filename, m.main_batch)
        f.center_anchor().set_pos(x, y)
        f.name = finger_name
        add_ctrl(f, MouseEvent.UP, on_finger)
        f.check_map()
        return f
    # f1 = Sprite('finger1.png', m.main_batch).set_pos(50, 30)

    new_finger('master_torso', w_mid, 260, 'master.png')
    new_finger('master', w_mid, 60, 'master.png')

    new_finger('hand_ik_ctrl_R', w_mid - 100, 370, 'hand.png')
    new_finger('hand_ik_ctrl_L', w_mid + 100, 370, 'hand.png')
    new_finger('elbow_pole_R', w_mid - 60, 310)
    new_finger('elbow_pole_L', w_mid + 60, 310)

    new_finger('sole_ctrl_R', w_mid - 100, 90, 'hand.png')
    new_finger('sole_ctrl_L', w_mid + 100, 90, 'hand.png')

    new_finger('fing_thumb_ctrl_R', w_mid - 143, 260)
    new_finger('fing_thumb_ctrl_L', w_mid + 143, 260)

    new_finger('fing_ind_ctrl_R', w_mid - 190, 240)
    new_finger('fing_ind_ctrl_L', w_mid + 190, 240)

    new_finger('fing_mid_ctrl_R', w_mid - 210, 207)
    new_finger('fing_mid_ctrl_L', w_mid + 210, 207)

    new_finger('fing_ring_ctrl_R', w_mid - 200, 170)
    new_finger('fing_ring_ctrl_L', w_mid + 200, 170)

    new_finger('fing_lit_ctrl_R', w_mid - 155, 160)
    new_finger('fing_lit_ctrl_L', w_mid + 155, 160)

    ###########
    # Bone(m, 'neck_fk_ctrl', 'sp1').set_pos(250, 200)

    label = pyglet.text.Label('0,0',
                              font_name='Inconsolata',
                              font_size=20,
                              x=0, y=win.height / 2,
                              anchor_x='center', anchor_y='center')
    ##### base event##########

    @win.event
    def on_key_release(symbol, modifiers):
        print(symbol)

    @win.event
    def on_mouse_release(x, y, button, modifiers):
        # m.button_up(x, y)
        v.mouse_release(x, y)

    @win.event
    def on_mouse_press(x, y, button, modifiers):
        # print(x, y, button)
        m.lmx, m.lmy = win32api.GetCursorPos()
        # m.button_down(x, win.height - y)
        v.mouse_press(x, y)

    @win.event
    def on_mouse_motion(x, y, dx, dy):
        label.text = str(x) + "," + str(y)
        label.x = x
        label.y = y
        pass

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
        label.draw()
        # batch = pyglet.graphics.Batch()
        # vertex_list = batch.add(2, pyglet.gl.GL_LINES, None,
        #                         ('v2i', (10, 15, 30, 35)),
        #                         ('c3B', (0, 0, 255, 0, 255, 0))
        #                         )
    pyglet.app.run()
    pass

if __name__ == '__main__':
    # print(globals())
    main()
