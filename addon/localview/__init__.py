# -*- coding: utf-8 -*-
import bpy

bl_info = {
    "name": "local view",
    "author": "SolPie",
    "version": (0, 1),
    "blender": (2, 80, 5),
    "location": "View3D > View",
    "description": "",
    "warning": "",
    "category": "3D View"}

import localview
localview.restore_obj = {}
localview.localview_obj = {}


class LocalViewRestore(bpy.types.Operator):
    bl_idname = 'localview.restore'
    bl_label = 'localview restore'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # for new obj
        bpy.ops.object.select_all(action='SELECT')
        for obj in bpy.context.selected_objects:
            localview.localview_obj[obj.name] = True

        bpy.ops.object.hide_view_clear()
        for obj in bpy.data.objects:
            if obj.name in localview.restore_obj or obj.name in localview.localview_obj:
                obj.select_set(action='SELECT')
            else:
                obj.select_set(action='DESELECT')
        bpy.ops.object.hide_view_set(unselected=True)

        for obj in bpy.data.objects:
            if obj.name in localview.localview_obj:
                obj.select_set(action='SELECT')
            else:
                obj.select_set(action='DESELECT')
        bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}


class LocalViewEnable(bpy.types.Operator):
    bl_idname = 'localview.enable'
    bl_label = 'localview'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        restore_obj = {}
        localview_obj = {}
        for obj in bpy.context.selected_objects:
            # restore_obj[obj.name] = True
            localview_obj[obj.name] = True

        bpy.ops.object.select_all(action='INVERT')

        for obj in bpy.context.selected_objects:
            restore_obj[obj.name] = True
            print('restore', obj.name)

        localview.restore_obj = restore_obj
        localview.localview_obj = localview_obj
        bpy.ops.object.hide_view_set(unselected=False)

        print('restore_obj', restore_obj)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(LocalViewEnable.bl_idname, text="local view")
    self.layout.operator(LocalViewRestore.bl_idname, text="local view restore")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_view.append(menu_func)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.VIEW3D_MT_view.remove(menu_func)
