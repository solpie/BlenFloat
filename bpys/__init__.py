def main():
    import bpy
    D = bpy.data
    C = bpy.context
    logs = []

    def info(self, context):
        t = '\n'.join(logs)
        self.layout.label(t)
    C.window_manager.popup_menu(info, title="info", icon='INFO')
main()
