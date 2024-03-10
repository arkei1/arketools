from . import version

bl_info = {
    "name" : "Arketools",
    "author" : "Arkeii",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : version.version,
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


import bpy

from . import add_object

class FindNonSubDMods(bpy.types.Operator):
    """Selects all objects that have any modifier that
    may be incompatible with other software after export.
    Basically selects objects that have anything besides
    subdivision surface modifier on it.
    """
    bl_idname = "object.find_non_subd_mods"
    bl_label = "Find non-SubD modifiers"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        view_layer = context.view_layer

        for obj in context.scene.objects:
            if not (obj.visible_get() and obj.type == 'MESH'): continue
            non_subsurf_found = False
            for mod in obj.modifiers:
                if mod.type != 'SUBSURF':
                    non_subsurf_found = True
                    break
            if non_subsurf_found:
                obj.select_set(True)
                view_layer.objects.active = obj
        return {'FINISHED'}


# Define a new menu that includes your operator
class ARKETOOLS_MT_Menu(bpy.types.Menu):
    bl_label = "Arketools"
    bl_idname = "ARKETOOLS_MT_Menu"

    def draw(self, context):
        layout = self.layout
        layout.operator(FindNonSubDMods.bl_idname)
        layout.menu(add_object.ARKETOOLS_ADDOBJECT_MT_Menu.bl_idname)


# Function to draw the menu
def draw_item(self, context):
    layout = self.layout
    layout.menu(ARKETOOLS_MT_Menu.bl_idname)

def register():
    add_object.register()
    bpy.utils.register_class(FindNonSubDMods)
    bpy.utils.register_class(ARKETOOLS_MT_Menu)
    # Add the menu to the 3D View header
    bpy.types.VIEW3D_MT_object.append(draw_item)

def unregister():
    add_object.unregister()
    bpy.utils.unregister_class(FindNonSubDMods)
    bpy.utils.unregister_class(ARKETOOLS_MT_Menu)
    bpy.types.VIEW3D_MT_object.remove(draw_item)

if __name__ == "__main__":
    register()