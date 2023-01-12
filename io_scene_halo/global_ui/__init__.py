# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2021 Steven Garcia
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

from itertools import permutations
import bpy

from bpy.types import (
        Operator,
        Panel,
        PropertyGroup
        )

from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        PointerProperty,
        FloatVectorProperty,
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
        scene = context.scene
        scene_halo = scene.halo
        if scene_halo.game_version == 'haloce' or scene_halo.game_version == 'halo2' or scene_halo.game_version == 'halo3':
            mat = context.material
        else:
            mat = False
        return mat

    def draw_header(self, context):
        current_material = context.object.active_material
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            self.layout.prop(material_ass_jms, "is_bm", text='')

    def draw(self, context):
        layout = self.layout
        current_material = context.object.active_material
        scene = context.scene
        scene_halo = scene.halo
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            layout.enabled = material_ass_jms.is_bm
            row = layout.row()
            if scene_halo.game_version == 'halo2' or scene_halo.game_version == 'halo3':
                row.label(text="Name Override:")
                row.prop(material_ass_jms, "name_override", text='')

            if scene_halo.game_version == 'halo2' or scene_halo.game_version == 'halo3':
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

    @classmethod
    def poll(self, context):  # Added poll here to that flags aren't drawn for Reach exports
        scene = context.scene
        scene_halo = scene.halo
        if scene_halo.game_version == 'haloce' or scene_halo.game_version == 'halo2' or scene_halo.game_version == 'halo3':
            return True

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

            if scene_halo.game_version == 'haloce':
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

            if scene_halo.game_version == 'halo2':
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

            if scene_halo.game_version == 'halo3':
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
        if scene_halo.game_version == 'halo2' or scene_halo.game_version == 'halo3':
            return True

    def draw(self, context):
        layout = self.layout
        current_material = context.object.active_material
        scene = context.scene
        scene_halo = scene.halo
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            layout.enabled = material_ass_jms.is_bm
            if scene_halo.game_version == 'halo2':
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

        if scene_halo.game_version == 'halo3':
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
    def poll(cls, context):
        scene = context.scene
        scene_halo = scene.halo

        obj = context.object
        mesh = obj.data

        show_panel = None
        if scene_halo.game_version == 'haloce' or scene_halo.game_version == 'halo2' or scene_halo.game_version == 'halo3':
            if hasattr(obj, 'marker') and obj.name[0:1].lower() == '#' or hasattr(mesh, 'ass_jms') and not scene_halo.game_version == 'haloce' or hasattr(obj, 'jmi') and obj.name[0:1].lower() == '!' and scene_halo.game_version == 'haloce':
                show_panel = True

            return show_panel

    def draw(self, context):
        layout = self.layout

class ASS_JMS_MeshProps(Panel):
    bl_label = "ASS/JMS Properties"
    bl_idname = "ASS_JMS_PT_DetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "HALO_PT_MeshDetailsPanel"

    @classmethod
    def poll(self, context):
        scene = context.scene
        scene_halo = scene.halo

        mesh = context.object.data

        ass_jms = None
        if hasattr(mesh, 'ass_jms') and not scene_halo.game_version == 'haloce':
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
        row.label(text='Scene Version:')
        row.prop(scene_halo, "game_version", text='')
        row = col.row()
        row.label(text='Expert Mode:')
        row.prop(scene_halo, "expert_mode", text='')
        row = col.row()
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        col = flow.column()
        col = col.row()
        col.scale_y = 1.5
        col.operator("halo.set_unit_scale")

class Halo_SetUnitScale(Operator):
    """Sets the scene unit scale to match Halo's scale"""
    bl_idname = 'halo.set_unit_scale'
    bl_label = 'Set Halo Unit Scale'
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # set the Halo scale
        context.scene.unit_settings.scale_length = 0.03048
        return {'FINISHED'}

def GameVersionWarning(self, context):
    self.layout.label(text=f"Please set your editing kit path for {context.scene.halo.game_version.upper()} in add-on preferences [Edit > Preferences > Add-ons > Halo Asset Blender Development Toolset]")

