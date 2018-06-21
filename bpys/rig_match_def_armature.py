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
        if not(ctrl_obj and brg5_obj):
            logs.append('rename two armatures')
            print('rename two armatures')
        else:
            logs.append('init :' + brg5_obj.name + ' ' + ctrl_obj.name)
            print('init select obj', brg5_obj.name, ctrl_obj.name)
        return brg5_obj, ctrl_obj

    def snap_bone(pose_bone, target_bone, rig_obj, target_obj, move_bone=None, tail_offset=None):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = area.regions[-1]
                # bpy.ops.view3d.view_selected(ctx)

                print('snap', pose_bone.name, 'to',
                      target_obj.name, target_bone.name)
                mat = target_obj.matrix_world * target_bone.matrix
                mat2 = pose_bone.matrix * rig_obj.matrix_world
                t = mat.translation - mat2.translation
                if tail_offset:
                    t += tail_offset

                if move_bone:
                    pose_bone = move_bone
                pose_bone.bone.select = True
                bpy.ops.transform.translate(value=t, constraint_axis=(
                    False, False, False), constraint_orientation='NORMAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                # bpy.ops.view3d.snap_selected_to_cursor(ctx, use_offset=False)
                pose_bone.bone.select = False  # True
                break

    # def snap_bone2(pose_bone, target_bone, target_obj):
    #     for area in bpy.context.screen.areas:
    #         if area.type == 'VIEW_3D':
    #             ctx = bpy.context.copy()
    #             ctx['area'] = area
    #             ctx['region'] = area.regions[-1]
    #             # bpy.ops.view3d.view_selected(ctx)

    #             print('snap', pose_bone.name, 'to',
    #                   target_obj.name, target_bone.name)
    #             mat = target_obj.matrix_world * target_bone.matrix
    #             bpy.context.scene.cursor_location = mat.translation
    #             pose_bone.bone.select = True
    #             bpy.ops.view3d.snap_selected_to_cursor(ctx, use_offset=False)
    #             pose_bone.bone.select = False  # True
    #             break

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
            ["master_torso", "master_torso"],
            ["spine_ctrl_1_str", "spine_1_fk"],
            ["spine_ctrl_2_str", "spine_2_fk"],
            ["spine_ctrl_3_str", "spine_3_fk"],
            ["spine_ctrl_4_str", "spine_3.tail_fk"],
            #head
            ["neck_ctrl_2_str", "neck_2_fk"],
            ["neck_ctrl_3_str", "neck_3_fk"],
            ["neck_ctrl_4_str", "neck_3.tail_fk"],
            #arm
            ["clavi_str_L", "shoulder_L"],
            ["shoulder_str_L", "arm_fk_L"],
            ["wrist_str_L", "hand_fk_L"],
            ["hand_str_L", "hand_fk.tail_L"],
            ["pelvis_str_L", "thigh_fk_L"],
            ["pelvis_str", "pelvis.tail"],
            ["pelvis_ctrl_str", "pelvis.tail"],
            # pole str bone
            ["elbow_str_L", "forearm_fk_L"],
            ["knee_str_L", "shin_fk_L"],
            #
            ["ankle_str_L", "foot_fk_L"],
            ["foot_str_L", "toe_1_fk_L"],
            ["toe_str_1_L", "toe_1_fk_L"],
            ["toe_str_2_L", "toe_1_fk.tail_L"],
            # finger
            ["fing_thumb_str_1_L", "fing_thumb_1_L"],
            ["fing_thumb_str_2_L", "fing_thumb_2_L"],
            ["fing_thumb_str_3_L", "fing_thumb_3_L"],
            ["fing_thumb_str_4_L", "fing_thumb_3.tail_L"],
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
            ["fing_ind_str_5_L", "fing_ind_4.tail_L"],
            ["fing_mid_str_5_L", "fing_mid_4.tail_L"],
            ["fing_ring_str_5_L", "fing_ring_4.tail_L"],
            ["fing_lit_str_5_L", "fing_lit_4.tail_L"],
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

        def _get_move_bone(pbone_name, bones):
            if 'elbow_str' in pbone_name:
                return bones[pbone_name.replace('elbow_str', 'elbow_pole_str')]
            if 'knee_str' in pbone_name:
                return bones[pbone_name.replace('knee_str', 'knee_pole_str')]
            return None

        for a in match_list_sym:
            tail_offset = None
            is_tail = False
            pose_bone_name = a[0]
            match_bone_name = a[1]

            if '.tail' in match_bone_name:
                is_tail = True
                match_bone_name = match_bone_name.replace('.tail', '')

            pbone = brg5_obj.pose.bones[pose_bone_name]
            rbone = rig_obj.pose.bones[match_bone_name]
            if is_tail:
                tail_offset = (rbone.tail - rbone.head)
            if 'toe_str_1' in pose_bone_name:
                tail_offset = (rbone.tail - rbone.head) * 0.1
            move_bone = _get_move_bone(pose_bone_name, brg5_obj.pose.bones)

            snap_bone(pbone, rbone, brg5_obj, rig_obj, move_bone, tail_offset)

        return match_list_sym

    def rename_bones():
        obj = C.active_object
        for bone in obj.data.edit_bones:
            if bone.name.find("def_") > -1 and bone.name.find('fing') > -1:
                bone.name = bone.name.replace('def_', "")
      ################
    b_obj, r_obj = init_select_obj()
    # func_1#m_list = match_rig(b_obj, r_obj)

    def label(self, context):
        t = '\n'.join(logs)
        self.layout.label(t)
    C.window_manager.popup_menu(label, title="info", icon='INFO')
    pass
main()
