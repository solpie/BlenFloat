# pose.bones["c_foot_ik.l"]["auto_stretch"]
# pose.bones["c_hand_ik.r"]["auto_stretch"]


def main():
    import bpy
    D = bpy.data
    C = bpy.context
    logs = ['fix stretch']
    act_obj = C.active_object
    fix_list = [
        "c_foot_ik.l",
        "c_hand_ik.l"
    ]
    for bone in fix_list:
        if bone[-2:] == '.l':
            bone_mirror = bone[:-1] + 'r'
            act_obj.pose.bones[bone_mirror]["auto_stretch"] = 0
        act_obj.pose.bones[bone]["auto_stretch"] = 0


    def info(self, context):
        t = '\n'.join(logs)
        self.layout.label(t)
    C.window_manager.popup_menu(info, title="info", icon='INFO')
main()
