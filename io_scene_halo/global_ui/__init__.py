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

import bpy
import bmesh

from enum import Flag, auto
from bpy.types import (
        PropertyGroup,
        Operator,
        UIList,
        Panel,
        Menu
        )

from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        PointerProperty,
        FloatVectorProperty,
        CollectionProperty
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

class ASS_JMS_MaterialProps(Panel):
    bl_label = "Halo Material Properties"
    bl_idname = "ASS_JMS_PT_MaterialPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self, context):
        mat = context.material

        return mat

    def draw_header(self, context):
        current_material = context.object.active_material
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            self.layout.prop(material_ass_jms, "is_bm", text='')

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo = scene.halo
        current_material = context.object.active_material
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            layout.enabled = material_ass_jms.is_bm
            row = layout.row()
            row.label(text="Name Override:")
            row.prop(material_ass_jms, "name_override", text='')
            if scene_halo.game_title == "halo2" or scene_halo.game_title == "halo3":
                row = layout.row()
                row.label(text="Material Effect:")
                row.prop(material_ass_jms, "material_effect", text='')

class ASS_JMS_MaterialFlagsProps(Panel):
    bl_label = "Flags"
    bl_idname = "ASS_JMS_PT_MaterialFlagsPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "ASS_JMS_PT_MaterialPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo = scene.halo
        current_material = context.object.active_material
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            layout.enabled = material_ass_jms.is_bm
            box = layout.split()
            col = box.column(align=True)
            row = col.row()

            if scene_halo.game_title == "halo1":
                row = col.row()
                row.label(text='Two-sided:')
                row.prop(material_ass_jms, "two_sided", text='')
                row = col.row()
                row.label(text='Transparent:')
                row.prop(material_ass_jms, "transparent_1_sided", text='')
                row = col.row()
                row.label(text='Render Only:')
                row.prop(material_ass_jms, "render_only", text='')
                row = col.row()
                row.label(text='Large Collideable:')
                row.prop(material_ass_jms, "sphere_collision_only", text='')
                row = col.row()
                row.label(text='Fog Plane:')
                row.prop(material_ass_jms, "fog_plane", text='')
                row = col.row()
                row.label(text='Ladder:')
                row.prop(material_ass_jms, "ladder", text='')
                row = col.row()
                row.label(text='Breakable:')
                row.prop(material_ass_jms, "breakable", text='')
                row = col.row()
                row.label(text='AI Deafening:')
                row.prop(material_ass_jms, "ai_deafening", text='')
                row = col.row()
                row.label(text='Collision Only:')
                row.prop(material_ass_jms, "collision_only", text='')
                row = col.row()
                row.label(text='Exact Portal:')
                row.prop(material_ass_jms, "portal_exact", text='')

            if scene_halo.game_title == "halo2":
                row = col.row()
                row.label(text='Two-sided:')
                row.prop(material_ass_jms, "two_sided", text='')
                row = col.row()
                row.label(text='One-sided Transparent:')
                row.prop(material_ass_jms, "transparent_1_sided", text='')
                row = col.row()
                row.label(text='Two-sided Transparent:')
                row.prop(material_ass_jms, "transparent_2_sided", text='')
                row = col.row()
                row.label(text='Render Only:')
                row.prop(material_ass_jms, "render_only", text='')
                row = col.row()
                row.label(text='Collision Only:')
                row.prop(material_ass_jms, "collision_only", text='')
                row = col.row()
                row.label(text='Sphere Collision Only:')
                row.prop(material_ass_jms, "sphere_collision_only", text='')
                row = col.row()
                row.label(text='Fog Plane:')
                row.prop(material_ass_jms, "fog_plane", text='')
                row = col.row()
                row.label(text='Ladder:')
                row.prop(material_ass_jms, "ladder", text='')
                row = col.row()
                row.label(text='Breakable:')
                row.prop(material_ass_jms, "breakable", text='')
                row = col.row()
                row.label(text='AI Deafening:')
                row.prop(material_ass_jms, "ai_deafening", text='')
                row = col.row()
                row.label(text='No Shadow:')
                row.prop(material_ass_jms, "no_shadow", text='')
                row = col.row()
                row.label(text='Shadow Only:')
                row.prop(material_ass_jms, "shadow_only", text='')
                col = box.column()
                row = col.row()
                row.label(text='Lightmap Only:')
                row.prop(material_ass_jms, "lightmap_only", text='')
                row = col.row()
                row.label(text='Precise:')
                row.prop(material_ass_jms, "precise", text='')
                row = col.row()
                row.label(text='Conveyor:')
                row.prop(material_ass_jms, "conveyor", text='')
                row = col.row()
                row.label(text='Portal (One-Way):')
                row.prop(material_ass_jms, "portal_1_way", text='')
                row = col.row()
                row.label(text='Portal (Door):')
                row.prop(material_ass_jms, "portal_door", text='')
                row = col.row()
                row.label(text='Portal (Vis Blocker):')
                row.prop(material_ass_jms, "portal_vis_blocker", text='')
                row = col.row()
                row.label(text='Dislikes Photons:')
                row.prop(material_ass_jms, "dislike_photons", text='')
                row = col.row()
                row.label(text='Ignored by Lightmapper:')
                row.prop(material_ass_jms, "ignored_by_lightmaps", text='')
                row = col.row()
                row.label(text='Portal (Sound Blocker):')
                row.prop(material_ass_jms, "blocks_sound", text='')
                row = col.row()
                row.label(text='Decal Offset:')
                row.prop(material_ass_jms, "decal_offset", text='')

            if scene_halo.game_title == "halo3":
                row = col.row()
                row.label(text='Two-sided:')
                row.prop(material_ass_jms, "two_sided", text='')
                row = col.row()
                row.label(text='One-sided Transparent:')
                row.prop(material_ass_jms, "transparent_1_sided", text='')
                row = col.row()
                row.label(text='Two-sided Transparent:')
                row.prop(material_ass_jms, "transparent_2_sided", text='')
                row = col.row()
                row.label(text='Render Only:')
                row.prop(material_ass_jms, "render_only", text='')
                row = col.row()
                row.label(text='Collision Only:')
                row.prop(material_ass_jms, "collision_only", text='')
                row = col.row()
                row.label(text='Sphere Collision Only:')
                row.prop(material_ass_jms, "sphere_collision_only", text='')
                row = col.row()
                row.label(text='Fog Plane:')
                row.prop(material_ass_jms, "fog_plane", text='')
                row = col.row()
                row.label(text='Ladder:')
                row.prop(material_ass_jms, "ladder", text='')
                row = col.row()
                row.label(text='Breakable:')
                row.prop(material_ass_jms, "breakable", text='')
                row = col.row()
                row.label(text='AI Deafening:')
                row.prop(material_ass_jms, "ai_deafening", text='')
                row = col.row()
                row.label(text='No Shadow:')
                row.prop(material_ass_jms, "no_shadow", text='')
                row = col.row()
                row.label(text='Shadow Only:')
                row.prop(material_ass_jms, "shadow_only", text='')
                col = box.column()
                row = col.row()
                row.label(text='Lightmap Only:')
                row.prop(material_ass_jms, "lightmap_only", text='')
                row = col.row()
                row.label(text='Precise:')
                row.prop(material_ass_jms, "precise", text='')
                row = col.row()
                row.label(text='Conveyor:')
                row.prop(material_ass_jms, "conveyor", text='')
                row = col.row()
                row.label(text='Portal (One-Way):')
                row.prop(material_ass_jms, "portal_1_way", text='')
                row = col.row()
                row.label(text='Portal (Door):')
                row.prop(material_ass_jms, "portal_door", text='')
                row = col.row()
                row.label(text='Portal (Vis Blocker):')
                row.prop(material_ass_jms, "portal_vis_blocker", text='')
                row = col.row()
                row.label(text='Ignored by Lightmapper:')
                row.prop(material_ass_jms, "ignored_by_lightmaps", text='')
                row = col.row()
                row.label(text='Portal (Sound Blocker):')
                row.prop(material_ass_jms, "blocks_sound", text='')
                row = col.row()
                row.label(text='Decal Offset:')
                row.prop(material_ass_jms, "decal_offset", text='')
                row = col.row()
                row.label(text='Water Surface:')
                row.prop(material_ass_jms, "water_surface", text='')
                row = col.row()
                row.label(text='Slip Surface:')
                row.prop(material_ass_jms, "slip_surface", text='')
                row = col.row()
                row.label(text='Group Transparents By Plane:')
                row.prop(material_ass_jms, "group_transparents_by_plane", text='')

