import os.path as p

import bpy


blends_dir_path = p.join(p.dirname(__file__), "blends")

class AddPrimitiveBaseOperator(bpy.types.Operator):
  """This is a base class for add primitive operations.
  Implements the logic of the operation. Children should
  override `nodetree_name` and `icon` class properties.

  - `nodetree_name` - name of the node tree as written in `shapes.blend` file
  - `icon` - id of the icon to be displayed in the menu
  - `filename` - name of the file in `blends` folder to append from (Optional, defaults to `shapes.blend`)
  """
  nodetree_name = "arketools_CubeShape"
  icon = "MESH_CUBE"
  filename = "shapes.blend"


  def execute(self, context):
    nodetree_name = self.nodetree_name

    # append node tree if need be
    if bpy.data.node_groups.get(nodetree_name) is None:
      filepath = p.join(blends_dir_path, self.filename)
      bpy.ops.wm.append(filename=nodetree_name, directory=filepath + "/NodeTree/")

    # create mesh object
    mesh = bpy.data.meshes.new(name="NewMesh")
    object_data = bpy.data.objects.new("NewObject", mesh)
    object_data.location = bpy.context.scene.cursor.location

    bpy.context.collection.objects.link(object_data)

    # Add geometry nodes modifier
    geom_nodes_modifier = object_data.modifiers.new("GeometryNodes", "NODES")
    geom_nodes_modifier.node_group = bpy.data.node_groups[nodetree_name]

    # Apply selection
    bpy.ops.object.select_all(action='DESELECT')
    object_data.select_set(True)
    bpy.context.view_layer.objects.active = object_data
    return {'FINISHED'}


class AddPrimitiveCube(AddPrimitiveBaseOperator):
  """Add a cube, which can be modified after creation
  """
  bl_label = "Add Cube"
  bl_idname = "object.add_procedural_primitive_cube"



class AddPrimitiveUVSphere(AddPrimitiveBaseOperator):
  bl_label = "Add UV Sphere"
  bl_idname = "object.add_procedural_primitive_uvsphere"

  nodetree_name = "arketools_UVSphereShape"
  icon = "MESH_UVSPHERE"


#MESH_CYLINDER
class AddPrimitiveCylinder(AddPrimitiveBaseOperator):
    bl_label = "Add Cylinder"
    bl_idname = "object.add_procedural_primitive_cylinder"

    nodetree_name = "arketools_CylinderShape"
    icon = "MESH_CYLINDER"


# arketools_ConeShape
class AddPrimitiveCone(AddPrimitiveBaseOperator):
    bl_label = "Add Cone"
    bl_idname = "object.add_procedural_primitive_cone"

    nodetree_name = "arketools_ConeShape"
    icon = "MESH_CONE"


# arketools_IcoSphereShape
class AddPrimitiveIcoSphere(AddPrimitiveBaseOperator):
    bl_label = "Add Ico Sphere"
    bl_idname = "object.add_procedural_primitive_ico_sphere"

    nodetree_name = "arketools_IcoSphereShape"
    icon = "MESH_ICOSPHERE"

ops = [
  AddPrimitiveCube,
  AddPrimitiveUVSphere,
  AddPrimitiveCylinder,
  AddPrimitiveCone,
  AddPrimitiveIcoSphere
]

class ARKETOOLS_ADDOBJECT_MT_Menu(bpy.types.Menu):
    bl_label = "Add Procedural Primitive"
    bl_idname = "ARKETOOLS_ADDOBJECT_MT_Menu"

    def draw(self, context):
        layout = self.layout
        
        for cls in ops:
          layout.operator(cls.bl_idname, icon=cls.icon)


def register():
    for op in ops:
      bpy.utils.register_class(op)
    bpy.utils.register_class(ARKETOOLS_ADDOBJECT_MT_Menu)


def unregister():
    for op in ops:
      bpy.utils.unregister_class(op)
    bpy.utils.unregister_class(ARKETOOLS_ADDOBJECT_MT_Menu)
