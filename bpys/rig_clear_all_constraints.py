def main():
    import bpy
    D = bpy.data
    C = bpy.context
    logs = ['clear all constraints']
    
    for b in C.active_object.pose.bones:
        for c in b.constraints:
            b.constraints.remove(c)

    def info(self, context):
        t = '\n'.join(logs)
        self.layout.label(t)
    C.window_manager.popup_menu(info, title="info", icon='INFO')
main()