class ASS_JMS_MaterialLightmapProps(Panel):
    bl_label = "Lightmap Resolution Properties"
    bl_idname = "ASS_JMS_PT_MaterialLightmapPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "ASS_JMS_PT_MaterialPanel"

    @classmethod
    def poll(self, context):
        scene = context.scene
        scene_halo = scene.halo
        if scene_halo.game_title == "halo2" or scene_halo.game_title == "halo3":
            return True

    def draw(self, context):
        layout = self.layout
        current_material = context.object.active_material
        scene = context.scene
        scene_halo = scene.halo
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            layout.enabled = material_ass_jms.is_bm
            if scene_halo.game_title == "halo2":
                col = layout.column(align=True)
                row = col.row()
                row.label(text='Lightmap Resolution Scale:')
                row.prop(material_ass_jms, "lightmap_resolution_scale", text='')
                row = col.row()
                row.label(text='Lightmap Power Scale:')
                row.prop(material_ass_jms, "lightmap_power_scale", text='')
                row = col.row()
                row.label(text='Lightmap Half-Life Scale:')
                row.prop(material_ass_jms, "lightmap_half_life", text='')
                row = col.row()
                row.label(text='Lightmap Diffuse Scale:')
                row.prop(material_ass_jms, "lightmap_diffuse_scale", text='')

            else:
                col_split = layout.column(align=True).split()
                col = layout.column(align=True)
                col_split_b = layout.column(align=True).split()
                col_b = layout.column(align=True)
                row = col_split.row()
                row.label(text='Override Lightmap Transparency:')
                row.prop(material_ass_jms, "override_lightmap_transparency", text='')
                row = col_split.row()
                row.label(text='Ignore Default Resolution Scale:')
                row.prop(material_ass_jms, "ignore_default_res_scale", text='')
                row = col.row()
                row.label(text='Two-sided Transparent Tint:')
                row.prop(material_ass_jms, "two_sided_transparent_tint", text='')
                row = col.row()
                row.label(text='Additive Transparency:')
                row.prop(material_ass_jms, "additive_transparency", text='')
                row = col_split_b.row()
                row.label(text='Lightmap Resolution:')
                row.prop(material_ass_jms, "lightmap_res", text='')
                row = col_split_b.row()
                row.label(text='Photon Fidelity:')
                row.prop(material_ass_jms, "photon_fidelity", text='')
                row = col_b.row()
                row.label(text='Use Shader Gel:')
                row.prop(material_ass_jms, "use_shader_gel", text='')

