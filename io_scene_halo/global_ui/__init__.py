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
                col.prop(material_ass_jms, "two_sided", text='')
                row = col.row()
                row.label(text='Transparent:')
                col.prop(material_ass_jms, "transparent_1_sided", text='')
                row = col.row()
                row.label(text='Render Only:')
                col.prop(material_ass_jms, "render_only", text='')
                row = col.row()
                row.label(text='Large Collideable:')
                col.prop(material_ass_jms, "sphere_collision_only", text='')
                row = col.row()
                row.label(text='Fog Plane:')
                col.prop(material_ass_jms, "fog_plane", text='')
                row = col.row()
                row.label(text='Ladder:')
                col.prop(material_ass_jms, "ladder", text='')
                row = col.row()
                row.label(text='Breakable:')
                col.prop(material_ass_jms, "breakable", text='')
                row = col.row()
                row.label(text='AI Deafening:')
                col.prop(material_ass_jms, "ai_deafening", text='')
                row = col.row()
                row.label(text='Collision Only:')
                col.prop(material_ass_jms, "collision_only", text='')
                row = col.row()
                row.label(text='Exact Portal:')
                col.prop(material_ass_jms, "portal_exact", text='')

            if scene_halo.game_version == 'halo2':
                row = col.row()
                row.label(text='Two-sided:')
                col.prop(material_ass_jms, "two_sided", text='')
                row = col.row()
                row.label(text='One-sided Transparent:')
                col.prop(material_ass_jms, "transparent_1_sided", text='')
                row = col.row()
                row.label(text='Two-sided Transparent:')
                col.prop(material_ass_jms, "transparent_2_sided", text='')
                row = col.row()
                row.label(text='Render Only:')
                col.prop(material_ass_jms, "render_only", text='')
                row = col.row()
                row.label(text='Collision Only:')
                col.prop(material_ass_jms, "collision_only", text='')
                row = col.row()
                row.label(text='Sphere Collision Only:')
                col.prop(material_ass_jms, "sphere_collision_only", text='')
                row = col.row()
                row.label(text='Fog Plane:')
                col.prop(material_ass_jms, "fog_plane", text='')
                row = col.row()
                row.label(text='Ladder:')
                col.prop(material_ass_jms, "ladder", text='')
                row = col.row()
                row.label(text='Breakable:')
                col.prop(material_ass_jms, "breakable", text='')
                row = col.row()
                row.label(text='AI Deafening:')
                col.prop(material_ass_jms, "ai_deafening", text='')
                row = col.row()
                row.label(text='No Shadow:')
                col.prop(material_ass_jms, "no_shadow", text='')
                row = col.row()
                row.label(text='Shadow Only:')
                col.prop(material_ass_jms, "shadow_only", text='')
                col = box.column()
                row = col.row()
                row.label(text='Lightmap Only:')
                col.prop(material_ass_jms, "lightmap_only", text='')
                row = col.row()
                row.label(text='Precise:')
                col.prop(material_ass_jms, "precise", text='')
                row = col.row()
                row.label(text='Conveyor:')
                col.prop(material_ass_jms, "conveyor", text='')
                row = col.row()
                row.label(text='Portal (One-Way):')
                col.prop(material_ass_jms, "portal_1_way", text='')
                row = col.row()
                row.label(text='Portal (Door):')
                col.prop(material_ass_jms, "portal_door", text='')
                row = col.row()
                row.label(text='Portal (Vis Blocker):')
                col.prop(material_ass_jms, "portal_vis_blocker", text='')
                row = col.row()
                row.label(text='Dislikes Photons:')
                col.prop(material_ass_jms, "dislike_photons", text='')
                row = col.row()
                row.label(text='Ignored by Lightmapper:')
                col.prop(material_ass_jms, "ignored_by_lightmaps", text='')
                row = col.row()
                row.label(text='Portal (Sound Blocker):')
                col.prop(material_ass_jms, "blocks_sound", text='')
                row = col.row()
                row.label(text='Decal Offset:')
                col.prop(material_ass_jms, "decal_offset", text='')

            if scene_halo.game_version == 'halo3':
                row = col.row()
                row.label(text='Two-sided:')
                col.prop(material_ass_jms, "two_sided", text='')
                row = col.row()
                row.label(text='One-sided Transparent:')
                col.prop(material_ass_jms, "transparent_1_sided", text='')
                row = col.row()
                row.label(text='Two-sided Transparent:')
                col.prop(material_ass_jms, "transparent_2_sided", text='')
                row = col.row()
                row.label(text='Render Only:')
                col.prop(material_ass_jms, "render_only", text='')
                row = col.row()
                row.label(text='Collision Only:')
                col.prop(material_ass_jms, "collision_only", text='')
                row = col.row()
                row.label(text='Sphere Collision Only:')
                col.prop(material_ass_jms, "sphere_collision_only", text='')
                row = col.row()
                row.label(text='Fog Plane:')
                col.prop(material_ass_jms, "fog_plane", text='')
                row = col.row()
                row.label(text='Ladder:')
                col.prop(material_ass_jms, "ladder", text='')
                row = col.row()
                row.label(text='Breakable:')
                col.prop(material_ass_jms, "breakable", text='')
                row = col.row()
                row.label(text='AI Deafening:')
                col.prop(material_ass_jms, "ai_deafening", text='')
                row = col.row()
                row.label(text='No Shadow:')
                col.prop(material_ass_jms, "no_shadow", text='')
                row = col.row()
                row.label(text='Shadow Only:')
                col.prop(material_ass_jms, "shadow_only", text='')
                col = box.column()
                row = col.row()
                row.label(text='Lightmap Only:')
                col.prop(material_ass_jms, "lightmap_only", text='')
                row = col.row()
                row.label(text='Precise:')
                col.prop(material_ass_jms, "precise", text='')
                row = col.row()
                row.label(text='Conveyor:')
                col.prop(material_ass_jms, "conveyor", text='')
                row = col.row()
                row.label(text='Portal (One-Way):')
                col.prop(material_ass_jms, "portal_1_way", text='')
                row = col.row()
                row.label(text='Portal (Door):')
                col.prop(material_ass_jms, "portal_door", text='')
                row = col.row()
                row.label(text='Portal (Vis Blocker):')
                col.prop(material_ass_jms, "portal_vis_blocker", text='')
                row = col.row()
                row.label(text='Ignored by Lightmapper:')
                col.prop(material_ass_jms, "ignored_by_lightmaps", text='')
                row = col.row()
                row.label(text='Portal (Sound Blocker):')
                col.prop(material_ass_jms, "blocks_sound", text='')
                row = col.row()
                row.label(text='Decal Offset:')
                col.prop(material_ass_jms, "decal_offset", text='')
                row = col.row()
                row.label(text='Water Surface:')
                col.prop(material_ass_jms, "water_surface", text='')
                row = col.row()
                row.label(text='Slip Surface:')
                col.prop(material_ass_jms, "slip_surface", text='')
                row = col.row()
                row.label(text='Group Transparents By Plane:')
                col.prop(material_ass_jms, "group_transparents_by_plane", text='')

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
                col.prop(material_ass_jms, "lightmap_resolution_scale", text='')
                row = col.row()
                row.label(text='Lightmap Power Scale:')
                col.prop(material_ass_jms, "lightmap_power_scale", text='')
                row = col.row()
                row.label(text='Lightmap Half-Life Scale:')
                col.prop(material_ass_jms, "lightmap_half_life", text='')
                row = col.row()
                row.label(text='Lightmap Diffuse Scale:')
                col.prop(material_ass_jms, "lightmap_diffuse_scale", text='')

            else:
                col_split = layout.column(align=True).split()
                col = layout.column(align=True)
                col_split_b = layout.column(align=True).split()
                col_b = layout.column(align=True)
                row = col_split.row()
                row.label(text='Override Lightmap Transparency:')
                col.prop(material_ass_jms, "override_lightmap_transparency", text='')
                row = col_split.row()
                row.label(text='Ignore Default Resolution Scale:')
                col.prop(material_ass_jms, "ignore_default_res_scale", text='')
                row = col.row()
                row.label(text='Two-sided Transparent Tint:')
                col.prop(material_ass_jms, "two_sided_transparent_tint", text='')
                row = col.row()
                row.label(text='Additive Transparency:')
                col.prop(material_ass_jms, "additive_transparency", text='')
                row = col_split_b.row()
                row.label(text='Lightmap Resolution:')
                col.prop(material_ass_jms, "lightmap_res", text='')
                row = col_split_b.row()
                row.label(text='Photon Fidelity:')
                col.prop(material_ass_jms, "photon_fidelity", text='')
                row = col_b.row()
                row.label(text='Use Shader Gel:')
                col.prop(material_ass_jms, "use_shader_gel", text='')

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
            col.prop(material_ass_jms, "power", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Color:')
            col.prop(material_ass_jms, "color", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Quality:')
            col.prop(material_ass_jms, "quality", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Power Per Unit Area:')
            col.prop(material_ass_jms, "power_per_unit_area", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Emissive Focus:')
            col.prop(material_ass_jms, "emissive_focus", text='')

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
            col.prop(material_ass_jms, "falloff_distance", text='')
            row = col.row()
            row.label(text='Cutoff Distance:')
            col.prop(material_ass_jms, "cutoff_distance", text='')

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
            col.prop(material_ass_jms, "frustum_blend", text='')
            row = col.row()
            row.label(text='Falloff:')
            col.prop(material_ass_jms, "frustum_falloff", text='')
            row = col.row()
            row.label(text='Cutoff:')
            col.prop(material_ass_jms, "frustum_cutoff", text='')

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
        col.prop(mesh_ass_jms, "bounding_radius", text='')
        row = col.row()
        row.label(text='Object Type:')
        col.prop(mesh_ass_jms, "Object_Type", text='')
        row = col.row()
        row.operator(Halo_XREFPath.bl_idname, text="XREF Path")
        col.prop(mesh_ass_jms, "XREF_path", text='')
        row = col.row()
        row.label(text='XREF Name:')
        col.prop(mesh_ass_jms, "XREF_name", text='')

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
        col.prop(scene_halo, "game_version", text='')
        row = col.row()
        row.label(text='Expert Mode:')
        col.prop(scene_halo, "expert_mode", text='')

class Halo_ScenePropertiesGroup(PropertyGroup):
    game_version: EnumProperty(
        name="Game:",
        description="What game will you be exporting for",
        items=[ ('haloce', "Halo CE", "Show properties for Halo Custom Edition Or Halo CE MCC"),
                ('halo2', "Halo 2", "Show properties for Halo 2 Vista or Halo 2 MCC"),
                ('halo3', "Halo 3", "Show properties for Halo 3 MCC"),
                ('reach', "Halo Reach", "Show properties for Halo Reach MCC"),
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
###################
# JSON PROPERTIES
###################
# OBJECT PROPERTIES

frame_prefixes = ('b ', 'b_', 'frame ', 'frame_')
marker_prefixes = '#'
mesh_prefixes = ('+', '@','-', '%','!', '$','<', '~','&','>', '\'')
special_prefixes = ('b ', 'b_', 'frame ', 'frame_','#','+', '@','-', '%','!', '$','<', '~','&','>', '\'')

special_materials = ('+portal','+seamsealer','+sky','+weatherpoly')


class JSON_ObjectProps(Panel):
    bl_label = "Halo Object Properties"
    bl_idname = "JSON_PT_ObjectDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_halo = scene.halo

        if scene_halo.game_version == 'reach':
            return (context.mesh or context.object.type == 'EMPTY')
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
        
        ob = context.object
        ob_halo_json = ob.halo_json

        has_special_prefix = context.active_object.name.startswith(special_prefixes)

        col = flow.column()

        if has_special_prefix:
            if context.active_object.type == 'EMPTY':
                col.prop(ob_halo_json, "Object_Type_No_Mesh_Locked", text='Object Type')
            else:
                col.prop(ob_halo_json, "Object_Type_All_Locked", text='Object Type')
        else:
            if context.active_object.type == 'EMPTY':
                col.prop(ob_halo_json, "Object_Type_No_Mesh", text='Object Type')
            else:
                col.prop(ob_halo_json, "Object_Type_All", text='Object Type')

#MESH PROPERTIES
class JSON_ObjectMeshProps(Panel):
    bl_label = "Mesh Properties"
    bl_idname = "JSON_PT_MeshDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_parent_id = "JSON_PT_ObjectDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.object
        ob_halo_json = ob.halo_json

        return (ob_halo_json.Object_Type_All == 'MESH' and ob_halo_json.Object_Type_All_Locked == 'MESH' and context.active_object.type != 'EMPTY')


    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_halo_json = ob.halo_json

        special_mesh_types = ('BOUNDARY SURFACE','DECORATOR','INSTANCED GEOMETRY','PLANAR FOG VOLUME','PORTAL','SEAM','WATER PHYSICS VOLUME',)

        has_special_prefix = context.active_object.name.startswith(special_prefixes)


        col = flow.column()
         
        if has_special_prefix:
            col.prop(ob_halo_json, "ObjectMesh_Type_Locked", text='Mesh Type')
        else:
            col.prop(ob_halo_json, "ObjectMesh_Type", text='Mesh Type')

        if (ob_halo_json.ObjectMesh_Type in special_mesh_types or ob_halo_json.ObjectMesh_Type_Locked in special_mesh_types):

            type_no_special_prefix = ob_halo_json.ObjectMesh_Type_Locked == 'DEFAULT'

            if (ob_halo_json.ObjectMesh_Type == 'BOUNDARY SURFACE' or ob_halo_json.ObjectMesh_Type_Locked == 'BOUNDARY SURFACE'):
                col.prop(ob_halo_json, "Boundary_Surface_Name", text='Name')
                col.prop(ob_halo_json, "Boundary_Surface_Type", text='Type')
            elif (ob_halo_json.ObjectMesh_Type == 'DECORATOR' and type_no_special_prefix):
                col.prop(ob_halo_json, "Decorator_Name", text='Decorator Name')
                col.prop(ob_halo_json, "Decorator_LOD", text='Decorator Level of Detail')
            elif (ob_halo_json.ObjectMesh_Type == 'INSTANCED GEOMETRY' or ob_halo_json.ObjectMesh_Type_Locked == 'INSTANCED GEOMETRY'):
                col.prop(ob_halo_json, "Poop_Lighting_Override", text='Instanced Geo Lighting')
                col.prop(ob_halo_json, "Poop_Pathfinding_Override", text='Instanced Geo Pathfinding')
                col.prop(ob_halo_json, "Poop_Imposter_Policy", text='Imposter Policy')
                col.prop(ob_halo_json, "Poop_Imposter_Transition_Distance", text='Imposter Transition Dist')
                col.prop(ob_halo_json, "Poop_Imposter_Fade_Range_Start", text='Fade In Range Start')
                col.prop(ob_halo_json, "Poop_Imposter_Fade_Range_End", text='Fade In Range End')
                col.prop(ob_halo_json, "Poop_Decomposition_Hulls", text='Decomposition Hulls')

                col.separator()

                col.prop(ob_halo_json, "Poop_Predominant_Shader_Name", text='Predominant Shader Name')

                col.separator()

                col = layout.column(heading="Flags")
                sub = col.column(align=True)
                sub.prop(ob_halo_json, "Poop_Render_Only", text='Render Only')
                sub.prop(ob_halo_json, "Poop_Chops_Portals", text='Chops Portals')
                sub.prop(ob_halo_json, "Poop_Does_Not_Block_AOE", text='Does Not Block AOE')
                sub.prop(ob_halo_json, "Poop_Excluded_From_Lightprobe", text='Excluded From Lightprobe')
                sub.prop(ob_halo_json, "Poop_Decal_Spacing", text='Decal Spacing')
                sub.prop(ob_halo_json, "Poop_Precise_Geometry", text='Precise Geometry')
            elif (ob_halo_json.ObjectMesh_Type == 'PORTAL' or ob_halo_json.ObjectMesh_Type_Locked == 'PORTAL'):
                col.prop(ob_halo_json, "Portal_Type", text='Portal Type')

                col.separator()

                col = layout.column(heading="Flags")
                sub = col.column(align=True)

                sub.prop(ob_halo_json, "Portal_AI_Deafening", text='AI Deafening')
                sub.prop(ob_halo_json, "Portal_Blocks_Sounds", text='Blocks Sounds')
                sub.prop(ob_halo_json, "Portal_Is_Door", text='Is Door')
            elif (ob_halo_json.ObjectMesh_Type == 'SEAM' or ob_halo_json.ObjectMesh_Type_Locked == 'SEAM'):
                col.prop(ob_halo_json, "Seam_Name", text='Seam BSP Name')
            elif (ob_halo_json.ObjectMesh_Type == 'WATER PHYSICS VOLUME' or ob_halo_json.ObjectMesh_Type_Locked == 'WATER PHYSICS VOLUME'):
                col.prop(ob_halo_json, "Water_Volume_Depth", text='Water Volume Depth')
                col.prop(ob_halo_json, "Water_Volume_Flow_Direction", text='Flow Direction')
                col.prop(ob_halo_json, "Water_Volume_Flow_Velocity", text='Flow Velocity')
                col.prop(ob_halo_json, "Water_Volume_Fog_Color", text='Underwater Fog Color')
                col.prop(ob_halo_json, "Water_Volume_Fog_Murkiness", text='Underwater Fog Murkiness')
            elif (ob_halo_json.ObjectMesh_Type == 'PLANAR FOG VOLUME' or ob_halo_json.ObjectMesh_Type_Locked == 'PLANAR FOG VOLUME'):
                col.prop(ob_halo_json, "Fog_Name", text='Fog Name')
                col.prop(ob_halo_json, "Fog_Appearance_Tag", text='Fog Appearance Tag')
                col.prop(ob_halo_json, "Fog_Volume_Depth", text='Fog Volume Depth')

class JSON_ObjectMeshFaceProps(Panel):
    bl_label = "Face Properties"
    bl_idname = "JSON_PT_MeshFaceDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_parent_id = "JSON_PT_MeshDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.object
        ob_halo_json = ob.halo_json

        invalid_mesh_types = ('BOUNDARY SURFACE', 'COOKIE CUTTER', 'INSTANCED GEOMETRY MARKER', 'INSTANCED GEOMETRY RAIN BLOCKER', 'INSTANCED GEOMETRY VERTICAL RAIN SHEET', 'LIGHTMAP REGION', 'PLANAR FOG VOLUME', 'PORTAL', 'SEAM', 'WATER PHYSICS VOLUME')

        override_active = context.active_object.name.startswith(special_prefixes)

        if override_active:
            return ob_halo_json.ObjectMesh_Type_Locked not in invalid_mesh_types
        else:
            return ob_halo_json.ObjectMesh_Type not in invalid_mesh_types

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_halo_json = ob.halo_json

        col = flow.column()
        col.prop(ob_halo_json, "Face_Type", text='Face Type')
        if ob_halo_json.Face_Type == 'SKY':
            sub = col.column(align=True)
            sub.prop(ob_halo_json, "Sky_Permutation_Index", text='Sky Permutation Index')
            col.separator()

        col.prop(ob_halo_json, "Face_Mode", text='Face Mode')
        col.prop(ob_halo_json, "Face_Sides", text='Face Sides')
        col.prop(ob_halo_json, "Face_Draw_Distance", text='Draw Distance')

        col.separator()

        col.prop(ob_halo_json, "Region_Name", text='Face Region')
        col.prop(ob_halo_json, "Face_Global_Material", text='Global Material')

        col.separator()

        col = layout.column(heading="Flags")
        sub = col.column(align=True)
        sub.prop(ob_halo_json, "Conveyor", text='Conveyor')
        sub.prop(ob_halo_json, "Ladder", text='Ladder')
        sub.prop(ob_halo_json, "Slip_Surface", text='Slip Surface')
        sub.prop(ob_halo_json, "Decal_Offset", text='Decal Offset')
        sub.prop(ob_halo_json, "Group_Transparents_By_Plane", text='Group Transparents By Plane')
        sub.prop(ob_halo_json, "No_Shadow", text='No Shadow')
        sub.prop(ob_halo_json, "Precise_Position", text='Precise Position')

class JSON_ObjectMeshMaterialLightingProps(Panel):
    bl_label = "Lighting Properties"
    bl_idname = "JSON_PT_MeshMaterialLightingDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "JSON_PT_MeshDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.object
        ob_halo_json = ob.halo_json

        invalid_mesh_types = ('BOUNDARY SURFACE', 'COOKIE CUTTER', 'INSTANCED GEOMETRY MARKER', 'INSTANCED GEOMETRY RAIN BLOCKER', 'INSTANCED GEOMETRY VERTICAL RAIN SHEET', 'LIGHTMAP REGION', 'PLANAR FOG VOLUME', 'PORTAL', 'SEAM', 'WATER PHYSICS VOLUME')

        override_active = context.active_object.name.startswith(special_prefixes)

        if override_active:
            return ob_halo_json.ObjectMesh_Type_Locked not in invalid_mesh_types
        else:
            return ob_halo_json.ObjectMesh_Type not in invalid_mesh_types

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_halo_json = ob.halo_json

        col = flow.column()
        col.prop(ob_halo_json, "Material_Lighting_Attenuation_Cutoff", text='Attenuation Cutoff')
        col.prop(ob_halo_json, "Material_Lighting_Attenuation_Falloff", text='Attenuation Falloff')
        col.prop(ob_halo_json, "Material_Lighting_Emissive_Focus", text='Emissive Focus')
        col.prop(ob_halo_json, "Material_Lighting_Emissive_Color", text='Emissive Color')
        col.prop(ob_halo_json, "Material_Lighting_Emissive_Power", text='Emissive Power')
        col.prop(ob_halo_json, "Material_Lighting_Emissive_Quality", text='Emissive Quality')
        col.prop(ob_halo_json, "Material_Lighting_Bounce_Ratio", text='Bounce Ratio')
        
        col.separator()

        col = layout.column(heading="Flags")
        sub = col.column(align=True)
        sub.prop(ob_halo_json, "Material_Lighting_Emissive_Per_Unit", text='Emissive Per Unit')
        sub.prop(ob_halo_json, "Material_Lighting_Use_Shader_Gel", text='Use Shader Gel')

class JSON_ObjectMeshLightmapProps(Panel):
    bl_label = "Lightmap Properties"
    bl_idname = "JSON_PT_MeshLightmapDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "JSON_PT_MeshDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.object
        ob_halo_json = ob.halo_json

        invalid_mesh_types = ('BOUNDARY SURFACE', 'COOKIE CUTTER', 'INSTANCED GEOMETRY MARKER', 'INSTANCED GEOMETRY RAIN BLOCKER', 'INSTANCED GEOMETRY VERTICAL RAIN SHEET', 'LIGHTMAP REGION', 'PLANAR FOG VOLUME', 'PORTAL', 'SEAM', 'WATER PHYSICS VOLUME')

        override_active = context.active_object.name.startswith(special_prefixes)

        if override_active:
            return ob_halo_json.ObjectMesh_Type_Locked not in invalid_mesh_types
        else:
            return ob_halo_json.ObjectMesh_Type not in invalid_mesh_types

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_halo_json = ob.halo_json

        col = flow.column()
        col.prop(ob_halo_json, "Lightmap_Type", text='Lightmap Type')
        col.prop(ob_halo_json, "Lightmap_Additive_Transparency", text='Additive Transparency')
        col.prop(ob_halo_json, "Lightmap_Translucency_Tint_Color", text='Translucency Tint Color')
        col.prop(ob_halo_json, "Lightmap_Resolution_Scale", text='Resolution Scale')
        col.prop(ob_halo_json, "Lightmap_Chart_Group", text='Chart Group')
        col.prop(ob_halo_json, "Lightmap_Analytical_Bounce_Modifier", text='Analytical Bounce Modifier')
        col.prop(ob_halo_json, "Lightmap_General_Bounce_Modifier", text='General Bounce Modifier')
        
        col.separator()

        col = layout.column(heading="Flags")
        sub = col.column(align=True)
        sub.prop(ob_halo_json, "Lightmap_Lighting_From_Both_Sides", text='Lighting From Both Sides')
        sub.prop(ob_halo_json, "Lightmap_Transparency_Override", text='Transparency Override')

class JSON_ObjectMeshExtraProps(Panel):
    bl_label = "Other Mesh Properties"
    bl_idname = "JSON_PT_MeshExtraDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_parent_id = "JSON_PT_MeshDetailsPanel"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        ob = context.object
        ob_halo_json = ob.halo_json

        invalid_mesh_types = ('BOUNDARY SURFACE', 'COOKIE CUTTER', 'INSTANCED GEOMETRY MARKER', 'INSTANCED GEOMETRY RAIN BLOCKER', 'INSTANCED GEOMETRY VERTICAL RAIN SHEET', 'LIGHTMAP REGION', 'PLANAR FOG VOLUME', 'PORTAL', 'SEAM', 'WATER PHYSICS VOLUME')

        override_active = context.active_object.name.startswith(special_prefixes)

        if override_active:
            return ob_halo_json.ObjectMesh_Type_Locked not in invalid_mesh_types
        else:
            return ob_halo_json.ObjectMesh_Type not in invalid_mesh_types

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_halo_json = ob.halo_json

        col = flow.column()
        col.prop(ob_halo_json, "Mesh_Tesselation_Density", text='Tesselation Density')
        col.prop(ob_halo_json, "Mesh_Compression", text='Compression')
        col.prop(ob_halo_json, "Mesh_Primitive_Type", text='Primitive Type')
        if ob_halo_json.Mesh_Primitive_Type != 'NONE':
            sub = col.column(align=True)
            match ob_halo_json.Mesh_Primitive_Type:
                case 'BOX':
                    sub.prop(ob_halo_json, "Box_Length", text='Length')
                    sub.prop(ob_halo_json, "Box_Width", text='Width')
                    sub.prop(ob_halo_json, "Box_Height", text='Height')
                case 'PILL':
                    sub.prop(ob_halo_json, "Pill_Radius", text='Radius')
                    sub.prop(ob_halo_json, "Pill_Height", text='Height')
                case 'SPHERE':
                    sub.prop(ob_halo_json, "Sphere_Radius", text='Radius')

# MARKER PROPERTIES
class JSON_ObjectMarkerProps(Panel):
    bl_label = "Marker Properties"
    bl_idname = "JSON_PT_MarkerDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_parent_id = "JSON_PT_ObjectDetailsPanel"

    @classmethod
    def poll(cls, context):
        ob = context.object
        ob_halo_json = ob.halo_json

        return ((ob_halo_json.Object_Type_All == 'MARKER' or  ob_halo_json.Object_Type_All_Locked == 'MARKER') or (context.active_object.type == 'EMPTY' and (ob_halo_json.Object_Type_No_Mesh == 'MARKER' or ob_halo_json.Object_Type_No_Mesh_Locked == 'MARKER')))

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        ob = context.object
        ob_halo_json = ob.halo_json

        col = flow.column()

        col.prop(ob_halo_json, "ObjectMarker_Type", text='Marker Type')
        
        group_marker_types = ('MODEL', 'HINT', 'TARGET')

        col.prop(ob_halo_json, "Marker_Region", text='Marker Region')

        if ob_halo_json.ObjectMarker_Type in group_marker_types:
            col.prop(ob_halo_json, "Marker_Group_Name", text='Marker Group')

        if ob_halo_json.ObjectMarker_Type == 'MODEL':
            col.separator()
            col.prop(ob_halo_json, "Marker_Velocity", text='Marker Velocity')

        if ob_halo_json.ObjectMarker_Type == 'GAME INSTANCE':
            col.separator()
            col.prop(ob_halo_json, "Marker_Game_Instance_Tag_Name", text='Game Instance Tag')
            col.prop(ob_halo_json, "Marker_Game_Instance_Tag_Variant_Name", text='Game Instance Tag Variant')

        if ob_halo_json.ObjectMarker_Type == 'PATHFINDING SPHERE':
            col.separator()
            col = layout.column(heading="Flags")
            sub = col.column(align=True)
            sub.prop(ob_halo_json, "Marker_Pathfinding_Sphere_Vehicle", text='Vehicle Only')
            sub.prop(ob_halo_json, "Pathfinding_Sphere_Remains_When_Open", text='Remains When Open')
            sub.prop(ob_halo_json, "Pathfinding_Sphere_With_Sectors", text='With Sectors')

        if ob_halo_json.ObjectMarker_Type == 'PHYSICS CONSTRAINT':
            col.separator()
            col.prop(ob_halo_json, "Physics_Constraint_Parent", text='Physics Constraint Parent')
            col.prop(ob_halo_json, "Physics_Constraint_Child", text='Physics Constraint Child')
            col.prop(ob_halo_json, "Physics_Constraint_Type", text='Physics Constraint Type')

            if ob_halo_json.Physics_Constraint_Type == 'HINGE':
                col.prop(ob_halo_json, "Hinge_Constraint_Minimum", text='Minimum')
                col.prop(ob_halo_json, "Hinge_Constraint_Maximum", text='Maximum')

            elif ob_halo_json.Physics_Constraint_Type == 'SOCKET':
                col.prop(ob_halo_json, "Cone_Angle", text='Cone Angle')

                col.prop(ob_halo_json, "Plane_Constraint_Minimum", text='Plane Minimum')
                col.prop(ob_halo_json, "Plane_Constraint_Maximum", text='Plane Maximum')
                
                col.prop(ob_halo_json, "Twist_Constraint_Start", text='Twist Start')
                col.prop(ob_halo_json, "Twist_Constraint_End", text='Twist End')

# MATERIAL PROPERTIES
class JSON_MaterialProps(Panel):
    bl_label = "Halo Material Properties"
    bl_idname = "JSON_PT_MaterialPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_halo = scene.halo

        if scene_halo.game_version == 'reach':
            return True

    def draw(self, context):
        layout = self.layout
        current_material = context.object.active_material
        scene = context.scene
        if current_material is not None:
            material_halo_json = current_material.halo_json
            row = layout.row()
            col = layout.column(align=True)
            row.label(text="Shader Path")
            col.prop(material_halo_json, "shader_path", text='')
            row = col.row()
            layout.use_property_split = True
            flow = layout.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)
            col = flow.column()
            # row.label(text="Shader Type")
            # row.prop(material_halo_json, "Shader_Type_Locked", text='')
            # row = col.row()
            if context.object.active_material.name in special_materials:
                col.prop(material_halo_json, "material_override_locked", text='Material Override')
            else:
                col.prop(material_halo_json, "material_override", text='Material Override')
            
# LIGHT PROPERTIES
class JSON_LightProps(Panel):
    bl_label = "Halo Light Properties"
    bl_idname = "JSON_PT_LightPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_halo = scene.halo

        if scene_halo.game_version == 'reach':
            return context.light

    def draw(self, context):
        layout = self.layout

        light = context.object.data
        light_halo_json = light.halo_json

        row = layout.row()
        col = layout.column(align=True)
        row = col.row()
        row.label(text="Light Type Override")
        col.prop(light_halo_json, "light_type_override", text='')

# JSON PROPERTY GROUPS
class JSON_ObjectPropertiesGroup(PropertyGroup):
    #OBJECT PROPERTIES

    def get_objecttype_enum(self):
        if bpy.context.active_object.name.startswith(frame_prefixes):
            return 0
        elif bpy.context.active_object.name.startswith(marker_prefixes):
            return 1
        elif bpy.context.active_object.name.startswith(mesh_prefixes):
            return 2

    object_type_items_all = [
        ('FRAME', "Frame", "Treat this object as a frame. Can be forced on with the prefixes: 'b_', 'b ', 'frame ', 'frame_'",),
        ('MARKER', "Marker", "Sets this object to be written to a json file as a marker. Can be forced on with the prefix: '#'"),
        ('MESH', "Mesh", "Treats this object as a mesh when writing to a json file"),
    ]

    object_type_items_no_mesh = [
        ('FRAME', "Frame", "Treat this object as a frame. Can be forced on with the prefixes: 'b_', 'b ', 'frame ', 'frame_'"),
        ('MARKER', "Marker", "Sets this object to be written to a json file as a marker. Can be forced on with the prefix: '#'"),
    ]

    Object_Type_All: EnumProperty(
        name="Object Type",
        options=set(),
        description="Sets the Halo object type of this object",
        default = 'MESH',
        items=object_type_items_all,
    )

    Object_Type_No_Mesh: EnumProperty(
        name="Object Type",
        options=set(),
        description="Sets the object type",
        default = 'MARKER',
        items=object_type_items_no_mesh,
    )

    Object_Type_All_Locked: EnumProperty(
        name="Object Type",
        options=set(),
        get=get_objecttype_enum,
        description="Sets the object type",
        default = 'MESH',
        items=object_type_items_all,
    )

    Object_Type_No_Mesh_Locked: EnumProperty(
        name="Object Type",
        options=set(),
        get=get_objecttype_enum,
        description="Sets the object type",
        default = 'MARKER',
        items=object_type_items_no_mesh,
    )

    def get_meshtype_enum(self):
        if bpy.context.active_object.name.startswith('+'):
            return 0
        elif bpy.context.active_object.name.startswith('@'):
            return 1
        elif bpy.context.active_object.name.startswith('-'):
            return 2
        elif bpy.context.active_object.name.startswith('%'):
            return 5
        elif bpy.context.active_object.name.startswith('!'):
            return 12
        elif bpy.context.active_object.name.startswith('$'):
            return 13
        elif bpy.context.active_object.name.startswith('<'):
            return 14
        elif bpy.context.active_object.name.startswith('~'):
            return 15
        elif bpy.context.active_object.name.startswith('&'):
            return 16
        elif bpy.context.active_object.name.startswith('>'):
            return 17
        elif bpy.context.active_object.name.startswith('\''):
            return 18

    mesh_type_items = [
        ('BOUNDARY SURFACE', "Boundary Surface", "Used in structure_design tags for soft_kill, soft_ceiling, and slip_sufaces. Only use when importing to a structure_design tag. Can be forced on with the prefix: '+'"),
        ('COLLISION', "Collision", "Sets this mesh to have collision geometry only. Can be forced on with the prefix: '@'"),
        ('COOKIE CUTTER', "Cookie Cutter", "Defines an area which ai will pathfind around. Can be forced on with the prefix: '-'"),
        ('DECORATOR', "Decorator", "Use this when making a decorator. Allows for different LOD levels to be set"),
        ('DEFAULT', "Default", "By default this mesh type will be treated as render only geometry in models, and render + bsp collision geometry in structures"),
        ('INSTANCED GEOMETRY', "Instanced Geometry", "Writes this mesh a json file as instanced geometry. Can be forced on with the prefix: '%'"),
        ('INSTANCED GEOMETRY COLLISION', "Instanced Geometry Collision", "This mesh will act as the collision geometry of its parent instanced geometry mesh. Can be forced on if this mesh is the child of an instanced geometry object and has the prefix: '@'"),
        ('INSTANCED GEOMETRY MARKER', "Instanced Geometry Marker", "This mesh will act a marker of its parent instanced geometry mesh. Can be forced on if this mesh is the child of an instanced geometry object and has the prefix: '#'"),
        ('INSTANCED GEOMETRY PHYSICS', "Instanced Geometry Physics", "This mesh will act as the physics geometry of its parent instanced geometry mesh. Can be forced on if this mesh is the child of an instanced geometry object and has the prefix: '$'"),
        ('INSTANCED GEOMETRY RAIN BLOCKER', "Instanced Geometry Rain Blocker", "This mesh will act as a rain blocker for its parent instanced geometry mesh"),
        ('INSTANCED GEOMETRY VERTICAL RAIN SHEET', "Instanced Geometry Vertical Rain Sheet", "This mesh will act as a verticle rain sheet for its parent instanced geometry mesh"),
        ('LIGHTMAP REGION', "Lightmap Region", "Defines an area of a structure which should be lightmapped. Can be referenced when lightmapping"),
        ('OBJECT INSTANCE', "Object Instance", "Writes this mesh to the json as an instanced object. Can be forced on with the prefix: '!'"),
        ('PHYSICS', "Physics", "Sets this mesh to have physics geometry only. Can be forced on with the prefix: '$'"),
        ('PLANAR FOG VOLUME', "Planar Fog Volume", "Defines an area for a fog volume. The same logic as used for portals should be applied to these.  Can be forced on with the prefix: '<'"),
        ('PORTAL', "Portal", "Cuts up a bsp and defines clusters. Can be forced on with the prefix '~'"),
        ('SEAM', "Seam", "Defines where two bsps meet. Its name should match the name of the bsp its in. Can be forced on with the prefix '&'"),
        ('WATER PHYSICS VOLUME', "Water Physics Volume", "Defines an area where water physics should apply. Only use when importing to a structure_design tag. Can be forced on with the prefix: '>'"),
        ('WATER SURFACE', "Water Surface", "Defines a mesh as a water surface. Can be forced on with the prefix: '"),
    ]

    #MESH PROPERTIES
    ObjectMesh_Type : EnumProperty(
        name="Mesh Type",
        options=set(),
        description="Sets the type of Halo mesh you want to create. This value is overridden by certain object prefixes",
        default = 'DEFAULT',
        items=mesh_type_items,
        )

    ObjectMesh_Type_Locked : EnumProperty(
        name="Mesh Type",
        options=set(),
        get=get_meshtype_enum,
        description="Sets the type of Halo mesh you want to create. This value is overridden by certain object prefixes: $, @, %",
        default = 'DEFAULT',
        items=mesh_type_items,
        )

    Mesh_Primitive_Type : EnumProperty(
        name="Mesh Primitive Type",
        options=set(),
        description="Select the primtive type of this mesh",
        default = "NONE",
        items=[ ('NONE', "None", "None"),
                ('BOX', "Box", "Box"),
                ('PILL', "Pill", "Pill"),
                ('SPHERE', "Sphere", "Sphere"),
               ]
        )

    Mesh_Tesselation_Density : EnumProperty(
        name="Mesh Tesselation Density",
        options=set(),
        description="Select the tesselation density you want applied to this mesh",
        default = "NONE",
        items=[ ('NONE', "None", "None"),
                ('4X', "4x", "4 times"),
                ('9X', "9x", "9 times"),
                ('36X', "36x", "36 times"),
               ]
        )
    Mesh_Compression : EnumProperty(
        name="Mesh Compression",
        options=set(),
        description="Select if you want additional compression forced on/off to this mesh",
        default = "DEFAULT",
        items=[ ('DEFAULT', "Default", "Default"),
                ('FORCE OFF', "Force Off", "Force Off"),
                ('FORCE ON', "Force On", "Force On"),
               ]
        )

    #FACE PROPERTIES
    Face_Type : EnumProperty(
        name="Face Type",
        options=set(),
        description="Select the face type for this mesh. Note that any override shaders will override the face type selected here for relevant materials",
        default = "NORMAL",
        items=[ ('NONE', "None", "None"),
                ('NORMAL', "Normal", "Normal"),
                ('SEAM SEALER', "Seam Sealer", "Set mesh faces to have the special seam sealer property"),
                ('SKY', "Sky", "Set mesh faces to render the sky"),
                ('WEATHER POLYHEDRA', "Weather Polyhedra", "Weather Polyhedra"),
               ]
        )

    Face_Mode : EnumProperty(
        name="Face Mode",
        options=set(),
        description="Select the face mode for this mesh",
        default = "NORMAL",
        items=[ ('NONE', "None", "None"),
                ('NORMAL', "Normal", "Normal"),
                ('RENDER ONLY', "Render Only", "Set mesh faces to be render only"),
                ('COLLISION ONLY', "Collision Only", "Set mesh faces to be collision only"),
                ('SPHERE COLLISION ONLY', "Sphere Collision Only", "Set mesh faces to be sphere collision only. Only objects with physics models can collide with these faces"),
                ('SHADOW ONLY', "Shadow Only", "Set mesh faces to only cast shadows"),
                ('LIGHTMAP ONLY', "Lightmap Only", "Set mesh faces to only be used during lightmapping. They will otherwise have no render / collision"),
                ('BREAKABLE', "Breakable", "Set mesh faces to be breakable. Time to smash some windows"),
               ]
        )

    Face_Sides : EnumProperty(
        name="Face Sides",
        options=set(),
        description="Select the face sides for this mesh",
        default = "ONE SIDED",
        items=[ ('NONE', "None", "None"),
                ('ONE SIDED', "One Sided", "Set mesh faces to only render on one side (the normal direction)"),
                ('ONE SIDED TRANSPARENT', "One Sided Transparent", "Set mesh faces to only render on one side (the normal direction), but also render geometry behind it"),
                ('TWO SIDED', "Two Sided", "Set mesh faces to  render on both sides"),
                ('TWO SIDED TRANSPARENT', "Two Sided Transparent", "Set mesh faces to render on both sides, but also render geometry through it"),
               ]
        )

    Face_Draw_Distance : EnumProperty(
        name="Face Draw Distance",
        options=set(),
        description="Select the draw distance for faces on this mesh",
        default = "NORMAL",
        items=[ ('NONE', "None", "None"),
                ('NORMAL', "Normal", "Normal"),
                ('MID', "Mid", "Render face details at medium range"),
                ('CLOSE', "Close", "Render face details at close range"),
               ]
        )

    Region_Name: StringProperty(
        name="Face Region",
        description="Define the name of the region these faces should be associated with.",
    )

    Face_Global_Material: StringProperty(
        name="Global Material",
        description="Set the global material of the faces of this mesh. For struture geometry leave blank to use the global material of the shader. The global material name should match a valid material defined in tags\globals\globals.globals",
    )

    Sky_Permutation_Index: IntProperty(
        name="Sky Permutation Index",
        options=set(),
        description="Set the sky permuation index of the mesh faces. Only valid if the face type is sky (or you are using the sky material override).",
        min=0,
    )

    Conveyor: BoolProperty(
        name ="Conveyor",
        options=set(),
        description = "Enable to give mesh faces the conveyor property",
        default = False,
        )

    Ladder: BoolProperty(
        name ="Ladder",
        options=set(),
        description = "Enable to make mesh faces climbable",
        default = False,
    )

    Slip_Surface: BoolProperty(
        name ="Slip Surface",
        options=set(),
        description = "Enable to make mesh faces slippery for units",
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
        description = "Enable to prevent mesh faces from casting shadows",
        default = False,
    )

    Precise_Position: BoolProperty(
        name ="Precise Position",
        options=set(),
        description = "Enable to prevent faces from being altered during the import process",
        default = False,
    )
    
    #PRIMITIVE PROPERTIES
    Box_Length: FloatProperty(
        name="Box Length",
        options=set(),
        description="Set length of the primitive box",
    )

    Box_Width: FloatProperty(
        name="Box Width",
        options=set(),
        description="Set width of the primitive box",
    )

    Box_Height: FloatProperty(
        name="Box Height",
        options=set(),
        description="Set height of the primitive box",
    )

    Pill_Radius: FloatProperty(
        name="Pill Radius",
        options=set(),
        description="Set radius of the primitive pill",
    )

    Pill_Height: FloatProperty(
        name="Pill Height",
        options=set(),
        description="Set height of the primitive pill",
    )

    Sphere_Radius: FloatProperty(
        name="Sphere Radius",
        options=set(),
        description="Set radius of the primitive sphere",
    )
    
    #BOUNDARY SURFACE PROPERTIES
    Boundary_Surface_Name: StringProperty(
        name="Boundary Surface Name",
        description="Define the name of the boundary surface. This will be referenced in the structure_design tag.",
        maxlen=32,
    )

    Boundary_Surface_Type : EnumProperty(
        name="Boundary Surface Name",
        options=set(),
        description="Set the type of boundary surface you want to create. You should only import files with this mesh type as struture_design tags",
        default = "SOFT CEILING",
        items=[ ('SOFT CEILING', "Soft Ceiling", "Defines this mesh as soft ceiling"),
                ('SOFT KILL', "Soft Kill", "Defines this mesh as soft kill barrier"),
                ('SLIP SURFACE', "Slip Surface", "Defines this mesh as a slip surface"),
               ]
        )
    
    #POOP PROPERTIES
    Poop_Lighting_Override : EnumProperty(
        name="Instanced Geometry Lighting Override",
        options=set(),
        description="Sets the lighting policy for this instanced geometry. If set to none, the exporter will defer to the object name prefix for the lighting policy",
        default = "PER VERTEX",
        items=[ ('NONE', "None", "None"),
                ('PER PIXEL', "Per Pixel", "Sets the lighting policy to per pixel. PREFIX: ?"),
                ('PER VERTEX', "Per Vertex", "Sets the lighting policy to per vertex. PREFX: !"),
                ('SINGLE PROBE', "Single Probe", "Sets the lighting policy to single probe."),
               ]
        )

    Poop_Pathfinding_Override : EnumProperty(
        name="Instanced Geometry Pathfinding Override",
        options=set(),
        description="Sets the pathfinding policy for this instanced geometry. If set to none, the exporter will defer to the object name prefix for the pathfinding policy",
        default = 'CUTOUT',
        items=[ ('CUTOUT', "Cutout", "Sets the pathfinding policy to cutout. AI will be able to pathfind around this mesh, but not on it."),
                ('NONE', "None", "Sets the pathfinding policy to none. This mesh will be ignored during pathfinding generation. PREFIX: -"),
                ('STATIC', "Static", "Sets the pathfinding policy to static. AI will be able to pathfind around and on this mesh. PREFIX: +"),
               ]
        )

    Poop_Imposter_Policy : EnumProperty(
        name="Instanced Geometry Imposter Policy",
        options=set(),
        description="Sets the imposter policy for this instanced geometry.",
        default = "POLYGON DEFAULT",
        items=[ ('POLYGON DEFAULT', "Polygon Default", ""),
                ('POLYGON HIGH', "Polygon High", ""),
                ('CARD DEFAULT', "Card Default", ""),
                ('CARD HIGH', "Card High", ""),
                ('NONE', "None", ""),
                ('NEVER', "Never", ""),
               ]
        )

    Poop_Imposter_Transition_Distance: FloatProperty(
        name="Instanced Geometry Imposter Transition Distance",
        options=set(),
        description="The distance at which the instanced geometry transitions to its imposter variant.",
        default=-1.0,
    )

    Poop_Imposter_Fade_Range_Start: FloatProperty(
        name="Instanced Geometry Fade Range Start",
        options=set(),
        description="The distance at which the instanced geometry starts to fade in.",
        default=36,
    )

    Poop_Imposter_Fade_Range_End: FloatProperty(
        name="Instanced Geometry Fade Range End",
        options=set(),
        description="The distance at which the instanced geometry fades in.",
        default=30,
    )

    Poop_Decomposition_Hulls: IntProperty(
        name="Instanced Geometry Decomposition Hulls",
        options=set(),
        description="",
        default=-1,
    )
    
    Poop_Predominant_Shader_Name: StringProperty(
        name="Instanced Geometry Predominant Shader Name",
        description="I have no idea what this does, but we'll write whatever you put here into the json file.",
        maxlen=1024,
    )

    Poop_Render_Only: BoolProperty(
        name ="Render Only",
        options=set(),
        description = "Sets this instanced geometry to only have render geometry",
        default = False,
    )

    Poop_Chops_Portals: BoolProperty(
        name ="Chops Portals",
        options=set(),
        description = "Sets this instanced geometry to chop portals. Hiya!",
        default = False,
    )

    Poop_Does_Not_Block_AOE: BoolProperty(
        name ="Does Not Block AOE",
        options=set(),
        description = "Sets this instanced geometry to not block area of effect forces",
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
        description = "Sets this instanced geometry have decal spacing (like decal_offset)",
        default = False,
    )

    Poop_Precise_Geometry: BoolProperty(
        name ="Precise Geometry",
        options=set(),
        description = "Sets this instanced geometry not have its geometry altered in the BSP pass.",
        default = False,
    )

    #PORTAL PROPERTIES
    Portal_Type : EnumProperty(
        name="Portal Type",
        options=set(),
        description="Sets the type of portal this mesh should be.",
        default = "TWO WAY",
        items=[ ('NONE', "None", ""),
                ('NO WAY', "No Way", "Sets the portal to block all visibility"),
                ('ONE WAY', "One Way", "Sets the portal to block visibility from one direction"),
                ('TWO WAY', "Two Way", "Sets the portal to have visiblity from both sides"),
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
    Decorator_Name: StringProperty(
        name="Decorator Name",
        description="Name of your decorator",
        maxlen=32,
    )

    Decorator_LOD: IntProperty(
        name="Decorator Level of Detail",
        options=set(),
        description="Level of detail objects to create expressed in an integer range of 1-4",
        default=1,
        min=1,
        max=4,
    )

    #SEAM PROPERTIES
    Seam_Name: StringProperty(
        name="Seam BSP Name",
        description="Name of the bsp associated with this seam",
        maxlen=32,
    )

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
        default=(0, 0, 0),
        subtype='COLOR',
    )

    Water_Volume_Fog_Murkiness: FloatProperty(
        name="Water Volume Fog Murkiness",
        options=set(),
        description="Set the fog murkiness of this water volume mesh",
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
    
    #LIGHTMAP PROPERTIES
    Lightmap_Additive_Transparency: FloatVectorProperty(
        name="lightmap Additive Transparency",
        options=set(),
        description="",
        default=(0, 0, 0),
        subtype='COLOR',
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

    Lightmap_Chart_Group: IntProperty(
        name="Lightmap Chart Group",
        options=set(),
        description="",
        default=3,
        min=1,
    )

    Lightmap_Type : EnumProperty(
        name="Lightmap Type",
        options=set(),
        description="Sets how this should be lit while lightmapping",
        default = "PER PIXEL",
        items=[ ('PER PIXEL', "Per Pixel", ""),
                ('PER VERTEX', "Per Vetex", ""),
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
        name="Water Volume Fog Color",
        options=set(),
        description="Lightmap Translucency Tint Color",
        default=(0, 0, 0),
        subtype='COLOR',
    )

    Lightmap_Lighting_From_Both_Sides: BoolProperty(
        name ="Lightmap Lighting From Both Sides",
        options=set(),
        description = "",
        default = False,
    )

    #MATERIAL LIGHTING PROPERTIES
    Material_Lighting_Attenuation_Cutoff: FloatProperty(
        name="Material Lighting Attenuation Cutoff",
        options=set(),
        description="",
    )

    Material_Lighting_Attenuation_Falloff: FloatProperty(
        name="Material Lighting Attenuation Falloff",
        options=set(),
        description="",
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
        default=(0, 0, 0),
        subtype='COLOR',
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
    )

    Material_Lighting_Emissive_Quality: FloatProperty(
        name="Material Lighting Emissive Quality",
        options=set(),
        description="",
        default=1,
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
    )

    #MARKER PROPERTIES
    ObjectMarker_Type : EnumProperty(
        name="Marker Type",
        options=set(),
        description="Select the marker type",
        default = "MODEL",
        items=[ ('NONE', "None", "None"),
                ('MODEL', "Model", "Model"),
                ('GAME INSTANCE', "Game Instance", "Game Instance"),
                ('PATHFINDING SPHERE', "Pathfinding Sphere", "Pathfinding Sphere"),
                ('WATER VOLUME FLOW', "Water Volume Flow", "Water Volume Flow"),
                ('PHYSICS CONSTRAINT', "Physics Constraint", "Physics Constraint"),
                ('TARGET', "Target", "Target"),
                ('GARBAGE', "Garbage", "Garbage"),
                ('EFFECTS', "Effects", "Effects"),
                ('HINT', "Hint", "Hint"),
               ]
        )
    
    def get_marker_group_name(self):
        group_name = bpy.context.active_object.name
        group_name = group_name.removeprefix('#')
        if group_name.rpartition('.')[0] != '':
            group_name = group_name.rpartition('.')[0]

        return group_name

    Marker_Group_Name: StringProperty(
        name="Marker Group",
        description="Define the name of the marker group",
        get=get_marker_group_name,
    )

    Marker_Region: StringProperty(
        name="Marker Group",
        description="Define the name of marker region. This should match a face region name",
    )

    Marker_Game_Instance_Tag_Name: StringProperty(
        name="Marker Game Instance Tag",
        description="Define the name of the marker game instance tag",
    )

    Marker_Game_Instance_Tag_Variant_Name: StringProperty(
        name="Marker Game Instance Tag Variant",
        description="Define the name of the marker game instance tag",
    ) 

    Marker_Velocity: FloatVectorProperty(
        name="Marker Velocity",
        options=set(),
        description="Define the name of the velocity of a marker",
        subtype='VELOCITY'
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
        default = "HINGE",
        items=[ ('HINGE', "Hinge", ""),
                ('SOCKET', "Socket", ""),
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
        min=-180,
        max=180,
    )

    Plane_Constraint_Minimum: FloatProperty(
        name="Plane Constraint Minimum",
        options=set(),
        description="Set the minimum rotation of a physics plane",
        default=-90,
        min=-180,
        max=180,
    )

    Plane_Constraint_Maximum: FloatProperty(
        name="Plane Constraint Maximum",
        options=set(),
        description="Set the maximum rotation of a physics plane",
        default=90,
        min=-180,
        max=180,
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

class JSON_MaterialPropertiesGroup(PropertyGroup):
    shader_path: StringProperty(
        name = "Shader Path",
        description = "Define the relative path to a shader, including the file extension",
        default = "",
        )

    # shader_types = [ ('SHADER', "Shader", ""),
    #             ('SHADER CORTANA', "Shader Cortana", ""),
    #             ('SHADER CUSTOM', "Shader Custom", ""),
    #             ('SHADER DECAL', "Shader Decal", ""),
    #             ('SHADER FOLIAGE', "Shader Foliage", ""),
    #             ('SHADER FUR', "Shader Fur", ""),
    #             ('SHADER FUR STENCIL', "Shader Fur Stencil", ""),
    #             ('SHADER GLASS', "Shader Glass", ""),
    #             ('SHADER HALOGRAM', "Shader Halogram", ""),
    #             ('SHADER MUX', "Shader Mux", ""),
    #             ('SHADER MUX MATERIAL', "Shader Mux Material", ""),
    #             ('SHADER SCREEN', "Shader Screen", ""),
    #             ('SHADER SKIN', "Shader Skin", ""),
    #             ('SHADER TERRAIN', "Shader Terrain", ""),
    #             ('SHADER WATER', "Shader Water", ""),
    #            ]

    # def shader_type_enum(self):
    #     print (bpy.types.Material.halo_json.shader_path.rpartition('.')[2])
    #     match bpy.types.Material.halo_json.shader_path.rpartition('.')[2]:
    #         case 'shader_cortana':
    #             return 1
    #         case 'shader_custom':
    #             return 2
    #         case 'shader_decal':
    #             return 3
    #         case 'shader_foliage':
    #             return 4
    #         case 'shader_fur':
    #             return 5
    #         case 'shader_fur_stencil':
    #             return 6
    #         case 'shader_glass':
    #             return 7
    #         case 'shader_mux':
    #             return 8
    #         case 'shader_mux_material':
    #             return 9
    #         case 'shader_screen':
    #             return 10
    #         case 'shader_skin':
    #             return 11
    #         case 'shader_terrain':
    #             return 12
    #         case 'shader_water':
    #             return 13
    #         case _:
    #             return 0

    # Shader_Type_Locked: EnumProperty(
    #     name = "Shader Type",
    #     options=set(),
    #     description = "",
    #     default = "SHADER",
    #     get=shader_type_enum,
    #     items=shader_types,
    #     )

    material_override: EnumProperty(
        name = "Material Override",
        options=set(),
        description = "Select to override the shader path with a special material type e.g. sky / seamsealer",
        default = "NONE",
        items=[ ('NONE', "None", "None"),
                ('PORTAL', "Portal", "Force all faces with this material to be portals"),
                ('SEAMSEALER', "Seamsealer", "Force all faces with this material to be seamsealer"),
                ('SKY', "Sky", "Force all faces with this material to be sky"),
                ('WEATHERPOLY', "Weather Polyhedra", "Force all faces with this material to be weather polyhedra"),

               ]
        )

    def material_name_is_special(self):
        match bpy.context.object.active_material.name:
            case '+portal':
                return 1
            case '+seamsealer':
                return 2
            case '+sky':
                return 3
            case '+weatherpoly':
                return 4


    material_override_locked: EnumProperty(
        name = "Material Override",
        options=set(),
        get=material_name_is_special,
        description = "Select to override the shader path with a special material type e.g. sky / seamsealer",
        default = "NONE",
        items=[ ('NONE', "None", "None"),
                ('PORTAL', "Portal", "Force all faces with this material to be portals"),
                ('SEAMSEALER', "Seamsealer", "Force all faces with this material to be seamsealer"),
                ('SKY', "Sky", "Force all faces with this material to be sky"),
                ('WEATHERPOLY', "Weather Polyhedra", "Force all faces with this material to be weather polyhedra"),

               ]
        )

class JSON_LightPropertiesGroup(PropertyGroup):
    light_type_override: EnumProperty(
        name = "Light Type Override",
        options=set(),
        description = "Select to override the light type",
        default = "NONE",
        items=[ ('NONE', "None", "None"),
                ('OMNI', "Omni", ""),
                ('SPOT', "Spot", ""),
                ('DIRECTIONAL', "Directional", ""),
               ]
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
    Halo_XREFPath,
    JSON_ObjectProps,
    JSON_ObjectMeshProps,
    JSON_ObjectMeshFaceProps,
    JSON_ObjectMeshMaterialLightingProps,
    JSON_ObjectMeshLightmapProps,
    JSON_ObjectMeshExtraProps,
    JSON_ObjectMarkerProps,
    JSON_MaterialProps,
    JSON_ObjectPropertiesGroup,
    JSON_MaterialPropertiesGroup,
    JSON_LightProps,
    JSON_LightPropertiesGroup
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.Light.halo_light = PointerProperty(type=ASS_LightPropertiesGroup, name="ASS Properties", description="Set properties for your light")
    bpy.types.Mesh.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.Material.ass_jms = PointerProperty(type=ASS_JMS_MaterialPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your materials")
    bpy.types.Scene.halo = PointerProperty(type=Halo_ScenePropertiesGroup, name="Halo Scene Properties", description="Set properties for your scene")
    bpy.types.Object.halo_json = PointerProperty(type=JSON_ObjectPropertiesGroup, name="Halo JSON Properties", description="Set Halo Object Properties")
    bpy.types.Material.halo_json = PointerProperty(type=JSON_MaterialPropertiesGroup, name="Halo JSON Properties", description="Set Halo Material Properties")
    bpy.types.Light.halo_json = PointerProperty(type=JSON_LightPropertiesGroup, name="Halo JSON Properties", description="Set Halo Light Properties")

def unregister():
    del bpy.types.Light.halo_light
    del bpy.types.mesh.ass_jms
    del bpy.types.Material.ass_jms
    del bpy.types.Scene.halo
    del bpy.types.Object.halo_json
    del bpy.types.Material.halo_json
    del bpy.types.Light.halo_json
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
