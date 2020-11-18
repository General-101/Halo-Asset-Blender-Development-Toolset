# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
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

ENABLE_DEBUGGING = False
ENABLE_PROFILING = False

bl_info = {
    "name": "Halo Asset Blender Development Toolset",
    "author": "General_101",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Halo CE/2 Jointed Model Skeleton File (.jms), Import-Export Halo CE/2 Jointed Model Animation File (.jma), and Import-Export Halo 2 Amalgam Scene Specification File (.ass). Initial JMS base by Cyboryxmen with changes by Fulsy + MosesofEgypt + con for JMS portion. Initial ASS exporter by Dave Barnes (Aerial Dave)",
    "warning": "",
    "wiki_url": "https://num0005.github.io/h2codez_docs/",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

if "bpy" in locals():
    import importlib
    if "import_jms" in locals():
        importlib.reload(import_jms)
    if "export_jms" in locals():
        importlib.reload(export_jms)
    if "import_jma" in locals():
        importlib.reload(import_jma)
    if "export_jma" in locals():
        importlib.reload(export_jma)
    if "import_ass" in locals():
        importlib.reload(import_ass)
    if "export_ass" in locals():
        importlib.reload(export_ass)
    if "global_functions" in locals():
        importlib.reload(global_functions)

import bpy
import sys
import argparse

def run_code(code_string):
    def toolset_exec(code):
        if ENABLE_PROFILING:
            import cProfile
            cProfile.runctx(code, globals(), caller_locals)
        else:
            exec(code, globals(), caller_locals)
    import inspect
    frame = inspect.currentframe()
    try:
        caller_locals = frame.f_back.f_locals
        # this hack is horrible but it works??
        toolset_exec(f"""locals()['__this_is_a_horrible_hack'] = {code_string}""")
        result = caller_locals['__this_is_a_horrible_hack']
        caller_locals.pop('__this_is_a_horrible_hack', None)
        return result
    except:
        import pdb, traceback
        if not ENABLE_DEBUGGING:
            raise
        _extype, _value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)
    finally:
        del frame

from io_scene_halo.global_functions import global_functions

from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        )

from bpy.types import (
        Operator,
        Panel,
        PropertyGroup,
        )

from bpy.props import (
        BoolProperty,
        EnumProperty,
        FloatProperty,
        IntProperty,
        PointerProperty,
        StringProperty,
        )

class JMS_PhysicsPropertiesGroup(PropertyGroup):
    jms_spring_type: EnumProperty(
    name="Spring Type",
    description="Choose spring type. This option does nothing in your Blender physics simulation.",
        items=(
            ('0', "Standard", "Standard spring"),
            ('1', "Limited",  "Limited spring"),
            ('2', "Stiff",    "Stiff spring"),
        )
    )

