def main():
    import bpy
    D = bpy.data
    C = bpy.context
    logs = ['set parent roll']
    act_ebone = C.active_bone
    act_ebone.parent.roll = act_ebone.roll
    bpy.ops.armature.select_hierarchy(direction='PARENT', extend=False)

    def info(self, context):
        t = '\n'.join(logs)
        self.layout.label(t)
    C.window_manager.popup_menu(info, title="info", icon='INFO')
main()
