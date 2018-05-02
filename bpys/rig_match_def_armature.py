def main():
    import bpy
    D = bpy.data
    C = bpy.context
    brg5_obj = None
    rig_obj = None
    logs = []

    def snap2(pbone, target_bone, fuse_obj):
        mat = fuse_obj.matrix_world * target_bone.matrix
        print('cl', mat.translation)
        bpy.context.scene.cursor_location = mat.translation
        pbone.matrix.translation = mat.translation

    def init_select_obj():
        # select target obj first then blenRig5,and toggle in pose mode
        if len(C.selected_objects) == 2:
            for obj in C.selected_objects:
                if obj.name == C.active_object.name:
                    brg5_obj = obj
                else:
                    rig_obj = obj
        else:
            print('selected two armatures')
        logs.append('init :' + brg5_obj.name + ' ' + rig_obj.name)
        print('init select obj', brg5_obj.name, rig_obj.name)

    def brg5_match_fuse_rig():
        prefix = 'mixamorig:'
        match_map = {"elbow_str_L": "LeftForeArm"}
        brg5_obj = bpy.data.objects["biped_blenrig"]

        # collect bone data
        fuse_bone_map = {}
        fuse_bones_name = []
        for k in match_map:
            fuse_bones_name.append(prefix + match_map[k])
        fuse_obj = bpy.data.objects['fuse']
        fuse_rig = fuse_obj.data
        bpy.ops.object.mode_set(mode='EDIT')
        fuse_matw = fuse_obj.matrix_world
        for bone in fuse_rig.edit_bones:
            if bone.name in fuse_bones_name:
                fuse_bone_map[bone.name] = bone
                print(bone.name, bone.head, 'cl', bone.head * fuse_matw)
        bpy.ops.object.mode_set(mode='OBJECT')
        # snap
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = brg5_obj
        brg5_obj.select = True
        # bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='POSE')

        for bone_name in match_map:
            target_name = prefix + match_map[bone_name]
            target_bone = fuse_bone_map[target_name]
            if brg5_obj.pose.bones[bone_name]:
                pbone = brg5_obj.pose.bones[bone_name]
                snap2(pbone, target_bone, fuse_obj)
        pass
    init_select_obj()

    def label(self, context):
        t = '\n'.join(logs)
        self.layout.label(t)
    C.window_manager.popup_menu(label, title="info", icon='INFO')
    pass
main()
