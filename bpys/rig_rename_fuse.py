def main():
    import bpy
    D = bpy.data
    C = bpy.context
    logs = ['clear all constraints']

    def rename_fuse():
        bone_map = {
            "mixamorig:LeftHandPinky1": "fing_lit_2_L",
            "mixamorig:LeftHandPinky2": "fing_lit_3_L",
            "mixamorig:LeftHandPinky3": "fing_lit_4_L",
            "mixamorig:LeftHandPinky4": "fing_lit_end",

            "mixamorig:LeftHandRing1": "fing_ring_2_L",
            "mixamorig:LeftHandRing2": "fing_ring_3_L",
            "mixamorig:LeftHandRing3": "fing_ring_4_L",
            "mixamorig:LeftHandRing4": "fing_ring_end",

            "mixamorig:LeftHandMiddle1": "fing_mid_2_L",
            "mixamorig:LeftHandMiddle2": "fing_mid_3_L",
            "mixamorig:LeftHandMiddle3": "fing_mid_4_L",
            "mixamorig:LeftHandMiddle4": "fing_mid_end",

            "mixamorig:LeftHandIndex1": "fing_ind_2_L",
            "mixamorig:LeftHandIndex2": "fing_ind_3_L",
            "mixamorig:LeftHandIndex3": "fing_ind_4_L",
            "mixamorig:LeftHandIndex4": "fing_ind_end",

            "mixamorig:LeftHandThumb1": "fing_thumb_1_L",
            "mixamorig:LeftHandThumb2": "fing_thumb_2_L",
            "mixamorig:LeftHandThumb3": "fing_thumb_3_L",
            "mixamorig:LeftHandThumb4": "fing_thumb_end",
        }

        bone_list = []
        for k in bone_map:
            bone_list.append([k, bone_map[k]])
            bone_list.append(
                [k.replace('Left', 'Right'), bone_map[k][: - 2] + '_R'])

        rig_obj = C.active_object
        for a in bone_list:

            print(a[0], 'to', a[1])
            if rig_obj.data.edit_bones[a[0]]:
                b = rig_obj.data.edit_bones[a[0]]
                b.name = a[1]
    rename_fuse()
    C.window_manager.popup_menu(lambda self, _:
                                self.layout.label('\n'.join(logs)), title="info", icon='INFO')
main()