class Halo_ScenePropertiesGroup(PropertyGroup):

    def CheckEKPaths(self, context):
        if self.game_version in ('reach', 'h4', 'h2a'):
            if get_ek_path() is None or get_ek_path() == '':
                context.window_manager.popup_menu(GameVersionWarning, title="Warning", icon='ERROR')
                
    game_version: EnumProperty(
        name="Game:",
        description="What game will you be exporting for",
        update=CheckEKPaths,
        items=[ ('haloce', "Halo CE", "Show properties for Halo Custom Edition Or Halo CE MCC"),
                ('halo2', "Halo 2", "Show properties for Halo 2 Vista or Halo 2 MCC"),
                ('halo3', "Halo 3", "Show properties for Halo 3 MCC"),
                ('reach', "Halo Reach", "Show properties for Halo Reach MCC"),
                ('h4', "Halo 4", "Show properties for Halo 4 MCC"),
                ('h2a', "Halo 2A MP", "Show properties for Halo 2A MP MCC"),
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
        scene = context.scene
        scene_halo = scene.halo
        light = context.light
        engine = context.engine
        if scene_halo.game_version == 'haloce' or scene_halo.game_version == 'halo2' or scene_halo.game_version == 'halo3':
            return (light and (light.type == 'SPOT' or light.type == 'AREA')) and (engine in cls.COMPAT_ENGINES)
        else:
            return False

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

##################################################################################################################
####################################### NWO PROPERTIES ##########################################################
##################################################################################################################

# ----- OBJECT PROPERTIES -------
# -------------------------------
from ..file_gr2.nwo_utils import (
    frame_prefixes,
    marker_prefixes,
    special_prefixes,
    boundary_surface_prefixes,
    poop_lighting_prefixes,
    poop_pathfinding_prefixes,
    poop_render_only_prefixes,
    object_prefix,
    invalid_mesh_types,
    get_prop_from_collection,
    is_design,
    get_ek_path,
    not_bungie_game,
    clean_tag_path,
    get_tags_path,

    CheckType
)

class NWO_GameInstancePath(Operator):
    """Set the path for the a game instance tag"""
    bl_idname = "nwo.game_instance_path"
    bl_label = "Find"
    filename_ext = ''

    filter_glob: StringProperty(
        default="*.biped;*.crate;*.creature;*.device_control;*.device_dispenser;*.device_machine;*.device_terminal;*.effect_scenery;*.equipment;*.giant;*.scenery;*.vehicle;*.weapon;*.prefab;*.cheap_light;*.light",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        name="game_instance_path",
        description="Set the path for the tag",
        subtype="FILE_PATH"
    )

    def execute(self, context):
        active_object = context.active_object
        active_object.nwo.Marker_Game_Instance_Tag_Name = self.filepath

        return {'FINISHED'}

    def invoke(self, context, event):
        self.filepath = get_tags_path()
        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}

class NWO_ObjectProps(Panel):
    bl_label = "Halo Object Properties"
    bl_idname = "NWO_PT_ObjectDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_halo = scene.halo

        return scene_halo.game_version in ('reach','h4','h2a') and context.object.type != 'ARMATURE'
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        
        ob = context.object
        ob_nwo = ob.nwo

        col = flow.column()

        if ob.type == 'LIGHT':
            col.prop(ob_nwo, "Object_Type_Light", text='Object Type')
        elif object_prefix(context.active_object, special_prefixes):
            if context.active_object.type == 'EMPTY':
                col.prop(ob_nwo, "Object_Type_No_Mesh_Locked", text='Object Type')
            else:
                col.prop(ob_nwo, "Object_Type_All_Locked", text='Object Type')
        else:
            if context.active_object.type == 'EMPTY':
                col.prop(ob_nwo, "Object_Type_No_Mesh", text='Object Type')
            else:
                col.prop(ob_nwo, "Object_Type_All", text='Object Type')

        sub = col.row()
        if is_design(ob):
            if ob_nwo.bsp_name_locked != '':
                sub.prop(ob_nwo, 'bsp_name_locked', text='Design Group')
            else:
                sub.prop(ob_nwo, 'bsp_name', text='Design Group')
        else:
            if ob_nwo.bsp_name_locked != '':
                sub.prop(ob_nwo, 'bsp_name_locked', text='BSP')
            else:
                sub.prop(ob_nwo, 'bsp_name', text='BSP')

        if ob_nwo.Permutation_Name_Locked != '':
            col.prop(ob_nwo, 'Permutation_Name_Locked', text='Permutation')
        else:
            col.prop(ob_nwo, 'Permutation_Name', text='Permutation')

        if CheckType.frame(ob) and not_bungie_game():
            col.prop(ob_nwo, 'is_pca')

#MESH PROPERTIES
class NWO_ObjectMeshProps(Panel):
    bl_label = "Mesh Properties"
    bl_idname = "NWO_PT_MeshDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_parent_id = "NWO_PT_ObjectDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.object

        return CheckType.mesh(ob)


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.active_object
        ob_nwo = ob.nwo

        col = flow.column()

        if not_bungie_game():
            if object_prefix(context.active_object, special_prefixes):
                col.prop(ob_nwo, "ObjectMesh_Type_Locked_H4", text='Mesh Type')
            else:
                col.prop(ob_nwo, "ObjectMesh_Type_H4", text='Mesh Type')
        else:
            if object_prefix(context.active_object, special_prefixes):
                col.prop(ob_nwo, "ObjectMesh_Type_Locked", text='Mesh Type')
            else:
                col.prop(ob_nwo, "ObjectMesh_Type", text='Mesh Type')

        if CheckType.boundary_surface(ob):
            if ob.name.startswith(boundary_surface_prefixes):
                col.prop(ob_nwo, "Boundary_Surface_Type_Locked", text='Type')
            else:
                    col.prop(ob_nwo, "Boundary_Surface_Type", text='Type')

        elif CheckType.collision(ob) and not_bungie_game():
            col.prop(ob_nwo, "Poop_Collision_Type")

        elif CheckType.decorator(ob):
            col.prop(ob_nwo, "Decorator_Name", text='Decorator Name')
            col.prop(ob_nwo, "Decorator_LOD", text='Decorator Level of Detail')
        elif CheckType.poop(ob):
            if not_bungie_game():
                col.prop(ob_nwo, "Poop_Collision_Type")

            if ob.name.startswith(poop_lighting_prefixes):
                col.prop(ob_nwo, "Poop_Lighting_Override_Locked", text='Lighting Policy')
            else:
                col.prop(ob_nwo, "Poop_Lighting_Override", text='Lighting Policy')
            
            if not_bungie_game():
                col.prop(ob_nwo, "poop_lightmap_resolution_scale")
                
            if ob.name.startswith(poop_pathfinding_prefixes):
                col.prop(ob_nwo, "Poop_Pathfinding_Override_Locked", text='Pathfinding Policy')
            else:
                col.prop(ob_nwo, "Poop_Pathfinding_Override", text='Pathfinding Policy')

            col.prop(ob_nwo, "Poop_Imposter_Policy", text='Imposter Policy')
            if ob_nwo.Poop_Imposter_Policy != '_connected_poop_instance_imposter_policy_never':
                sub = col.row(heading="Imposter Transition")
                sub.prop(ob_nwo, 'Poop_Imposter_Transition_Distance_Auto', text='Automatic')
                if not ob_nwo.Poop_Imposter_Transition_Distance_Auto:
                    sub.prop(ob_nwo, 'Poop_Imposter_Transition_Distance', text='Distance')
                if not_bungie_game():
                    col.prop(ob_nwo, 'poop_imposter_brightness')
                # col.prop(ob_nwo, "Poop_Imposter_Fade_Range_Start", text='Fade In Start')
                # col.prop(ob_nwo, "Poop_Imposter_Fade_Range_End", text='Fade In End')
            #col.prop(ob_nwo, "Poop_Decomposition_Hulls", text='Decomposition Hulls') commented out so it can be set automatically. 

            # col.separator()

            # col.prop(ob_nwo, "Poop_Predominant_Shader_Name", text='Predominant Shader Name')

            if not_bungie_game():
                col.prop(ob_nwo, 'poop_streaming_priority')
                col.prop(ob_nwo, 'poop_cinematic_properties')

            col.separator()

            col = layout.column(heading="Flags")
            sub = col.column(align=True)

            if ob.name.startswith(poop_render_only_prefixes):
                sub.prop(ob_nwo, "Poop_Render_Only_Locked", text='Render Only')
            else:
                sub.prop(ob_nwo, "Poop_Render_Only", text='Render Only')

            sub.prop(ob_nwo, "Poop_Chops_Portals", text='Chops Portals')
            sub.prop(ob_nwo, "Poop_Does_Not_Block_AOE", text='Does Not Block AOE')
            sub.prop(ob_nwo, "Poop_Excluded_From_Lightprobe", text='Excluded From Lightprobe')
            sub.prop(ob_nwo, "Poop_Decal_Spacing", text='Decal Spacing')
            if not_bungie_game():
                sub.prop(ob_nwo, "poop_remove_from_shadow_geometry")
                sub.prop(ob_nwo, "poop_disallow_lighting_samples",)
                sub.prop(ob_nwo, "poop_rain_occluder")

        elif CheckType.portal(ob):
            col.prop(ob_nwo, "Portal_Type", text='Portal Type')

            col.separator()

            col = layout.column(heading="Flags")
            sub = col.column(align=True)

            sub.prop(ob_nwo, "Portal_AI_Deafening", text='AI Deafening')
            sub.prop(ob_nwo, "Portal_Blocks_Sounds", text='Blocks Sounds')
            sub.prop(ob_nwo, "Portal_Is_Door", text='Is Door')
        # elif (ob_nwo.ObjectMesh_Type == 'SEAM' or ob_nwo.ObjectMesh_Type_Locked == 'SEAM'):
        #     if ob.name.startswith('+seam:') and ob.name.rpartition(':')[2] != ob.name:
        #         col.prop(ob_nwo, "Seam_Name_Locked", text='Seam BSP Name')
        #     else:
        #         col.prop(ob_nwo, "Seam_Name", text='Seam BSP Name')

        elif CheckType.water_physics(ob):
            col.prop(ob_nwo, "Water_Volume_Depth", text='Water Volume Depth')
            col.prop(ob_nwo, "Water_Volume_Flow_Direction", text='Flow Direction')
            col.prop(ob_nwo, "Water_Volume_Flow_Velocity", text='Flow Velocity')
            col.prop(ob_nwo, "Water_Volume_Fog_Color", text='Underwater Fog Color')
            col.prop(ob_nwo, "Water_Volume_Fog_Murkiness", text='Underwater Fog Murkiness')
        elif CheckType.fog(ob):
            col.prop(ob_nwo, "Fog_Name", text='Fog Name')
            col.prop(ob_nwo, "Fog_Appearance_Tag", text='Fog Appearance Tag')
            col.prop(ob_nwo, "Fog_Volume_Depth", text='Fog Volume Depth')

        elif CheckType.obb_volume(ob):
            col.prop(ob_nwo, "obb_volume_type")

        elif CheckType.physics(ob):
            col.prop(ob_nwo, "Mesh_Primitive_Type", text='Primitive Type')

        if CheckType.default(ob) or CheckType.poop(ob) or CheckType.decorator(ob) or CheckType.object_instance(ob) or CheckType.water_surface(ob) or CheckType.collision(ob):
            col.prop(ob_nwo, "Face_Global_Material", text='Global Material')

class NWO_ObjectMeshFaceProps(Panel):
    bl_label = "Face Properties"
    bl_idname = "NWO_PT_MeshFaceDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_parent_id = "NWO_PT_MeshDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        ob_nwo = ob.nwo

        return CheckType.render(ob) or CheckType.poop(ob) or CheckType.decorator(ob) or CheckType.object_instance(ob) or CheckType.water_surface(ob)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_nwo = ob.nwo

        col = flow.column()
        col.prop(ob_nwo, "Face_Type", text='Face Type')
        if ob_nwo.Face_Type == '_connected_geometry_face_type_sky':
            sub = col.column(align=True)
            sub.prop(ob_nwo, "Sky_Permutation_Index", text='Sky Permutation Index')
            col.separator()

        col.prop(ob_nwo, "Face_Mode", text='Face Mode')
        col.prop(ob_nwo, "Face_Sides", text='Face Sides')
        col.prop(ob_nwo, "Face_Draw_Distance", text='Draw Distance')
        col.prop(ob_nwo, 'texcoord_usage')
        if not_bungie_game():
            col.prop(ob_nwo, "Mesh_Tessellation_Density", text='Tessellation Density')
            col.prop(ob_nwo, "Mesh_Compression", text='Compression')

        col.separator()

        if ob_nwo.Region_Name_Locked != '':
            col.prop(ob_nwo, 'Region_Name_Locked', text='Region')
        else:
            col.prop(ob_nwo, "Region_Name", text='Region')

        col.separator()

        col = layout.column(heading="Flags")
        sub = col.column(align=True)
        sub.prop(ob_nwo, "Conveyor", text='Conveyor')
        sub.prop(ob_nwo, "Ladder", text='Ladder')
        sub.prop(ob_nwo, "Slip_Surface", text='Slip Surface')
        sub.prop(ob_nwo, "Decal_Offset", text='Decal Offset')
        sub.prop(ob_nwo, "Group_Transparents_By_Plane", text='Group Transparents By Plane')
        sub.prop(ob_nwo, "No_Shadow", text='No Shadow')
        sub.prop(ob_nwo, "Precise_Position", text='Precise Position')
        if not_bungie_game():
            sub.prop(ob_nwo, "no_lightmap")
            sub.prop(ob_nwo, "no_pvs")
            if CheckType.poop(ob) or CheckType.default(ob):
                sub.prop(ob_nwo, 'compress_verts')
            if CheckType.default(ob):
                sub.prop(ob_nwo, 'uvmirror_across_entire_model')



class NWO_ObjectMeshMaterialLightingProps(Panel):
    bl_label = "Lighting Properties"
    bl_idname = "NWO_PT_MeshMaterialLightingDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "NWO_PT_MeshFaceDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.object
        ob_nwo = ob.nwo

        if object_prefix(context.active_object, special_prefixes):
            return ob_nwo.ObjectMesh_Type_Locked not in invalid_mesh_types
        else:
            return ob_nwo.ObjectMesh_Type not in invalid_mesh_types

    def draw_header(self, context):
        ob = context.object
        ob_nwo = ob.nwo
        self.layout.prop(ob_nwo, "Material_Lighting_Enabled", text='')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_nwo = ob.nwo

        col = flow.column()

        layout.enabled = ob_nwo.Material_Lighting_Enabled
        
        col.prop(ob_nwo, "Material_Lighting_Emissive_Color", text='Emissive Color')
        col.prop(ob_nwo, "Material_Lighting_Emissive_Power", text='Emissive Power')
        col.prop(ob_nwo, "Material_Lighting_Emissive_Focus", text='Emissive Focus')
        col.prop(ob_nwo, "Material_Lighting_Emissive_Quality", text='Emissive Quality')

        col.separator()

        col.prop(ob_nwo, "Material_Lighting_Attenuation_Falloff", text='Attenuation Falloff')
        col.prop(ob_nwo, "Material_Lighting_Attenuation_Cutoff", text='Attenuation Cutoff')

        col.separator()

        col.prop(ob_nwo, "Material_Lighting_Bounce_Ratio", text='Bounce Ratio')
        
        col.separator()

        col = layout.column(heading="Flags")
        sub = col.column(align=True)
        sub.prop(ob_nwo, "Material_Lighting_Emissive_Per_Unit", text='Emissive Per Unit')
        sub.prop(ob_nwo, "Material_Lighting_Use_Shader_Gel", text='Use Shader Gel')

class NWO_ObjectMeshLightmapProps(Panel):
    bl_label = "Lightmap Properties"
    bl_idname = "NWO_PT_MeshLightmapDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "NWO_PT_MeshFaceDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.object
        ob_nwo = ob.nwo

        if object_prefix(context.active_object, special_prefixes):
            return ob_nwo.ObjectMesh_Type_Locked not in invalid_mesh_types
        else:
            return ob_nwo.ObjectMesh_Type not in invalid_mesh_types

    def draw_header(self, context):
        ob = context.object
        ob_nwo = ob.nwo
        self.layout.prop(ob_nwo, "Lightmap_Settings_Enabled", text='')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_nwo = ob.nwo

        col = flow.column()

        layout.enabled = ob_nwo.Lightmap_Settings_Enabled

        col.prop(ob_nwo, "Lightmap_Type", text='Lightmap Type')

        col.separator()

        col.prop(ob_nwo, "Lightmap_Translucency_Tint_Color", text='Translucency Tint Color')
        col.prop(ob_nwo, "Lightmap_Additive_Transparency", text='Additive Transparency')
        
        col.separator()

        col.prop(ob_nwo, "Lightmap_Resolution_Scale", text='Resolution Scale')
        col.prop(ob_nwo, "lightmap_photon_fidelity")

        # col.prop(ob_nwo, "Lightmap_Chart_Group", text='Chart Group')

        # col.separator()

        # col.prop(ob_nwo, "Lightmap_Analytical_Bounce_Modifier", text='Analytical Bounce Modifier')
        # col.prop(ob_nwo, "Lightmap_General_Bounce_Modifier", text='General Bounce Modifier')
        
        col.separator()

        col = layout.column(heading="Flags")
        sub = col.column(align=True)
        sub.prop(ob_nwo, "Lightmap_Lighting_From_Both_Sides", text='Lighting From Both Sides')
        sub.prop(ob_nwo, "Lightmap_Transparency_Override", text='Transparency Override')
        

# MARKER PROPERTIES
class NWO_ObjectMarkerProps(Panel):
    bl_label = "Marker Properties"
    bl_idname = "NWO_PT_MarkerDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_parent_id = "NWO_PT_ObjectDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.object

        return CheckType.marker(ob)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_nwo = ob.nwo

        col = flow.column()
        if not_bungie_game():
            if object_prefix(ob, ('?')):
                col.prop(ob_nwo, "ObjectMarker_Type_Locked_H4", text='Marker Type')
            else:
                col.prop(ob_nwo, "ObjectMarker_Type_H4", text='Marker Type')
        else:
            if object_prefix(ob, ('?')):
                col.prop(ob_nwo, "ObjectMarker_Type_Locked", text='Marker Type')
            else:
                col.prop(ob_nwo, "ObjectMarker_Type", text='Marker Type')

        if CheckType.model(ob):
            col.prop(ob_nwo, "Marker_Group_Name", text='Marker Group')
            col.prop(ob_nwo, "Marker_Velocity", text='Marker Velocity')
            sub = col.row(align=True)
            if not ob_nwo.Marker_All_Regions:
                sub.prop(ob_nwo, "Marker_Region", text='Marker Region')
            sub.prop(ob_nwo, 'Marker_All_Regions', text='All Regions')

        elif CheckType.game_instance(ob):
            row = col.row()
            row.prop(ob_nwo, "Marker_Game_Instance_Tag_Name", text='Tag Path')
            row.operator('nwo.game_instance_path')
            col.prop(ob_nwo, "Marker_Game_Instance_Tag_Variant_Name", text='Tag Variant')
            if not_bungie_game():
                col.prop(ob_nwo, 'marker_game_instance_run_scripts') 
                
        elif CheckType.hint(ob) and not_bungie_game():
            col.prop(ob_nwo, "Marker_Group_Name", text='Marker Group')
            col.prop(ob_nwo, 'marker_hint_length')

        elif CheckType.pathfinding_sphere(ob):
            col.separator()
            col = layout.column(heading="Flags")
            sub = col.column(align=True)
            sub.prop(ob_nwo, "Marker_Pathfinding_Sphere_Vehicle", text='Vehicle Only')
            sub.prop(ob_nwo, "Pathfinding_Sphere_Remains_When_Open", text='Remains When Open')
            sub.prop(ob_nwo, "Pathfinding_Sphere_With_Sectors", text='With Sectors')

        elif CheckType.physics_constraint(ob):
            col.separator()
            col.prop(ob_nwo, "Physics_Constraint_Parent", text='Physics Constraint Parent')
            col.prop(ob_nwo, "Physics_Constraint_Child", text='Physics Constraint Child')

            sus = col.row(align=True)

            sus.prop(ob_nwo, "Physics_Constraint_Type", text='Physics Constraint Type')
            sus.prop(ob_nwo, 'Physics_Constraint_Uses_Limits', text='Uses Limits')

            if ob_nwo.Physics_Constraint_Uses_Limits:
                if ob_nwo.Physics_Constraint_Type == 'HINGE':
                    col.prop(ob_nwo, "Hinge_Constraint_Minimum", text='Minimum')
                    col.prop(ob_nwo, "Hinge_Constraint_Maximum", text='Maximum')

                elif ob_nwo.Physics_Constraint_Type == 'SOCKET':
                    col.prop(ob_nwo, "Cone_Angle", text='Cone Angle')

                    col.prop(ob_nwo, "Plane_Constraint_Minimum", text='Plane Minimum')
                    col.prop(ob_nwo, "Plane_Constraint_Maximum", text='Plane Maximum')
                    
                    col.prop(ob_nwo, "Twist_Constraint_Start", text='Twist Start')
                    col.prop(ob_nwo, "Twist_Constraint_End", text='Twist End')

        elif CheckType.target(ob):
            col.prop(ob_nwo, "Marker_Group_Name", text='Marker Group')

        elif CheckType.airprobe(ob) and not_bungie_game():
            col.prop(ob_nwo, "Marker_Group_Name", text='Air Probe Group')

        elif CheckType.envfx(ob) and not_bungie_game():
            col.prop(ob_nwo, "marker_looping_effect")

        elif CheckType.lightCone(ob) and not_bungie_game(): 
            col.prop(ob_nwo, "marker_light_cone_tag")
            col.prop(ob_nwo, "marker_light_cone_color")
            col.prop(ob_nwo, "marker_light_cone_alpha") 
            col.prop(ob_nwo, "marker_light_cone_intensity")
            col.prop(ob_nwo, "marker_light_cone_width")
            col.prop(ob_nwo, "marker_light_cone_length")
            col.prop(ob_nwo, "marker_light_cone_curve")

# MATERIAL PROPERTIES
class NWO_MaterialProps(Panel):
    bl_label = "Halo Material Properties"
    bl_idname = "NWO_PT_MaterialPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_halo = scene.halo

        if scene_halo.game_version in ('reach','h4','h2a'):
            return context.material

    def draw(self, context):
        scene = context.scene
        scene_halo = scene.halo
        layout = self.layout
        ob = context.active_object
        current_material = ob.active_material
        if current_material is not None:
            material_nwo = current_material.nwo
            is_override = CheckType.override(current_material)
            layout.use_property_split = True
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            # fun setup to display the correct fields
            if not_bungie_game():
                if is_override:
                    if current_material.name.startswith('+'):
                        col.prop(material_nwo, "material_override_h4_locked")
                    else:
                        col.prop(material_nwo, "material_override_h4")
                else:
                    col.prop(material_nwo, "shader_path", text='Material Path')
                    col.prop(material_nwo, "material_override_h4")
            else:
                if is_override:
                    if current_material.name.startswith('+'):
                        col.prop(material_nwo, "material_override_locked")
                    else:
                        col.prop(material_nwo, "material_override")
                else:
                    col.prop(material_nwo, "shader_path")
                    col.prop(material_nwo, "Shader_Type")
                    col.prop(material_nwo, "material_override")
                        
# LIGHT PROPERTIES
class NWO_LightProps(Panel):
    bl_label = "Light Properties"
    bl_idname = "NWO_PT_LightPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_parent_id = "NWO_PT_ObjectDetailsPanel"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_halo = scene.halo

        if scene_halo.game_version in ('reach','h4','h2a'):
            return context.object.type == 'LIGHT'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_nwo = ob.nwo

        col = flow.column()

        scene = context.scene
        scene_halo = scene.halo

        if scene_halo.game_version in ('h4','h2a'):
            col.prop(ob_nwo, 'Light_Color', text='Color')
            col.prop(ob_nwo, 'light_mode')
            col.prop(ob_nwo, 'light_lighting_mode')
            col.prop(ob_nwo, 'light_type_h4')
            if ob_nwo.light_type_h4 == '_connected_geometry_light_type_spot' and not ob_nwo.light_mode == '_connected_geometry_light_mode_dynamic':

                col.separator()

                col.prop(ob_nwo, 'light_cone_projection_shape')
                col.prop(ob_nwo, 'light_inner_cone_angle')
                col.prop(ob_nwo, 'light_outer_cone_angle')

            col.separator()
            col.prop(ob_nwo, 'Light_IntensityH4')
            if ob_nwo.light_lighting_mode == '_connected_geometry_lighting_mode_artistic':
                col.prop(ob_nwo, 'Light_Near_Attenuation_StartH4')
                col.prop(ob_nwo, 'Light_Near_Attenuation_EndH4')
            
            col.separator()
                
            if ob_nwo.light_mode == '_connected_geometry_light_mode_dynamic':
                col.prop(ob_nwo, 'light_cinema')
                col.prop(ob_nwo, 'light_destroy_after')
                col.prop(ob_nwo, "light_shadows")
                if ob_nwo.light_shadows:
                    col.prop(ob_nwo, 'light_shadow_color')
                    col.prop(ob_nwo, 'light_dynamic_shadow_quality')
                    col.prop(ob_nwo, 'light_shadow_near_clipplane')
                    col.prop(ob_nwo, 'light_shadow_far_clipplane')
                    col.prop(ob_nwo, 'light_shadow_bias_offset')
                col.prop(ob_nwo, 'light_cinema_objects_only')
                col.prop(ob_nwo, "light_specular_contribution")
                col.prop(ob_nwo, "light_diffuse_contribution")
                col.prop(ob_nwo, "light_ignore_dynamic_objects")
                col.prop(ob_nwo, "light_screenspace")
                if ob_nwo.light_screenspace:
                    col.prop(ob_nwo, 'light_specular_power')
                    col.prop(ob_nwo, 'light_specular_intensity')

                # col = layout.column(heading="Flags")
                # sub = col.column(align=True)
            else:
                col.prop(ob_nwo, 'light_jitter_quality')
                col.prop(ob_nwo, 'light_jitter_angle')
                col.prop(ob_nwo, 'light_jitter_sphere_radius')

                col.separator()

                col.prop(ob_nwo, 'light_amplification_factor')

                col.separator()
                # col.prop(ob_nwo, 'light_attenuation_near_radius')
                # col.prop(ob_nwo, 'light_attenuation_far_radius')
                # col.prop(ob_nwo, 'light_attenuation_power')
                # col.prop(ob_nwo, 'light_tag_name')
                col.prop(ob_nwo, "light_indirect_only")
                col.prop(ob_nwo, "light_static_analytic")

            # col.prop(ob_nwo, 'light_intensity_off', text='Light Intensity Set Via Tag')
            # if ob_nwo.light_lighting_mode == '_connected_geometry_lighting_mode_artistic':
            #     col.prop(ob_nwo, 'near_attenuation_end_off', text='Near Attenuation Set Via Tag')
            # if ob_nwo.light_type_h4 == '_connected_geometry_light_type_spot':
            #     col.prop(ob_nwo, 'outer_cone_angle_off', text='Outer Cone Angle Set Via Tag')

            if ob_nwo.manual_fade_distance:
                col.prop(ob_nwo, 'Light_Far_Attenuation_StartH4')
                col.prop(ob_nwo, 'Light_Far_Attenuation_EndH4')
                col.prop(ob_nwo, 'Light_Fade_Start_Distance')
                col.prop(ob_nwo, 'Light_Fade_End_Distance')
            

        else:
            if context.active_object.data.type == 'POINT' or context.active_object.data.type == 'SUN':
                col.prop(ob_nwo, "light_type_override_locked", text='Type')
            else:
                col.prop(ob_nwo, "light_type_override", text='Type')

            col.prop(ob_nwo, 'Light_Game_Type', text='Game Type')
            col.prop(ob_nwo, 'Light_Shape', text='Shape')
            col.prop(ob_nwo, 'Light_Color', text='Color') 
            col.prop(ob_nwo, 'Light_Intensity', text='Intensity')

            col.separator()

            col.prop(ob_nwo, 'Light_Fade_Start_Distance', text='Fade Out Start Distance')
            col.prop(ob_nwo, 'Light_Fade_End_Distance', text='Fade Out End Distance')

            col.separator()

            col.prop(ob_nwo, 'Light_Hotspot_Size', text='Hotspot Size')
            col.prop(ob_nwo, 'Light_Hotspot_Falloff', text='Hotspot Falloff')
            col.prop(ob_nwo, 'Light_Falloff_Shape', text='Falloff Shape')
            col.prop(ob_nwo, 'Light_Aspect', text='Light Aspect')

            col.separator()

            col.prop(ob_nwo, 'Light_Frustum_Width', text='Frustum Width')
            col.prop(ob_nwo, 'Light_Frustum_Height', text='Frustum Height')

            col.separator()

            col.prop(ob_nwo, 'Light_Volume_Distance', text='Light Volume Distance')
            col.prop(ob_nwo, 'Light_Volume_Intensity', text='Light Volume Intensity')

            col.separator()

            col.prop(ob_nwo, 'Light_Bounce_Ratio', text='Light Bounce Ratio')

            col.separator()

            col = layout.column(heading="Flags")
            sub = col.column(align=True)

            sub.prop(ob_nwo, 'Light_Ignore_BSP_Visibility', text='Ignore BSP Visibility') 
            sub.prop(ob_nwo, 'Light_Dynamic_Has_Bounce', text='Light Has Dynamic Bounce')
            if ob_nwo.light_sub_type == '_connected_geometry_lighting_sub_type_screenspace':
                sub.prop(ob_nwo, 'Light_Screenspace_Has_Specular', text='Screenspace Light Has Specular')

            col = flow.column()

            col.prop(ob_nwo, 'Light_Near_Attenuation_Start', text='Near Attenuation Start')
            col.prop(ob_nwo, 'Light_Near_Attenuation_End', text='Near Attenuation End')

            col.separator()

            col.prop(ob_nwo, 'Light_Far_Attenuation_Start', text='Far Attenuation Start')
            col.prop(ob_nwo, 'Light_Far_Attenuation_End', text='Far Attenuation End')

            col.separator()

            col.prop(ob_nwo, 'Light_Tag_Override', text='Light Tag Override')
            col.prop(ob_nwo, 'Light_Shader_Reference', text='Shader Tag Reference')
            col.prop(ob_nwo, 'Light_Gel_Reference', text='Gel Tag Reference')
            col.prop(ob_nwo, 'Light_Lens_Flare_Reference', text='Lens Flare Tag Reference')

            # col.separator() # commenting out light clipping for now.

            # col.prop(ob_nwo, 'Light_Clipping_Size_X_Pos', text='Clipping Size X Forward')
            # col.prop(ob_nwo, 'Light_Clipping_Size_Y_Pos', text='Clipping Size Y Forward')
            # col.prop(ob_nwo, 'Light_Clipping_Size_Z_Pos', text='Clipping Size Z Forward')
            # col.prop(ob_nwo, 'Light_Clipping_Size_X_Neg', text='Clipping Size X Backward')
            # col.prop(ob_nwo, 'Light_Clipping_Size_Y_Neg', text='Clipping Size Y Backward')
            # col.prop(ob_nwo, 'Light_Clipping_Size_Z_Neg', text='Clipping Size Z Backward')

# BONE PROPERTIES
class NWO_BoneProps(Panel):
    bl_label = "Halo Bone Properties"
    bl_idname = "NWO_PT_BoneDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "bone"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_halo = scene.halo
        return scene_halo.game_version in ('reach','h4','h2a')
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        
        bone = context.bone
        bone_nwo = bone.nwo
        scene = context.scene
        scene_halo = scene.halo

        # layout.enabled = scene_halo.expert_mode
        
        col = flow.column()
        col.prop(bone_nwo, "frame_id1", text='Frame ID 1')
        col.prop(bone_nwo, "frame_id2", text='Frame ID 2')

        col.separator()

        col.prop(bone_nwo, "object_space_node", text='Object Space Offset Node')
        col.prop(bone_nwo, "replacement_correction_node", text='Replacement Correction Node')
        col.prop(bone_nwo, "fik_anchor_node", text='Forward IK Anchor Node')

# NWO PROPERTY GROUPS
class NWO_ObjectPropertiesGroup(PropertyGroup):
    #OBJECT PROPERTIES
    object_id: StringProperty(
        name="Object ID",
    )

    def get_objecttype_enum(self):
        if bpy.context.active_object.name.startswith(frame_prefixes):
            return 0
        elif bpy.context.active_object.name.startswith(marker_prefixes):
            return 1
        else:
            return 2

    object_type_items_all = [
        ('_connected_geometry_object_type_frame', 'Frame', "Treat this object as a frame. Can be forced on with the prefixes: 'b_', 'b ', 'frame ', 'frame_'"),
        ('_connected_geometry_object_type_marker', 'Marker', "Sets this object to be written to a json file as a marker. Can be forced on with the prefix: '#'"),
        ('_connected_geometry_object_type_mesh', 'Mesh', "Treats this object as a mesh when writing to a json file"),
    ]

    object_type_items_no_mesh = [
        ('_connected_geometry_object_type_frame', "Frame", "Treat this object as a frame. Can be forced on with the prefixes: 'b_', 'b ', 'frame ', 'frame_'"),
        ('_connected_geometry_object_type_marker', "Marker", "Sets this object to be written to a json file as a marker. Can be forced on with the prefix: '#'"),
    ]

    Object_Type_All: EnumProperty(
        name="Object Type",
        options=set(),
        description="Sets the Halo object type of this object",
        default = '_connected_geometry_object_type_mesh',
        items=object_type_items_all,
    )

    Object_Type_No_Mesh: EnumProperty(
        name="Object Type",
        options=set(),
        description="Sets the object type",
        default = '_connected_geometry_object_type_marker',
        items=object_type_items_no_mesh,
    )

    Object_Type_All_Locked: EnumProperty(
        name="Object Type",
        options=set(),
        get=get_objecttype_enum,
        description="Sets the object type",
        default = '_connected_geometry_object_type_mesh',
        items=object_type_items_all,
    )

    Object_Type_No_Mesh_Locked: EnumProperty(
        name="Object Type",
        options=set(),
        get=get_objecttype_enum,
        description="Sets the object type",
        default = '_connected_geometry_object_type_marker',
        items=object_type_items_no_mesh,
    )

    def LockLight(self):
        return 0

    Object_Type_Light: EnumProperty(
        name="Object Type",
        options=set(),
        get=LockLight,
        description="Sets the object type",
        default = '_connected_geometry_object_type_light',
        items=[('_connected_geometry_object_type_light', 'Light', '')],
    ) 

    compress_verts: BoolProperty(
        name="Compress Vertices",
        options=set(),
        default = False,
    )

    uvmirror_across_entire_model: BoolProperty(
        name="UV Mirror Across Model",
        options=set(),
        default = False,
    )

    bsp_name: StringProperty(
        name="BSP Name",
        default='000',
        description="Set bsp name for this object. Only valid for scenario exports",
    )

    def get_bsp_from_collection(self):
        bsp = get_prop_from_collection(self.id_data, ('+bsp:', '+design:'))
        return bsp

    bsp_name_locked: StringProperty(
        name="BSP Name",
        default='',
        description="Set bsp name for this object. Only valid for scenario exports",
        get=get_bsp_from_collection,
    )

    def get_meshtype_enum(self):
        a_ob = bpy.context.active_object
        if a_ob.name.startswith(('+soft_ceiling','+soft_kill','+slip_surface')):
            return 0
        elif a_ob.name.startswith('@'):
            return 1
        elif a_ob.name.startswith('+cookie'):
            return 2
        elif a_ob.name.startswith('%'):
            return 5
        elif a_ob.name.startswith('+flair'):
            return 10
        elif a_ob.name.startswith('$'):
            return 11
        elif a_ob.name.startswith('+fog'):
            return 12
        elif a_ob.name.startswith('+portal'):
            return 13
        elif a_ob.name.startswith('+seam'):
            return 14
        elif a_ob.name.startswith('+water'):
            return 15
        elif a_ob.name.startswith('\''):
            return 16
        else:
            return 4

    mesh_type_items = [
        ('_connected_geometry_mesh_type_boundary_surface', "Boundary Surface", "Used in structure_design tags for soft_kill, soft_ceiling, and slip_sufaces. Only use when importing to a structure_design tag. Can be forced on with the prefixes: '+soft_ceiling', 'soft_kill', 'slip_surface'"), # 0
        ('_connected_geometry_mesh_type_collision', "Collision", "Sets this mesh to have collision geometry only. Can be forced on with the prefix: '@'"), #1
        ('_connected_geometry_mesh_type_cookie_cutter', "Cookie Cutter", "Defines an area which ai will pathfind around. Can be forced on with the prefix: '+cookie'"), # 2
        ('_connected_geometry_mesh_type_decorator', "Decorator", "Use this when making a decorator. Allows for different LOD levels to be set"), # 3
        ('_connected_geometry_mesh_type_default', "Render / Structure", "By default this mesh type will be treated as render only geometry in models, and render + bsp collision geometry in structures"), #4
        ('_connected_geometry_mesh_type_poop', "Instanced Geometry", "Writes this mesh to a json file as instanced geometry. Can be forced on with the prefix: '%'"), # 5
        ('_connected_geometry_mesh_type_poop_marker', "Instanced Marker", ""), # 6
        ('_connected_geometry_mesh_type_poop_rain_blocker', "Rain Occluder",'Rain is not rendered in the the volume this mesh occupies.'), # 7
        ('_connected_geometry_mesh_type_poop_vertical_rain_sheet', "Vertical Rain Sheet", ''), # 8
        ('_connected_geometry_mesh_type_lightmap_region', "Lightmap Region", "Defines an area of a structure which should be lightmapped. Can be referenced when lightmapping"), # 9
        ('_connected_geometry_mesh_type_object_instance', "Object Instance", "Writes this mesh to the json as an instanced object. Can be forced on with the prefix: '+flair'"), # 10
        ('_connected_geometry_mesh_type_physics', "Physics", "Sets this mesh to have physics geometry only. Can be forced on with the prefix: '$'"), # 11
        ('_connected_geometry_mesh_type_planar_fog_volume', "Planar Fog Volume", "Defines an area for a fog volume. The same logic as used for portals should be applied to these.  Can be forced on with the prefix: '+fog'"), # 12
        ('_connected_geometry_mesh_type_portal', "Portal", "Cuts up a bsp and defines clusters. Can be forced on with the prefix '+portal'"), # 13
        ('_connected_geometry_mesh_type_seam', "Seam", "Defines where two bsps meet. Its name should match the name of the bsp its in. Can be forced on with the prefix '+seam'"), # 14
        ('_connected_geometry_mesh_type_water_physics_volume', "Water Physics Volume", "Defines an area where water physics should apply. Only use when importing to a structure_design tag. Can be forced on with the prefix: '+water'"), # 15
        ('_connected_geometry_mesh_type_water_surface', "Water Surface", "Defines a mesh as a water surface. Can be forced on with the prefix: '"), # 16
    ]

    #MESH PROPERTIES
    ObjectMesh_Type : EnumProperty(
        name="Mesh Type",
        options=set(),
        description="Sets the type of Halo mesh you want to create. This value is overridden by certain object prefixes",
        default = '_connected_geometry_mesh_type_default',
        items=mesh_type_items,
        )

    ObjectMesh_Type_Locked : EnumProperty(
        name="Mesh Type",
        options=set(),
        get=get_meshtype_enum,
        description="Sets the type of Halo mesh you want to create. This value is overridden by certain object prefixes e.g. $, @, %",
        default = '_connected_geometry_mesh_type_default',
        items=mesh_type_items,
        )

    def get_meshtype_enum_h4(self):
        a_ob = bpy.context.active_object
        if a_ob.name.startswith(('+soft_ceiling','+soft_kill','+slip_surface')):
            return 0
        elif a_ob.name.startswith('@'):
            return 1
        elif a_ob.name.startswith('+cookie'):
            return 2
        elif a_ob.name.startswith('%'):
            return 5
        elif a_ob.name.startswith('+flair'):
            return 10
        elif a_ob.name.startswith('$'):
            return 11
        elif a_ob.name.startswith('+fog'):
            return 12
        elif a_ob.name.startswith('+portal'):
            return 13
        elif a_ob.name.startswith('+seam'):
            return 14
        elif a_ob.name.startswith('+water'):
            return 15
        elif a_ob.name.startswith('\''):
            return 16
        else:
            return 4

    # dupes for h4
    mesh_type_items_h4 = [
        ('_connected_geometry_mesh_type_boundary_surface', "Boundary Surface", "Used in structure_design tags for soft_kill, soft_ceiling, and slip_sufaces. Only use when importing to a structure_design tag. Can be forced on with the prefix: '+'"), # 0
        ('_connected_geometry_mesh_type_collision', "Collision", "Sets this mesh to have collision geometry only. Can be forced on with the prefix: '@'"), #1
        ('_connected_geometry_mesh_type_cookie_cutter', "Cookie Cutter", "Defines an area which ai will pathfind around. Can be forced on with the prefix: '+cookie'"), # 2
        ('_connected_geometry_mesh_type_decorator', "Decorator", "Use this when making a decorator. Allows for different LOD levels to be set"), # 3
        ('_connected_geometry_mesh_type_default', "Render / Structure", "By default this mesh type will be treated as render only geometry in models, and render + bsp collision geometry in structures"), #4
        ('_connected_geometry_mesh_type_poop', "Instanced Geometry", "Writes this mesh to a json file as instanced geometry. Can be forced on with the prefix: '%'"), # 5
        ('_connected_geometry_mesh_type_object_instance', "Object Instance", "Writes this mesh to the json as an instanced object. Can be forced on with the prefix: '+flair'"), # 6
        ('_connected_geometry_mesh_type_physics', "Physics", "Sets this mesh to have physics geometry only. Can be forced on with the prefix: '$'"), # 7
        ('_connected_geometry_mesh_type_planar_fog_volume', "Planar Fog Volume", "Defines an area for a fog volume. The same logic as used for portals should be applied to these.  Can be forced on with the prefix: '+fog'"), # 8
        ('_connected_geometry_mesh_type_portal', "Portal", "Cuts up a bsp and defines clusters. Can be forced on with the prefix '+portal'"), # 9
        ('_connected_geometry_mesh_type_seam', "Seam", "Defines where two bsps meet. Its name should match the name of the bsp its in. Can be forced on with the prefix '+seam'"), # 10
        ('_connected_geometry_mesh_type_water_physics_volume', "Water Physics Volume", "Defines an area where water physics should apply. Only use when importing to a structure_design tag. Can be forced on with the prefix: '+water'"), # 11
        ('_connected_geometry_mesh_type_water_surface', "Water Surface", "Defines a mesh as a water surface. Can be forced on with the prefix: '"), # 12
        ('_connected_geometry_mesh_type_obb_volume', 'OBB Volume', ''), # 13
    ]

    def get_default_mesh_type(self):
        if bpy.context.scene.gr2.default_mesh_type == '_connected_geometry_mesh_type_default':
            return self.get("ObjectMesh_Type_H4", 4)
        elif bpy.context.scene.gr2.default_mesh_type == '_connected_geometry_mesh_type_poop':
            return self.get("ObjectMesh_Type_H4", 5)
        else:
            return self.get("ObjectMesh_Type_H4", 4)
    
    def set_default_mesh_type(self, value):
        self["ObjectMesh_Type_H4"] = value

    ObjectMesh_Type_H4 : EnumProperty(
        name="Mesh Type",
        options=set(),
        description="Sets the type of Halo mesh you want to create. This value is overridden by certain object prefixes",
        default = '_connected_geometry_mesh_type_default',
        get=get_default_mesh_type,
        set=set_default_mesh_type,
        items=mesh_type_items_h4,
        )

    ObjectMesh_Type_H4 : EnumProperty(
        name="Mesh Type",
        options=set(),
        description="Sets the type of Halo mesh you want to create. This value is overridden by certain object prefixes",
        default = '_connected_geometry_mesh_type_default',
        get=get_default_mesh_type,
        set=set_default_mesh_type,
        items=mesh_type_items_h4,
        )

    ObjectMesh_Type_Locked_H4 : EnumProperty(
        name="Mesh Type",
        options=set(),
        get=get_meshtype_enum,
        description="Sets the type of Halo mesh you want to create. This value is overridden by certain object prefixes e.g. $, @, %",
        default = '_connected_geometry_mesh_type_default',
        items=mesh_type_items_h4,
        )

    Mesh_Primitive_Type : EnumProperty(
        name="Mesh Primitive Type",
        options=set(),
        description="Select the primtive type of this mesh",
        default = "_connected_geometry_primitive_type_none",
        items=[ ('_connected_geometry_primitive_type_none', "None", "None"),
                ('_connected_geometry_primitive_type_box', "Box", "Box"),
                ('_connected_geometry_primitive_type_pill', "Pill", "Pill"),
                ('_connected_geometry_primitive_type_sphere', "Sphere", "Sphere"),
                ('_connected_geometry_primitive_type_mopp', "MOPP", ""),
               ]
        )

    Mesh_Tessellation_Density : EnumProperty(
        name="Mesh Tessellation Density",
        options=set(),
        description="Select the tesselation density you want applied to this mesh",
        default = "_connected_geometry_mesh_tessellation_density_none",
        items=[ ('_connected_geometry_mesh_tessellation_density_none', "None", ""),
                ('_connected_geometry_mesh_tessellation_density_4x', "4x", "4 times"),
                ('_connected_geometry_mesh_tessellation_density_9x', "9x", "9 times"),
                ('_connected_geometry_mesh_tessellation_density_36x', "36x", "36 times"),
               ]
        )
    Mesh_Compression : EnumProperty(
        name="Mesh Compression",
        options=set(),
        description="Select if you want additional compression forced on/off to this mesh",
        default = "_connected_geometry_mesh_additional_compression_default",
        items=[ ('_connected_geometry_mesh_additional_compression_default', "Default", "Default"),
                ('_connected_geometry_mesh_additional_compression_force_off', "Force Off", "Force Off"),
                ('_connected_geometry_mesh_additional_compression_force_on', "Force On", "Force On"),
               ]
        )

    #FACE PROPERTIES
    Face_Type : EnumProperty(
        name="Face Type",
        options=set(),
        description="Sets the face type for this mesh. Note that any override shaders will override the face type selected here for relevant materials",
        default = '_connected_geometry_face_type_normal',
        items=[ ('_connected_geometry_face_type_normal', "Normal", "This face type has no special properties"),
                ('_connected_geometry_face_type_seam_sealer', "Seam Sealer", "Set mesh faces to have the special seam sealer property. Collsion only geometry"),
                ('_connected_geometry_face_type_sky', "Sky", "Set mesh faces to render the sky"),
               ]
        )

    Face_Mode : EnumProperty(
        name="Face Mode",
        options=set(),
        description="Sets face mode for this mesh",
        default = '_connected_geometry_face_mode_normal',
        items=[ ('_connected_geometry_face_mode_normal', "Normal", "This face mode has no special properties"),
                ('_connected_geometry_face_mode_render_only', "Render Only", "Faces set to render only"),
                ('_connected_geometry_face_mode_collision_only', "Collision Only", "Faces set to collision only"),
                ('_connected_geometry_face_mode_sphere_collision_only', "Sphere Collision Only", "Faces set to sphere collision only. Only objects with physics models can collide with these faces"),
                ('_connected_geometry_face_mode_shadow_only', "Shadow Only", "Faces set to only cast shadows"),
                ('_connected_geometry_face_mode_lightmap_only', "Lightmap Only", "Faces set to only be used during lightmapping. They will otherwise have no render / collision geometry"),
                ('_connected_geometry_face_mode_breakable', "Breakable", "Faces set to be breakable"),
               ]
        )

    Face_Sides : EnumProperty(
        name="Face Sides",
        options=set(),
        description="Sets the face sides for this mesh",
        default = '_connected_geometry_face_sides_one_sided',
        items=[ ('_connected_geometry_face_sides_one_sided', "One Sided", "Faces set to only render on one side (the direction of face normals)"),
                ('_connected_geometry_face_sides_one_sided_transparent', "One Sided Transparent", "Faces set to only render on one side (the direction of face normals), but also render geometry behind them"),
                ('_connected_geometry_face_sides_two_sided', "Two Sided", "Faces set to render on both sides"),
                ('_connected_geometry_face_sides_two_sided_transparent', "Two Sided Transparent", "Faces set to render on both sides and are transparent"),
                ('_connected_geometry_face_sides_mirror', "Mirror", "H4+ only"),
                ('_connected_geometry_face_sides_mirror_transparent', "Mirror Transparent", "H4+ only"),
                ('_connected_geometry_face_sides_keep', "Keep", "H4+ only"),
                ('_connected_geometry_face_sides_keep_transparent', "Keep Transparent", "H4+ only"),
               ]
        )

    Face_Draw_Distance : EnumProperty(
        name="Face Draw Distance",
        options=set(),
        description="Select the draw distance for faces on this mesh",
        default = "_connected_geometry_face_draw_distance_normal",
        items=[ ('_connected_geometry_face_draw_distance_normal', "Normal", ""),
                ('_connected_geometry_face_draw_distance_detail_mid', "Mid", ""),
                ('_connected_geometry_face_draw_distance_detail_close', "Close", ""),
               ]
        ) 

    texcoord_usage : EnumProperty(
        name="Texture Coordinate Usage",
        options=set(),
        description="",
        default = '_connected_material_texcoord_usage_default',
        items=[ ('_connected_material_texcoord_usage_default', "Default", ""),
                ('_connected_material_texcoord_usage_none', "None", ""),
                ('_connected_material_texcoord_usage_anisotropic', "Ansiotropic", ""),
               ]
        )

    Region_Name: StringProperty(
        name="Face Region",
        default='default',
        description="Define the name of the region these faces should be associated with",
    )

    def get_region_from_collection(self):
        region = get_prop_from_collection(self.id_data, ('+region:', '+reg:'))
        return region

    Region_Name_Locked: StringProperty(
        name="Face Region",
        description="Define the name of the region these faces should be associated with",
        get=get_region_from_collection,
    )

    Permutation_Name: StringProperty(
        name="Permutation",
        default='default',
        description="Define the permutation of this object. Leave blank for default",
    )

    def get_permutation_from_collection(self):
        permutation = get_prop_from_collection(self.id_data, ('+perm:', '+permuation:'))
        return permutation

    Permutation_Name_Locked: StringProperty(
        name="Permutation",
        description="Define the permutation of this object. Leave blank for default",
        get=get_permutation_from_collection,
    )

    is_pca: BoolProperty(
        name="Frame PCA",
        options=set(),
        description="",
        default=False,
    )

    Face_Global_Material: StringProperty(
        name="Global Material",
        default='',
        description="Set the global material of the faces of this mesh. For struture geometry leave blank to use the global material of the shader. The global material name should match a valid material defined in tags\globals\globals.globals",
    )

    Sky_Permutation_Index: IntProperty(
        name="Sky Permutation Index",
        options=set(),
        description="Set the sky permutation index of the faces. Only valid if the face type is sky",
        min=0,
    )

    Conveyor: BoolProperty(
        name ="Conveyor",
        options=set(),
        description = "Enables the conveyor property",
        default = False,
        )

    Ladder: BoolProperty(
        name ="Ladder",
        options=set(),
        description = "Makes faces climbable",
        default = False,
    )

    Slip_Surface: BoolProperty(
        name ="Slip Surface",
        options=set(),
        description = "Makes faces slippery for units",
        default = False,
    )

    Decal_Offset: BoolProperty(
        name ="Decal Offset",
        options=set(),
        description = "Enable to offset these faces so that they appear to be layered on top of another face",
        default = False,
    )

    Group_Transparents_By_Plane: BoolProperty(
        name ="Group Transparents By Plane",
        options=set(),
        description = "Enable to group transparent geometry by fitted planes",
        default = False,
    )

    No_Shadow: BoolProperty(
        name ="No Shadow",
        options=set(),
        description = "Enable to prevent faces from casting shadows",
        default = False,
    )

    Precise_Position: BoolProperty(
        name ="Precise Position",
        options=set(),
        description = "Enable to prevent faces from being altered during the import process",
        default = False,
    )

    no_lightmap: BoolProperty(
        name ="Exclude From Lightmap",
        options=set(),
        description = "",
        default = False,
    )

    no_pvs: BoolProperty(
        name ="Invisible To PVS",
        options=set(),
        description = "",
        default = False,
    )
    
    #PRIMITIVE PROPERTIES
    # Box_Length: FloatProperty(
    #     name="Box Length",
    #     options=set(),
    #     description="Set the length of the primitive box",
    # )

    # Box_Width: FloatProperty(
    #     name="Box Width",
    #     options=set(),
    #     description="Set the width of the primitive box",
    # )

    # Box_Height: FloatProperty(
    #     name="Box Height",
    #     options=set(),
    #     description="Set the height of the primitive box",
    # )

    # Pill_Radius: FloatProperty(
    #     name="Pill Radius",
    #     options=set(),
    #     description="Set the radius of the primitive pill",
    # )

    # Pill_Height: FloatProperty(
    #     name="Pill Height",
    #     options=set(),
    #     description="Set the height of the primitive pill",
    # )

    # Sphere_Radius: FloatProperty(
    #     name="Sphere Radius",
    #     options=set(),
    #     description="Set the radius of the primitive sphere",
    # )
    
    #BOUNDARY SURFACE PROPERTIES
    def get_boundary_surface_name(self):
        name = self.id_data.name
        name = name.removeprefix('+soft_ceiling')
        name = name.removeprefix('+soft_kill')
        name = name.removeprefix('+slip_surface')

        return max(name, name.rpartition('.')[0]).lower()

    Boundary_Surface_Name: StringProperty(
        name="Boundary Surface Name",
        description="Define the name of the boundary surface. This will be referenced in the structure_design tag.",
        get=get_boundary_surface_name,
        maxlen=32,
    )

    boundary_surface_items = [  ('_connected_geometry_boundary_surface_type_soft_ceiling', "Soft Ceiling", "Defines this mesh as soft ceiling"),
                                ('_connected_geometry_boundary_surface_type_soft_kill', "Soft Kill", "Defines this mesh as soft kill barrier"),
                                ('_connected_geometry_boundary_surface_type_slip_surface', "Slip Surface", "Defines this mesh as a slip surface"),
                                ]

    Boundary_Surface_Type : EnumProperty(
        name="Boundary Surface Type",
        options=set(),
        description="Set the type of boundary surface you want to create. You should only import files with this mesh type as struture_design tags",
        default = '_connected_geometry_boundary_surface_type_soft_ceiling',
        items=boundary_surface_items,
        )

    def get_boundary_surface(self):
        a_ob = bpy.context.active_object

        if a_ob.name.startswith('+soft_ceiling'):
            return 0
        elif a_ob.name.startswith('+soft_kill'):
            return 1
        elif a_ob.name.startswith('+slip_surface'):
            return 2
        else:
            return 0

    Boundary_Surface_Type_Locked : EnumProperty(
        name="Boundary Surface Type",
        options=set(),
        get=get_boundary_surface,
        description="Set the type of boundary surface you want to create. You should only import files with this mesh type as struture_design tags",
        default = '_connected_geometry_boundary_surface_type_soft_ceiling',
        items=boundary_surface_items,
        )
    

    poop_lighting_items = [ ('_connected_geometry_poop_lighting_default', "Default", "Sets the lighting policy automatically"),
                            ('_connected_geometry_poop_lighting_per_pixel', "Per Pixel", "Sets the lighting policy to per pixel. Can be forced on with the prefix: '%?'"),
                            ('_connected_geometry_poop_lighting_per_vertex', "Per Vertex", "Sets the lighting policy to per vertex. Can be forced on with the prefix: '%!'"),
                            ('_connected_geometry_poop_lighting_single_probe', "Single Probe", "Sets the lighting policy to single probe. Can be forced on with the prefix: '%>'"),
                            ('_connected_geometry_poop_lighting_per_vertex_ao', "Per Vertex AO", "H4+ only. Sets the lighting policy to per vertex ambient occlusion."),
                            ]


    #POOP PROPERTIES
    Poop_Lighting_Override : EnumProperty(
        name="Lighting Policy",
        options=set(),
        description="Sets the lighting policy for this instanced geometry",
        default = '_connected_geometry_poop_lighting_default',
        items=poop_lighting_items,
        )

    def get_poop_lighting_policy(self):
        if bpy.context.active_object.name.startswith(('%!',     '%-!','%+!','%*!',     '%-*!','%+*!',     '%*-!','%*+!')):
            return 1
        elif bpy.context.active_object.name.startswith(('%?',     '%-?','%+?','%*?',     '%-*?','%+*?',     '%*-?','%*+?')):
            return 2
        elif bpy.context.active_object.name.startswith(('%>',     '%->','%+>','%*>',     '%-*>','%+*>',     '%*->','%*+>')):
            return 3
        else:
            return 0 # else won't ever be hit, but adding it stops errors

    Poop_Lighting_Override_Locked : EnumProperty(
        name="Lighting Policy",
        options=set(),
        get=get_poop_lighting_policy,
        description="Sets the lighting policy for this instanced geometry",
        default = '_connected_geometry_poop_lighting_default',
        items=poop_lighting_items,
        )

    poop_lightmap_resolution_scale : FloatProperty( # H4+ only
        name="Lightmap Resolution Scale",
        options=set(),
        description="Sets lightmap resolutions scale for this instance",
        default = 1.0,
        min = 0.0
    )

    poop_pathfinding_items = [  ('_connected_poop_instance_pathfinding_policy_cutout', "Cutout", "Sets the pathfinding policy to cutout. AI will be able to pathfind around this mesh, but not on it."),
                                ('_connected_poop_instance_pathfinding_policy_none', "None", "Sets the pathfinding policy to none. This mesh will be ignored during pathfinding generation. Can be forced on with the prefix: '%-'"),
                                ('_connected_poop_instance_pathfinding_policy_static', "Static", "Sets the pathfinding policy to static. AI will be able to pathfind around and on this mesh. Can be forced on with the prefix: '%+'"),
                                ]

    Poop_Pathfinding_Override : EnumProperty(
        name="Instanced Geometry Pathfinding Override",
        options=set(),
        description="Sets the pathfinding policy for this instanced geometry",
        default = '_connected_poop_instance_pathfinding_policy_cutout',
        items=poop_pathfinding_items,
        )

    def get_poop_pathfinding_policy(self):
        if bpy.context.active_object.name.startswith(('%-',     '%!-','%?-','%>-','%*-',     '%!*-','%?*-','%>*-',     '%*!-','%*?-','%*>-')):
            return 1
        elif bpy.context.active_object.name.startswith(('%+',     '%!+','%?+','%>+','%*+',     '%!*+','%?*+','%>*+',     '%*!+','%*?+','%*>+')):
            return 2
        else:
            return 0 # else won't ever be hit, but adding it stops errors

    Poop_Pathfinding_Override_Locked : EnumProperty(
        name="Instanced Geometry Pathfinding Override",
        options=set(),
        get=get_poop_pathfinding_policy,
        description="Sets the pathfinding policy for this instanced geometry",
        default = '_connected_poop_instance_pathfinding_policy_cutout',
        items=poop_pathfinding_items,
        )

    Poop_Imposter_Policy : EnumProperty(
        name="Instanced Geometry Imposter Policy",
        options=set(),
        description="Sets the imposter policy for this instanced geometry",
        default = "_connected_poop_instance_imposter_policy_never",
        items=[ ('_connected_poop_instance_imposter_policy_polygon_default', "Polygon Default", ""),
                ('_connected_poop_instance_imposter_policy_polygon_high', "Polygon High", ""),
                ('_connected_poop_instance_imposter_policy_card_default', "Card Default", ""),
                ('_connected_poop_instance_imposter_policy_card_high', "Card High", ""),
                ('_connected_poop_instance_imposter_policy_none', "None", ""),
                ('_connected_poop_instance_imposter_policy_never', "Never", ""),
               ]
        )

    poop_imposter_brightness: FloatProperty( # h4+
        name="Imposter Brightness",
        options=set(),
        description="Sets the brightness of the imposter variant of this instance",
        default=0.0,
        min=0.0
    )

    Poop_Imposter_Transition_Distance: FloatProperty(
        name="Instanced Geometry Imposter Transition Distance",
        options=set(),
        description="The distance at which the instanced geometry transitions to its imposter variant",
        default=50,
    )

    Poop_Imposter_Transition_Distance_Auto: BoolProperty(
        name="Instanced Geometry Imposter Transition Automatic",
        options=set(),
        description="Enable to let the engine set the imposter transition distance by object size",
        default=True,
    )

    poop_streaming_priority : EnumProperty( # h4+
        name="Streaming Priority",
        options=set(),
        description="Sets the streaming priority for this instance",
        default = "_connected_geometry_poop_streamingpriority_default",
        items=[ ('_connected_geometry_poop_streamingpriority_default', "Default", ""),
                ('_connected_geometry_poop_streamingpriority_higher', "Higher", ""),
                ('_connected_geometry_poop_streamingpriority_highest', "Highest", ""),
               ]
        )

    # Poop_Imposter_Fade_Range_Start: IntProperty(
    #     name="Instanced Geometry Fade Start",
    #     options=set(),
    #     description="Start to fade in this instanced geometry when its bounding sphere is more than or equal to X pixels on the screen",
    #     default=36,
    #     subtype='PIXEL',
    # )

    # Poop_Imposter_Fade_Range_End: IntProperty(
    #     name="Instanced Geometry Fade End",
    #     options=set(),
    #     description="Renders this instanced geometry fully when its bounding sphere is more than or equal to X pixels on the screen",
    #     default=30,
    #     subtype='PIXEL',
    # )

    # Poop_Decomposition_Hulls: FloatProperty(
    #     name="Instanced Geometry Decomposition Hulls",
    #     options=set(),
    #     description="",
    #     default= 4294967295,
    # )
    
    # Poop_Predominant_Shader_Name: StringProperty(
    #     name="Instanced Geometry Predominant Shader Name",
    #     description="I have no idea what this does, but we'll write whatever you put here into the json file. The path should be relative and contain the shader extension (e.g. shader_relative_path\shader_name.shader)",
    #     maxlen=1024,
    # )

    Poop_Render_Only: BoolProperty(
        name ="Render Only",
        options=set(),
        description = "Instanced geometry set to render only",
        default = False,
    )

    def get_poop_render_only(self):
        if bpy.context.active_object.name.startswith(poop_render_only_prefixes):
            return True
        else:
            return False

    Poop_Render_Only_Locked: BoolProperty(
        name ="Render Only",
        options=set(),
        get=get_poop_render_only,
        description = "Instanced geometry set to render only",
        default = False,
    )

    Poop_Chops_Portals: BoolProperty(
        name ="Chops Portals",
        options=set(),
        description = "Instanced geometry set to chop portals",
        default = False,
    )

    Poop_Does_Not_Block_AOE: BoolProperty(
        name ="Does Not Block AOE",
        options=set(),
        description = "Instanced geometry set to not block area of effect forces",
        default = False,
    )

    Poop_Excluded_From_Lightprobe: BoolProperty(
        name ="Excluded From Lightprobe",
        options=set(),
        description = "Sets this instanced geometry to be exlcuded from any lightprobes",
        default = False,
    )

    Poop_Decal_Spacing: BoolProperty(
        name ="Decal Spacing",
        options=set(),
        description = "Instanced geometry set to have decal spacing (like decal_offset)",
        default = False,
    )

    Poop_Precise_Geometry: BoolProperty(
        name ="Precise Geometry",
        options=set(),
        description = "Instanced geometry set to not have its geometry altered in the BSP pass",
        default = False,
    )

    poop_remove_from_shadow_geometry: BoolProperty( # H4+
        name ="Remove From Shadow Geo",
        options=set(),
        description = "",
        default = False,
    )

    poop_disallow_lighting_samples: BoolProperty( # H4+
        name ="Disallow Lighting Samples",
        options=set(),
        description = "",
        default = False,
    )

    poop_rain_occluder: BoolProperty( # H4+
        name ="Rain Occluder",
        options=set(),
        description = "",
        default = False,
    )

    poop_cinematic_properties : EnumProperty( # h4+
        name="Cinematic Properties",
        options=set(),
        description="Sets whether the instance should render only in cinematics, only outside of cinematics, or in both environments",
        default = "_connected_geometry_poop_cinema_default",
        items=[ ('_connected_geometry_poop_cinema_default', "Default", "Include both in cinematics and outside of them"),
                ('_connected_geometry_poop_cinema_only', "Cinematic Only", "Only render in cinematics"),
                ('_connected_geometry_poop_cinema_exclude', "Exclude From Cinematics", "Do not render in cinematics"),
               ]
        )

    # poop light channel flags. Not included for now   

    Poop_Collision_Type: EnumProperty(
        name ="Instanced Collision Type",
        options=set(),
        description = "Set the instanced collision type. Only used when exporting a scenario",
        default = '_connected_geometry_poop_collision_type_default',
        items=[ ('_connected_geometry_poop_collision_type_default', 'Default', 'Collision mesh that interacts with the physics objects and with projectiles'),
                ('_connected_geometry_poop_collision_type_play_collision', 'Sphere Collision', 'The collision mesh affects physics objects, but not projectiles'),
                ('_connected_geometry_poop_collision_type_bullet_collision', 'Projectile', 'The collision mesh only interacts with projectiles'),
                ('_connected_geometry_poop_collision_type_invisible_wall', 'Invisible Wall', "Projectiles go through this but the physics objects can't. You cannot directly place objects on wall collision mesh in Sapien"),
            ]
    )

    #PORTAL PROPERTIES
    Portal_Type : EnumProperty(
        name="Portal Type",
        options=set(),
        description="Sets the type of portal this mesh should be",
        default = "_connected_geometry_portal_type_two_way",
        items=[ ('_connected_geometry_portal_type_no_way', "No Way", "Sets the portal to block all visibility"),
                ('_connected_geometry_portal_type_one_way', "One Way", "Sets the portal to block visibility from one direction"),
                ('_connected_geometry_portal_type_two_way', "Two Way", "Sets the portal to have visiblity from both sides"),
               ]
        )

    Portal_AI_Deafening: BoolProperty(
        name ="AI Deafening",
        options=set(),
        description = "Stops AI hearing through this portal",
        default = False,
    )

    Portal_Blocks_Sounds: BoolProperty(
        name ="Blocks Sounds",
        options=set(),
        description = "Stops sound from travelling past this portal",
        default = False,
    )

    Portal_Is_Door: BoolProperty(
        name ="Is Door",
        options=set(),
        description = "Portal visibility is attached to a device machine state",
        default = False,
    )

    #DECORATOR PROPERTIES

    def get_decorator_name(self):
        name = self.id_data.name
        name = name.removeprefix('+decorator')

        return max(name, name.rpartition('.')[0]).lower()

    Decorator_Name: StringProperty(
        name="Decorator Name",
        description="Name of your decorator",
        get=get_decorator_name,
    )

    Decorator_LOD: IntProperty(
        name="Decorator Level of Detail",
        options=set(),
        description="Level of detail objects to create expressed in an integer range of 1-4",
        default=1,
        min=1,
        max=4,
    )

    #SEAM PROPERTIES # commented out 03-11-2022 as seam name is something that can be infered at export
    # Seam_Name: StringProperty(
    #     name="Seam BSP Name",
    #     description="Name of the bsp associated with this seam", 
    #     maxlen=32,
    # )

    # def get_seam_name(self):
    #     a_ob = bpy.context.active_object
        
    #     var =  a_ob.name.rpartition(':')[2]
    #     return var[0:31]

    # Seam_Name_Locked: StringProperty(
    #     name="Seam BSP Name",
    #     description="Name of the bsp associated with this seam",
    #     get=get_seam_name,
    #     maxlen=32,
    # )

    #WATER VOLUME PROPERTIES
    Water_Volume_Depth: FloatProperty( # this something which can probably be automated?
        name="Water Volume Depth",
        options=set(),
        description="Set the depth of this water volume mesh",
        default=20,
    )
    Water_Volume_Flow_Direction: FloatProperty( # this something which can probably be automated?
        name="Water Volume Flow Direction",
        options=set(),
        description="Set the flow direction of this water volume mesh",
        min=-180,
        max=180,
    )

    Water_Volume_Flow_Velocity: FloatProperty(
        name="Water Volume Flow Velocity",
        options=set(),
        description="Set the flow velocity of this water volume mesh",
        default=20,
    )

    Water_Volume_Fog_Color: FloatVectorProperty(
        name="Water Volume Fog Color",
        options=set(),
        description="Set the fog color of this water volume mesh",
        default=(1.0, 1.0, 1.0),
        subtype='COLOR',
        min=0.0,
        max=1.0
    )

    Water_Volume_Fog_Murkiness: FloatProperty(
        name="Water Volume Fog Murkiness",
        options=set(),
        description="Set the fog murkiness of this water volume mesh",
        default=0.5,
        subtype='FACTOR',
        min=0.0,
        max=1.0
    )

    #FOG PROPERTIES
    Fog_Name: StringProperty(
        name="Fog Name",
        description="Name of this fog volume",
        maxlen=32,
    )

    Fog_Appearance_Tag: StringProperty(
        name="Fog Appearance Tag",
        description="Name of the tag defining the fog volumes appearance",
        maxlen=32,
    )

    Fog_Volume_Depth: FloatProperty(
        name="Fog Volume Depth",
        options=set(),
        description="Set the depth of the fog volume",
        default=20,
    )

    # OBB PROPERTIES (H4+)
    obb_volume_type : EnumProperty(
        name="OBB Type",
        options=set(),
        description="",
        default = "_connected_geometry_mesh_obb_volume_type_streamingvolume",
        items=[ ('_connected_geometry_mesh_obb_volume_type_streamingvolume', "Streaming Volume", ""),
                ('_connected_geometry_mesh_obb_volume_type_lightmapexclusionvolume', "Lightmap Exclusion Volume", ""),
               ]
        )
    #LIGHTMAP PROPERTIES
    Lightmap_Settings_Enabled: BoolProperty(
        name ="Enable to use lightmap settings",
        options=set(),
        description = "",
        default = False,
    )

    Lightmap_Additive_Transparency: FloatProperty(
        name="lightmap Additive Transparency",
        options=set(),
        description="",
        default=0.0,
        subtype='FACTOR',
        min=0.0,
        max=1.0
    )

    Lightmap_Ignore_Default_Resolution_Scale: BoolProperty(
        name ="Lightmap Resolution Scale",
        options=set(),
        description = "",
        default = False,
    )

    Lightmap_Resolution_Scale: IntProperty(
        name="Lightmap Resolution Scale",
        options=set(),
        description="",
        default=3,
        min=1,
    )

    lightmap_photon_fidelity : EnumProperty(
        name="Photon Fidelity",
        options=set(),
        description="H4+ only",
        default = "_connected_material_lightmap_photon_fidelity_normal",
        items=[ ('_connected_material_lightmap_photon_fidelity_normal', "Normal", ""),
                ('_connected_material_lightmap_photon_fidelity_medium', "Medium", ""),
                ('_connected_material_lightmap_photon_fidelity_high', "High", ""),
                ('_connected_material_lightmap_photon_fidelity_none', "None", ""),
               ]
        )

    # Lightmap_Chart_Group: IntProperty(
    #     name="Lightmap Chart Group",
    #     options=set(),
    #     description="",
    #     default=3,
    #     min=1,
    # )

    Lightmap_Type : EnumProperty(
        name="Lightmap Type",
        options=set(),
        description="Sets how this should be lit while lightmapping",
        default = "_connected_material_lightmap_type_per_pixel",
        items=[ ('_connected_material_lightmap_type_per_pixel', "Per Pixel", ""),
                ('_connected_material_lightmap_type_per_vertex', "Per Vetex", ""),
               ]
        )

    Lightmap_Transparency_Override: BoolProperty(
        name ="Lightmap Transparency Override",
        options=set(),
        description = "",
        default = False,
    )

    Lightmap_Analytical_Bounce_Modifier: FloatProperty(
        name="Lightmap Analytical Bounce Modifier",
        options=set(),
        description="",
        default=9999,
    )
    
    Lightmap_General_Bounce_Modifier: FloatProperty(
        name="Lightmap General Bounce Modifier",
        options=set(),
        description="",
        default=9999,
    )

    Lightmap_Translucency_Tint_Color: FloatVectorProperty(
        name="Lightmap Translucency Tint Color",
        options=set(),
        description="",
        default=(1.0, 1.0, 1.0),
        subtype='COLOR',
        min=0.0,
        max=1.0
    )

    Lightmap_Lighting_From_Both_Sides: BoolProperty(
        name ="Lightmap Lighting From Both Sides",
        options=set(),
        description = "",
        default = False,
    )

    #MATERIAL LIGHTING PROPERTIES
    Material_Lighting_Enabled: BoolProperty(
        name="Toggle whether to use material lighting settings",
        options=set(),
        description="",
        default=False,
    )

    Material_Lighting_Attenuation_Cutoff: FloatProperty(
        name="Material Lighting Attenuation Cutoff",
        options=set(),
        description="Determines how far light travels before it stops",
        min=0,
        default=200,
    )

    Material_Lighting_Attenuation_Falloff: FloatProperty(
        name="Material Lighting Attenuation Falloff",
        options=set(),
        description="Determines how far light travels before its power begins to falloff",
        min=0,
        default=100,
    )

    Material_Lighting_Emissive_Focus: FloatProperty(
        name="Material Lighting Emissive Focus",
        options=set(),
        description="",
    )

    Material_Lighting_Emissive_Color: FloatVectorProperty(
        name="Material Lighting Emissive Color",
        options=set(),
        description="",
        default=(1.0, 1.0, 1.0),
        subtype='COLOR',
        min=0.0,
        max=1.0,
    )

    Material_Lighting_Emissive_Per_Unit: BoolProperty(
        name ="Material Lighting Emissive Per Unit",
        options=set(),
        description = "",
        default = False,
    )

    Material_Lighting_Emissive_Power: FloatProperty(
        name="Material Lighting Emissive Quality",
        options=set(),
        description="",
        min=0,
        default=100,
    )

    Material_Lighting_Emissive_Quality: FloatProperty(
        name="Material Lighting Emissive Quality",
        options=set(),
        description="",
        default=1,
        min=0,
    )

    Material_Lighting_Use_Shader_Gel: BoolProperty(
        name ="Material Lighting Use Shader Gel",
        options=set(),
        description = "",
        default = False,
    )

    Material_Lighting_Bounce_Ratio: FloatProperty(
        name="Material Lighting Bounce Ratio",
        options=set(),
        description="",
        default=1,
        min=0,
    )

    def get_markertype_enum(self):
        if self.id_data.name.startswith('?'):
            return 2
        else:
            return 0

    marker_types = [ ('_connected_geometry_marker_type_model', "Model", "Default marker type. Defines render_model markers for models, and structure markers for bsps"),
                ('_connected_geometry_marker_type_effects', "Effects", "Marker for effects only."),
                ('_connected_geometry_marker_type_game_instance', "Game Instance", "Game Instance marker"),
                ('_connected_geometry_marker_type_garbage', "Garbage", "marker to define position that garbage pieces should be created"),
                ('_connected_geometry_marker_type_hint', "Hint", "Used for ai hints"),
                ('_connected_geometry_marker_type_pathfinding_sphere', "Pathfinding Sphere", "Used to create ai pathfinding spheres"),
                ('_connected_geometry_marker_type_physics_constraint', "Physics Constraint", "Used to define various types of physics constraints"),
                ('_connected_geometry_marker_type_target', "Target", "Defines the markers used in a model's targets'"),
                ('_connected_geometry_marker_type_water_volume_flow', "Water Volume Flow", "Used to define water flow for water physics volumes. For structure_design tags only"),
               ]

    #MARKER PROPERTIES
    ObjectMarker_Type : EnumProperty(
        name="Marker Type",
        options=set(),
        description="Select the marker type",
        default = "_connected_geometry_marker_type_model",
        items=marker_types,
        )

    ObjectMarker_Type_Locked : EnumProperty(
        name="Marker Type",
        options=set(),
        description="Select the marker type",
        default = "_connected_geometry_marker_type_model",
        get=get_markertype_enum,
        items=marker_types,
        )
    
    # h4 versions
    marker_types_h4 = [ ('_connected_geometry_marker_type_model', "Model", "Default marker type. Defines render_model markers for models, and structure markers for bsps"),
                ('_connected_geometry_marker_type_effects', "Effects", "Marker for effects only."),
                ('_connected_geometry_marker_type_game_instance', "Game Instance", "Game Instance marker. Can be set with the prefix: ?"),
                ('_connected_geometry_marker_type_garbage', "Garbage", "marker to define position that garbage pieces should be created"),
                ('_connected_geometry_marker_type_hint', "Hint", "Used for ai hints"),
                ('_connected_geometry_marker_type_pathfinding_sphere', "Pathfinding Sphere", "Used to create ai pathfinding spheres"),
                ('_connected_geometry_marker_type_physics_constraint', "Physics Constraint", "Used to define various types of physics constraints"),
                ('_connected_geometry_marker_type_target', "Target", "Defines the markers used in a model's targets'"),
                ('_connected_geometry_marker_type_water_volume_flow', "Water Volume Flow", "Used to define water flow for water physics volumes. For structure_design tags only"),
                ('_connected_geometry_marker_type_airprobe', "Airprobe", "Airprobes tell the game how to handle static lighting on dynamic objects"),
                ('_connected_geometry_marker_type_envfx', "Environment Effect", "Plays an effect on this point in the structure"),
                ('_connected_geometry_marker_type_lightCone', "Light Cone", "Creates a light cone with the defined parameters"),
               ]

    ObjectMarker_Type_H4 : EnumProperty(
        name="Marker Type",
        options=set(),
        description="Select the marker type",
        default = "_connected_geometry_marker_type_model",
        items=marker_types_h4,
        )

    ObjectMarker_Type_Locked_H4 : EnumProperty(
        name="Marker Type",
        options=set(),
        description="Select the marker type",
        default = "_connected_geometry_marker_type_model",
        get=get_markertype_enum,
        items=marker_types_h4,
        )
    
    def get_marker_group_name(self):
        name = self.id_data.name
        name = name.removeprefix('#')
        if name.rpartition('.')[0] != '':
            name = name.rpartition('.')[0]

        return max(name, name.rpartition('.')[0]).lower()

    Marker_Group_Name: StringProperty(
        name="Marker Group",
        description="Displays the name of the marker group. Marker groups equal the object name minus the '#' prefix and text after the last '.', allowing for multiple markers to share the same group",
        get=get_marker_group_name,
    )

    Marker_Region: StringProperty(
        name="Marker Group",
        description="Define the name of marker region. This should match a face region name. Leave blank for the 'default' region",
    )

    Marker_All_Regions: BoolProperty(
        name="Marker All Regions",
        options=set(),
        description="Associate this marker with all regions rather than a specific one",
    )

    def game_instance_clean_tag_path(self, context):
        self['Marker_Game_Instance_Tag_Name'] = clean_tag_path(self['Marker_Game_Instance_Tag_Name']).strip('"')

    Marker_Game_Instance_Tag_Name: StringProperty(
        name="Marker Game Instance Tag",
        description="Define the name of the marker game instance tag",
        update=game_instance_clean_tag_path,
    )

    Marker_Game_Instance_Tag_Variant_Name: StringProperty(
        name="Marker Game Instance Tag Variant",
        description="Define the name of the marker game instance tag variant",
    )

    marker_game_instance_run_scripts: BoolProperty(
        name="Always Run Scripts",
        options=set(),
        description="Tells this game instance object to always run scripts if it has any",
        default=True
    )

    marker_hint_length: FloatProperty(
        name="Hint Length",
        options=set(),
        description="",
        default=0.0,
        min=0.0,
    )

    Marker_Velocity: FloatVectorProperty(
        name="Marker Velocity",
        options=set(),
        description="",
        subtype='VELOCITY',
    )

    Marker_Pathfinding_Sphere_Vehicle: BoolProperty(
        name="Vehicle Only Pathfinding Sphere",
        options=set(),
        description="This pathfinding sphere only affects vehicles",
    )

    Pathfinding_Sphere_Remains_When_Open: BoolProperty(
        name="Pathfinding Sphere Remains When Open",
        options=set(),
        description="Pathfinding sphere remains even when a machine is open",
    )

    Pathfinding_Sphere_With_Sectors: BoolProperty(
        name="Pathfinding Sphere With Sectors",
        options=set(),
        description="Not sure",
    )

    Physics_Constraint_Parent: StringProperty( #need to make this into an object picker at some point
        name="Physics Constraint Parent",
        description="Enter the name of the object that is this marker's parent",
    )

    Physics_Constraint_Child: StringProperty( #need to make this into an object picker at some point
        name="Physics Constraint Child",
        description="Enter the name of the object that is this marker's child",
    )

    Physics_Constraint_Type : EnumProperty(
        name="Constraint Type",
        options=set(),
        description="Select the physics constraint type",
        default = "_connected_geometry_marker_type_physics_hinge_constraint",
        items=[ ('_connected_geometry_marker_type_physics_hinge_constraint', "Hinge", ""),
                ('_connected_geometry_marker_type_physics_socket_constraint', "Socket", ""),
               ]
        )

    Physics_Constraint_Uses_Limits: BoolProperty(
        name="Physics Constraint Uses Limits",
        options=set(),
        description="Set whether the limits of this physics constraint should be constrained or not",
    )

    Hinge_Constraint_Minimum: FloatProperty(
        name="Hinge Constraint Minimum",
        options=set(),
        description="Set the minimum rotation of a physics hinge",
        default=-180,
        min=-180,
        max=180,
    )

    Hinge_Constraint_Maximum: FloatProperty(
        name="Hinge Constraint Maximum",
        options=set(),
        description="Set the maximum rotation of a physics hinge",
        default=180,
        min=-180,
        max=180,
    )

    Cone_Angle: FloatProperty(
        name="Cone Angle",
        options=set(),
        description="Set the cone angle",
        default=90,
        min=0,
        max=180,
    )

    Plane_Constraint_Minimum: FloatProperty(
        name="Plane Constraint Minimum",
        options=set(),
        description="Set the minimum rotation of a physics plane",
        default=-90,
        min=-90,
        max=0,
    )

    Plane_Constraint_Maximum: FloatProperty(
        name="Plane Constraint Maximum",
        options=set(),
        description="Set the maximum rotation of a physics plane",
        default=90,
        min=-0,
        max=90,

    )

    Twist_Constraint_Start: FloatProperty(
        name="Twist Constraint Minimum",
        options=set(),
        description="Set the starting angle of a twist constraint",
        default=-180,
        min=-180,
        max=180,
    )

    Twist_Constraint_End: FloatProperty(
        name="Twist Constraint Maximum",
        options=set(),
        description="Set the ending angle of a twist constraint",
        default=180,
        min=-180,
        max=180,
    )

    marker_looping_effect: StringProperty(
        name="Effect Path",
        description="Tag path to an effect",
    )

    marker_light_cone_tag: StringProperty(
        name="Light Cone Tag Path",
        description="Tag path to a light cone",
    )

    marker_light_cone_color: FloatVectorProperty(
        name="Light Cone Color",
        options=set(),
        description="",
        default=(1.0, 1.0, 1.0),
        subtype='COLOR',
        min=0.0,
        max=1.0,
    )

    marker_light_cone_alpha: FloatProperty(
        name="Light Cone Alpha",
        options=set(),
        description="",
        default=1.0,
        subtype='FACTOR',
        min=0.0,
        max=1.0,
    )

    marker_light_cone_width: FloatProperty(
        name="Light Cone Width",
        options=set(),
        description="",
        default=5,
        min=0,
    )

    marker_light_cone_length: FloatProperty(
        name="Light Cone Length",
        options=set(),
        description="",
        default=10,
        min=0,
    )

    marker_light_cone_intensity: FloatProperty(
        name="Light Cone Intensity",
        options=set(),
        description="",
        default=1,
        min=0,
    )

    marker_light_cone_curve: StringProperty(
        name="Light Cone Curve Tag Path",
        description="",
    )

# LIGHTS #


    light_type_override: EnumProperty(
        name = "Light Type",
        options=set(),
        description = "Displays the light type. Use the blender light types to change the value of this field",
        default = "_connected_geometry_light_type_omni",
        items=[ ('_connected_geometry_light_type_spot', "Spot", ""),
                ('_connected_geometry_light_type_directional', "Directional", ""),
                ('_connected_geometry_light_type_omni', "Point", ""),
               ]
        )

    Light_Game_Type: EnumProperty(
        name = "Light Game Type",
        options=set(),
        description = "",
        default = "_connected_geometry_bungie_light_type_default",
        items=[ ('_connected_geometry_bungie_light_type_default', "Default", ""),
                ('_connected_geometry_bungie_light_type_inlined', "Inlined", ""),
                ('_connected_geometry_bungie_light_type_rerender', "Rerender", ""),
                ('_connected_geometry_bungie_light_type_screen_space', "Screen Space", ""),
                ('_connected_geometry_bungie_light_type_uber', "Uber", ""),
               ]
        )

    Light_Shape: EnumProperty(
        name = "Light Shape",
        options=set(),
        description = "",
        default = "_connected_geometry_light_shape_circle",
        items=[ ('_connected_geometry_light_shape_circle', "Circle", ""),
                ('_connected_geometry_light_shape_rectangle', "Rectangle", ""),
               ]
        )

    Light_Near_Attenuation: BoolProperty(
        name="Light Uses Near Attenuation",
        options=set(),
        description="",
        default=True,
    )

    Light_Far_Attenuation: BoolProperty(
        name="Light Uses Far Attenuation",
        options=set(),
        description="",
        default=True,
    )

    Light_Near_Attenuation_Start: FloatProperty(
        name="Light Near Attenuation Start Distance",
        options=set(),
        description="The power of the light remains zero up until this point",
        default=0,
        min=0,
    )

    Light_Near_Attenuation_End: FloatProperty(
        name="Light Near Attenuation End Distance",
        options=set(),
        description="From the starting near attenuation, light power gradually increases up until the end point",
        default=0,
        min=0,
    )

    Light_Far_Attenuation_Start: FloatProperty(
        name="Light Near Attenuation Start Distance",
        options=set(),
        description="After this point, the light will begin to lose power",
        default=500,
        min=0,
    )

    Light_Far_Attenuation_End: FloatProperty(
        name="Light Near Attenuation Start Distance",
        options=set(),
        description="From the far attenuation start, the light will gradually lose power until it reaches zero by the end point",
        default=1000,
        min=0,
    )

    Light_Volume_Distance: FloatProperty(
        name="Light Volume Distance",
        options=set(),
        description="",
    )

    Light_Volume_Intensity: FloatProperty(
        name="Light Volume Intensity",
        options=set(),
        description="",
        default=1.0,
        min=0.0,
        soft_max=10.0,
        subtype='FACTOR',
    )

    Light_Fade_Start_Distance: FloatProperty(
        name="Light Fade Out Start",
        options=set(),
        description="The light starts to fade out when the camera is x world units away",
        default=100.0,
    )

    Light_Fade_End_Distance: FloatProperty(
        name="Light Fade Out End",
        options=set(),
        description="The light completely fades out when the camera is x world units away",
        default=150.0,
    )

    Light_Ignore_BSP_Visibility: BoolProperty(
        name="Light Ignore BSP Visibility",
        options=set(),
        description="",
        default=False,
    )

    def set_blend_light_color(self, context):
        ob = self.id_data
        if ob.type == 'LIGHT':
            ob.data.color = self.Light_Color

    Light_Color: FloatVectorProperty(
        name="Light Color",
        options=set(),
        description="",
        default=(1.0, 1.0, 1.0),
        subtype='COLOR',
        min=0.0,
        max=1.0,
        update=set_blend_light_color,
    )

    Light_Intensity: FloatProperty(
        name="Light Intensity",
        options=set(),
        description="",
        default=1,
        min=0.0,
        soft_max=10.0,
        subtype='FACTOR',
    )

    Light_Use_Clipping: BoolProperty(
        name="Light Uses Clipping",
        options=set(),
        description="",
        default=False,
    )

    Light_Clipping_Size_X_Pos: FloatProperty(
        name="Light Clipping Size X Forward",
        options=set(),
        description="",
        default=100,
    )

    Light_Clipping_Size_Y_Pos: FloatProperty(
        name="Light Clipping Size Y Forward",
        options=set(),
        description="",
        default=100,
    )

    Light_Clipping_Size_Z_Pos: FloatProperty(
        name="Light Clipping Size Z Forward",
        options=set(),
        description="",
        default=100,
    )

    Light_Clipping_Size_X_Neg: FloatProperty(
        name="Light Clipping Size X Backward",
        options=set(),
        description="",
        default=100,
    )

    Light_Clipping_Size_Y_Neg: FloatProperty(
        name="Light Clipping Size Y Backward",
        options=set(),
        description="",
        default=100,
    )

    Light_Clipping_Size_Z_Neg: FloatProperty(
        name="Light Clipping Size Z Backward",
        options=set(),
        description="",
        default=100,
    )

    Light_Hotspot_Size: FloatProperty(
        name="Light Hotspot Size",
        options=set(),
        description="",
        default=25,
    )

    Light_Hotspot_Falloff: FloatProperty(
        name="Light Hotspot Size",
        options=set(),
        description="",
        default=80,
    )

    Light_Falloff_Shape: FloatProperty(
        name="Light Falloff Shape",
        options=set(),
        description="",
        default=1,
        min=0.0,
        soft_max=10.0,
        subtype='FACTOR',
    )

    Light_Aspect: FloatProperty(
        name="Light Aspect",
        options=set(),
        description="",
        default=1,
        min=0.0,
        max=1.0,
        subtype='FACTOR',
    )

    Light_Frustum_Width: FloatProperty(
        name="Light Hotspot Size",
        options=set(),
        description="",
        default=1.0,
    )

    Light_Frustum_Height: FloatProperty(
        name="Light Hotspot Size",
        options=set(),
        description="",
        default=1.0,
    )

    Light_Bounce_Ratio: FloatProperty(
        name="Light Falloff Shape",
        options=set(),
        description="",
        default=1,
        min=0.0,
        max=1.0,
        subtype='FACTOR',
    )

    Light_Dynamic_Has_Bounce: BoolProperty(
        name="Light Has Dynamic Bounce",
        options=set(),
        description="",
        default=False,
    )

    Light_Screenspace_Has_Specular: BoolProperty(
        name="Screenspace Light Has Specular",
        options=set(),
        description="",
        default=False,
    )

    Light_Tag_Override: StringProperty(
        name="Light Tag Override",
        options=set(),
        description="",
        maxlen=128,
    )

    Light_Shader_Reference: StringProperty(
        name="Light Shader Reference",
        options=set(),
        description="",
        maxlen=128,
    )

    Light_Gel_Reference: StringProperty(
        name="Light Gel Reference",
        options=set(),
        description="",
        maxlen=128,
    )

    Light_Lens_Flare_Reference: StringProperty(
        name="Light Lens Flare Reference",
        options=set(),
        description="",
        maxlen=128,
    )

    # H4 LIGHT PROPERTIES
    light_dynamic_shadow_quality: EnumProperty(
        name = "Shadow Quality",
        options=set(),
        description = "",
        default = "_connected_geometry_dynamic_shadow_quality_normal",
        items=[ ('_connected_geometry_dynamic_shadow_quality_normal', "Normal", ""),
                ('_connected_geometry_dynamic_shadow_quality_expensive', "Expensive", ""),
               ]
        )

    light_specular_contribution: BoolProperty(
        name="Specular Contribution",
        options=set(),
        description="",
        default=False,
    )

    light_amplification_factor: FloatProperty(
        name="Indirect Amplification",
        options=set(),
        description="",
        default=0.5,
        subtype='FACTOR',
        min=0.0,
        max=1.0
    )

    light_attenuation_near_radius: FloatProperty(
        name="Near Attenuation Radius",
        options=set(),
        description="",
        default=0,
        min=0.0,
    )

    light_attenuation_far_radius: FloatProperty(
        name="Far Attenuation Radius",
        options=set(),
        description="",
        default=0,
        min=0.0,
    )

    light_attenuation_power: FloatProperty(
        name="Attenuation Power",
        options=set(),
        description="",
        default=0,
        min=0.0,
    )

    light_cinema_objects_only: BoolProperty( 
        name="Only Light Cinematic Objects",
        options=set(),
        description="",
        default=False,
    )

    light_tag_name: StringProperty(
        name="Light Tag Name",
        options=set(),
        description="",
    )

    light_type_h4: EnumProperty(
        name = "Light Type",
        options=set(),
        description = "",
        default = "_connected_geometry_light_type_point",
        items=[ ('_connected_geometry_light_type_point', "Point", ""),
                ('_connected_geometry_light_type_spot', "Spot", ""),
                ('_connected_geometry_light_type_directional', "Directional", ""),
                ('_connected_geometry_light_type_sun', "Sun", ""),
               ]
        )

    light_outer_cone_angle: FloatProperty(
        name="Outer Cone Angle",
        options=set(),
        description="",
        default=80,
        min=0.0,
        max=160.0
    )

    light_lighting_mode: EnumProperty(
        name = "Lighting Mode",
        options=set(),
        description = "",
        default = "_connected_geometry_lighting_mode_artistic",
        items=[ ('_connected_geometry_lighting_mode_artistic', "Artistic", ""),
                ('_connected_geometry_lighting_physically_correct', "Physically Correct", ""),
               ]
        )

    light_specular_power: FloatProperty(
        name="Specular Power",
        options=set(),
        description="",
        default=32,
        min=0.0,
    )

    light_specular_intensity: FloatProperty(
        name="Specular Intensity",
        options=set(),
        description="",
        default=0,
        min=0.0,
    )

    light_inner_cone_angle: FloatProperty(
        name="Inner Cone Angle",
        options=set(),
        description="",
        default=50,
        min=0.0,
        max=160
    )

    light_cinema: EnumProperty(
        name="Cinematic Render",
        options=set(),
        description="Define whether this light should only render in cinematics, outside of cinematics, or always render",
        default='_connected_geometry_lighting_cinema_default',
        items=[ ('_connected_geometry_lighting_cinema_default', "Always", ""),
                ('_connected_geometry_lighting_cinema_only', "Cinematics Only", ""),
                ('_connected_geometry_lighting_cinema_exclude', "Exclude from Cinematics", ""),
               ]
        )

    light_cone_projection_shape: EnumProperty(
        name="Cone Projection Shape",
        options=set(),
        description = "",
        default = "_connected_geometry_cone_projection_shape_cone",
        items=[ ('_connected_geometry_cone_projection_shape_cone', "Cone", ""),
                ('_connected_geometry_cone_projection_shape_frustum', "Frustum", ""),
               ]
        )

    light_shadow_near_clipplane: FloatProperty(
        name="Shadow Near Clip Plane",
        options=set(),
        description="",
        default=0,
        min=0.0,
    )

    light_jitter_sphere_radius: FloatProperty(
        name="Light Jitter Sphere Radius",
        options=set(),
        description="",
        default=2.5,
        min=0.0,
    )

    light_shadow_far_clipplane: FloatProperty(
        name="Shadow Far Clip Plane",
        options=set(),
        description="",
        default=0,
        min=0.0,
    )

    light_shadow_bias_offset: FloatProperty(
        name="Shadow Bias Offset",
        options=set(),
        description="",
        default=0,
        min=0.0,
    )

    light_shadow_color: FloatVectorProperty(
        name="Shadow Color",
        options=set(),
        description="",
        default=(0.0, 0.0, 0.0),
        subtype='COLOR',
        min=0.0,
        max=1.0,
    )

    light_shadows: BoolProperty(
        name="Has Shadows",
        options=set(),
        description="",
        default=True,
    )

    light_sub_type: EnumProperty(
        name="Light Sub-Type",
        options=set(),
        description="",
        default='_connected_geometry_lighting_sub_type_default',
        items=[ ('_connected_geometry_lighting_sub_type_default', "Default", ""),
                ('_connected_geometry_lighting_sub_type_screenspace', "Screenspace", ""),
                ('_connected_geometry_lighting_sub_type_uber', "Uber", ""),
               ]
        )  

    light_ignore_dynamic_objects: BoolProperty(
        name="Ignore Dynamic Objects",
        options=set(),
        description="",
        default=False,
    )

    light_diffuse_contribution: BoolProperty(
        name="Diffuse Contribution",
        options=set(),
        description="",
        default=True,
    )

    light_destroy_after: FloatProperty(
        name="Destroy After (seconds)",
        options=set(),
        description="Destroy the light after x seconds. 0 means the light is never destroyed",
        subtype='TIME',
        unit='TIME',
        step=100,
        default=0,
        min=0.0,
    )

    light_jitter_angle: FloatProperty(
        name="Light Jitter Angle",
        options=set(),
        description="",
        default=0,
        min=0.0,
    )

    light_jitter_quality: EnumProperty(
        name="Light Jitter Quality",
        options=set(),
        description="",
        default='_connected_geometry_light_jitter_quality_low',
        items=[ ('_connected_geometry_light_jitter_quality_low', "Low", ""),
                ('_connected_geometry_light_jitter_quality_medium', "Medium", ""),
                ('_connected_geometry_light_jitter_quality_high', "High", ""),
               ]
        )

    light_indirect_only: BoolProperty(
        name="Indirect Only",
        options=set(),
        description="",
        default=False,
    )

    light_screenspace: BoolProperty(
        name="Screenspace Light",
        options=set(),
        description="",
        default=False,
    )

    light_intensity_off: BoolProperty(
        name="Set Via Tag",
        options=set(),
        description="Stops this value being passed to the game. Use if you want to set the intensity manually in the tag (such as if you want to make use of functions for lights)",
        default=False,
    )

    near_attenuation_end_off: BoolProperty(
        name="Set Via Tag",
        options=set(),
        description="Stops this value being passed to the game. Use if you want to set the near attenuation end manually in the tag (such as if you want to make use of functions for lights)",
        default=False,
    )

    outer_cone_angle_off: BoolProperty(
        name="Set Via Tag",
        options=set(),
        description="Stops this value being passed to the game. Use if you want to set the outer cone angle manually in the tag (such as if you want to make use of functions for lights)",
        default=False,
    )

    manual_fade_distance: BoolProperty(
        name="Specify Fade Out Distance",
        options=set(),
        description="Reveals fade out distance settings",
        default=False,
    )

    light_static_analytic: BoolProperty(
        name="Static Analytic",
        options=set(),
        description="",
        default=False,
    )

    light_mode: EnumProperty(
        name="Light Mode",
        options=set(),
        description="",
        default='_connected_geometry_light_mode_static',
        items=[ ('_connected_geometry_light_mode_static', "Static", ""),
                ('_connected_geometry_light_mode_dynamic', "Dynamic", ""),
                ('_connected_geometry_light_mode_analytic', "Analytic", ""),
               ]
        )

    Light_Near_Attenuation_StartH4: FloatProperty(
        name="Attenuation Start Distance",
        options=set(),
        description="",
        default=0.2,
        min=0,
    )

    Light_Near_Attenuation_EndH4: FloatProperty(
        name="Attenuation End Distance",
        options=set(),
        description="",
        default=10,
        min=0,
    )

    Light_Far_Attenuation_StartH4: FloatProperty(
        name="Camera Distance Fade Start",
        options=set(),
        description="",
        default=0,
        min=0,
    )

    Light_Far_Attenuation_EndH4: FloatProperty(
        name="Camera Distance Fade End",
        options=set(),
        description="",
        default=0,
        min=0,
    )

    def set_blend_light_intensity_h4(self, context):
        ob = self.id_data
        if ob.type == 'LIGHT':
            ob.data.energy = self.Light_IntensityH4 * 10 * context.scene.unit_settings.scale_length ** -2 # mafs. Gets around unit scale altering the light intensity to unwanted values

    Light_IntensityH4: FloatProperty(
        name="Light Intensity",
        options=set(),
        description="",
        default=50,
        min=0.0,
        update=set_blend_light_intensity_h4
    )

class NWO_MaterialPropertiesGroup(PropertyGroup):
    
    def update_shader_type(self, context):
        material_path = self.shader_path.replace('"','')
        if material_path != material_path.rpartition('.')[2]:
            try:
                self.Shader_Type = material_path.rpartition('.')[2]
            except:
                self.Shader_Type = 'shader'

    shader_path: StringProperty(
        name = "Shader Path",
        description = "Define the path to a shader. This can either be a relative path, or if you have added your Editing Kit Path to add on preferences, the full path. Including the file extension will automatically update the shader type",
        default = "",
        update=update_shader_type,
        )

    shader_types = [ ('shader', "Shader", ""),
                ('shader_cortana', "Shader Cortana", ""),
                ('shader_custom', "Shader Custom", ""),
                ('shader_decal', "Shader Decal", ""),
                ('shader_foliage', "Shader Foliage", ""),
                ('shader_fur', "Shader Fur", ""),
                ('shader_fur_stencil', "Shader Fur Stencil", ""),
                ('shader_glass', "Shader Glass", ""),
                ('shader_halogram', "Shader Halogram", ""),
                ('shader_mux', "Shader Mux", ""),
                ('shader_mux_material', "Shader Mux Material", ""),
                ('shader_screen', "Shader Screen", ""),
                ('shader_skin', "Shader Skin", ""),
                ('shader_terrain', "Shader Terrain", ""),
                ('shader_water', "Shader Water", ""),
               ]

    Shader_Type: EnumProperty(
        name = "Shader Type",
        options=set(),
        description = "Set by the extension of the shader path. Alternatively this field can be updated manually",
        default = "shader",
        items=shader_types,
        )

    material_items = [  ('none', "None", "None"),
                        ('+portal', "Portal", "Force all faces with this material to be portals"),
                        ('+seamsealer', "Seamsealer", "Force all faces with this material to be seamsealer"),
                        ('+sky', "Sky", "Force all faces with this material to be sky"),
                        ]

    material_override: EnumProperty(
        name = "Material Override",
        options=set(),
        description = "Select to override the shader path with a special material type e.g. sky / seamsealer",
        default = "none",
        items=material_items,
        )

    def material_name_is_special(self):
        if self.id_data.name.lower().startswith('+portal'):
            return 1
        elif self.id_data.name.lower().startswith('+seamsealer'):
            return 2
        elif self.id_data.name.lower().startswith('+sky'):
            return 3
        else:
            return 1

    material_override_locked: EnumProperty(
        name = "Material Override",
        options=set(),
        get=material_name_is_special,
        description = "Select to override the shader path with a special material type e.g. sky / seamsealer",
        default = "none",
        items=material_items,
        )

    def material_name_is_special_h4(self):
        if self.id_data.name.lower().startswith('+sky'):
            return 1
        elif self.id_data.name.lower().startswith('+physics'):
            return 2
        elif self.id_data.name.lower().startswith('+seam'):
            return 3
        elif self.id_data.name.lower().startswith('+portal'):
            return 4
        elif self.id_data.name.lower().startswith('+collision'):
            return 5
        elif self.id_data.name.lower().startswith('+player_collision'):
            return 6
        elif self.id_data.name.lower().startswith('+wall_collision'):
            return 7
        elif self.id_data.name.lower().startswith('+cookie_cutter'):
            return 8
        elif self.id_data.name.lower().startswith('+bullet_collision'):
            return 9
        elif self.id_data.name.lower().startswith('+rain_blocker'):
            return 10
        elif self.id_data.name.lower().startswith('+water_volume'):
            return 11
        elif self.id_data.name.lower().startswith('+structure'):
            return 12
        elif self.id_data.name.lower().startswith('+override'):
            return 13
        else:
            return 0

    material_items_h4 = [
                        ('none', "None", "None"),  
                        ('InvisibleSky', "Sky", "None"),
                        ('Physics', 'Physics', ''),
                        ('Seam', "Seam", ""),
                        ('Portal', "Portal", ""),
                        ('Collision', "Collision", ""),
                        ('playCollision', "Player Collision", ""),
                        ('wallCollision', "Wall Collision", ""),
                        ('bulletCollision', "Bullet Collision", ""),
                        ('CookieCutter', "Cookie Cutter", ""),
                        ('rainBlocker', "Rain Blocker", ""),
                        ('waterVolume', "Water Volume", ""),
                        ('Structure', "Structure", ""),
                        ]

    material_override_h4 : EnumProperty(
        name = "Material Override",
        options=set(),
        description = "Select to override the shader path with a special material type",
        default = "none",
        items=material_items_h4,
        )

    material_override_h4_locked : EnumProperty(
        name = "Material Override",
        options=set(),
        get=material_name_is_special_h4,
        default = 'none',
        items=material_items_h4,
    )

class NWO_BonePropertiesGroup(PropertyGroup):

    frame_id1: StringProperty(
        name = "Frame ID 1",
        description = "The Frame ID 1 for this bone. Leave blank for automatic assignment of a Frame ID. Can be manually edited when using expert mode, but don't do this unless you know what you're doing",
        default = "",
        )
    frame_id2: StringProperty(
        name = "Frame ID 2",
        description = "The Frame ID 1 for this bone. Leave blank for automatic assignment of a Frame ID. Can be manually edited when using expert mode, but don't do this unless you know what you're doing",
        default = "",
        )
    object_space_node: BoolProperty(
        name = "Object Space Offset Node",
        description = "",
        default = False,
        options=set(),
        )
    replacement_correction_node: BoolProperty(
        name = "Replacement Correction Node",
        description = "",
        default = False,
        options=set(),
        )
    fik_anchor_node: BoolProperty(
        name = "Forward IK Anchor Node",
        description = "",
        default = False,
        options=set(),
        )

classeshalo = (
    ASS_JMS_MeshPropertiesGroup,
    ASS_JMS_MaterialPropertiesGroup,
    Halo_MeshProps,
    ASS_JMS_MeshProps,
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
    Halo_SetUnitScale,
    Halo_XREFPath,
    NWO_GameInstancePath,
    NWO_ObjectProps,
    NWO_ObjectMeshProps,
    NWO_ObjectMeshFaceProps,
    NWO_ObjectMeshMaterialLightingProps,
    NWO_ObjectMeshLightmapProps,
    NWO_ObjectMarkerProps,
    NWO_MaterialProps,
    NWO_ObjectPropertiesGroup,
    NWO_MaterialPropertiesGroup,
    NWO_LightProps,
    NWO_BoneProps,
    NWO_BonePropertiesGroup,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.Light.halo_light = PointerProperty(type=ASS_LightPropertiesGroup, name="ASS Properties", description="Set properties for your light")
    bpy.types.Mesh.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.Material.ass_jms = PointerProperty(type=ASS_JMS_MaterialPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your materials")
    bpy.types.Scene.halo = PointerProperty(type=Halo_ScenePropertiesGroup, name="Halo Scene Properties", description="Set properties for your scene")
    bpy.types.Object.nwo = PointerProperty(type=NWO_ObjectPropertiesGroup, name="Halo NWO Properties", description="Set Halo Object Properties")
    bpy.types.Material.nwo = PointerProperty(type=NWO_MaterialPropertiesGroup, name="Halo NWO Properties", description="Set Halo Material Properties") 
    bpy.types.Bone.nwo = PointerProperty(type=NWO_BonePropertiesGroup, name="Halo NWO Properties", description="Set Halo Bone Properties")

def unregister():
    del bpy.types.Light.halo_light
    del bpy.types.Mesh.ass_jms
    del bpy.types.Material.ass_jms
    del bpy.types.Scene.halo
    del bpy.types.Object.nwo
    del bpy.types.Material.nwo
    del bpy.types.Bone.nwo
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