class JMS_PhysicsProps(Panel):
    bl_label = "JMS Physics Properties"
    bl_idname = "JMS_PT_PhysicsPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "physics"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "PHYSICS_PT_rigid_body_constraint"
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    @classmethod
    def poll(cls, context):
        ob = context.object
        rbc = ob.rigid_body_constraint

        scene = context.scene
        scene_halo = scene.halo

        if scene_halo.game_version == 'halo2':
            return (ob and rbc and (rbc.type in {'GENERIC_SPRING'})
                    and context.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        scene_halo = scene.halo

        ob = context.object
        obj_jms = ob.jms

        if scene_halo.game_version == 'halo2':
            box = layout.box()
            box.label(text="Spring Type:")
            col = box.column(align=True)
            row = col.row()
            row.prop(obj_jms, "jms_spring_type", text='')

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

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        scene_halo = scene.halo
        current_material = context.object.active_material
        if current_material is not None:
            material_ass_jms = current_material.ass_jms
            if scene_halo.game_version == 'halo2':
                box = layout.box()
                box.label(text="Material Effect:")
                col = box.column(align=True)
                row = col.row()
                row.prop(material_ass_jms, "material_effect", text='')

            box = layout.box()
            col = box.column(align=True)
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

class ASS_JMS_MaterialPropertiesGroup(PropertyGroup):
    material_effect: StringProperty(
        name = "Material Effect",
        default = "",
        description = "Set material effect name"
        )

    two_sided: BoolProperty(
        name ="Two-sided",
        description = "This flag or shader symbol when applied to a material that is applied to a face or surface renders both sides of the surface instead of just the side that the normal is facing.",
        default = False,
        )

    transparent_1_sided: BoolProperty(
        name ="One-sided Transparent",
        description = "One-sided but non-manifold collidable geometry.",
        default = False,
        )

    transparent_2_sided: BoolProperty(
        name ="Two-sided Transparent",
        description = "Two-sided collidable geometry that is not connected to or touching one-sided geometry.",
        default = False,
        )

    render_only: BoolProperty(
        name ="Render Only",
        description = "Non-collidable, Non-solid geometry.",
        default = False,
        )

    collision_only: BoolProperty(
        name ="Collision Only",
        description = "Non-rendered geometry.",
        default = False,
        )

    sphere_collision_only: BoolProperty(
        name ="Sphere Collision Only",
        description = "Non-rendered geometry that ray tests pass through but spheres (bipeds and vehicles) will not.",
        default = False,
        )

    fog_plane: BoolProperty(
        name ="Fog Plane",
        description = "Non-collidable fog plane. This shader symbol when applied to a material that is applied to a face or surface makes the surface not be rendered. The faces acts as a fog plane that can be used to define a volumetric fog region.",
        default = False,
        )

    ladder: BoolProperty(
        name ="Ladder",
        description = "Climbable geometry. This flag or shader symbol when applied to a material that is applied to a face or surface sets the surface up to act as a ladder for the player.",
        default = False,
        )

    breakable: BoolProperty(
        name ="Breakable",
        description = "Two-sided breakable geometry.",
        default = False,
        )

    ai_deafening: BoolProperty(
        name ="AI Deafening",
        description = "A portal that does not propagate sound. This property does not apply to multiplayer levels.",
        default = False,
        )

    no_shadow: BoolProperty(
        name ="No Shadow",
        description = "Does not cast real time shadows.",
        default = False,
        )

    shadow_only: BoolProperty(
        name ="Shadow Only",
        description = "Casts real time shadows but is not visible.",
        default = False,
        )

    lightmap_only: BoolProperty(
        name ="Lightmap Only",
        description = "Emits light in the light mapper but is otherwise non-existent. (non-collidable and non-rendered)",
        default = False,
        )

    precise: BoolProperty(
        name ="Precise",
        description = "Points and triangles are precise and will not be fiddled with in the BSP pass.",
        default = False,
        )

    conveyor: BoolProperty(
        name ="Conveyor",
        description = "Geometry which will have a surface coordinate system and velocity.",
        default = False,
        )

    portal_1_way: BoolProperty(
        name ="Portal (One-Way)",
        description = "Portal can only be seen through in a single direction.",
        default = False,
        )

    portal_door: BoolProperty(
        name ="Portal (Door)",
        description = "Portal visibility is attached to a device machine state.",
        default = False,
        )

    portal_vis_blocker: BoolProperty(
        name ="Portal (Vis Blocker)",
        description = "Portal visibility is completely blocked by this portal.",
        default = False,
        )

    portal_exact: BoolProperty(
        name ="Portal (Exact Portal)",
        description = "Exact Portal property. This flag or shader symbol when applied to a material that is applied to a face or surface makes the surface able to be used to define an exact portal.",
        default = False,
        )

    dislike_photons: BoolProperty(
        name ="Dislikes Photons",
        description = "Photons from sky/sun quads will ignore these materials",
        default = False,
        )

    ignored_by_lightmaps: BoolProperty(
        name ="Dislikes Photons",
        description = "Lightmapper will not add this geometry to it's raytracing scene representation.",
        default = False,
        )

    blocks_sound: BoolProperty(
        name ="Portal (Sound Blocker)",
        description = "Portal that does not propagate any sound.",
        default = False,
        )

    decal_offset: BoolProperty(
        name ="Decal Offset",
        description = "Offsets the faces that this material is applied to as it would normally for a decal.",
        default = False,
        )

class Halo_SceneProps(Panel):
    bl_label = "Halo Scene Properties"
    bl_idname = "HALO_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        scene = context.scene
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_halo, "game_version", text='')
        box = layout.box()
        box.label(text="Export Settings:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Expert Mode:')
        row.prop(scene_halo, "expert_mode", text='')

class Halo_ScenePropertiesGroup(PropertyGroup):
    game_version: EnumProperty(
        name="Game:",
        description="What game will you be exporting for",
        default="halo2",
        items=[ ('haloce', "Halo CE", "Show properties for Halo Custom Edition"),
                ('halo2', "Halo 2", "Show properties for Halo 2 Vista"),
               ]
        )

    expert_mode: BoolProperty(
        name ="Expert Mode",
        description = "Reveal hidden options. If you're not a developer or know what you're doing then you probably shouldn't be messing with this.",
        default = False,
        )

class ASS_SceneProps(Panel):
    bl_label = "ASS Scene Properties"
    bl_idname = "ASS_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GameVersionPanel"
    def draw(self, context):
        scene = context.scene
        scene_ass = scene.ass
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_ass, "game_version", text='')
        if scene_ass.game_version == 'halo2vista':
            if scene_halo.expert_mode:
                box = layout.box()
                box.label(text="File Details:")
                col = box.column(align=True)
                row = col.row()
                row.label(text='ASS Version:')
                row.prop(scene_ass, "ass_version_h2", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Export Hidden Geometry:')
        row.prop(scene_ass, "hidden_geo", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Apply Modifiers:')
        row.prop(scene_ass, "apply_modifiers", text='')
        row = col.row()
        row.label(text='Triangulate:')
        row.prop(scene_ass, "triangulate_faces", text='')
        row = col.row()
        row.label(text='Clean and Normalize Weights:')
        row.prop(scene_ass, "clean_normalize_weights", text='')
        row = col.row()
        row.label(text='Use Edge Split:')
        row.prop(scene_ass, "edge_split", text='')
        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_ass, "use_scene_properties", text='')
        if scene_ass.edge_split == True:
            box = layout.box()
            box.label(text="Edge Split:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Edge Angle:')
            row.prop(scene_ass, "use_edge_angle", text='')
            row.active = scene_ass.use_edge_angle
            row.prop(scene_ass, "split_angle", text='')
            row = col.row()
            row.label(text='Sharp Edges:')
            row.prop(scene_ass, "use_edge_sharp", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.prop(scene_ass, "scale_enum", expand=True)
        if scene_ass.scale_enum == '2':
            row = box.row()
            row.prop(scene_ass, "scale_float")

class ASS_ScenePropertiesGroup(PropertyGroup):
    ass_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="2",
        items=[ ('1', "1", "H2"),
                ('2', "2", "H2"),
               ]
        )

    ass_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="2",
        items=[ ('1', "1", "H2"),
                ('2', "2", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        default="halo2utf8",
        items=[ ('halo2utf8', "Halo 2", "Export a level intended for Halo 2 Vista"),
               ]
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    hidden_geo: BoolProperty(
        name ="Export hidden geometry",
        description = "Whether or not we ignore geometry that has scene options that hides it from the viewport",
        default = True,
        )

    scale_enum: EnumProperty(
    name="Scale",
    description="Choose a preset value to multiply position values by.",
        items=(
            ('0', "Default(ASS)", "Export as is"),
            ('1', "World Units",  "Multiply position values by 100 units"),
            ('2', "Custom",       "Set your own scale multiplier."),
        )
    )

    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by.",
        default=1.0,
        min=1.0,
    )

    console: BoolProperty(
        name ="Console",
        description = "Is your console running?",
        default = False,
        options={'HIDDEN'},
        )

    apply_modifiers: BoolProperty(
        name ="Apply Modifiers",
        description = "Automatically apply modifiers. Does not permanently affect scene",
        default = True,
        )

    triangulate_faces: BoolProperty(
        name ="Triangulate faces",
        description = "Automatically triangulate all faces. Does not permanently affect scene",
        default = True,
        )

    clean_normalize_weights: BoolProperty(
        name ="Clean and Normalize Weights",
        description = "Remove unused vertex groups and normalize weights before export. Permanently affects scene",
        default = True,
        )

    edge_split: BoolProperty(
        name ="Edge Split",
        description = "Apply a edge split modifier.",
        default = True,
        )

    use_edge_angle: BoolProperty(
        name ="Use Edge Angle",
        description = "Split edges with high angle between faces.",
        default = False,
        )

    use_edge_sharp: BoolProperty(
        name ="Use Edge Sharp",
        description = "Split edges that are marked as sharp.",
        default = True,
        )

    split_angle: FloatProperty(
        name="Split Angle",
        description="Angle above which to split edges.",
        subtype='ANGLE',
        default=0.523599,
        min=0.0,
        max=3.141593,
    )

class JMA_SceneProps(Panel):
    bl_label = "JMA Scene Properties"
    bl_idname = "JMA_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GameVersionPanel"
    def draw(self, context):
        scene = context.scene
        scene_jma = scene.jma
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_jma, "game_version", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_jma.game_version == 'haloce':
            row = col.row()
            row.label(text='Extension:')
            row.prop(scene_jma, "extension_ce", text='')
            if scene_halo.expert_mode:
                row = col.row()
                row.label(text='JMA Version:')
                row.prop(scene_jma, "jma_version_ce", text='')

        elif scene_jma.game_version == 'halo2vista':
            row = col.row()
            row.label(text='Extension:')
            row.prop(scene_jma, "extension_h2", text='')
            if scene_halo.expert_mode:
                row = col.row()
                row.label(text='JMA Version:')
                row.prop(scene_jma, "jma_version_h2", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        if scene_jma.game_version == 'halo2vista' and scene_jma.jma_version_h2 == '16395':
            row = col.row()
            row.label(text='Biped Controller:')
            row.prop(scene_jma, "biped_controller", text='')

        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_jma, "use_scene_properties", text='')
        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.prop(scene_jma, "scale_enum", expand=True)
        if scene_jma.scale_enum == '2':
            row = box.row()
            row.prop(scene_jma, "scale_float")

class JMA_ScenePropertiesGroup(PropertyGroup):
    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        options={'HIDDEN'},
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE/H2"),
                ('.JMM', "JMM", "Jointed Model Moving CE/H2"),
                ('.JMT', "JMT", "Jointed Model Turning CE/H2"),
                ('.JMO', "JMO", "Jointed Model Overlay CE/H2"),
                ('.JMR', "JMR", "Jointed Model Replacement CE/H2"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2"),
                ('.JMH', "JMH", "Jointed Model Havok H2"),
                ('.JMZ', "JMZ", "Jointed Model Height CE/H2"),
                ('.JMW', "JMW", "Jointed Model World CE/H2"),
               ]
        )

    extension_ce: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE"),
                ('.JMM', "JMM", "Jointed Model Moving CE"),
                ('.JMT', "JMT", "Jointed Model Turning CE"),
                ('.JMO', "JMO", "Jointed Model Overlay CE"),
                ('.JMR', "JMR", "Jointed Model Replacement CE"),
                ('.JMZ', "JMZ", "Jointed Model Height CE"),
                ('.JMW', "JMW", "Jointed Model World CE"),
               ]
        )

    extension_h2: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation H2"),
                ('.JMM', "JMM", "Jointed Model Moving H2"),
                ('.JMT', "JMT", "Jointed Model Turning H2"),
                ('.JMO', "JMO", "Jointed Model Overlay H2"),
                ('.JMR', "JMR", "Jointed Model Replacement H2"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2"),
                ('.JMH', "JMH", "Jointed Model Havok H2"),
                ('.JMZ', "JMZ", "Jointed Model Height H2"),
                ('.JMW', "JMW", "Jointed Model World H2"),
               ]
        )

    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        options={'HIDDEN'},
        items=[ ('16390', "16390", "CE/H2"),
                ('16391', "16391", "CE/H2"),
                ('16392', "16392", "CE/H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
               ]
        )

    jma_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        items=[ ('16390', "16390", "CE"),
                ('16391', "16391", "CE"),
                ('16392', "16392", "CE"),
               ]
        )

    jma_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H2"),
                ('16391', "16391", "H2"),
                ('16392', "16392", "H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        default="halo2vista",
        items=[ ('haloce', "Halo CE", "Export an animation intended for Halo CE"),
                ('halo2vista', "Halo 2 Vista", "Export an animation intended for Halo 2 Vista"),
               ]
        )

    biped_controller: BoolProperty(
        name ="Biped Controller",
        description = "Transform values for armature object",
        default = False,
        options={'HIDDEN'},
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    scale_enum: EnumProperty(
    name="Scale",
    description="Choose a preset value to multiply position values by.",
        items=(
            ('0', "Default(JMA)", "Export as is"),
            ('1', "World Units",  "Multiply position values by 100 units"),
            ('2', "Custom",       "Set your own scale multiplier."),
        )
    )

    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by.",
        default=1.0,
        min=1.0,
    )

