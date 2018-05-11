import pyglet
__ = {}

from enum import Enum


class MouseEvent(Enum):
    DOWN = 'down'
    UP = 'up'


class EventDispatcher():
    __func_map = None

    def on(self, event, callback):
        if not self.__func_map:
            self.__func_map = {}

        if event not in self.__func_map:
            self.__func_map[event] = {}
        self.__func_map[event][callback] = True

    def emit(self, event, *param):
        if event in self.__func_map:
            for func_id in self.__func_map[event]:
                if len(param):
                    func_id(*param)
                else:
                    func_id()

    def check_map(self):
        # print(self.__func_map)
        for e in self.__func_map:
            print(e, len(self.__func_map))
        pass


class Control(EventDispatcher):
    width = 0
    height = 0
    x = 0
    y = 0

    def __init__(self, width, height, x=0, y=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def is_in(self, x, y, anchor_x=0, anchor_y=0):
        if x > (self.x - anchor_x) and x < (self.x - anchor_x + self.width):
            if y > (self.y - anchor_y) and y < (self.y - anchor_y + self.height):
                return True
        return False


def __set_pos(sp, x=None, y=None):
    if x:
        sp.x = x
    if y:
        sp.y = y
__['set_pos'] = __set_pos


class Sprite(Control):
    __sp = None
    anchor_x = 0
    anchor_y = 0
    name = ''

    def __init__(self, filename, batch):
        img = pyglet.resource.image(filename)
        self.__sp = pyglet.sprite.Sprite(img=img, batch=batch)
        super().__init__(img.width, img.height)
        # print('img width', self.width, self.height)

    def center_anchor(self):
        self.anchor_x = int(self.width / 2)
        self.anchor_y = int(self.height / 2)
        return self

    def over(self, **e):
        self.__sp.color = (255, 255, 0)

    def is_in(self, x, y):
        v = super().is_in(x, y, self.anchor_x, self.anchor_y)
        if v:
            self.down()
        else:
            self.up()

        return v

    def down(self, **e):
        # self.set_alpha(0.5)
        # print('down', self.name)
        pass

    def set_alpha(self, a):
        self.__sp.opacity = int(255 * a)

    def set_pos(self, x, y):
        super().set_pos(x, y)
        __['set_pos'](self.__sp, x - self.anchor_x, y - self.anchor_y)
        return self

    def up(self, **e):
        # self.set_alpha(1)
        pass


class View(object):
    ctrls = []

    def add_ctrl(self, ctrl, event, callback):
        self.ctrls.append(ctrl)
        ctrl.on(event, callback)

    def mouse_press(self, x, y):
        print('mouse_press')
        for a in self.ctrls:
            if a.is_in(x, y):
                print(a.name)
                a.emit(MouseEvent.DOWN, a)
                # break

    def mouse_release(self, x, y):
        print('mouse_release')
        for a in self.ctrls:
            if a.is_in(x, y):
                a.emit(MouseEvent.UP, a)
                # break
view = View()
