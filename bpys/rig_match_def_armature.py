def main():
    import bpy
    D = bpy.data
    C = bpy.context
    logs = []

    def init_select_obj():
        # rename def armature to "def@xxxx" then blenRig5 to "ctrl@xxxx",and toggle in pose mode
        # only one 3d_view open
        # repose
        # bake armature
        # edit mode fix joints calc roll

        # rest contraints
        # repose
        ctrl_obj = None
        brg5_obj = None
        for obj in D.objects:
            if 'def@' in obj.name:
                ctrl_obj = obj
            if 'ctrl@' in obj.name:
                brg5_obj = obj
        # if len(C.selected_objects) == 2:
        #     for obj in C.selected_objects:
        #         if obj.name == C.active_object.name:
        #             brg5_obj = obj
        #         else:
        #             rig_obj = obj
        # else:
        if not(ctrl_obj and brg5_obj):
            logs.append('rename two armatures')
            print('rename two armatures')
        else:
            logs.append('init :' + brg5_obj.name + ' ' + ctrl_obj.name)
            print('init select obj', brg5_obj.name, ctrl_obj.name)
        return brg5_obj, ctrl_obj

    def snap_bone(pose_bone, target_bone, target_obj):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = area.regions[-1]
        #         # bpy.ops.view3d.view_selected(ctx)

                print('snap', pose_bone.name, 'to',
                      target_obj.name, target_bone.name)
                mat = target_obj.matrix_world * target_bone.matrix
                bpy.context.scene.cursor_location = mat.translation
                pose_bone.bone.select = True
                bpy.ops.view3d.snap_selected_to_cursor(ctx, use_offset=False)
                pose_bone.bone.select = False  # True
                break

    def copy_except(bone, target, idx):
        # idx 0,1,2 x y z

        if not(0 & idx):
            bone.location.x = target.location.x
        if not(1 & idx):
            bone.location.y = target.location.y
        if not(2 & idx):
            bone.location.z = target.location.z
        pass

    def symmrtry(list):
        list_sym = list.copy()
        for a in list:
            k = a[0]
            v = a[1]
            if k[-2:] == '_L':
                k_R = k[: - 2] + '_R'
                v_R = v[:-2] + '_R'
                list_sym.append([k_R, v_R])
        return list_sym

    def match_rig(brg5_obj, rig_obj):
        match_list_L = [
            ["master_torso", "spine_1_def"],
            ["spine_ctrl_1_str", "spine_2_def"],
            ["spine_ctrl_2_str", "spine_3_def"],
            # ["spine_ctrl_3_str", "neck_1_fk"],
            ["spine_ctrl_4_str", "neck_1_fk"],
            ["clavi_str_L", "shoulder_L"],
            ["shoulder_str_L", "arm_fk_L"],
            ["elbow_str_L", "forearm_fk_L"],
            ["wrist_str_L", "hand_fk_L"],
            ["hand_str_L", "hand_end_L"],
            ["pelvis_str_L", "thigh_fk_L"],
            ["pelvis_str", "pelvis_end"],
            # todo pelvis_str pelvis_end
            ["knee_str_L", "shin_fk_L"],
            ["ankle_str_L", "foot_fk_L"],
            ["foot_str_L", "toe_1_fk_L"],
            ["toe_str_1_L", "toe_2_fk_L"],
            ["toe_str_2_L", "toe_end_L"],
            # finger
            ["fing_thumb_str_1_L", "fing_thumb_1_L"],
            ["fing_thumb_str_2_L", "fing_thumb_2_L"],
            ["fing_thumb_str_3_L", "fing_thumb_3_L"],
            ["fing_thumb_str_4_L", "fing_thumb_end_L"],
            ["fing_ind_str_2_L", "fing_ind_2_L"],
            ["fing_mid_str_2_L", "fing_mid_2_L"],
            ["fing_ring_str_2_L", "fing_ring_2_L"],
            ["fing_lit_str_2_L", "fing_lit_2_L"],
            ["fing_ind_str_3_L", "fing_ind_3_L"],
            ["fing_mid_str_3_L", "fing_mid_3_L"],
            ["fing_ring_str_3_L", "fing_ring_3_L"],
            ["fing_lit_str_3_L", "fing_lit_3_L"],
            ["fing_ind_str_4_L", "fing_ind_4_L"],
            ["fing_mid_str_4_L", "fing_mid_4_L"],
            ["fing_ring_str_4_L", "fing_ring_4_L"],
            ["fing_lit_str_4_L", "fing_lit_4_L"],
            ["fing_ind_str_5_L", "fing_ind_end_L"],
            ["fing_mid_str_5_L", "fing_mid_end_L"],
            ["fing_ring_str_5_L", "fing_ring_end_L"],
            ["fing_lit_str_5_L", "fing_lit_end_L"],
        ]
        match_list_sym = match_list_L.copy()
        for a in match_list_L:
            k = a[0]
            v = a[1]
            if k[-2:] == '_L':
                k_R = k[: - 2] + '_R'
                v_R = v[:-2] + '_R'
                match_list_sym.append([k_R, v_R])

        bpy.ops.pose.select_all(action='DESELECT')
        for a in match_list_sym:
            pose_bone_name = a[0]
            match_bone_name = a[1]

            pbone = brg5_obj.pose.bones[pose_bone_name]
            rbone = rig_obj.pose.bones[match_bone_name]
            snap_bone(pbone, rbone, rig_obj)

        align_list = [
            ['elbow_pole_str_L', 'elbow_str_L', 1],
            ['elbow_pole_str_R', 'elbow_str_R', 1],
            ['knee_pole_str_L', 'knee_str_L', 1],
            ['knee_pole_str_R', 'knee_str_R', 1],
        ]
        for a in align_list:
            bone = brg5_obj.pose.bones[a[0]]
            target = brg5_obj.pose.bones[a[1]]
            axis = a[2]
            # copy_except(bone, target, axis)
        return match_list_sym

    def set_constraint_to_brg5(rig_obj, brg5_obj):
        match_list = symmrtry([
            ["arm_fk_L", "arm_ik_L"],
            ["forearm_fk_L", "forearm_ik_L"],
            ["thigh_fk_L", "thigh_ik_L"],
            ["shin_fk_L", "shin_ik_L"],
            ["foot_fk_L", "foot_ik_ctrl_L"],
        ])
        # add finger
        for b in rig_obj.pose.bones:
            if 'fing' in b.name and 'end' not in b.name:
                match_list.append([b.name, b.name])

        for a in match_list:
            b = rig_obj.pose.bones[a[0]]
            print('pose bone', b.name, 'copy', a[1])
            c1 = None
            for c in b.constraints:
                if c.type == 'COPY_TRANSFORMS':
                    c1 = c
                    break
            if not c1:
                c1 = b.constraints.new("COPY_TRANSFORMS")
            c1.target = brg5_obj  # bpy.data.objects[act_rig_obj.name]
            c1.subtarget = a[1]
            c1.target_space = 'POSE'
            c1.owner_space = 'POSE'

    def rename_bones():
        obj = C.active_object
        for bone in obj.data.edit_bones:
            if bone.name.find("def_") > -1 and bone.name.find('fing') > -1:
                bone.name = bone.name.replace('def_', "")
      ################
    b_obj, r_obj = init_select_obj()
    # func_1#m_list = match_rig(b_obj, r_obj)
    # func_2#set_constraint_to_brg5(r_obj, b_obj)

    def label(self, context):
        t = '\n'.join(logs)
        self.layout.label(t)
    C.window_manager.popup_menu(label, title="info", icon='INFO')
    pass
main()