class JMS_SceneProps(Panel):
    bl_label = "JMS Scene Properties"
    bl_idname = "JMS_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_GameVersionPanel"
    def draw(self, context):
        scene = context.scene
        scene_jms = scene.jms
        scene_halo = scene.halo

        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(scene_jms, "game_version", text='')
        if scene_jms.game_version == 'haloce':
            box = layout.box()
            box.label(text="File Details:")
            col = box.column(align=True)
            if scene_halo.expert_mode:
                row = col.row()
                row.label(text='JMS Version:')
                row.prop(scene_jms, "jms_version_ce", text='')

            row = col.row()
            row.label(text='Permutation:')
            row.prop(scene_jms, "permutation_ce", text='')
            row = col.row()
            row.label(text='LOD:')
            row.prop(scene_jms, "level_of_detail_ce", text='')

        elif scene_jms.game_version == 'halo2vista':
            if scene_halo.expert_mode:
                box = layout.box()
                box.label(text="File Details:")
                col = box.column(align=True)
                row = col.row()
                row.label(text='JMS Version:')
                row.prop(scene_jms, "jms_version_h2", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Export Hidden Geometry:')
        row.prop(scene_jms, "hidden_geo", text='')
        row = col.row()
        row.label(text='Export Render Geometry:')
        row.prop(scene_jms, "export_render", text='')
        row = col.row()
        row.label(text='Export Collision Geometry:')
        row.prop(scene_jms, "export_collision", text='')
        if not scene_jms.game_version == 'haloce' :
            row = col.row()
            row.label(text='Export Physics Geometry:')
            row.prop(scene_jms, "export_physics", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.label(text='Generate Asset Subdirectories:')
        row.prop(scene_jms, "folder_structure", text='')
        row = col.row()
        row.label(text='Apply Modifiers:')
        row.prop(scene_jms, "apply_modifiers", text='')
        row = col.row()
        row.label(text='Triangulate:')
        row.prop(scene_jms, "triangulate_faces", text='')
        row = col.row()
        row.label(text='Clean and Normalize Weights:')
        row.prop(scene_jms, "clean_normalize_weights", text='')
        row = col.row()
        row.label(text='Use Edge Split:')
        row.prop(scene_jms, "edge_split", text='')
        row = col.row()
        row.label(text='Use As Default Export Settings:')
        row.prop(scene_jms, "use_scene_properties", text='')
        if scene_jms.edge_split == True:
            box = layout.box()
            box.label(text="Edge Split:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Edge Angle:')
            row.prop(scene_jms, "use_edge_angle", text='')
            row.active = scene_jms.use_edge_angle
            row.prop(scene_jms, "split_angle", text='')
            row = col.row()
            row.label(text='Sharp Edges:')
            row.prop(scene_jms, "use_edge_sharp", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.prop(scene_jms, "scale_enum", expand=True)
        if scene_jms.scale_enum == '2':
            row = box.row()
            row.prop(scene_jms, "scale_float")

class JMS_ScenePropertiesGroup(PropertyGroup):
    permutation_ce: StringProperty(
        name="Permutation",
        description="Permutation for a JMS file",
        subtype="FILE_NAME"
    )

    level_of_detail_ce: EnumProperty(
        name="LOD:",
        description="What LOD to use for the JMS file",
        items=[ ('0', "NONE", ""),
                ('1', "SuperLow", ""),
                ('2', "Low", ""),
                ('3', "Medium", ""),
                ('4', "High", ""),
                ('5', "SuperHigh", ""),
               ]
        )

    jms_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8200",
        options={'HIDDEN'},
        items=[ ('8197', "8197", "CE/H2"),
                ('8198', "8198", "CE/H2"),
                ('8199', "8199", "CE/H2"),
                ('8200', "8200", "CE/H2"),
                ('8201', "8201", "H2 Non-functional"),
                ('8202', "8202", "H2 Non-functional"),
                ('8203', "8203", "H2 Non-functional"),
                ('8204', "8204", "H2 Non-functional"),
                ('8205', "8205", "H2"),
                ('8206', "8206", "H2 Non-functional"),
                ('8207', "8207", "H2 Non-functional"),
                ('8208', "8208", "H2 Non-functional"),
                ('8209', "8209", "H2"),
                ('8210', "8210", "H2"),
               ]
        )

    jms_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8200",
        items=[ ('8197', "8197", "CE"),
                ('8198', "8198", "CE"),
                ('8199', "8199", "CE"),
                ('8200', "8200", "CE"),
               ]
        )

    jms_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8210",
        items=[ ('8197', "8197", "H2"),
                ('8198', "8198", "H2"),
                ('8199', "8199", "H2"),
                ('8200', "8200", "H2"),
                ('8201', "8201", "H2 Non-functional"),
                ('8202', "8202", "H2 Non-functional"),
                ('8203', "8203", "H2 Non-functional"),
                ('8204', "8204", "H2 Non-functional"),
                ('8205', "8205", "H2"),
                ('8206', "8206", "H2 Non-functional"),
                ('8207', "8207", "H2 Non-functional"),
                ('8208', "8208", "H2 Non-functional"),
                ('8209', "8209", "H2"),
                ('8210', "8210", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        default="halo2vista",
        items=[ ('haloce', "Halo CE", "Export a JMS intended for Halo Custom Edition"),
                ('halo2vista', "Halo 2 Vista", "Export a JMS intended for Halo 2 Vista"),
               ]
        )

    folder_structure: BoolProperty(
        name ="Generate Asset Subdirectories",
        description = "Generate folder subdirectories for exported assets",
        default = True,
        )

    apply_modifiers: BoolProperty(
        name ="Apply Modifiers",
        description = "Automatically apply modifiers. Does not permanently affect scene",
        default = True,
        )

    triangulate_faces: BoolProperty(
        name ="Triangulate faces",
        description = "Automatically triangulate all faces. Does not permanently affect scene",
        default = True,
        )

    clean_normalize_weights: BoolProperty(
        name ="Clean and Normalize Weights",
        description = "Remove unused vertex groups and normalize weights before export. Permanently affects scene",
        default = True,
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    hidden_geo: BoolProperty(
        name ="Export hidden geometry",
        description = "Whether or not we ignore geometry that has scene options that hides it from the viewport",
        default = True,
        )

    export_render: BoolProperty(
        name ="Export render geometry",
        description = "Whether or not we ignore geometry that is marked as render",
        default = True,
        )

    export_collision: BoolProperty(
        name ="Export collision geometry",
        description = "Whether or not we ignore geometry that is marked as collision",
        default = True,
        )

    export_physics: BoolProperty(
        name ="Export physics geometry",
        description = "Whether or not we ignore geometry that is marked as physics",
        default = True,
        )

    edge_split: BoolProperty(
        name ="Edge Split",
        description = "Apply a edge split modifier.",
        default = True,
        )

    use_edge_angle: BoolProperty(
        name ="Use Edge Angle",
        description = "Split edges with high angle between faces.",
        default = False,
        )

    use_edge_sharp: BoolProperty(
        name ="Use Edge Sharp",
        description = "Split edges that are marked as sharp.",
        default = True,
        )

    split_angle: FloatProperty(
        name="Split Angle",
        description="Angle above which to split edges.",
        subtype='ANGLE',
        default=0.523599,
        min=0.0,
        max=3.141593,
    )

    scale_enum: EnumProperty(
    name="Scale",
    description="Choose a preset value to multiply position values by.",
        items=(
            ('0', "Default(JMS)", "Export as is"),
            ('1', "World Units",  "Multiply position values by 100 units"),
            ('2', "Custom",       "Set your own scale multiplier."),
        )
    )

    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by.",
        default=1.0,
        min=1.0,
    )

class ASS_JMS_MeshProps(Panel):
    bl_label = "Halo Mesh Properties"
    bl_idname = "ASS_JMS_PT_MeshDetailsPanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(self, context):
        scene = context.scene
        scene_halo = scene.halo

        obj = context.object.data

        ass_jms = None
        if hasattr(obj, 'ass_jms'):
            if scene_halo.game_version == 'halo2':
                ass_jms = obj.ass_jms

        return ass_jms

    def draw(self, context):
        layout = self.layout

        obj = context.object.data
        obj_ass_jms = obj.ass_jms

        scene = context.scene
        scene_halo = scene.halo

        box = layout.box()
        box.label(text="JMS Mesh Details:")
        col = box.column(align=True)
        if scene_halo.game_version == 'halo2':
            row = col.row()
            row.label(text='Bounding Radius:')
            row.prop(obj_ass_jms, "bounding_radius", text='')
            row = col.row()
            row.label(text='LOD:')
            row.prop(obj_ass_jms, "level_of_detail", text='')
            row = col.row()
            row.label(text='Object Type:')
            row.prop(obj_ass_jms, "Object_Type", text='')
            row = col.row()
            row.label(text='XREF Path:')
            row.prop(obj_ass_jms, "XREF_path", text='')

class ASS_JMS_MeshPropertiesGroup(PropertyGroup):
    bounding_radius: BoolProperty(
        name ="Bounding Radius",
        description = "Sets object as a bounding radius",
        default = False,
        )

    level_of_detail: EnumProperty(
        name="LOD:",
        description="What LOD to use for the object",
        items=[ ('0', "NONE", "No level of detail set"),
                ('1', "L1", "Super Low"),
                ('2', "L2", "Low"),
                ('3', "L3", "Medium"),
                ('4', "L4", "High"),
                ('5', "L5", "Super High"),
                ('6', "L6", "Hollywood"),
               ]
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
        subtype="FILE_PATH"
    )

class ExportASS(Operator, ExportHelper):
    """Write an ASS file"""
    bl_idname = 'export_scene.ass'
    bl_label = 'Export ASS'
    filename_ext = '.ASS'
    ass_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="2",
        items=[ ('1', "1", "H2 Non-functional"),
                ('2', "2", "H2"),
               ]
        )

    ass_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="2",
        items=[ ('1', "1", "H2 Non-functional"),
                ('2', "2", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        default="halo2utf8",
        items=[ ('halo2utf8', "Halo 2", "Export a level intended for Halo 2 Vista"),
               ]
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    hidden_geo: BoolProperty(
        name ="Export hidden geometry",
        description = "Whether or not we ignore geometry that has scene options that hides it from the viewport",
        default = True,
        )

    apply_modifiers: BoolProperty(
        name ="Apply Modifiers",
        description = "Automatically apply modifiers. Does not permanently affect scene",
        default = True,
        )

    triangulate_faces: BoolProperty(
        name ="Triangulate faces",
        description = "Automatically triangulate all faces. Does not permanently affect scene",
        default = True,
        )

    clean_normalize_weights: BoolProperty(
        name ="Clean and Normalize Weights",
        description = "Remove unused vertex groups and normalize weights before export. Permanently affects scene",
        default = True,
        )

    edge_split: BoolProperty(
        name ="Edge Split",
        description = "Apply a edge split modifier.",
        default = True,
        )

    use_edge_angle: BoolProperty(
        name ="Use Edge Angle",
        description = "Split edges with high angle between faces.",
        default = False,
        )

    use_edge_sharp: BoolProperty(
        name ="Use Edge Sharp",
        description = "Split edges that are marked as sharp.",
        default = True,
        )

    split_angle: FloatProperty(
        name="Split Angle",
        description="Angle above which to split edges.",
        subtype='ANGLE',
        default=0.523599,
        min=0.0,
        max=3.141593,
    )

    scale_enum: EnumProperty(
    name="Scale",
    description="Choose a preset value to multiply position values by.",
        items=(
            ('0', "Default(ASS)", "Export as is"),
            ('1', "World Units",  "Multiply position values by 100 units"),
            ('2', "Custom",       "Set your own scale multiplier."),
        )
    )

    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by.",
        default=1.0,
        min=1.0,
    )

    console: BoolProperty(
        name ="Console",
        description = "Is your console running?",
        default = False,
        options={'HIDDEN'},
        )

    filter_glob: StringProperty(
        default="*.ass",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from io_scene_halo.file_ass import export_ass
        keywords = [context,
                    self.filepath,
                    self.report,
                    self.ass_version,
                    self.ass_version_h2,
                    self.use_scene_properties,
                    self.hidden_geo,
                    self.apply_modifiers,
                    self.triangulate_faces,
                    self.edge_split,
                    self.use_edge_angle,
                    self.use_edge_sharp,
                    self.split_angle,
                    self.clean_normalize_weights,
                    self.scale_enum,
                    self.scale_float,
                    self.console]

        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--use_scene_properties', dest='use_scene_properties', action='store_true')
            parser.add_argument('-arg3', '--ass_version', dest='ass_version', type=str, default="2")
            parser.add_argument('-arg4', '--game_version', dest='game_version', type=str, default="halo2vista")
            parser.add_argument('-arg5', '--hidden_geo', dest='hidden_geo', action='store_true')
            parser.add_argument('-arg6', '--apply_modifiers', dest='apply_modifiers', action='store_true')
            parser.add_argument('-arg7', '--triangulate_faces', dest='triangulate_faces', action='store_true')
            parser.add_argument('-arg8', '--clean_normalize_weights', dest='clean_normalize_weights', action='store_true')
            parser.add_argument('-arg9', '--edge_split', dest='edge_split', action='store_true')
            parser.add_argument('-arg10', '--use_edge_angle', dest='use_edge_angle', action='store_true')
            parser.add_argument('-arg11', '--use_edge_sharp', dest='use_edge_sharp', action='store_true')
            parser.add_argument('-arg12', '--split_angle', dest='split_angle', type=float, default=1.0)
            parser.add_argument('-arg13', '--scale_enum', dest='scale_enum', type=str, default="0")
            parser.add_argument('-arg14', '--scale_float', dest='scale_float', type=float, default=1.0)
            parser.add_argument('-arg15', '--console', dest='console', action='store_true', default=True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('use_scene_properties: ', args.use_scene_properties)
            print('ass_version: ', args.ass_version)
            print('game_version: ', args.game_version)
            print('hidden_geo: ', args.hidden_geo)
            print('apply_modifiers: ', args.apply_modifiers)
            print('triangulate_faces: ', args.triangulate_faces)
            print('clean_normalize_weights: ', args.clean_normalize_weights)
            print('edge_split: ', args.edge_split)
            print('use_edge_angle: ', args.use_edge_angle)
            print('use_edge_sharp: ', args.use_edge_sharp)
            print('split_angle: ', args.split_angle)
            print('scale_enum: ', args.scale_enum)
            print('scale_float: ', args.scale_float)
            print('console: ', args.console)
            self.filepath = args.filepath
            self.ass_version = args.ass_version
            self.game_version = args.game_version
            self.use_scene_properties = args.use_scene_properties
            self.hidden_geo = args.hidden_geo
            self.apply_modifiers = args.apply_modifiers
            self.triangulate_faces = args.triangulate_faces
            self.clean_normalize_weights = args.clean_normalize_weights
            self.edge_split = args.edge_split
            self.use_edge_angle = args.use_edge_angle
            self.use_edge_sharp = args.use_edge_sharp
            self.split_angle = args.split_angle
            self.scale_enum = args.scale_enum
            self.scale_float = args.scale_float
            self.console = args.console

        encoding = global_functions.get_encoding(self.game_version)
        game_version = self.game_version
        if self.game_version == 'halo2vista':
            game_version = 'halo2'

        return run_code("export_ass.write_file(*keywords, game_version, encoding)")

    def draw(self, context):
        scene = context.scene
        scene_ass = scene.ass
        scene_halo = scene.halo

        layout = self.layout
        is_enabled = True
        if scene_ass.use_scene_properties:
            is_enabled = False

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.prop(self, "game_version", text='')
        if scene_ass.use_scene_properties:
            self.game_version = scene_ass.game_version
            self.ass_version_h2 = scene_ass.ass_version_h2
            self.apply_modifiers = scene_ass.apply_modifiers
            self.triangulate_faces = scene_ass.triangulate_faces
            self.clean_normalize_weights = scene_ass.clean_normalize_weights
            self.hidden_geo = scene_ass.hidden_geo
            self.edge_split = scene_ass.edge_split
            self.use_edge_angle = scene_ass.use_edge_angle
            self.use_edge_sharp = scene_ass.use_edge_sharp
            self.split_angle = scene_ass.split_angle
            self.scale_enum = scene_ass.scale_enum
            self.scale_float = scene_ass.scale_float

        if self.game_version == 'halo2vista':
            if scene_halo.expert_mode:
                box = layout.box()
                box.label(text="File Details:")
                col = box.column(align=True)
                row = col.row()
                row.enabled = is_enabled
                row.label(text='ASS Version:')
                row.prop(self, "ass_version_h2", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Hidden Geometry:')
        row.prop(self, "hidden_geo", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Apply Modifiers:')
        row.prop(self, "apply_modifiers", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Triangulate:')
        row.prop(self, "triangulate_faces", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Clean and Normalize Weights:')
        row.prop(self, "clean_normalize_weights", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Use Edge Split:')
        row.prop(self, "edge_split", text='')
        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_ass, "use_scene_properties", text='')
        if self.edge_split == True:
            box = layout.box()
            box.label(text="Edge Split:")
            col = box.column(align=True)
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Edge Angle:')
            row.prop(self, "use_edge_angle", text='')
            row.active = self.use_edge_angle
            row.prop(self, "split_angle", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Sharp Edges:')
            row.prop(self, "use_edge_sharp", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.enabled = is_enabled
        row.prop(self, "scale_enum", expand=True)
        if self.scale_enum == '2':
            row = box.row()
            row.enabled = is_enabled
            row.prop(self, "scale_float")

class ImportASS(Operator, ImportHelper):
    """Import an ASS file"""
    bl_idname = "import_scene.ass"
    bl_label = "Import ASS"
    filename_ext = '.ASS'

    filter_glob: StringProperty(
        default="*.ass",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from io_scene_halo.file_ass import import_ass
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            self.filepath = args.filepath

        return run_code("import_ass.load_file(context, self.filepath, self.report)")

class ExportJMS(Operator, ExportHelper):
    """Write a JMS file"""
    bl_idname = "export_scene.jms"
    bl_label = "Export JMS"
    filename_ext = ''
    permutation_ce: StringProperty(
        name="Permutation",
        description="Permutation for a JMS file",
        subtype="FILE_NAME"
    )

    level_of_detail_ce: EnumProperty(
        name="LOD:",
        description="What LOD to use for the JMS file",
        items=[ ('0', "NONE", ""),
                ('1', "Super Low", ""),
                ('2', "Low", ""),
                ('3', "Medium", ""),
                ('4', "High", ""),
                ('5', "Super High", ""),
               ]
        )

    jms_version: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8200",
        options={'HIDDEN'},
        items=[ ('8197', "8197", "CE/H2"),
                ('8198', "8198", "CE/H2"),
                ('8199', "8199", "CE/H2"),
                ('8200', "8200", "CE/H2"),
                ('8201', "8201", "H2 Non-functional"),
                ('8202', "8202", "H2 Non-functional"),
                ('8203', "8203", "H2 Non-functional"),
                ('8204', "8204", "H2 Non-functional"),
                ('8205', "8205", "H2"),
                ('8206', "8206", "H2 Non-functional"),
                ('8207', "8207", "H2 Non-functional"),
                ('8208', "8208", "H2 Non-functional"),
                ('8209', "8209", "H2"),
                ('8210', "8210", "H2"),
               ]
        )

    jms_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8200",
        items=[ ('8197', "8197", "CE"),
                ('8198', "8198", "CE"),
                ('8199', "8199", "CE"),
                ('8200', "8200", "CE"),
               ]
        )

    jms_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the model file",
        default="8210",
        items=[ ('8197', "8197", "H2"),
                ('8198', "8198", "H2"),
                ('8199', "8199", "H2"),
                ('8200', "8200", "H2"),
                ('8201', "8201", "H2 Non-functional"),
                ('8202', "8202", "H2 Non-functional"),
                ('8203', "8203", "H2 Non-functional"),
                ('8204', "8204", "H2 Non-functional"),
                ('8205', "8205", "H2"),
                ('8206', "8206", "H2 Non-functional"),
                ('8207', "8207", "H2 Non-functional"),
                ('8208', "8208", "H2 Non-functional"),
                ('8209', "8209", "H2"),
                ('8210', "8210", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        default="halo2vista",
        items=[ ('haloce', "Halo CE", "Export a JMS intended for Halo Custom Edition"),
                ('halo2vista', "Halo 2 Vista", "Export a JMS intended for Halo 2 Vista"),
               ]
        )

    folder_structure: BoolProperty(
        name ="Generate Asset Subdirectories",
        description = "Generate folder subdirectories for exported assets",
        default = True,
        )

    apply_modifiers: BoolProperty(
        name ="Apply Modifiers",
        description = "Automatically apply modifiers. Does not permanently affect scene",
        default = True,
        )

    triangulate_faces: BoolProperty(
        name ="Triangulate faces",
        description = "Automatically triangulate all faces. Does not permanently affect scene",
        default = True,
        )

    clean_normalize_weights: BoolProperty(
        name ="Clean and Normalize Weights",
        description = "Remove unused vertex groups and normalize weights before export. Permanently affects scene",
        default = True,
        )

    use_scene_properties: BoolProperty(
        name ="Use scene properties",
        description = "Use the options set in the scene or uncheck this to override",
        default = False,
        )

    hidden_geo: BoolProperty(
        name ="Export hidden geometry",
        description = "Whether or not we ignore geometry that has scene options that hides it from the viewport",
        default = True,
        )

    export_render: BoolProperty(
        name ="Export render geometry",
        description = "Whether or not we ignore geometry that is marked as render",
        default = True,
        )

    export_collision: BoolProperty(
        name ="Export collision geometry",
        description = "Whether or not we ignore geometry that is marked as collision",
        default = True,
        )

    export_physics: BoolProperty(
        name ="Export physics geometry",
        description = "Whether or not we ignore geometry that is marked as physics",
        default = True,
        )

    edge_split: BoolProperty(
        name ="Edge Split",
        description = "Apply a edge split modifier.",
        default = True,
        )

    use_edge_angle: BoolProperty(
        name ="Use Edge Angle",
        description = "Split edges with high angle between faces.",
        default = False,
        )

    use_edge_sharp: BoolProperty(
        name ="Use Edge Sharp",
        description = "Split edges that are marked as sharp.",
        default = True,
        )

    split_angle: FloatProperty(
        name="Split Angle",
        description="Angle above which to split edges.",
        subtype='ANGLE',
        default=0.523599,
        min=0.0,
        max=3.141593,
    )

    scale_enum: EnumProperty(
    name="Scale",
    description="Choose a preset value to multiply position values by.",
        items=(
            ('0', "Default(JMS)", "Export as is"),
            ('1', "World Units",  "Multiply position values by 100 units"),
            ('2', "Custom",       "Set your own scale multiplier."),
        )
    )

    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by.",
        default=1.0,
        min=1.0,
    )

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    console: BoolProperty(
        name ="Console",
        description = "Is your console running?",
        default = False,
        options={'HIDDEN'},
        )

    def execute(self, context):
        from io_scene_halo.file_jms import export_jms
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--use_scene_properties', dest='use_scene_properties', action='store_true')
            parser.add_argument('-arg3', '--jms_version', dest='jms_version', type=str, default="8210")
            parser.add_argument('-arg4', '--game_version', dest='game_version', type=str, default="halo2vista")
            parser.add_argument('-arg5', '--folder_structure', dest='folder_structure', action='store_true')
            parser.add_argument('-arg6', '--apply_modifiers', dest='apply_modifiers', action='store_true')
            parser.add_argument('-arg7', '--triangulate_faces', dest='triangulate_faces', action='store_true')
            parser.add_argument('-arg8', '--clean_normalize_weights', dest='clean_normalize_weights', action='store_true')
            parser.add_argument('-arg9', '--hidden_geo', dest='hidden_geo', action='store_true')
            parser.add_argument('-arg10', '--permutation', dest='permutation_ce', type=str, default="")
            parser.add_argument('-arg11', '--lod', dest='level_of_detail_ce', type=str, default="0")
            parser.add_argument('-arg12', '--edge_split', dest='edge_split', action='store_true')
            parser.add_argument('-arg13', '--use_edge_angle', dest='use_edge_angle', action='store_true')
            parser.add_argument('-arg14', '--use_edge_sharp', dest='use_edge_sharp', action='store_true')
            parser.add_argument('-arg15', '--split_angle', dest='split_angle', type=float, default=1.0)
            parser.add_argument('-arg16', '--scale_enum', dest='scale_enum', type=str, default="0")
            parser.add_argument('-arg17', '--scale_float', dest='scale_float', type=float, default=1.0)
            parser.add_argument('-arg18', '--console', dest='console', action='store_true', default=True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('use_scene_properties: ', args.use_scene_properties)
            print('jms_version: ', args.jms_version)
            print('game_version: ', args.game_version)
            print('folder_structure: ', args.folder_structure)
            print('apply_modifiers: ', args.apply_modifiers)
            print('triangulate_faces: ', args.triangulate_faces)
            print('clean_normalize_weights: ', args.clean_normalize_weights)
            print('hidden_geo: ', args.hidden_geo)
            print('permutation_ce: ', args.permutation_ce)
            print('level_of_detail_ce: ', args.level_of_detail_ce)
            print('edge_split: ', args.edge_split)
            print('use_edge_angle: ', args.use_edge_angle)
            print('use_edge_sharp: ', args.use_edge_sharp)
            print('split_angle: ', args.split_angle)
            print('scale_enum: ', args.scale_enum)
            print('scale_float: ', args.scale_float)
            print('console: ', args.console)
            self.filepath = args.filepath
            self.use_scene_properties = args.use_scene_properties
            self.jms_version = args.jms_version
            self.game_version = args.game_version
            self.folder_structure = args.folder_structure
            self.apply_modifiers = args.apply_modifiers
            self.triangulate_faces = args.triangulate_faces
            self.clean_normalize_weights = args.clean_normalize_weights
            self.hidden_geo = args.hidden_geo
            self.permutation_ce = args.permutation_ce
            self.level_of_detail_ce = args.level_of_detail_ce
            self.edge_split = args.edge_split
            self.use_edge_angle = args.use_edge_angle
            self.use_edge_sharp = args.use_edge_sharp
            self.split_angle = args.split_angle
            self.scale_enum = args.scale_enum
            self.scale_float = args.scale_float
            self.console = args.console

        encoding = global_functions.get_encoding(self.game_version)
        game_version = self.game_version
        if self.game_version == 'halo2vista':
            game_version = 'halo2'

        return run_code("export_jms.command_queue(context, self.filepath, self.report, self.jms_version, self.jms_version_ce, self.jms_version_h2, self.folder_structure, self.apply_modifiers, self.triangulate_faces, self.edge_split, self.use_edge_angle, self.use_edge_sharp, self.split_angle, self.clean_normalize_weights, self.scale_enum, self.scale_float, self.console, self.permutation_ce, self.level_of_detail_ce, self.hidden_geo, self.export_render, self.export_collision, self.export_physics, game_version, encoding)")

    def draw(self, context):
        scene = context.scene
        scene_jms = scene.jms
        scene_halo = scene.halo

        layout = self.layout

        is_enabled = True
        if scene_jms.use_scene_properties:
            is_enabled = False

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.prop(self, "game_version", text='')

        if scene_jms.use_scene_properties:
            self.game_version = scene_jms.game_version
            self.jms_version_ce = scene_jms.jms_version_ce
            self.permutation_ce = scene_jms.permutation_ce
            self.level_of_detail_ce = scene_jms.level_of_detail_ce
            self.jms_version_h2 = scene_jms.jms_version_h2
            self.folder_structure = scene_jms.folder_structure
            self.apply_modifiers = scene_jms.apply_modifiers
            self.triangulate_faces = scene_jms.triangulate_faces
            self.clean_normalize_weights = scene_jms.clean_normalize_weights
            self.hidden_geo = scene_jms.hidden_geo
            self.export_render = scene_jms.export_render
            self.export_collision = scene_jms.export_collision
            self.export_physics = scene_jms.export_physics
            self.edge_split = scene_jms.edge_split
            self.use_edge_angle = scene_jms.use_edge_angle
            self.split_angle = scene_jms.split_angle
            self.use_edge_sharp = scene_jms.use_edge_sharp
            self.scale_enum = scene_jms.scale_enum
            self.scale_float = scene_jms.scale_float

        if self.game_version == 'haloce':
            box = layout.box()
            box.label(text="File Details:")
            col = box.column(align=True)
            if scene_halo.expert_mode:
                row = col.row()
                row.enabled = is_enabled
                row.label(text='JMS Version:')
                row.prop(self, "jms_version_ce", text='')

            row = col.row()
            row.enabled = is_enabled
            row.label(text='Permutation:')
            row.prop(self, "permutation_ce", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='LOD:')
            row.prop(self, "level_of_detail_ce", text='')

        elif self.game_version == 'halo2vista':
            if scene_halo.expert_mode:
                box = layout.box()
                box.label(text="File Details:")
                col = box.column(align=True)
                row = col.row()
                row.enabled = is_enabled
                row.label(text='JMS Version:')
                row.prop(self, "jms_version_h2", text='')

        box = layout.box()
        box.label(text="Mask Options:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Hidden Geometry:')
        row.prop(self, "hidden_geo", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Render Geometry:')
        row.prop(self, "export_render", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Export Collision Geometry:')
        row.prop(self, "export_collision", text='')
        if not self.game_version == 'haloce':
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Export Physics Geometry:')
            row.prop(self, "export_physics", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Generate Asset Subdirectories:')
        row.prop(self, "folder_structure", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Apply Modifiers:')
        row.prop(self, "apply_modifiers", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Triangulate:')
        row.prop(self, "triangulate_faces", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Clean and Normalize Weights:')
        row.prop(self, "clean_normalize_weights", text='')
        row = col.row()
        row.enabled = is_enabled
        row.label(text='Use Edge Split:')
        row.prop(self, "edge_split", text='')
        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_jms, "use_scene_properties", text='')
        if self.edge_split == True:
            box = layout.box()
            box.label(text="Edge Split:")
            col = box.column(align=True)
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Edge Angle:')
            row.prop(self, "use_edge_angle", text='')
            row.active = self.use_edge_angle
            row.prop(self, "split_angle", text='')
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Sharp Edges:')
            row.prop(self, "use_edge_sharp", text='')

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.enabled = is_enabled
        row.prop(self, "scale_enum", expand=True)
        if self.scale_enum == '2':
            row = box.row()
            row.enabled = is_enabled
            row.prop(self, "scale_float")

class ImportJMS(Operator, ImportHelper):
    """Import a JMS file"""
    bl_idname = "import_scene.jms"
    bl_label = "Import JMS"
    filename_ext = '.JMS'
    game_version: EnumProperty(
        name="Game:",
        description="What game was the model file made for",
        default="auto",
        items=[ ('auto', "Auto", "Attempt to guess the game this JMS was intended for. Will default to CE if this fails."),
                ('haloce', "Halo CE", "Import a JMS intended for Halo Custom Edition"),
                ('halo2', "Halo 2", "Import a JMS intended for Halo 2 Vista"),
               ]
        )

    fix_parents: BoolProperty(
        name ="Force node parents",
        description = "Force thigh bones to use pelvis and clavicles to use spine1. Used to match node import behavior used by Halo 2",
        default = True,
        )

    filter_glob: StringProperty(
        default="*.jms;*.jmp",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from io_scene_halo.file_jms import import_jms
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--game_version', dest='game_version', type=str, default="halo2")
            parser.add_argument('-arg3', '--fix_parents', dest='fix_parents', action='store_true')
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('game_version: ', args.game_version)
            print('fix_parents: ', args.fix_parents)
            self.filepath = args.filepath
            self.game_version = args.game_version
            self.fix_parents = args.fix_parents

        return run_code("import_jms.load_file(context, self.filepath, self.report, self.game_version, self.fix_parents)")

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(self, "game_version", text='')
        if self.game_version == 'auto' or self.game_version == 'halo2':
            box = layout.box()
            box.label(text="Import Options:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Force node parents:')
            row.prop(self, "fix_parents", text='')

class ExportJMA(Operator, ExportHelper):
    """Write a JMA file"""
    bl_idname = "export_jma.export"
    bl_label = "Export Animation"
    filename_ext = ''
    extension: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        options={'HIDDEN'},
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE/H2"),
                ('.JMM', "JMM", "Jointed Model Moving CE/H2"),
                ('.JMT', "JMT", "Jointed Model Turning CE/H2"),
                ('.JMO', "JMO", "Jointed Model Overlay CE/H2"),
                ('.JMR', "JMR", "Jointed Model Replacement CE/H2"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2"),
                ('.JMH', "JMH", "Jointed Model Havok H2"),
                ('.JMZ', "JMZ", "Jointed Model Height CE/H2"),
                ('.JMW', "JMW", "Jointed Model World CE/H2"),
               ]
        )

    extension_ce: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation CE"),
                ('.JMM', "JMM", "Jointed Model Moving CE"),
                ('.JMT', "JMT", "Jointed Model Turning CE"),
                ('.JMO', "JMO", "Jointed Model Overlay CE"),
                ('.JMR', "JMR", "Jointed Model Replacement CE"),
                ('.JMZ', "JMZ", "Jointed Model Height CE"),
                ('.JMW', "JMW", "Jointed Model World CE"),
               ]
        )

    extension_h2: EnumProperty(
        name="Extension:",
        description="What extension to use for the animation file",
        items=[ ('.JMA', "JMA", "Jointed Model Animation H2"),
                ('.JMM', "JMM", "Jointed Model Moving H2"),
                ('.JMT', "JMT", "Jointed Model Turning H2"),
                ('.JMO', "JMO", "Jointed Model Overlay H2"),
                ('.JMR', "JMR", "Jointed Model Replacement H2"),
                ('.JMRX', "JMRX", "Jointed Model Replacement Extended H2"),
                ('.JMH', "JMH", "Jointed Model Havok H2"),
                ('.JMZ', "JMZ", "Jointed Model Height H2"),
                ('.JMW', "JMW", "Jointed Model World H2"),
               ]
        )

    jma_version: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        options={'HIDDEN'},
        items=[ ('16390', "16390", "CE/H2"),
                ('16391', "16391", "CE/H2"),
                ('16392', "16392", "CE/H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
               ]
        )

    jma_version_ce: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16392",
        items=[ ('16390', "16390", "CE"),
                ('16391', "16391", "CE"),
                ('16392', "16392", "CE"),
               ]
        )

    jma_version_h2: EnumProperty(
        name="Version:",
        description="What version to use for the animation file",
        default="16395",
        items=[ ('16390', "16390", "H2"),
                ('16391', "16391", "H2"),
                ('16392', "16392", "H2"),
                ('16393', "16393", "H2"),
                ('16394', "16394", "H2"),
                ('16395', "16395", "H2"),
               ]
        )

    game_version: EnumProperty(
        name="Game:",
        description="What game will the model file be used for",
        default="halo2vista",
        items=[ ('haloce', "Halo CE", "Export an animation intended for Halo CE"),
                ('halo2vista', "Halo 2 Vista", "Export an animation intended for Halo 2 Vista"),
               ]
        )

    custom_frame_rate: EnumProperty(
        name="Framerate:",
        description="Set the framerate this animation will run at.",
        default="30",
        items=[ ("23.98", "23.98", ""),
                ("24", "24", ""),
                ("25", "25", ""),
                ("29.97", "29.97", ""),
                ("30", "30", ""),
                ("50", "50", ""),
                ("59.94", "59.94", ""),
                ("60", "60", ""),
                ("CUSTOM", "CUSTOM", ""),
               ]
        )

    frame_rate_float: IntProperty(
        name="Custom Framerate",
        description="Set your own framerate.",
        default=30,
        min=1,
    )

    biped_controller: BoolProperty(
        name ="Biped Controller",
        description = "Transform values for armature objct",
        default = False,
        options={'HIDDEN'},
        )

    scale_enum: EnumProperty(
    name="Scale",
    description="Choose a preset value to multiply position values by.",
        items=(
            ('0', "Default(JMA)", "Export as is"),
            ('1', "World Units",  "Multiply position values by 100 units"),
            ('2', "Custom",       "Set your own scale multiplier."),
        )
    )

    scale_float: FloatProperty(
        name="Custom Scale",
        description="Choose a custom value to multiply position values by.",
        default=1.0,
        min=1.0,
    )

    filter_glob: StringProperty(
        default="*.jma;*.jmm;*.jmt;*.jmo;*.jmr;*.jmrx;*.jmh;*.jmz;*.jmw",
        options={'HIDDEN'},
        )

    console: BoolProperty(
        name ="Console",
        description = "Is your console running?",
        default = False,
        options={'HIDDEN'},
        )

    def execute(self, context):
        from io_scene_halo.file_jma import export_jma
        keywords = [context,
                    self.filepath,
                    self.report,
                    self.extension,
                    self.extension_ce,
                    self.extension_h2,
                    self.jma_version,
                    self.jma_version_ce,
                    self.jma_version_h2,
                    self.custom_frame_rate,
                    self.frame_rate_float,
                    self.biped_controller,
                    self.scale_enum,
                    self.scale_float,
                    self.console]

        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--extension', dest='extension', type=str, default=".JMA")
            parser.add_argument('-arg3', '--jma_version', dest='jma_version', type=str, default="16392")
            parser.add_argument('-arg4', '--game_version', dest='game_version', type=str, default="halo2vista")
            parser.add_argument('-arg5', '--custom_frame_rate', dest='custom_frame_rate', type=str, default="30")
            parser.add_argument('-arg6', '--frame_rate_float', dest='frame_rate_float', type=str, default=30)
            parser.add_argument('-arg7', '--biped_controller', dest='biped_controller', action='store_true')
            parser.add_argument('-arg8', '--scale_enum', dest='scale_enum', type=str, default="0")
            parser.add_argument('-arg9', '--scale_float', dest='scale_float', type=float, default=1.0)
            parser.add_argument('-arg10', '--console', dest='console', action='store_true', default=True)
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('extension: ', args.extension)
            print('jma_version: ', args.jma_version)
            print('game_version: ', args.game_version)
            print('custom_frame_rate: ', args.custom_frame_rate)
            print('frame_rate_float: ', args.frame_rate_float)
            print('biped_controller: ', args.biped_controller)
            print('scale_enum: ', args.scale_enum)
            print('scale_float: ', args.scale_float)
            print('console: ', args.console)
            self.filepath = args.filepath
            self.extension = args.extension
            self.jma_version = args.jma_version
            self.game_version = args.game_version
            self.custom_frame_rate = args.custom_frame_rate
            self.frame_rate_float = args.frame_rate_float
            self.biped_controller = args.biped_controller
            self.scale_enum = args.scale_enum
            self.scale_float = args.scale_float
            self.console = args.console

        encoding = global_functions.get_encoding(self.game_version)
        game_version = self.game_version
        if self.game_version == 'halo2vista':
            game_version = 'halo2'

        return export_jma.write_file(*keywords, game_version, encoding)

    def draw(self, context):
        fps_options = [23.98, 24, 25, 29.97, 30, 50, 59.94, 60]
        scene = context.scene
        scene_jma = scene.jma
        scene_halo = scene.halo

        layout = self.layout
        is_enabled = True
        if scene_jma.use_scene_properties:
            is_enabled = False

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.enabled = is_enabled
        row.prop(self, "game_version", text='')
        box = layout.box()
        box.label(text="File Details:")
        col = box.column(align=True)
        if scene_jma.use_scene_properties:
            self.game_version = scene_jma.game_version
            self.extension_ce = scene_jma.extension_ce
            self.jma_version_ce = scene_jma.jma_version_ce
            self.extension_h2 = scene_jma.extension_h2
            self.jma_version_h2 = scene_jma.jma_version_h2
            self.scale_enum = scene_jma.scale_enum
            self.scale_float = scene_jma.scale_float
            self.biped_controller = scene_jma.biped_controller
            if scene.render.fps not in fps_options:
                self.custom_frame_rate = 'CUSTOM'
                self.frame_rate_float = scene.render.fps

            else:
                self.custom_frame_rate = '%s' % (scene.render.fps)

        if self.game_version == 'haloce':
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Extension:')
            row.prop(self, "extension_ce", text='')
            if scene_halo.expert_mode:
                row = col.row()
                row.enabled = is_enabled
                row.label(text='JMA Version:')
                row.prop(self, "jma_version_ce", text='')

        elif self.game_version == 'halo2vista':
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Extension:')
            row.prop(self, "extension_h2", text='')
            if scene_halo.expert_mode:
                row = col.row()
                row.enabled = is_enabled
                row.label(text='JMA Version:')
                row.prop(self, "jma_version_h2", text='')

        box = layout.box()
        box.label(text="Scene Options:")
        col = box.column(align=True)
        if self.game_version == 'halo2vista' and self.jma_version_h2 == '16395':
            row = col.row()
            row.enabled = is_enabled
            row.label(text='Biped Controller:')
            row.prop(self, "biped_controller", text='')

        row = col.row()
        row.label(text='Use Scene Export Settings:')
        row.prop(scene_jma, "use_scene_properties", text='')
        if scene_halo.expert_mode:
            box = layout.box()
            box.label(text="Custom Frame Rate:")
            row = box.row()
            row.enabled = is_enabled
            row.prop(self, "custom_frame_rate", text='')
            if self.custom_frame_rate == 'CUSTOM':
                row = box.row()
                row.enabled = is_enabled
                row.prop(self, "frame_rate_float")

        box = layout.box()
        box.label(text="Scale:")
        row = box.row()
        row.enabled = is_enabled
        row.prop(self, "scale_enum", expand=True)
        if self.scale_enum == '2':
            row = box.row()
            row.enabled = is_enabled
            row.prop(self, "scale_float")

class ImportJMA(Operator, ImportHelper):
    """Import a JMA file"""
    bl_idname = "import_scene.jma"
    bl_label = "Import JMA"
    filename_ext = '.JMA'

    game_version: EnumProperty(
        name="Game:",
        description="What game was the model file made for",
        default="auto",
        items=[ ('auto', "Auto", "Attempt to guess the game this JMS was intended for. Will default to CE if this fails."),
                ('haloce', "Halo CE", "Import a JMS intended for Halo Custom Edition"),
                ('halo2', "Halo 2", "Import a JMS intended for Halo 2 Vista"),
               ]
        )

    fix_parents: BoolProperty(
        name ="Force node parents",
        description = "Force thigh bones to use pelvis and clavicles to use spine1. Used to match node import behavior used by Halo 2",
        default = True,
        )

    filter_glob: StringProperty(
        default="*.jma;*.jmm;*.jmt;*.jmo;*.jmr;*.jmrx;*.jmh;*.jmz;*.jmw",
        options={'HIDDEN'},
        )

    def execute(self, context):
        from io_scene_halo.file_jma import import_jma
        if '--' in sys.argv:
            argv = sys.argv[sys.argv.index('--') + 1:]
            parser = argparse.ArgumentParser()
            parser.add_argument('-arg1', '--filepath', dest='filepath', metavar='FILE', required = True)
            parser.add_argument('-arg2', '--fix_parents', dest='fix_parents', action='store_true')
            args = parser.parse_known_args(argv)[0]
            print('filepath: ', args.filepath)
            print('fix_parents: ', args.fix_parents)
            self.filepath = args.filepath
            self.fix_parents = args.fix_parents

        return run_code("import_jma.load_file(context, self.filepath, self.report, self.fix_parents, self.game_version)")

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Game Version:")
        col = box.column(align=True)
        row = col.row()
        row.prop(self, "game_version", text='')
        if self.game_version == 'auto' or self.game_version == 'halo2':
            box = layout.box()
            box.label(text="Import Options:")
            col = box.column(align=True)
            row = col.row()
            row.label(text='Force node parents:')
            row.prop(self, "fix_parents", text='')

def menu_func_export(self, context):
    self.layout.operator(ExportASS.bl_idname, text='Halo Amalgam Scene Specification (.ass)')
    self.layout.operator(ExportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")
    self.layout.operator(ExportJMA.bl_idname, text="Halo Jointed Model Animation (.jma)")

def menu_func_import(self, context):
    self.layout.operator(ImportASS.bl_idname, text="Halo Amalgam Scene Specification (.ass)")
    self.layout.operator(ImportJMS.bl_idname, text="Halo Jointed Model Skeleton (.jms)")
    self.layout.operator(ImportJMA.bl_idname, text="Halo Jointed Model Animation (.jma)")

classeshalo = (
    ASS_JMS_MeshPropertiesGroup,
    ASS_JMS_MaterialPropertiesGroup,
    JMS_PhysicsPropertiesGroup,
    Halo_ScenePropertiesGroup,
    ASS_ScenePropertiesGroup,
    JMS_ScenePropertiesGroup,
    JMA_ScenePropertiesGroup,
    ASS_JMS_MeshProps,
    ASS_JMS_MaterialProps,
    JMS_PhysicsProps,
    Halo_SceneProps,
    ASS_SceneProps,
    JMS_SceneProps,
    JMA_SceneProps,
    ImportASS,
    ExportASS,
    ImportJMS,
    ExportJMS,
    ImportJMA,
    ExportJMA,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)

    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.Armature.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.SunLight.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.AreaLight.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.SpotLight.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.PointLight.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.Mesh.ass_jms = PointerProperty(type=ASS_JMS_MeshPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your mesh")
    bpy.types.Material.ass_jms = PointerProperty(type=ASS_JMS_MaterialPropertiesGroup, name="ASS/JMS Properties", description="Set properties for your materials")
    bpy.types.Object.jms = PointerProperty(type=JMS_PhysicsPropertiesGroup, name="JMS Properties", description="Set properties for your constraints")
    bpy.types.Scene.halo = PointerProperty(type=Halo_ScenePropertiesGroup, name="Halo Scene Properties", description="Set properties for your scene")
    bpy.types.Scene.ass = PointerProperty(type=ASS_ScenePropertiesGroup, name="ASS Scene Properties", description="Set properties for the ASS exporter")
    bpy.types.Scene.jms = PointerProperty(type=JMS_ScenePropertiesGroup, name="JMS Scene Properties", description="Set properties for the JMS exporter")
    bpy.types.Scene.jma = PointerProperty(type=JMA_ScenePropertiesGroup, name="JMA Scene Properties", description="Set properties for the JMA exporter")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    del bpy.types.SunLight.ass_jms
    del bpy.types.AreaLight.ass_jms
    del bpy.types.SpotLight.ass_jms
    del bpy.types.PointLight.ass_jms
    del bpy.types.Armature.ass_jms
    del bpy.types.Mesh.ass_jms
    del bpy.types.Object.jms
    del bpy.types.Material.ass_jms
    del bpy.types.Scene.halo
    del bpy.types.Scene.ass
    del bpy.types.Scene.jms
    del bpy.types.Scene.jma
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == '__main__':
    register()
