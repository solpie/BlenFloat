def main():
    import pyglet
    import sys
    import os
    import win32api
    import win32con
    import win32gui
    dirname = os.path.dirname(__file__)
    pyglet.resource.path = ['./res']
    pyglet.resource.reindex()
    print('load res', __file__)

    from views.ui.control import Control, Sprite, EventDispatcher, MouseEvent, view as v
    add_ctrl = v.add_ctrl

    class Marionette(pyglet.window.Window):
        lmx = -1
        lmy = -1
        main_batch = pyglet.graphics.Batch()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            mx, my = win32api.GetCursorPos()
            self.set_location(mx - 420, my - 10)
            self.bg_batch = pyglet.graphics.Batch()
            self.init_ui()

        def init_ui(self):
            self.label.opacity = 128
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
            # win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32con.WS_POPUP)
            print('p1o13p')
            # win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, (win32gui.GetWindowLong(
            #     hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED) & (~(win32con.WS_CAPTION
            #                                                                | win32con.WS_THICKFRAME
            #                                                                | win32con.WS_MINIMIZEBOX
            #                                                                | win32con.WS_MAXIMIZEBOX
            #                                                                | win32con.WS_SYSMENU
            #                                                                | win32con.WS_BORDER
            #                                                                | win32con.WS_DLGFRAME
            #                                                                )))
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            # win32con.WS_BORDER)
            win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(
                95, 95, 95), int(alpha * 255), win32con.LWA_ALPHA)
            # SetWindowPos(hwnd, NULL, 0,0,0,0, SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOOWNERZORDER);
            # SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_NOOWNERZORDER
            # win32gui.SetWindowPos(hwnd, 0, 0, 0, 480, 640, win32con.SWP_NOMOVE |
            #                       win32con.SWP_NOSIZE | win32con.SWP_NOOWNERZORDER |
            # win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
            pass

        def new_sprite(self, filename, batch=None):
            img = pyglet.resource.image(filename)
            b = self.main_batch
            if batch:
                b = batch
            sp = pyglet.sprite.Sprite(img=img, batch=b)
            return sp

        label = pyglet.text.Label('0,0',
                                  font_name='Inconsolata',
                                  font_size=15,
                                  x=0, y=320,
                                  anchor_x='center', anchor_y='center')

        is_over_bone = False

        def show_bone_name(self, name):
            self.is_over_bone = True
            self.label.text = name
            self.label.opacity = 128
            pass
        # base event

        def on_draw(self):
            self.clear()
            self.bg_batch.draw()
            self.main_batch.draw()
            self.label.draw()

        def on_key_release(self, symbol, modifiers):
            print(symbol)

        def on_mouse_release(self, x, y, button, modifiers):
            v.mouse_release(x, y)

        def on_mouse_press(self, x, y, button, modifiers):
            self.lmx, self.lmy = win32api.GetCursorPos()
            v.mouse_press(x, y)

        def on_mouse_motion(self, x, y, dx, dy):
            self.is_over_bone = False
            v.mouse_move(x, y)
            if self.is_over_bone:
                pass
            else:
                # self.label.text = str(x) + "," + str(y)
                self.label.text = ""
                pass
            self.label.x = x
            self.label.y = y + 30
            pass

        def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
            if self.lmx > -1:
                mx, my = win32api.GetCursorPos()
                dx = mx - self.lmx
                self.lmx = mx
                dy = my - self.lmy
                self.lmy = my
                # print(dx, dy)
                cur = self.get_location()
                self.set_location(cur[0] + dx, cur[1] + dy)

    def set_pos(sp, x=None, y=None):
        if x:
            sp.x = x
        if y:
            sp.y = win.height - y - sp.height

    run_bpy_str = globals()['run_bpy_str']

    config = pyglet.gl.Config(sample_buffers=1, samples=4)
    m = Marionette(config=config,
                   resizable=False,
                   style='borderless',
                   width=480, height=640)
    win = m
    # init control
    bg = Sprite('char_bg.png', m.bg_batch)

    # set tool bar
    button_pin = Sprite('pin_up.png', m.main_batch).set_pos(10, 580)
    add_ctrl(button_pin, MouseEvent.DOWN, m.toggle_topmost)
    m.toggle_topmost()

    def exit1(self, **e):
        m.close()
        pass

    def reload1(t=None):
        globals()['frame'].on_char_open()
        pyglet.clock.schedule_once(exit1, 0.5)
        pass

    b = Sprite('reload_up.png', m.main_batch).set_pos(420, 580)
    add_ctrl(b, MouseEvent.DOWN, reload1)

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

    def over_bone(b):
        # print(b.name)
        m.show_bone_name(b.name)
        pass

    def _bone(finger_name, x, y, filename='finger1.png'):
        f = Sprite(filename, m.main_batch)
        f.center_anchor().set_pos(x, y)
        f.name = finger_name
        add_ctrl(f, MouseEvent.UP, on_finger)
        add_ctrl(f, MouseEvent.OVER, over_bone)
        f.check_map()
        return f

    _bone('master_torso', w_mid, 290, 'master.png')
    _bone('head_fk', w_mid, 410, 'head.png')
    _bone('neck_fk_ctrl', w_mid, 354, 'neck.png')
    _bone('breath', w_mid, 333, 'breath.png')
    _bone('torso_ik_ctrl', w_mid, 313, 'torso.png')
    _bone('pelvis_ctrl', w_mid, 270, 'pelvis.png')
    _bone('master', w_mid, 60, 'master.png')

    _bone('shoulder_R', w_mid - 30, 348, 'shld_R.png')
    _bone('shoulder_L', w_mid + 30, 348, 'shld_L.png')

    _bone('hand_ik_ctrl_R', w_mid - 100, 358, 'hand2.png')
    _bone('hand_ik_ctrl_L', w_mid + 100, 358, 'hand2.png')
    _bone('elbow_pole_R', w_mid - 60, 310)
    _bone('elbow_pole_L', w_mid + 60, 310)

    _bone('knee_pole_R', w_mid - 30, 180)
    _bone('knee_pole_L', w_mid + 30, 180)

    _bone('foot_roll_ctrl_R', w_mid - 30, 110)
    _bone('foot_roll_ctrl_L', w_mid + 30, 110)

    _bone('sole_ctrl_R', w_mid - 100, 90, 'hand2.png')
    _bone('sole_ctrl_L', w_mid + 100, 90, 'hand2.png')

    _bone('hand_close_R', w_mid - 100, 220, 'close.png')
    _bone('hand_close_L', w_mid + 100, 220, 'close.png')

    _bone('fing_thumb_ctrl_R', w_mid - 143, 260)
    _bone('fing_thumb_ctrl_L', w_mid + 143, 260)

    _bone('fing_ind_ctrl_R', w_mid - 190, 240)
    _bone('fing_ind_ctrl_L', w_mid + 190, 240)

    _bone('fing_mid_ctrl_R', w_mid - 210, 207)
    _bone('fing_mid_ctrl_L', w_mid + 210, 207)

    _bone('fing_ring_ctrl_R', w_mid - 200, 170)
    _bone('fing_ring_ctrl_L', w_mid + 200, 170)

    _bone('fing_lit_ctrl_R', w_mid - 155, 160)
    _bone('fing_lit_ctrl_L', w_mid + 155, 160)

    ###########

    ##### base event##########

    pyglet.app.run()
    pass

if __name__ == '__main__':
    # print(globals())
    main()