class ASS_JMS_MaterialBasicProps(Panel):
    bl_label = "Lightmap Properties"
    bl_idname = "ASS_JMS_PT_MaterialBasicPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "ASS_JMS_PT_MaterialPanel"

    @classmethod
    def poll(self, context):
        scene = context.scene
        scene_halo = scene.halo

        if scene_halo.game_title == "halo3":
            return True

    def draw(self, context):
        layout = self.layout
        current_material = context.object.active_material
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            layout.enabled = material_ass_jms.is_bm
            is_enabled = True
            if material_ass_jms.power <= 0.0:
                is_enabled = False
            col = layout.column(align=True)
            row = col.row()
            row.label(text='Power:')
            row.prop(material_ass_jms, "power", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Color:')
            row.prop(material_ass_jms, "color", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Quality:')
            row.prop(material_ass_jms, "quality", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Power Per Unit Area:')
            row.prop(material_ass_jms, "power_per_unit_area", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Emissive Focus:')
            row.prop(material_ass_jms, "emissive_focus", text='')

class ASS_JMS_MaterialAttenuationProps(Panel):
    bl_label = "Attenuation"
    bl_idname = "ASS_JMS_PT_MaterialAttenuationPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "ASS_JMS_PT_MaterialBasicPanel"

    def draw_header(self, context):
        current_material = context.object.active_material
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            if material_ass_jms.power <= 0.0 or not material_ass_jms.is_bm:
                self.layout.enabled = False

            self.layout.prop(material_ass_jms, "attenuation_enabled", text='')

    def draw(self, context):
        layout = self.layout
        current_material = context.object.active_material
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            if material_ass_jms.power <= 0.0 or not material_ass_jms.is_bm or not material_ass_jms.attenuation_enabled:
                layout.enabled = False

            col = layout.column(align=True)
            row = col.row()
            row.label(text='Falloff Distance:')
            row.prop(material_ass_jms, "falloff_distance", text='')
            row = col.row()
            row.label(text='Cutoff Distance:')
            row.prop(material_ass_jms, "cutoff_distance", text='')

class ASS_JMS_MaterialFrustumProps(Panel):
    bl_label = "Frustum"
    bl_idname = "ASS_JMS_PT_MaterialFrustumPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "ASS_JMS_PT_MaterialBasicPanel"

    def draw(self, context):
        layout = self.layout
        current_material = context.object.active_material
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            layout.enabled = material_ass_jms.is_bm
            if material_ass_jms.power <= 0.0:
                layout.enabled = False

            col = layout.column(align=True)
            row = col.row()
            row.label(text='Blend:')
            row.prop(material_ass_jms, "frustum_blend", text='')
            row = col.row()
            row.label(text='Falloff:')
            row.prop(material_ass_jms, "frustum_falloff", text='')
            row = col.row()
            row.label(text='Cutoff:')
            row.prop(material_ass_jms, "frustum_cutoff", text='')

class ASS_JMS_MaterialPropertiesGroup(PropertyGroup):
    name_override: StringProperty(
        name = "Name Override",
        description = "If filled then export will use the name set here instead of the material name",
        default = "",
        )

    material_effect: StringProperty(
        name = "Material Effect",
        description = "Set material effect name",
        default = "",
        )

    two_sided: BoolProperty(
        name ="Two-sided",
        description = "This flag or shader symbol when applied to a material that is applied to a face or surface renders both sides of the surface instead of just the side that the normal is facing",
        default = False,
        )

    transparent_1_sided: BoolProperty(
        name ="One-sided Transparent",
        description = "One-sided but non-manifold collidable geometry",
        default = False,
        )

    transparent_2_sided: BoolProperty(
        name ="Two-sided Transparent",
        description = "Two-sided collidable geometry that is not connected to or touching one-sided geometry",
        default = False,
        )

    render_only: BoolProperty(
        name ="Render Only",
        description = "Non-collidable, Non-solid geometry",
        default = False,
        )

    collision_only: BoolProperty(
        name ="Collision Only",
        description = "Non-rendered geometry",
        default = False,
        )

    sphere_collision_only: BoolProperty(
        name ="Sphere Collision Only",
        description = "Non-rendered geometry that ray tests pass through but spheres (bipeds and vehicles) will not",
        default = False,
        )

    fog_plane: BoolProperty(
        name ="Fog Plane",
        description = "Non-collidable fog plane. This shader symbol when applied to a material that is applied to a face or surface makes the surface not be rendered. The faces acts as a fog plane that can be used to define a volumetric fog region",
        default = False,
        )

    ladder: BoolProperty(
        name ="Ladder",
        description = "Climbable geometry. This flag or shader symbol when applied to a material that is applied to a face or surface sets the surface up to act as a ladder for the player",
        default = False,
        )

    breakable: BoolProperty(
        name ="Breakable",
        description = "Two-sided breakable geometry",
        default = False,
        )

    ai_deafening: BoolProperty(
        name ="AI Deafening",
        description = "A portal that does not propagate sound. This property does not apply to multiplayer levels",
        default = False,
        )

    no_shadow: BoolProperty(
        name ="No Shadow",
        description = "Does not cast real time shadows",
        default = False,
        )

    shadow_only: BoolProperty(
        name ="Shadow Only",
        description = "Casts real time shadows but is not visible",
        default = False,
        )

    lightmap_only: BoolProperty(
        name ="Lightmap Only",
        description = "Emits light in the light mapper but is otherwise non-existent (non-collidable and non-rendered)",
        default = False,
        )

    precise: BoolProperty(
        name ="Precise",
        description = "Points and triangles are precise and will not be fiddled with in the BSP pass",
        default = False,
        )

    conveyor: BoolProperty(
        name ="Conveyor",
        description = "Geometry which will have a surface coordinate system and velocity",
        default = False,
        )

    portal_1_way: BoolProperty(
        name ="Portal (One-Way)",
        description = "Portal can only be seen through in a single direction",
        default = False,
        )

    portal_door: BoolProperty(
        name ="Portal (Door)",
        description = "Portal visibility is attached to a device machine state",
        default = False,
        )

    portal_vis_blocker: BoolProperty(
        name ="Portal (Vis Blocker)",
        description = "Portal visibility is completely blocked by this portal",
        default = False,
        )

    portal_exact: BoolProperty(
        name ="Portal (Exact Portal)",
        description = "Exact Portal property. This flag or shader symbol when applied to a material that is applied to a face or surface makes the surface able to be used to define an exact portal",
        default = False,
        )

    dislike_photons: BoolProperty(
        name ="Dislikes Photons",
        description = "Photons from sky/sun quads will ignore these materials",
        default = False,
        )

    ignored_by_lightmaps: BoolProperty(
        name ="Dislikes Photons",
        description = "Lightmapper will not add this geometry to it's raytracing scene representation",
        default = False,
        )

    blocks_sound: BoolProperty(
        name ="Portal (Sound Blocker)",
        description = "Portal that does not propagate any sound",
        default = False,
        )

    decal_offset: BoolProperty(
        name ="Decal Offset",
        description = "Offsets the faces that this material is applied to as it would normally for a decal",
        default = False,
        )

    water_surface: BoolProperty(
        name ="Water Surface",
        description = "This flag or shader symbol when applied to a material that is applied to a face or surface marks that surface as a water surface",
        default = False,
        )

    slip_surface: BoolProperty(
        name ="Blocks Sound",
        description = "Offsets the faces that this material is applied to as it would normally for a decal",
        default = False,
        )

    group_transparents_by_plane: BoolProperty(
        name ="Group Transparents by Plane",
        description = "This flag or shader symbol when applied to a material that is applied to a face or surface groups the transparent geometry by fitted planes",
        default = False,
        )

    override_lightmap_transparency: BoolProperty(
        name ="Override Lightmap Transparency",
        description = "This flag or shader symbol when applied to a material that is applied to a face or surface overrides the lightmap transparency for that surface",
        default = False,
        )

    ignore_default_res_scale: BoolProperty(
        name ="Ignore Default Resolution Scale",
        description = "This flag or shader symbol when applied to a material that is applied to a face or surface overrides the default lightmap resolution for that surface",
        default = False,
        )

    use_shader_gel: BoolProperty(
        name ="Use Shader Gel",
        description = "I have no idea what this is",
        default = False,
        )

    lightmap_res: FloatProperty(
        name = "Lightmap Resolution",
        description = "Lightmap resolution scale for the material",
        default = 1.0,
        max = 50000.0,
        min = 0.001,
        )

    photon_fidelity: IntProperty(
        name = "Photon Fidelity",
        description = "I have no idea what this is",
        default = 1,
        max = 3,
        min = 0,
        )

    two_sided_transparent_tint: FloatVectorProperty(
        name = "Two-sided Transparent Tint",
        description = "Tint for two-sided transparent meshes",
        subtype = 'COLOR',
        default = (0.0, 0.0, 0.0),
        max = 1.0,
        min = 0.0,
        )

    additive_transparency: FloatVectorProperty(
        name = "Additive Transparency",
        description = "I have no idea what this is",
        subtype = 'COLOR',
        default = (0.0, 0.0, 0.0),
        max = 1.0,
        min = 0.0,
        )

    power: FloatProperty(
        name = "Power",
        description = "Lightmap power for the material",
        default = 0.0,
        max = 1000.0,
        min = 0,
        )

    color: FloatVectorProperty(
        name = "Color",
        description = "Color of the light emitted by the material",
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        max = 1.0,
        min = 0.0,
        )

    quality: FloatProperty(
        name = "Quality",
        description = "Lightmap quality for the material",
        default = 1.0,
        max = 1000.0,
        min = 0.1,
        )

    power_per_unit_area: BoolProperty(
        name ="Power Per Unit Area",
        description = "I have no idea what this is",
        default = False,
        )

    emissive_focus: FloatProperty(
        name = "Emissive Focus",
        description = "I have no idea what this is",
        default = 0.0,
        max = 1.0,
        min = 0.0,
        )

    attenuation_enabled: BoolProperty(
        name ="Attenuation Enabled",
        description = "I have no idea what this is",
        default = False,
        )

    falloff_distance: FloatProperty(
        name = "Falloff Distance",
        description = "I have no idea what this is",
        default = 1000.0,
        max = 100000.0,
        min = 0.0,
        )

    cutoff_distance: FloatProperty(
        name = "Cutoff Distance",
        description = "I have no idea what this is",
        default = 2000.0,
        max = 100000.0,
        min = 0.0,
        )

    frustum_blend: FloatProperty(
        name = "Frustum Blend",
        description = "I have no idea what this is",
        default = 0.0,
        max = 1.0,
        min = 0.0,
        )

    frustum_falloff: FloatProperty(
        name = "Frustum Falloff",
        description = "I have no idea what this is",
        default = 25.0,
        max = 170.0,
        min = 2.0,
        )

    frustum_cutoff: FloatProperty(
        name = "Frustum Cutoff",
        description = "I have no idea what this is",
        default = 45.0,
        max = 170.0,
        min = 2.0,
        )

    is_bm: BoolProperty(
        name = "Halo Material Enabled",
        description = "Enable material flags and settings",
        default = False,
        )

    lightmap_resolution_scale: FloatProperty(
        name = "Lightmap Resolution Scale",
        description = "Lightmap resolution scale for the material",
        default = 0.0,
        min = 0.0,
        )

    lightmap_power_scale: FloatProperty(
        name = "Lightmap Power Scale",
        description = "Lightmap power scale for the material",
        default = 0.0,
        min = 0.0,
        )

    lightmap_half_life: FloatProperty(
        name = "Lightmap Half-Life",
        description = "Lightmap half-Life for the material",
        default = 0.0,
        min = 0.0,
        )

    lightmap_diffuse_scale: FloatProperty(
        name = "Lightmap Diffuse Scale",
        description = "Lightmap diffuse scale for the material",
        default = 0.0,
        min = 0.0,
        )

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
        row = col.row()
        row.label(text='Tag Path:')
        row.prop(ob_ass_jms, "tag_path", text='')
        if ob.name[0:1].lower() == '#':
            row = col.row()
            row.label(text='Mask Type:')
            row.prop(ob_ass_jms, "marker_mask_type", text='')
            if scene_halo.game_title == "halo1":
                row = col.row()
                row.label(text='Region:')
                row.prop(ob_ass_jms, "marker_region", text='')

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

    tag_path: StringProperty(
        name="Tag Path",
        description="Store the tag path here."
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

class Halo_SceneProps(Panel):
    bl_label = "Halo Scene Properties"
    bl_idname = "HALO_PT_ScenePropertiesPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

class Halo_GlobalSettings(Panel):
    bl_label = "Global Settings"
    bl_idname = "HALO_PT_GlobalSettings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo = scene.halo

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Scene Game Title:')
        row.prop(scene_halo, "game_title", text='')
        row = col.row()
        row.label(text='Expert Mode:')
        row.prop(scene_halo, "expert_mode", text='')

class Halo_ScenePropertiesGroup(PropertyGroup):
    game_title: EnumProperty(
        name="Game:",
        description="What game will you be exporting for",
        items=[ ('halo1', "Halo 1", "Show properties for Halo Custom Edition Or Halo CE MCC"),
                ('halo2', "Halo 2", "Show properties for Halo 2 Vista or Halo 2 MCC"),
                ('halo3', "Halo 3", "Show properties for Halo 3 MCC"),
               ]
        )

    expert_mode: BoolProperty(
        name ="Expert Mode",
        description = "Reveal hidden options. If you're not a developer or know what you're doing then you probably shouldn't be messing with this.",
        default = False,
        )

class ASS_LightPropertiesGroup(PropertyGroup):
    use_near_atten: BoolProperty(
        name = "Near Attenuation",
        description = "No idea",
        default = False,
        )

    near_atten_start: FloatProperty(
        name = "Near Attenuation Start",
        description = "No idea",
        default = 0.0,
        max = 999999.0,
        min = 0.0,
        )

    near_atten_end: FloatProperty(
        name = "Near Attenuation End",
        description = "No idea",
        default = 40.0,
        max = 999999.0,
        min = 0.0,
        )

    use_far_atten: BoolProperty(
        name = "Near Attenuation",
        description = "No idea",
        default = False,
        )

    far_atten_start: FloatProperty(
        name = "Far Attenuation Start",
        description = "No idea",
        default = 80.0,
        max = 999999.0,
        min = 0.0,
        )

    far_atten_end: FloatProperty(
        name = "Far Attenuation End",
        description = "No idea",
        default = 200.0,
        max = 999999.0,
        min = 0.0,
        )

    light_cone_shape : EnumProperty(
        name="Light Cone Shape",
        description="What shape to use for the light cone",
        default = "0",
        items=[ ('0', "Rectangle", "Rectangle"),
                ('1', "Circle", "Circle"),
               ]
        )

    aspect_ratio: FloatProperty(
        name = "Aspect Ratio",
        description = "No idea. Only used if the light cone is a rectangle.",
        default = 1.0,
        max = 100.0,
        min = 0.001,
        )

    spot_size: FloatProperty(
        name="Spot Size",
        description="Angle of the spotlight beam",
        subtype='ANGLE',
        default=0.785398,
        min=0.017453,
        max=3.141593,
        )

    spot_blend: FloatProperty(
        name = "Spot Blend",
        description = "The softness of the spotlight edge",
        precision = 3,
        default = 0.150,
        max = 1.0,
        min = 0.0,
        )

class ASS_LightProps(Panel):
    bl_label = "ASS Light Properties"
    bl_idname = "ASS_PT_LightPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "DATA_PT_EEVEE_light"
    COMPAT_ENGINES = {'BLENDER_EEVEE'}

    @classmethod
    def poll(cls, context):
        light = context.light
        engine = context.engine

        return (light and (light.type == 'SPOT' or light.type == 'AREA')) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        light = context.light
        light_ass = light.halo_light

        layout = self.layout

        row = layout.row()
        row.label(text='Light Cone Shape:')
        row.prop(light_ass, "light_cone_shape", text='')
        row = layout.row()
        row.label(text='Aspect Ratio:')
        row.prop(light_ass, "aspect_ratio", text='')

class ASS_LightSpot(Panel):
    bl_label = "Spot Shape"
    bl_idname = "ASS_PT_SpotShapePanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "ASS_PT_LightPanel"

    def draw(self, context):
        light = context.light
        light_ass = light.halo_light

        layout = self.layout

        row = layout.row()
        row.label(text='Size:')
        row.prop(light_ass, "spot_size", text='')
        row = layout.row()
        row.label(text='Blend:')
        row.prop(light_ass, "spot_blend", text='', slider=True)

class ASS_LightNearAtten(Panel):
    bl_label = "Near Attenuation"
    bl_idname = "ASS_PT_NearAttenuationPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "ASS_PT_LightPanel"

    def draw_header(self, context):
        light = context.light
        light_ass = light.halo_light

        self.layout.prop(light_ass, "use_near_atten", text='')

    def draw(self, context):
        light = context.light
        light_ass = light.halo_light

        layout = self.layout

        if not light_ass.use_near_atten:
            layout.enabled = False

        row = layout.row()
        row.label(text='Start:')
        row.prop(light_ass, "near_atten_start", text='')
        row = layout.row()
        row.label(text='End:')
        row.prop(light_ass, "near_atten_end", text='')

class ASS_LightFarAtten(Panel):
    bl_label = "Far Attenuation"
    bl_idname = "ASS_PT_FarAttenuationPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "ASS_PT_LightPanel"

    def draw_header(self, context):
        light = context.light
        light_ass = light.halo_light

        self.layout.prop(light_ass, "use_far_atten", text='')

    def draw(self, context):
        light = context.light
        light_ass = light.halo_light

        layout = self.layout

        if not light_ass.use_far_atten:
            layout.enabled = False

        row = layout.row()
        row.label(text='Start:')
        row.prop(light_ass, "far_atten_start", text='')
        row = layout.row()
        row.label(text='End:')
        row.prop(light_ass, "far_atten_end", text='')

class Halo_SurfaceFlags(Panel):
    """Set settings for surface to be used in the Halo maze generator"""
    bl_label = "Halo Surface Flags"
    bl_idname = "OBJECT_PT_halo_surface_flags"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    ebm = dict()

    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            me = context.edit_object.data

            cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
            return True

        cls.ebm.clear()
        return False

    def draw(self, context):
        layout = self.layout
        me = context.edit_object.data

        row = layout.row()
        row.label(text="Valid Surface:")
        row.prop(me, "halo_valid_surface", text='')
        row = layout.row()
        row.label(text="Valid Character Flags:")
        row.prop(me, "halo_valid_characters", text='')

        box = layout.split()
        col = box.column(align=True)
        row = col.row()

        row = col.row()
        row.label(text='Marine:')
        row.prop(me, "halo_marine", text='')
        row = col.row()
        row.label(text='Elite:')
        row.prop(me, "halo_elite", text='')
        row = col.row()
        row.label(text='Grunt:')
        row.prop(me, "halo_grunt", text='')
        row = col.row()
        row.label(text='Hunter:')
        row.prop(me, "halo_hunter", text='')
        row = col.row()
        row.label(text='Jackal:')
        row.prop(me, "halo_jackal", text='')
        row = col.row()
        row.label(text='Floodcarrier:')
        row.prop(me, "halo_floodcarrier", text='')
        col = box.column()
        row = col.row()
        row.label(text='Floodcombat Elite:')
        row.prop(me, "halo_floodcombat_elite", text='')
        row = col.row()
        row.label(text='Floodcombat Human:')
        row.prop(me, "halo_floodcombat_human", text='')
        row = col.row()
        row.label(text='Flood Infection:')
        row.prop(me, "halo_flood_infection", text='')
        row = col.row()
        row.label(text='Sentinel:')
        row.prop(me, "halo_sentinel", text='')
        row = col.row()
        row.label(text='Drinol:')
        row.prop(me, "halo_drinol", text='')
        row = col.row()
        row.label(text='Slug Man:')
        row.prop(me, "halo_slug_man", text='')

def set_surface_usage(self, value):
    hvs = self.attributes.get("Halo Valid Surface")
    if hvs is None:
        self.attributes.new(name="Halo Valid Surface", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Surface")

    af = bm.faces.active
    if af and surface_layer:
        af[surface_layer] = value
        bmesh.update_edit_mesh(self)

def get_surface_usage(self):
    hvs = self.attributes.get("Halo Valid Surface")
    if hvs is None:
        self.attributes.new(name="Halo Valid Surface", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Surface")

    af = bm.faces.active
    if af and surface_layer:
        is_valid = af[surface_layer]

    return is_valid

def set_character_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        af[surface_layer] = value
        bmesh.update_edit_mesh(self)

def get_character_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        is_valid = af[surface_layer]

    return is_valid

class CharacterFlags(Flag):
    marine = auto()
    elite = auto()
    grunt = auto()
    hunter = auto()
    jackal = auto()
    floodcarrier = auto()
    floodcombat_elite = auto()
    floodcombat_human = auto()
    flood_infection = auto()
    sentinel = auto()
    drinol = auto()
    slug_man = auto()

def set_marine_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.marine.value
        else:
            af[surface_layer] -= CharacterFlags.marine.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_marine_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.marine in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_elite_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.elite.value
        else:
            af[surface_layer] -= CharacterFlags.elite.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_elite_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.elite in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_grunt_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.grunt.value
        else:
            af[surface_layer] -= CharacterFlags.grunt.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_grunt_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.grunt in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_hunter_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.hunter.value
        else:
            af[surface_layer] -= CharacterFlags.hunter.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_hunter_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.hunter in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_jackal_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.jackal.value
        else:
            af[surface_layer] -= CharacterFlags.jackal.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_jackal_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.jackal in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_floodcarrier_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.floodcarrier.value
        else:
            af[surface_layer] -= CharacterFlags.floodcarrier.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_floodcarrier_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.floodcarrier in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_floodcombat_elite_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.floodcombat_elite.value
        else:
            af[surface_layer] -= CharacterFlags.floodcombat_elite.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_floodcombat_elite_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.floodcombat_elite in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_floodcombat_human_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.floodcombat_human.value
        else:
            af[surface_layer] -= CharacterFlags.floodcombat_human.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_floodcombat_human_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.floodcombat_human in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_flood_infection_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.flood_infection.value
        else:
            af[surface_layer] -= CharacterFlags.flood_infection.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_flood_infection_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.flood_infection in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_sentinel_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.sentinel.value
        else:
            af[surface_layer] -= CharacterFlags.sentinel.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_sentinel_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.sentinel in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_drinol_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.drinol.value
        else:
            af[surface_layer] -= CharacterFlags.drinol.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_drinol_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.drinol in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_slug_man_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.slug_man.value
        else:
            af[surface_layer] -= CharacterFlags.slug_man.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_slug_man_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.slug_man in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def get_custom_attribute(self, attribute_name="Region Assignment"):
    region_attribute = self.attributes.get(attribute_name)
    if region_attribute == None:
        region_attribute = self.attributes.new(name=attribute_name, type="INT", domain="FACE")

    return region_attribute

def get_unique_name(region_list, name):
    formatted_name = name
    region_name_dic = {}
    region_set = set(region_list)
    for region in region_set:
        region_name_dic[region] = region_list.count(region)

    if region_name_dic[name] > 1:
        increment_count = 1
        while not region_name_dic.get(formatted_name) == None:
            formatted_name = "{0}.{1:003}".format(name, increment_count)
            increment_count += 1

    return formatted_name

def update_region_prop(self, context):
    scene = context.scene
    if len(scene.active_region_list) > 1:
        self["name"] = get_unique_name(scene.active_region_list, self.name)

def region_add(self, name="unnamed"):
    scene = bpy.context.scene
    scene.active_region_list.clear()
    for region in self.region_list:
        scene.active_region_list.append(region.name)

    scene.active_region_list.append(name)

    region = self.region_list.add()
    region.name = name
    self.active_region = 0

class RegionItem(PropertyGroup):
    name: StringProperty(
           name="Name",
           description="A name for this item",
           default="unnamed",
           update=update_region_prop
           )

class REGION_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon='FACE_MAPS')

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class Halo_OT_RegionAdd(Operator):
    """Add a new region to the active object"""
    bl_idname = "region_list.region_add"
    bl_label = "Add region"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH":
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object

        ob.region_add()
        ob.data.get_custom_attribute()
        ob.active_region = len(ob.region_list) - 1

        return{'FINISHED'}

class Halo_OT_RegionRemove(Operator):
    """Remove a region from the active object"""
    bl_idname = "region_list.region_remove"
    bl_label = "Remove a region"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and len(active_object.region_list) > 0:
            valid = True

        return valid

    def execute(self, context):
        ob = context.object
        data = ob.data

        region_list = ob.region_list
        active_region = ob.active_region
        data_region_value = active_region + 1

        modified_indices = list(range(active_region, len(ob.region_list)))
        for idx, index in enumerate(modified_indices):
            modified_indices[idx] += 1

        del modified_indices[0]

        region_attribute = ob.data.get_custom_attribute()
        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(data)

            surface_layer = bm.faces.layers.int.get("Region Assignment")
            for face in bm.faces:
                face_value = face[surface_layer]
                if face_value == data_region_value:
                    face[surface_layer] = -1
                elif face_value in modified_indices:
                    face[surface_layer] += -1

            bmesh.update_edit_mesh(data)

        else:
            for face in data.polygons:
                face_value = region_attribute.data[face.index].value
                if face_value == data_region_value:
                    region_attribute.data[face.index].value = -1
                elif face_value in modified_indices:
                    region_attribute.data[face.index].value += -1

        region_list.remove(active_region)
        ob.active_region = min(max(0, active_region), len(region_list) - 1)

        return{'FINISHED'}

class Halo_OT_RegionMove(Operator):
    """Move the active region up/down in the list"""
    bl_idname = "region_list.region_move"
    bl_label = "Move region"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""), ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and len(context.active_object.region_list) > 0:
            valid = True

        return valid

    def move_attribute_index(self, context, neighbor, active_region):
        ob = context.object
        data = ob.data

        neighbor += 1
        active_region += 1

        region_attribute = ob.data.get_custom_attribute()
        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(data)

            surface_layer = bm.faces.layers.int.get("Region Assignment")
            for face in bm.faces:
                if face[surface_layer] == neighbor:
                    face[surface_layer] = active_region
                elif face[surface_layer] == active_region:
                    face[surface_layer] = neighbor

            bmesh.update_edit_mesh(data)

        else:
            for face in data.polygons:
                if region_attribute.data[face.index].value == neighbor:
                    region_attribute.data[face.index].value = active_region
                elif region_attribute.data[face.index].value == active_region:
                    region_attribute.data[face.index].value = neighbor

    def move_index(self, ob):
        active_region = ob.active_region
        list_length = len(ob.region_list) - 1
        new_index = active_region + (-1 if self.direction == 'UP' else 1)

        ob.active_region = max(0, min(new_index, list_length))

    def execute(self, context):
        ob = context.object

        region_list = ob.region_list
        active_region = ob.active_region

        neighbor = active_region + (-1 if self.direction == 'UP' else 1)
        self.move_attribute_index(context, neighbor, active_region)
        region_list.move(neighbor, active_region)
        self.move_index(ob)

        return{'FINISHED'}

class Halo_OT_RegionAssign(Operator):
    """Assign faces to a region"""
    bl_idname = "region_list.region_assign"
    bl_label = "Region Assign"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object
        data = ob.data
        active_region = ob.active_region + 1

        ob.data.get_custom_attribute()

        bm = bmesh.from_edit_mesh(data)

        surface_layer = bm.faces.layers.int.get("Region Assignment")
        for face in bm.faces:
            if face.select:
                face[surface_layer] = active_region

        bmesh.update_edit_mesh(data)

        return{'FINISHED'}

class Halo_OT_RegionRemoveFrom(Operator):
    """Remove faces from a region"""
    bl_idname = "region_list.region_remove_from"
    bl_label = "Region Remove From"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object
        data = ob.data
        active_region = ob.active_region + 1

        ob.data.get_custom_attribute()

        bm = bmesh.from_edit_mesh(data)

        surface_layer = bm.faces.layers.int.get("Region Assignment")
        for face in bm.faces:
            if face.select and face[surface_layer] == active_region:
                face[surface_layer] = -1

        bmesh.update_edit_mesh(data)

        return{'FINISHED'}

class Halo_OT_RegionSelect(Operator):
    """Select faces beloging to a region"""
    bl_idname = "region_list.region_select"
    bl_label = "Region Select"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object
        data = ob.data
        active_region = ob.active_region + 1

        ob.data.get_custom_attribute()

        bm = bmesh.from_edit_mesh(data)

        surface_layer = bm.faces.layers.int.get("Region Assignment")
        for face in bm.faces:
            if face[surface_layer] == active_region:
                face.select = True

        bmesh.update_edit_mesh(data)

        return{'FINISHED'}

class Halo_OT_RegionDeselect(Operator):
    """Deselect faces beloging to a region"""
    bl_idname = "region_list.region_deselect"
    bl_label = "Region Deselect"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object
        data = ob.data
        active_region = ob.active_region + 1

        ob.data.get_custom_attribute()

        bm = bmesh.from_edit_mesh(data)

        surface_layer = bm.faces.layers.int.get("Region Assignment")
        for face in bm.faces:
            if face[surface_layer] == active_region:
                face.select = False

        bmesh.update_edit_mesh(data)

        return{'FINISHED'}

class Halo_OT_RegionRemoveUnused(Operator):
    """Removes all unused regions from the active object"""
    bl_idname = "region_list.region_remove_unused"
    bl_label = "Remove unused regions"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and len(active_object.region_list) > 0:
            valid = True

        return valid

    def execute(self, context):
        ob = context.object
        data = ob.data

        region_list = ob.region_list
        active_region = ob.active_region
        data_region_value = active_region + 1
        region_attribute = ob.data.get_custom_attribute()
        index_set = set()
        unused_indices = set()
        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(data)

            surface_layer = bm.faces.layers.int.get("Region Assignment")
            for face in bm.faces:
                if not face[surface_layer] == 0:
                    index_set.add(face[surface_layer] - 1)

            bmesh.update_edit_mesh(data)

        else:
            for face in data.polygons:
                if not region_attribute.data[face.index].value == 0:
                    index_set.add(region_attribute.data[face.index].value - 1)

        for region_idx, region in enumerate(region_list):
            if not region_idx in index_set:
                unused_indices.add(region_idx)

        for region_index in reversed(sorted(unused_indices)):
            modified_indices = list(range(region_index, len(ob.region_list)))
            for idx, index in enumerate(modified_indices):
                modified_indices[idx] += 1

            del modified_indices[0]

            if context.mode == 'EDIT_MESH':
                bm = bmesh.from_edit_mesh(data)

                surface_layer = bm.faces.layers.int.get("Region Assignment")
                for face in bm.faces:
                    face_value = face[surface_layer]
                    if face_value in modified_indices:
                        face[surface_layer] += -1

                bmesh.update_edit_mesh(data)

            else:
                for face in data.polygons:
                    face_value = region_attribute.data[face.index].value
                    if face_value in modified_indices:
                        region_attribute.data[face.index].value += -1

            region_list.remove(region_index)
            ob.active_region = min(max(0, active_region), len(region_list) - 1)

        return{'FINISHED'}

class REGION_MT_context_menu(Menu):
    bl_label = "Region Specials"

    def draw(self, _context):
        layout = self.layout

        layout.operator("region_list.region_remove_unused")

class Halo_RegionsPanel(Panel):
    bl_label = "Halo Regions"
    bl_idname = "OBJECT_PT_halo_regions"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH":
            valid = True

        return valid

    def draw(self, context):
        layout = self.layout
        ob = context.object
        data = ob.data
        region_count = len(ob.region_list)

        scene = context.scene
        if ob and ob.type == "MESH":
            scene.active_region_list.clear()
            for region in ob.region_list:
                scene.active_region_list.append(region.name)

        row = layout.row()
        row.template_list("REGION_UL_List", "Region_List", ob, "region_list", ob, "active_region")

        col = row.column(align=True)
        col.operator("region_list.region_add", icon='ADD', text="")
        col.operator("region_list.region_remove", icon='REMOVE', text="")

        if region_count >= 2:
            col.separator()
            col.operator("region_list.region_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("region_list.region_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        col.separator()
        col.menu("REGION_MT_context_menu", icon='DOWNARROW_HLT', text="")
        if region_count >= 1:
            if ob.mode == 'EDIT' and ob.type == 'MESH':
                row = layout.row()

                sub = row.row(align=True)
                sub.operator("region_list.region_assign", text="Assign")
                sub.operator("region_list.region_remove_from", text="Remove")

                sub = row.row(align=True)
                sub.operator("region_list.region_select", text="Select")
                sub.operator("region_list.region_deselect", text="Deselect")

classeshalo = (
    Halo_SurfaceFlags,
    ASS_JMS_ObjectPropertiesGroup,
    ASS_JMS_MeshPropertiesGroup,
    ASS_JMS_MaterialPropertiesGroup,
    Halo_ObjectProps,
    Halo_BoneProps,
    Halo_MeshProps,
    ASS_LightPropertiesGroup,
    ASS_LightProps,
    ASS_LightSpot,
    ASS_LightNearAtten,
    ASS_LightFarAtten,
    ASS_JMS_MaterialProps,
    ASS_JMS_MaterialFlagsProps,
    ASS_JMS_MaterialLightmapProps,
    ASS_JMS_MaterialBasicProps,
    ASS_JMS_MaterialAttenuationProps,
    ASS_JMS_MaterialFrustumProps,
    Halo_ScenePropertiesGroup,
    Halo_SceneProps,
    Halo_GlobalSettings,
    Halo_XREFPath,
    Halo_RegionsPanel,
    Halo_OT_RegionMove,
    Halo_OT_RegionRemove,
    Halo_OT_RegionAdd,
    REGION_UL_List,
    RegionItem,
    Halo_OT_RegionAssign,
    Halo_OT_RegionRemoveFrom,
    Halo_OT_RegionSelect,
    Halo_OT_RegionDeselect,
    Halo_OT_RegionRemoveUnused,
    REGION_MT_context_menu
    )

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.Light.halo_light = PointerProperty(type=ASS_LightPropertiesGroup, name="ASS Properties", description="Set properties for your light")
    bpy.types.Object.ass_jms = PointerProperty(type=ASS_JMS_ObjectPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your object")
    bpy.types.Armature.ass_jms = PointerProperty(type=ASS_JMS_ObjectPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your object")
    bpy.types.Bone.ass_jms = PointerProperty(type=ASS_JMS_ObjectPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your Bone")
    bpy.types.Mesh.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.Material.ass_jms = PointerProperty(type=ASS_JMS_MaterialPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your materials")
    bpy.types.Scene.halo = PointerProperty(type=Halo_ScenePropertiesGroup, name="Halo Scene Properties", description="Set properties for your scene")
    bpy.types.Mesh.halo_valid_surface = BoolProperty(name="Valid Surface", get=get_surface_usage, set=set_surface_usage)
    bpy.types.Mesh.halo_valid_characters = IntProperty(name="Valid Characters Flag", get=get_character_usage, set=set_character_usage)
    bpy.types.Mesh.halo_marine = BoolProperty(name="Marine", get=get_marine_usage, set=set_marine_usage)
    bpy.types.Mesh.halo_elite = BoolProperty(name="Elite", get=get_elite_usage, set=set_elite_usage)
    bpy.types.Mesh.halo_grunt = BoolProperty(name="Grunt", get=get_grunt_usage, set=set_grunt_usage)
    bpy.types.Mesh.halo_hunter = BoolProperty(name="Hunter", get=get_hunter_usage, set=set_hunter_usage)
    bpy.types.Mesh.halo_jackal = BoolProperty(name="Jackal", get=get_jackal_usage, set=set_jackal_usage)
    bpy.types.Mesh.halo_floodcarrier = BoolProperty(name="Flood Carrier", get=get_floodcarrier_usage, set=set_floodcarrier_usage)
    bpy.types.Mesh.halo_floodcombat_elite = BoolProperty(name="Floodcombat Elite", get=get_floodcombat_elite_usage, set=set_floodcombat_elite_usage)
    bpy.types.Mesh.halo_floodcombat_human = BoolProperty(name="Floodcombat Human", get=get_floodcombat_human_usage, set=set_floodcombat_human_usage)
    bpy.types.Mesh.halo_flood_infection = BoolProperty(name="Flood Infection", get=get_flood_infection_usage, set=set_flood_infection_usage)
    bpy.types.Mesh.halo_sentinel = BoolProperty(name="Sentinel", get=get_sentinel_usage, set=set_sentinel_usage)
    bpy.types.Mesh.halo_drinol = BoolProperty(name="Drinol", get=get_drinol_usage, set=set_drinol_usage)
    bpy.types.Mesh.halo_slug_man = BoolProperty(name="Slug Man", get=get_slug_man_usage, set=set_slug_man_usage)
    bpy.types.Object.region_list = CollectionProperty(type = RegionItem)
    bpy.types.Object.active_region = IntProperty(name = "Active region index", description="Active index in the region array", default = -1)
    bpy.types.Scene.active_region_list = []
    bpy.types.Object.region_add = region_add
    bpy.types.Mesh.get_custom_attribute = get_custom_attribute

def unregister():
    del bpy.types.Light.halo_light
    del bpy.types.Object.ass_jms
    del bpy.types.Armature.ass_jms
    del bpy.types.Mesh.ass_jms
    del bpy.types.Material.ass_jms
    del bpy.types.Scene.halo
    del bpy.types.Object.region_list
    del bpy.types.Object.active_region
    del bpy.types.Scene.active_region_list
    del bpy.types.Object.region_add
    del bpy.types.Mesh.get_custom_attribute
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
