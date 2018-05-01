# -*- coding: utf-8 -*-
__author__ = 'SolPie'
import bpy

bl_info = {
    "name": "BlenFloat",
    "author": "SolPie",
    "version": (1, 0),
    "blender": (2, 7, 9),
    "location": "c:/tmp",
    "description": "Blender Float call from external app",
    "warning": "",
    "category": "Misc"}

from bpy.props import StringProperty, IntProperty, BoolProperty

# Addon prefs


class BlenFloatPrefs(bpy.types.AddonPreferences):
    bl_idname = __name__
    bpypath = StringProperty \
        (
            name="bpy path",
            default='c:/tmp/',

            subtype='DIR_PATH',
        )

    def draw(self, context):
        layout = self.layout
        layout.label(text="set tmp dir")
        layout.prop(self, "bpypath")
    # self.checkEnable(context)
####################################


class BlenCall(bpy.types.Operator):
    bl_idname = "blenfloat.call"
    bl_label = "run.BlenCall"

    def execute(self, context):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences
        bpypath = addon_prefs.bpypath
        try:
            with open(bpypath + 'bpy.py', 'r+') as f:
                bpy_text = f.read()
                # print(bpy_text)
                if len(bpy_text):
                    print('BlenCall')
                    exec(compile(bpy_text, '<string>', 'exec'))
                    f.seek(0)
                    f.write('')
                    f.truncate()
                else:
                    print('no bpy')
                f.close()
                pass
        except Exception as e:
            print('stop BlenCall', e)
        return {'PASS_THROUGH'}
# store keymaps here to access after registration
addon_keymaps = []

###########


def register():
    bpy.utils.register_class(BlenFloatPrefs)
    bpy.utils.register_class(BlenCall)
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="Window", space_type="EMPTY")
    kmi = km.keymap_items.new(BlenCall.bl_idname, 'F5', 'PRESS')
    # kmi.properties.name = "BlenFloat_call"
    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(BlenFloatPrefs)
    bpy.utils.unregister_class(BlenCall)
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
