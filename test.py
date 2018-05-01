def main():
    import bpy

    import mathutils

    def extract_bones():
        act_rig_obj = bpy.context.active_object
        act_rig = act_rig_obj.data
        def_bones = [
            'arm_fk_L',
            'forearm_fk_L'
        ]
        new_bones = []
        new_bones_data = []
        zup = mathutils.Vector((0, 0, 0))
        for bone in act_rig.edit_bones:
            if bone.name in def_bones:
                new_bones.append(bone)
                pass
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.armature_add(enter_editmode=True, location=(0, 0, 0))
        new_obj = bpy.context.active_object
        new_rig = new_obj.data
        print(new_obj.name, new_rig.name)
        new_rig.edit_bones.remove(new_rig.edit_bones[0])
        for b in new_bones:
            new_bone = new_rig.edit_bones.new(b.name)
            new_bone.head = b.head
            new_bone.tail = b.tail
            new_bone.roll = b.roll
        # add constraint
        print('extract bones count:', len(new_bones))

        bpy.ops.object.editmode_toggle()

        for b in bpy.data.objects[new_obj.name].pose.bones:
            print('pose bone', b.name)
            c = b.constraints.new("COPY_TRANSFORMS")
            c.target = bpy.data.objects[act_rig_obj.name]
            c.subtarget = b.name
            c.target_space = 'POSE'
            c.owner_space = 'POSE'

    def rename_fuse_to_blenrig5():
        # in edit mode only
        fuse_obj = bpy.data.objects['A']
        fuse_rig = fuse_obj.data
        bone_map = {
            "arm_L": "arm_fk_L",
            "arm_fk_L": "arm_fkf2_L",
        }
        for bone in fuse_obj.data.edit_bones:
            if bone.name in bone_map:
                pass
                #bone.name = bone_map[bone.name]

        target_rig = bpy.data.objects["biped_blenrig"]
        print('fuse head', fuse_rig.edit_bones[0].head)
        # todo toggle to target rig ,get edit_bone 's data instead of pose bone
        fuse_rig.edit_bones[
            'arm_fk_L'].head = target_rig.pose.bones['arm_fk_L'].head
        fuse_rig.edit_bones[
            'arm_fk_L'].tail = target_rig.pose.bones['arm_fk_L'].tail
        fuse_rig.edit_bones[
            'arm_fk_L'].roll = target_rig.pose.bones['arm_fk_L'].roll
        # fuse_rig.edit_bones['arm_fk_L'].tail = target_rig.edit_bones['arm_fk_L'].tail

        pass
    from mathutils import Matrix

    def match2(src, target):
        # print(target.head, target.tail)
        src.head = target['head']
        src.tail = target['tail']
        src.roll = target['roll']
        # src.head = target.head
        # src.tail = target.tail
        # src.roll = target.roll

    def snap2(pbone, target_bone, fuse_obj):
        mat = fuse_obj.matrix_world * target_bone.matrix
        print('cl',mat.translation)
        bpy.context.scene.cursor_location = mat.translation
        pbone.matrix.translation =mat.translation 

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
                # bone = brg5_obj.data.edit_bones[bone_name]
                pbone = brg5_obj.pose.bones[bone_name]
                snap2(pbone, target_bone, fuse_obj)

        # bpy.ops.object.posemode_toggle()

        # bpy.ops.object.mode_set(mode='EDIT')
        # for bone in brg5_rig.edit_bones:
        #     match2(bone, 1)
        pass
    brg5_match_fuse_rig()
    # extract_bones()
    # rename_fuse_to_blenrig5()
main()
