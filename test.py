def main():
    import bpy

    import mathutils
    C = bpy.context
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
    def rename_bones():
        obj = C.active_object
        for bone in obj.data.edit_bones:
            if bone.name.find("def_") > -1 and bone.name.find('fing') > -1:
                bone.name = bone.name.replace('def_', "")
    # brg5_match_fuse_rig()
    def remove_copy_transforms():
        for b in bpy.context.active_object.pose.bones:
            for c in b.constraints:
                if c.type == 'COPY_TRANSFORMS':
                    b.constraints.remove(c)
        pass
    remove_copy_transforms()
    # rename_bones()
    # extract_bones()
    # rename_fuse_to_blenrig5()
main()
