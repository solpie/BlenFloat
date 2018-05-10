def main():
    import bpy
    D = bpy.data
    C = bpy.context
    bone = "# bone_name#"
    if C.active_object.type == 'ARMATURE':
        bpy.ops.pose.select_all(action='DESELECT')
        b = C.active_object.pose.bones[bone]
        b.bone.select = True
main()
