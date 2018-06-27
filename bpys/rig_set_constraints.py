def main():
    import bpy
    D = bpy.data
    C = bpy.context
    logs = []

    def init_select_obj():
        # rename def armature to "@def@xxxx" then blenRig5 to "@ctrl@xxxx",and toggle in pose mode
        # only one 3d_view open
        # repose
        # bake armature
        # edit mode fix joints calc roll

        # rest contraints
        # repose
        def_obj = None
        ctrl_obj = None
        for obj in D.objects:
            if '@def@' in obj.name:
                def_obj = obj
            if '@ctrl@' in obj.name:
                ctrl_obj = obj
        if not(def_obj and ctrl_obj):
            logs.append('rename two armatures')
            print('rename two armatures')
        else:
            logs.append('init :' + ctrl_obj.name + ' ' + def_obj.name)
            print('init select obj', ctrl_obj.name, def_obj.name)
        return ctrl_obj, def_obj

    def calc_rolls(def_obj, ctrl_obj, match_list):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action='DESELECT')
        ctrl_obj.select = True
        C.scene.objects.active = ctrl_obj
        bpy.ops.object.mode_set(mode="EDIT")
        def_roll_map = {}
        for a in match_list:
            if ctrl_obj.data.edit_bones.get(a[1]):
                ebone = ctrl_obj.data.edit_bones[a[1]]
                def_roll_map[a[0]] = ebone.roll
                # print('col roll', ebone.name, ebone.roll)
            pass
        bpy.ops.object.mode_set(mode="OBJECT")
        ctrl_obj.select = False
        def_obj.select = True
        C.scene.objects.active = def_obj
        bpy.ops.object.mode_set(mode="EDIT")
        for bname in def_roll_map:
            roll = def_roll_map[bname]
            def_obj.data.edit_bones[bname].roll = roll  # def_roll_map[bname]
            print('set roll', bname, roll)
        pass

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

    def set_constraint_to_brg5(rig_obj, brg5_obj):
        def _set_constraints(set_obj, target_obj, m_list, type, ex_setting=None):
            for a in m_list:
                b = set_obj.pose.bones[a[0]]
                c1 = None
                for c_exist in b.constraints:
                    if c_exist.type == type:
                        c1 = c_exist
                        break
                if not c1:
                    c1 = b.constraints.new(type)
                c1.target = target_obj
                c1.subtarget = a[1]
                if ex_setting:
                    ex_setting(c1)
        # main bones
        damped_track_list = symmrtry([
            ["arm_fk_L", "arm_ik_L"],
            ["forearm_fk_L", "forearm_ik_L"],


            ["thigh_fk_L", "thigh_ik_L"],
            ["shin_fk_L", "shin_ik_L"],
            ["foot_fk_L", "foot_ik_L"],
            ["toe_1_fk_L", "toes_ik_ctrl_L"],
        ])

        def _set_damped_track(c):
            c.head_tail = 1

        # add finger
        match_list_finger = []
        copy_rot_list = []

        def _set_scale_to_rot(c):
            c.map_from = 'SCALE'
            c.map_to = 'ROTATION'
            c.use_motion_extrapolate = True
            c.from_min_y_scale = 0.5
            c.from_max_y_scale = 1
            c.from_min_z_scale = 1
            c.from_max_z_scale = 1
            c.map_to_x_from = 'Y'
            c.to_min_x_rot = 1.5708
            c.target_space = 'POSE'
            c.target_space = 'LOCAL'
            c.owner_space = 'LOCAL'
            pass

        scale_2_rot_list = []
        for b in rig_obj.pose.bones:
            if 'fing' in b.name:
                a = b.name.split('_')
                if a[2] != '1':
                    target_name = '_'.join([a[0], a[1], 'ctrl', a[3]])
                    scale_2_rot_list.append([b.name, target_name])
                if a[2] == '2':
                    damped_track_list.append([b.name,target_name])

        _set_constraints(rig_obj, brg5_obj, scale_2_rot_list,
                         "TRANSFORM", _set_scale_to_rot)

        def _set_x_only(c):
            c.use_x = True
            c.use_y = False
            c.use_z = False
            c.target_space = 'POSE'
            c.owner_space = 'POSE'

        def _set_copy_transforms(c):
            c.target_space = 'POSE'
            c.owner_space = 'POSE'

        def _set_copy_transforms_world(c):
            c.target_space = 'WORLD'
            c.owner_space = 'WORLD'
            # st = c.subtarget
            # if not c.id_data.pose.bones.get(st):
            #     finger_num = int(st[-3:-2])-1
            # c.subtarget = c.id_data
            #     print(c.subtarget,c.subtarget)
        # match_list.extend(match_list_finger)
        copy_rot_list.extend(symmrtry([
            ['hand_fk_L', 'hand_fk_L'],
            ["pelvis", "pelvis_ctrl"],
            # ['head_fk', 'head_fk'],
        ]))
        _set_constraints(rig_obj, brg5_obj, copy_rot_list,
                         "COPY_ROTATION", _set_copy_transforms)
        #  "COPY_TRANSFORMS", _set_copy_transforms)
        #  "LOCKED_TRACK", _set_damped_track)
        _set_constraints(rig_obj, brg5_obj, match_list_finger,
                         #  "LOCKED_TRACK", _set_damped_track)
                         "DAMPED_TRACK", _set_damped_track)

        _set_constraints(rig_obj, brg5_obj, symmrtry([
            ["master_torso", "master_torso"],
            ["spine_1_fk", "spine_1_fk"],
            ["spine_2_fk", "spine_2_fk"],
            ["spine_3_fk", "spine_3_fk"],
            ["neck_1_fk", "neck_1_fk"],
            ["neck_2_fk", "neck_2_fk"],
            ["neck_3_fk", "neck_3_fk"],
            ['head_fk', 'head_fk'],
            ['shoulder_L', 'shoulder_L'],
        ]),
            "COPY_TRANSFORMS", _set_copy_transforms_world)

        _set_constraints(rig_obj, brg5_obj, damped_track_list,
                         "DAMPED_TRACK", _set_damped_track)
        #  "COPY_TRANSFORMS", _set_copy_transforms)

        return damped_track_list
      ################
    ctrl_obj, def_obj = init_select_obj()
    match_list = set_constraint_to_brg5(def_obj, ctrl_obj)
    # calc_rolls(def_obj, ctrl_obj, match_list)

    def label(self, context):
        t = '\n'.join(logs)
        self.layout.label(t)
    C.window_manager.popup_menu(label, title="info", icon='INFO')
    pass
main()
