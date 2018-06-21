def main():
    import bpy
    D = bpy.data
    C = bpy.context
    logs = ['hide cs shape']
    # bpy.context.scene.layers[19] = True
    ctrl_obj = None
    for obj in D.objects:
        if 'ctrl@' in obj.name:
            ctrl_obj = obj
    for obj in D.objects:
        if obj.type == 'MESH':
            # if 'cs_' in obj.name:# and 'blenrig' in obj.users_group[0].name:
            if 'cs_' in obj.name and('blenrig' in obj.users_group[0].name):
                obj.parent = ctrl_obj
                print(obj.name, 'blenrig' in obj.users_group[0].name)
    # bpy.context.scene.layers[19] = False

    def info(self, context):
        t = '\n'.join(logs)
        self.layout.label(t)
    C.window_manager.popup_menu(info, title="info", icon='INFO')
main()
