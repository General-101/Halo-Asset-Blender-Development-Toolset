# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

from bpy.types import (
        PropertyGroup,
        Operator,
        Panel
        )

from bpy.props import (
        BoolProperty,
        EnumProperty,
        StringProperty,
        FloatProperty
        )

class Halo_XREFPath(Operator):
    """Set the path for the XREF model file"""
    bl_idname = "import_scene.xref_path"
    bl_label = "Set XREF"
    filename_ext = ''

    filter_glob: StringProperty(
        default="*.jms;*.jmi;*.blend;*.max",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        name="XREF",
        description="Set path for the XREf file",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        active_object = context.view_layer.objects.active
        if active_object:
            active_object.data.ass_jms.XREF_path = self.filepath
            context.area.tag_redraw()

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}

class Halo_MeshProps(Panel):
    bl_label = "Halo Mesh Properties"
    bl_idname = "HALO_PT_MeshDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context):
        scene = context.scene
        scene_halo = scene.halo

        mesh = context.object.data

        ass_jms = None
        if hasattr(mesh, 'ass_jms') and not scene_halo.game_title == "halo1":
            ass_jms = mesh.ass_jms

        return ass_jms

    def draw(self, context):
        layout = self.layout

        mesh = context.object.data
        mesh_ass_jms = mesh.ass_jms

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Bounding Radius:')
        row.prop(mesh_ass_jms, "bounding_radius", text='')
        row = col.row()
        row.label(text='Object Type:')
        row.prop(mesh_ass_jms, "Object_Type", text='')
        row = col.row()
        row.operator(Halo_XREFPath.bl_idname, text="XREF Path")
        row.prop(mesh_ass_jms, "XREF_path", text='')
        row = col.row()
        row.label(text='XREF Name:')
        row.prop(mesh_ass_jms, "XREF_name", text='')

class ASS_JMS_MeshPropertiesGroup(PropertyGroup):
    bounding_radius: BoolProperty(
        name ="Bounding Radius",
        description = "Sets object as a bounding radius",
        default = False,
        )

    Object_Type : EnumProperty(
        name="Object Type",
        description="Select object type to write mesh as",
        default = "CONVEX SHAPES",
        items=[ ('SPHERE', "Sphere", "Sphere"),
                ('BOX', "Box", "Box"),
                ('CAPSULES', "Pill", "Pill/Capsule"),
                ('CONVEX SHAPES', "Convex Shape", "Convex Shape/Mesh"),
               ]
        )

    XREF_path: StringProperty(
        name="XREF Object",
        description="Select a path to a model file",
    )

    XREF_name: StringProperty(
        name="XREF Name",
        description="Set the name of the XREF object. The model file should contain an object by this name",
    )

class Halo_ObjectProps(Panel):
    bl_label = "Halo Object Properties"
    bl_idname = "HALO_PT_ObjectDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context):
        valid = False
        ob = context.object

        if hasattr(ob, 'ass_jms'):
            valid = True

        return valid

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo = scene.halo

        ob = context.object
        ob_ass_jms = ob.ass_jms

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Name Override:')
        row.prop(ob_ass_jms, "name_override", text='')
        row = col.row()
        row.label(text='Unique ID:')
        row.prop(ob_ass_jms, "unique_id", text='')
        if ob.name[0:1].lower() == '#':
            row = col.row()
            row.label(text='Mask Type:')
            row.prop(ob_ass_jms, "marker_mask_type", text='')
            if scene_halo.game_title == "halo1":
                row = col.row()
                row.label(text='Region:')
                row.prop(ob_ass_jms, "marker_region", text='')

        if scene_halo.game_title == "halo3":
            if ob.type == 'ARMATURE':
                row = col.row()
                row.label(text='Ubercam Object Type:')
                row.prop(ob_ass_jms, "ubercam_object_type", text='')
                row = col.row()
                row.label(text='Ubercam Object Animation:')
                row.prop(ob_ass_jms, "ubercam_object_animation", text='')

class Halo_BoneProps(Panel):
    bl_label = "Halo Bone Properties"
    bl_idname = "HALO_PT_BoneDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "bone"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context):
        valid = False
        ob = context.object

        if ob.type == 'ARMATURE' and ob.data.bones.active:
            if hasattr(ob, 'ass_jms'):
                valid = True

        return valid

    def draw(self, context):
        layout = self.layout

        ob = context.object
        bone = ob.data.bones.active
        bone_ass_jms = bone.ass_jms

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Name Override:')
        row.prop(bone_ass_jms, "name_override", text='')
        row = col.row()
        row.label(text='Unique ID:')
        row.prop(bone_ass_jms, "unique_id", text='')

class ASS_JMS_ObjectPropertiesGroup(PropertyGroup):
    name_override: StringProperty(
        name="Name Override",
        description="If filled then export will use the name set here instead of the object name",
    )

    unique_id: StringProperty(
        name="Unique ID",
        description="Store the original ID here. Uses a random value if nothing is defined"
    )

    marker_mask_type: EnumProperty(
        name="Mask Type",
        description="Choose the mask type for the marker object",
        items=( ('0', "Render",    "Render"),
                ('1', "Collision", "Collision"),
                ('2', "Physics",   "Physics"),
                ('3', "All",       "All"),
            )
        )

    marker_region: StringProperty(
        name="Region",
        description="Region for a marker object. If empty then the first assigned facemap will be used",
        default = "",
        )

    ubercam_object_type: EnumProperty(
        name="Ubercam Object Type",
        description="Choose the group for the object",
        items=( ('0', "Unit",    "Unit"),
                ('1', "Scenery", "Scenery"),
                ('2', "Effect Scenery",   "Effect Scenery"),
            )
        )

    ubercam_object_animation: StringProperty(
            name = "Ubercam Animation Path",
            description="Source file for ubercam object animation",
            default="",
            maxlen=1024,
            subtype='FILE_PATH'
    )

class QUA_ObjectPropertiesGroup(PropertyGroup):
    ubercam_type: StringProperty(
        name="Ubercam Type",
        description="Type of camera the ubercam is set to",
        default = "",
        )

    near_focal_plane_distance: FloatProperty(
        name="Near Focal Plane Distance",
        description="Near distance for depth of field"
        )

    far_focal_plane_distance: FloatProperty(
        name="Far Focal Plane Distance",
        description="Far distance for depth of field"
        )

class Halo_CameraProps(Panel):
    bl_label = "Halo Camera Properties"
    bl_idname = "HALO_PT_CameraDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context):
        valid = False
        scene = context.scene
        scene_halo = scene.halo
        ob_data = context.object.data

        if hasattr(ob_data, 'qua') and scene_halo.game_title == "halo3":
            valid = True

        return valid

    def draw(self, context):
        layout = self.layout

        ob = context.object
        ob_qua = ob.data.qua

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Ubercam Type:')
        row.prop(ob_qua, "ubercam_type", text='')
        row = col.row()
        row.label(text='Near Focal Plane Distance:')
        row.prop(ob_qua, "near_focal_plane_distance", text='')
        row = col.row()
        row.label(text='Far Focal Plane Distance:')
        row.prop(ob_qua, "far_focal_plane_distance", text='')
