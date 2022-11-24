# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Generalkidd & Crisp
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


####################
# TODO NEED TO CHANGE STRUCTURE DESIGN. SHOULD NOT FOLLOW BSP INDEX RULE. SHOULD NOT CONTAIN SHARED


bl_info = {
    'name': 'Halo GR2 Export',
    'author': 'Generalkidd, Crisp',
    'version': (117, 343, 2552),
    'blender': (3, 3, 0),
    'location': 'File > Export',
    'category': 'Export',
    'description': 'Halo Gen4 Asset Exporter'
    }

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty, CollectionProperty
from bpy.types import Operator, Panel, PropertyGroup, UIList
from addon_utils import check
from os.path import exists as file_exists
from os import path
import ctypes
import traceback


from io_scene_halo.gr2_utils import GetDataPath

lightmapper_run_once = False
sidecar_read = False

class Export_Scene_GR2(Operator, ExportHelper):
    """Exports a Halo Granny Asset using your Halo Editing Kit"""
    bl_idname = 'export_scene.gr2'
    bl_label = 'Export Asset'
    bl_options = {'UNDO', 'PRESET'}

    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default='*.fbx',
        options={'HIDDEN'},
        maxlen=1024,
    )
    game_version:EnumProperty(
        name="Game Version",
        description="The game to export this asset for",
        default='reach',
        items=[('reach', "Halo Reach", "Export an asset intended for Halo Reach"), ('h4', "Halo 4", "Export an asset intended for Halo 4"), ('h2a', "Halo 2A MP", "Export an asset intended for Halo 2A MP")]
    )
    keep_fbx: BoolProperty(
        name="FBX",
        description="Keep the source FBX file after GR2 conversion",
        default=True,
    )
    keep_json: BoolProperty(
        name="JSON",
        description="Keep the source JSON file after GR2 conversion",
        default=True,
    )
    export_sidecar_xml: BoolProperty(
        name="Build Sidecar",
        description="",
        default=True,
    )
    sidecar_type: EnumProperty(
        name='Asset Type',
        description='',
        default='MODEL',
        items=[ ('MODEL', "Model", ""), ('SCENARIO', "Scenario", ""), ('SKY', 'Sky', ''), ('DECORATOR SET', 'Decorator Set', ''), ('PARTICLE MODEL', 'Particle Model', '')]
    )
    export_method: EnumProperty(
        name="Export Method",
        description="",
        items=[('BATCH', "Batch", ""), ('SELECTED', "Selected", "")]
    )
    export_animations: BoolProperty(
        name='Animations',
        description='',
        default=True,
    )
    export_render: BoolProperty(
        name='Render Models',
        description='',
        default=True,
    )
    export_collision: BoolProperty(
        name='Collision Models',
        description='',
        default=True,
    )
    export_physics: BoolProperty(
        name='Physics Models',
        description='',
        default=True,
    )
    export_markers: BoolProperty(
        name='Markers',
        description='',
        default=True,
    )
    export_structure: BoolProperty(
        name='Structure',
        description='',
        default=True,
    )
    export_poops: BoolProperty(
        name='Instanced Geometry',
        description='',
        default=True,
    )
    export_markers: BoolProperty(
        name='Markers',
        description='',
        default=True,
    )
    export_lights: BoolProperty(
        name='Lights',
        description='',
        default=True,
    )
    export_portals: BoolProperty(
        name='Portals',
        description='',
        default=True,
    )
    export_seams: BoolProperty(
        name='Seams',
        description='',
        default=True,
    )
    export_water_surfaces: BoolProperty(
        name='Water Surfaces',
        description='',
        default=True,
    )
    export_fog_planes: BoolProperty(
        name='Fog Planes',
        description='',
        default=True,
    )
    export_cookie_cutters: BoolProperty(
        name='Cookie Cutters',
        description='',
        default=True,
    )
    export_lightmap_regions: BoolProperty(
        name='Lightmap Regions',
        description='',
        default=True,
    )
    export_boundary_surfaces: BoolProperty(
        name='Boundary Surfaces',
        description='',
        default=True,
    )
    export_water_physics: BoolProperty(
        name='Water Physics',
        description='',
        default=True,
    )
    export_rain_occluders: BoolProperty(
        name='Rain Occluders',
        description='',
        default=True,
    )
    export_shared: BoolProperty(
        name='Shared',
        description='Export geometry which is shared across all BSPs',
        default=True,
    )
    export_all_bsps: BoolProperty(
        name='All BSPs',
        description='',
        default=True,
    )
    export_specific_bsp: StringProperty(
        name='BSP',
        description='',
        default='',
    )
    export_all_perms: BoolProperty(
        name='All Permutations',
        description='',
        default=True,
    )
    export_specific_perm: StringProperty(
        name='Permutation',
        description='Limited exporting to the named permutation only. Must match case',
        default='',
    )
    output_biped: BoolProperty(
        name='Biped',
        description='',
        default=False,
    )
    output_crate: BoolProperty(
        name='Crate',
        description='',
        default=False,
    )
    output_creature: BoolProperty(
        name='Creature',
        description='',
        default=False,
    )
    output_device_control: BoolProperty(
        name='Device Control',
        description='',
        default=False,
    )
    output_device_machine: BoolProperty(
        name='Device Machine',
        description='',
        default=False,
    )
    output_device_terminal: BoolProperty(
        name='Device Terminal',
        description='',
        default=False,
    )
    output_effect_scenery: BoolProperty(
        name='Effect Scenery',
        description='',
        default=False,
    )
    output_equipment: BoolProperty(
        name='Equipment',
        description='',
        default=False,
    )
    output_giant: BoolProperty(
        name='Giant',
        description='',
        default=False,
    )
    output_scenery: BoolProperty(
        name='Scenery',
        description='',
        default=False,
    )
    output_vehicle: BoolProperty(
        name='Vehicle',
        description='',
        default=False,
    )
    output_weapon: BoolProperty(
        name='Weapon',
        description='',
        default=False,
    )
    import_to_game: BoolProperty(
        name='Import to Game',
        description='',
        default=True,
    )
    show_output: BoolProperty(
        name='Show Output',
        description='',
        default=True
    )
    run_tagwatcher: BoolProperty(
        name='Run Tagwatcher',
        description='Runs tag watcher after asset has been imported',
        default=False
    )
    import_check: BoolProperty(
        name='Check',
        description='Run the import process but produce no output files',
        default=False,
    )
    import_force: BoolProperty(
        name='Force',
        description="Force all files to import even if they haven't changed",
        default=False,
    )
    import_verbose: BoolProperty(
        name='Verbose',
        description="Write additional import progress information to the console",
        default=False,
    )
    import_draft: BoolProperty(
        name='Draft',
        description="Skip generating PRT data. Faster speed, lower quality",
        default=False,
    )
    import_seam_debug: BoolProperty(
        name='Seam Debug',
        description="Write extra seam debugging information to the console",
        default=False,
    )
    import_skip_instances: BoolProperty(
        name='Skip Instances',
        description="Skip importing all instanced geometry",
        default=False,
    )
    import_decompose_instances: BoolProperty(
        name='Decompose Instances',
        description="Run convex decomposition for instanced geometry physics (very slow)",
        default=False,
    )
    import_surpress_errors: BoolProperty(
        name='Surpress Errors',
        description="Do not write errors to vrml files",
        default=False,
    )
    apply_unit_scale: BoolProperty(
        name="Apply Unit",
        description="",
        default=True,
    )
    apply_scale_options: EnumProperty(
        default='FBX_SCALE_UNITS',
        items=[('FBX_SCALE_UNITS', "FBX Units Scale",""),]
    )
    use_selection: BoolProperty(
        name="selection",
        description="",
        default=True,
    )
    add_leaf_bones: BoolProperty(
        name='',
        description='',
        default=False
    )
    bake_anim: BoolProperty(
        name='',
        description='',
        default=True
    )
    bake_anim_use_all_bones: BoolProperty(
        name='',
        description='',
        default=False
    )
    bake_anim_use_nla_strips: BoolProperty(
        name='',
        description='',
        default=False
    )
    bake_anim_use_all_actions: BoolProperty(
        name='',
        description='',
        default=False
    )
    bake_anim_force_startend_keying: BoolProperty(
        name='',
        description='',
        default=False
    )
    use_mesh_modifiers: BoolProperty(
        name='Apply Modifiers',
        description='',
        default=True,
    )
    use_triangles: BoolProperty(
        name='Triangulate',
        description='',
        default=True,
    )
    global_scale: FloatProperty(
        name='Scale',
        description='',
        default=1.0
    )
    use_armature_deform_only: BoolProperty(
        name='Deform Bones Only',
        description='Only export bones with the deform property ticked',
        default=True,
    )

    def UpdateVisible(self, context):
        if self.export_hidden == True:
            self.use_visible = False
        else:
            self.use_visible = True
    
    export_hidden: BoolProperty(
        name="Hidden",
        update=UpdateVisible,
        description="Export visible objects only",
        default=True,
    )
    use_visible: BoolProperty(
        name="",
        description="",
        default=False,
    )
    import_in_background: BoolProperty(
        name='Run In Background',
        description="If enabled does not pause use of blender during the import process",
        default=False
    )
    lightmap_structure: BoolProperty(
        name='Run Lightmapper',
        default=False,
    )
    lightmap_quality: EnumProperty(
        name='Quality',
        items=(('DIRECT', "Direct", ""),
                ('DRAFT', "Draft", ""),
                ('LOW', "Low", ""),
                ('MEDIUM', "Medium", ""),
                ('HIGH', "High", ""),
                ('SUPER', "Super (very slow)", ""),
                ),
        default='DIRECT',
    )
    lightmap_all_bsps: BoolProperty(
        name='Lightmap All',
        default=True,
    )
    lightmap_specific_bsp: IntProperty(
        name='Specific BSP',
        default=0,
        min=0,
        max=99,
        step=5,
    )
    mesh_smooth_type_better: EnumProperty(
            name="Smoothing",
            items=(('None', "None", "Do not generate smoothing groups"),
                   ('Blender', "By Hard edges", ""),
                   ('FBXSDK', "By FBX SDK", ""),
                   ),
            description="Determine how smoothing groups should be generated",
            default='FBXSDK',
            )
    mesh_smooth_type: EnumProperty(
            name="Smoothing",
            items=(('OFF', "Normals Only", "Export only normals instead of writing edge or face smoothing data"),
                   ('FACE', "Face", "Write face smoothing"),
                   ('EDGE', "Edge", "Write edge smoothing"),
                   ),
            description="Export smoothing information "
                        "(prefer 'Normals Only' option if your target importer understand split normals)",
            default='OFF',
            )
    quick_export: BoolProperty(
        name='',
        default=False,
    )
    export_gr2: BoolProperty(
        name='Export GR2 Files',
        default=True,
    )
    # import_bitmaps: BoolProperty(
    #     name='Import Bitmaps',
    #     default=False,
    # )
    # bitmap_type: EnumProperty(
    #     name='Bitmap Type',
    #     items=(('2dtextures', "2D Textures", ""),
    #             ('3dtextures', "3D Textures", ""),
    #             ('cubemaps', "Cubemaps", ""),
    #             ('sprites', "Sprites", ""),
    #             ('interface', "Interface", ""),
    #             ),
    #     default='2dtextures',
    # )

    def __init__(self):
        # SETUP #
        scene = bpy.context.scene
        if scene.halo.game_version in (('reach','h4','h2a')):
            self.game_version = scene.halo.game_version

        sidecar_filepath = scene.gr2_halo_launcher.sidecar_path
        export_settings = []
        if sidecar_filepath != '' and file_exists(sidecar_filepath):
            export_settings = ExportSettingsFromSidecar(sidecar_filepath)
            self.filepath = path.join(sidecar_filepath.rpartition('\\')[0], 'untitled.fbx')
            print(self.filepath)
            # now apply settings
            match export_settings[0]:
                case 'model':
                    self.sidecar_type = 'MODEL'
                case 'scenario':
                    self.sidecar_type = 'SCENARIO'
                case 'sky':
                    self.sidecar_type = 'SKY'
                case 'decorator_set':
                    self.sidecar_type = 'DECORATOR SET'
                case 'particle_model':
                    self.sidecar_type = 'PARTICLE MODEL'
            
            if len(export_settings) > 1: # checks if we should also set output tags
                for tag in export_settings[1]:
                    match tag:
                        case 'biped':
                            self.output_biped = True
                        case 'crate':
                            self.output_crate = True
                        case 'creature':
                            self.output_creature = True
                        case 'device_control':
                            self.output_device_control = True
                        case 'device_machine':
                            self.output_device_machine = True
                        case 'device_terminal':
                            self.output_device_terminal = True
                        case 'effect_scenery':
                            self.output_effect_scenery = True
                        case 'equipment':
                            self.output_equipment = True
                        case 'giant':
                            self.output_giant = True
                        case 'scenery':
                            self.output_scenery = True
                        case 'vehicle':
                            self.output_vehicle = True
                        case 'weapon':
                            self.output_weapon = True

    def execute(self, context):
        #lightmap warning
        skip_lightmapper = False
        global lightmapper_run_once
        if self.lightmap_structure and not lightmapper_run_once:
            response = ctypes.windll.user32.MessageBoxW(0, 'Lightmapping can take a long time & Blender will be unresponsive during the process. Do you want to continue?', 'WARNING', 4)
            lightmapper_run_once = True
            if response != 6:
                skip_lightmapper = True

        print('Preparing Scene for Export...')

        keywords = self.as_keywords()
        console = bpy.ops.wm

        if self.show_output:
            console.console_toggle() # toggle the console so users can see progress of export

        from .prepare_scene import prepare_scene
        (objects_selection, active_object, hidden_objects, mode, model_armature, temp_armature, asset_path, asset, skeleton_bones, halo_objects, timeline_start, timeline_end, lod_count, proxies, unselectable_objects, enabled_exclude_collections
        ) = prepare_scene(context, self.report, **keywords) # prepares the scene for processing and returns information about the scene
        try:
            from .process_scene import process_scene
            process_scene(self, context, keywords, self.report, model_armature, asset_path, asset, skeleton_bones, halo_objects, timeline_start, timeline_end, lod_count, UsingBetterFBX(), skip_lightmapper, **keywords)
        except:
            print('ASSERT: Scene processing failed')
            error = traceback.format_exc()
            self.report({'ERROR'}, error)

        from .repair_scene import repair_scene
        repair_scene(context, self.report, objects_selection, active_object, hidden_objects, mode, temp_armature, timeline_start, timeline_end, model_armature, halo_objects.lights, proxies, unselectable_objects, enabled_exclude_collections, **keywords)

        if self.show_output:
            console.console_toggle()

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        box = layout.box()

        # SETTINGS #
        box.label(text="Settings")

        col = box.column()
        col.prop(self, "game_version", text='Game Version')
        #col.prop(self, "export_method", text='Export Method') # commented out 21.10.2022 - Selected mode is unsupported
        col.prop(self, "sidecar_type", text='Asset Type')
        col.prop(self, "show_output", text='Show Output')
        # GR2 SETTINGS #
        box = layout.box()
        box.label(text="GR2 Settings")
        col = box.column()
        col.prop(self, "export_gr2", text='Export GR2 Files')
        if self.export_gr2:
            col.separator()
            sub = col.column(heading="Keep")
            sub.prop(self, "keep_fbx")
            sub.prop(self, "keep_json")
            col.separator()
            sub = col.column(heading="Export")
            sub.prop(self, "export_hidden")
            if self.sidecar_type == 'MODEL':
                sub.prop(self, "export_animations")
                sub.prop(self, "export_render")
                sub.prop(self, "export_collision")
                sub.prop(self, "export_physics")
                sub.prop(self, "export_markers")
            elif self.sidecar_type == 'SCENARIO':
                sub.prop(self, "export_structure")
                sub.prop(self, 'export_poops')
                sub.prop(self, 'export_markers')
                sub.prop(self, 'export_lights')
                sub.prop(self, 'export_portals')
                sub.prop(self, 'export_seams')
                sub.prop(self, 'export_water_surfaces')
                sub.prop(self, 'export_fog_planes')
                sub.prop(self, 'export_cookie_cutters')
                col.separator()
                sub.prop(self, "export_boundary_surfaces")
                sub.prop(self, "export_water_physics")
                sub.prop(self, "export_rain_occluders")
                col.separator()
                sub.prop(self, 'export_shared')
                if not self.export_all_bsps:
                    sub.prop(self, 'export_specific_bsp')
                sub.prop(self, 'export_all_bsps')
            else:
                sub.prop(self, "export_render")
            if (self.sidecar_type not in ('DECORATOR SET', 'PARTICLE MODEL')):
                col.separator()
                if not self.export_all_perms:
                    sub.prop(self, 'export_specific_perm', text='Permutation')
                sub.prop(self, 'export_all_perms', text='All Permutations')
        # SIDECAR SETTINGS #
        box = layout.box()
        box.label(text="Sidecar Settings")
        col = box.column()
        col.prop(self, "export_sidecar_xml")
        if self.export_sidecar_xml:
            if self.sidecar_type == 'MODEL' and self.export_sidecar_xml:
                sub = box.column(heading="Output Tags")
            if self.sidecar_type == 'MODEL':
                sub.prop(self, "output_biped")
                sub.prop(self, "output_crate")
                sub.prop(self, "output_creature")
                sub.prop(self, "output_device_control")
                sub.prop(self, "output_device_machine")
                sub.prop(self, "output_device_terminal")
                sub.prop(self, "output_effect_scenery")
                sub.prop(self, "output_equipment")
                sub.prop(self, "output_giant")
                sub.prop(self, "output_scenery")
                sub.prop(self, "output_vehicle")
                sub.prop(self, "output_weapon")

        # IMPORT SETTINGS #
        box = layout.box()
        box.label(text="Import Settings")
        col = box.column()
        col.prop(self, "import_to_game")
        if self.import_to_game:
            col.prop(self, "run_tagwatcher")
            #col.prop(self, 'import_in_background') removed for now as risk of causing issues
        if self.import_to_game:
            sub = box.column(heading="Import Flags")
            sub.prop(self, "import_check")
            sub.prop(self, "import_force")
            sub.prop(self, "import_verbose")
            sub.prop(self, "import_surpress_errors")
            if self.sidecar_type == 'SCENARIO':
                sub.prop(self, "import_seam_debug")
                sub.prop(self, "import_skip_instances")
                sub.prop(self, "import_decompose_instances")
            else:
                sub.prop(self, "import_draft")

        # LIGHTMAP SETTINGS #
        if self.sidecar_type == 'SCENARIO':
            box = layout.box()
            box.label(text="Lightmap Settings")
            col = box.column()
            col.prop(self, "lightmap_structure")
            if self.lightmap_structure:
                col.prop(self, "lightmap_quality")
                if not self.lightmap_all_bsps:
                    col.prop(self, 'lightmap_specific_bsp')
                col.prop(self, 'lightmap_all_bsps')

        # # BITMAP SETTINGS #
        # box = layout.box()
        # box.label(text="Bitmap Settings")
        # col = box.column()
        # col.prop(self, "import_bitmaps")
        # if self.import_bitmaps:
        #     col.prop(self, "bitmap_type")

        # SCENE SETTINGS #
        box = layout.box()
        box.label(text="Scene Settings")
        col = box.column()
        col.prop(self, "use_mesh_modifiers")
        col.prop(self, "use_triangles")
        col.prop(self, 'use_armature_deform_only')
        if UsingBetterFBX():
            col.prop(self, 'mesh_smooth_type_better')
        else:
            col.prop(self, 'mesh_smooth_type')
        col.separator()
        col.prop(self, "global_scale")

def menu_func_export(self, context):
    self.layout.operator(Export_Scene_GR2.bl_idname, text="Halo GR2 Exporter (.gr2)")

def UsingBetterFBX():
    using_better_fbx = False
    addon_default, addon_state = check('better_fbx')

    if addon_default or addon_state:
        using_better_fbx = True

    return using_better_fbx

def ExportSettingsFromSidecar(sidecar_filepath):
    settings = []
    import xml.etree.ElementTree as ET
    tree = ET.parse(sidecar_filepath)
    metadata = tree.getroot()
    # get the type of sidecar this is
    asset = metadata.find('Asset')
    asset_type = asset.get('Type')
    # append the type to the settings list
    settings.append(asset_type)
    # if asset type is a model, we need to grab some additional info
    output_tags = []
    if settings[0] == 'model':
        output_collection = asset.find('OutputTagCollection')
        for tag in output_collection.findall('OutputTag'):
            if tag.get('Type') != 'model': # don't collect the model output_tag, we don't need this
                output_tags.append(tag.get('Type'))

        settings.append(output_tags)


    return settings
##############################################
# GR2 Scene Settings
##############################################
class GR2_SceneProps(Panel):
    bl_label = "GR2 Scene Properties"
    bl_idname = "GR2_PT_GameVersionPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"

    def draw(self, context):
        layout = self.layout

# class GR2_UL_SceneProps_RegionManager(UIList):
#     use_name_reverse: bpy.props.BoolProperty(
#         name="Reverse Name",
#         default=False,
#         options=set(),
#         description="Reverse name sort order",
#     )

#     use_order_name: bpy.props.BoolProperty(
#         name="Name",
#         default=False,
#         options=set(),
#         description="Sort groups by their name (case-insensitive)",
#     )

#     filter_string: bpy.props.StringProperty(
#         name="filter_string",
#         default = "",
#         description="Filter string for name"
#     )

#     filter_invert: bpy.props.BoolProperty(
#         name="Invert",
#         default = False,
#         options=set(),
#         description="Invert Filter"
#     )


#     def filter_items(self, context,
#                     data, 
#                     property 
#         ):


#         items = getattr(data, property)
#         if not len(items):
#             return [], []

#         if self.filter_string:
#             flt_flags = bpy.types.UI_UL_list.filter_items_by_name(
#                     self.filter_string,
#                     self.bitflag_filter_item,
#                     items, 
#                     propname="name",
#                     reverse=self.filter_invert)
#         else:
#             flt_flags = [self.bitflag_filter_item] * len(items)

#         if self.use_order_name:
#             flt_neworder = bpy.types.UI_UL_list.sort_items_by_name(items, "name")
#             if self.use_name_reverse:
#                 flt_neworder.reverse()
#         else:
#             flt_neworder = []    


#         return flt_flags, flt_neworder        

#     def draw_filter(self, context,
#                     layout
#         ):

#         row = layout.row(align=True)
#         row.prop(self, "filter_string", text="Filter", icon="VIEWZOOM")
#         row.prop(self, "filter_invert", text="", icon="ARROW_LEFTRIGHT")


#         row = layout.row(align=True)
#         row.label(text="Order by:")
#         row.prop(self, "use_order_name", toggle=True)

#         icon = 'TRIA_UP' if self.use_name_reverse else 'TRIA_DOWN'
#         row.prop(self, "use_name_reverse", text="", icon=icon)

#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         if self.layout_type in {'DEFAULT', 'COMPACT'}:
#             if scene:
#                 layout.label(text=item.region_name, icon='BOOKMARKS')
#             else:
#                 layout.label(text='')
#         elif self.layout_type == 'GRID':
#             layout.alignment = 'CENTER'
#             layout.label(text="", icon_value=icon)

# class GR2_List_Assign_Region(Operator):
#     """ Add an Item to the UIList"""
#     bl_idname = "gr2_region.assign"
#     bl_label = "Add"
#     bl_description = "Add a new shared asset (sidecar) to the list."
#     filename_ext = ''

#     filter_glob: StringProperty(
#         default="*.xml",
#         options={'HIDDEN'},
#         )

#     filepath: StringProperty(
#         name="Sidecar",
#         description="Set path for the Sidecar file",
#         subtype="FILE_PATH"
#     )

#     @classmethod
#     def poll(cls, context):
#         return context.scene
    
#     def execute(self, context):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         scene_gr2.shared_assets.add()
        
#         path = self.filepath
#         path = path.replace(GetDataPath(), '')
#         scene_gr2.shared_assets[-1].shared_asset_path = path
#         scene_gr2.shared_assets_index = len(scene_gr2.shared_assets) - 1
#         context.area.tag_redraw()
#         return {'FINISHED'}

#     def invoke(self, context, event):
#         context.window_manager.fileselect_add(self)

#         return {'RUNNING_MODAL'}

# class GR2_List_Remove_Region(Operator):
#     """ Remove an Item from the UIList"""
#     bl_idname = "gr2_shared_asset.list_remove"
#     bl_label = "Remove"
#     bl_description = "Remove a region from the list."

#     @classmethod
#     def poll(cls, context):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         return context.scene and len(scene_gr2.shared_assets) > 0
    
#     def execute(self, context):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         index = scene_gr2.shared_assets_index
#         scene_gr2.shared_assets.remove(index)
#         return {'FINISHED'}

# class GR2_List_Select_Region(Operator):
#     """ Remove an Item from the UIList"""
#     bl_idname = "gr2_shared_asset.list_remove"
#     bl_label = "Remove"
#     bl_description = "Remove a region from the list."

#     @classmethod
#     def poll(cls, context):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         return context.scene and len(scene_gr2.shared_assets) > 0
    
#     def execute(self, context):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         index = scene_gr2.shared_assets_index
#         scene_gr2.shared_assets.remove(index)
#         return {'FINISHED'}

# class GR2_List_Deselect_Region(Operator):
#     """ Remove an Item from the UIList"""
#     bl_idname = "gr2_shared_asset.list_remove"
#     bl_label = "Remove"
#     bl_description = "Remove a region from the list."

#     @classmethod
#     def poll(cls, context):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         return context.scene and len(scene_gr2.shared_assets) > 0
    
#     def execute(self, context):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         index = scene_gr2.shared_assets_index
#         scene_gr2.shared_assets.remove(index)
#         return {'FINISHED'}

# class GR2_List_CreateAssign_Region(Operator):
#     """ Remove an Item from the UIList"""
#     bl_idname = "gr2_shared_asset.list_remove"
#     bl_label = "Remove"
#     bl_description = "Remove a region from the list."

#     @classmethod
#     def poll(cls, context):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         return context.scene and len(scene_gr2.shared_assets) > 0
    
#     def execute(self, context):
#         scene = context.scene
#         scene_gr2 = scene.gr2
#         index = scene_gr2.shared_assets_index
#         scene_gr2.shared_assets.remove(index)
#         return {'FINISHED'}

# class GR2_Region_ListItems(PropertyGroup):

#     def GetRegionName(self):
#         name = self.shared_asset_path
#         name = name.rpartition('\\')[2]
#         name = name.rpartition('.sidecar.xml')[0]

#         return name

#     region_name: StringProperty(
#         get=GetRegionName,
#     )

class GR2_UL_SceneProps_SharedAssets(UIList):
    use_name_reverse: bpy.props.BoolProperty(
        name="Reverse Name",
        default=False,
        options=set(),
        description="Reverse name sort order",
    )

    use_order_name: bpy.props.BoolProperty(
        name="Name",
        default=False,
        options=set(),
        description="Sort groups by their name (case-insensitive)",
    )

    filter_string: bpy.props.StringProperty(
        name="filter_string",
        default = "",
        description="Filter string for name"
    )

    filter_invert: bpy.props.BoolProperty(
        name="Invert",
        default = False,
        options=set(),
        description="Invert Filter"
    )


    def filter_items(self, context,
                    data, 
                    property 
        ):


        items = getattr(data, property)
        if not len(items):
            return [], []

        if self.filter_string:
            flt_flags = bpy.types.UI_UL_list.filter_items_by_name(
                    self.filter_string,
                    self.bitflag_filter_item,
                    items, 
                    propname="name",
                    reverse=self.filter_invert)
        else:
            flt_flags = [self.bitflag_filter_item] * len(items)

        if self.use_order_name:
            flt_neworder = bpy.types.UI_UL_list.sort_items_by_name(items, "name")
            if self.use_name_reverse:
                flt_neworder.reverse()
        else:
            flt_neworder = []    


        return flt_flags, flt_neworder        

    def draw_filter(self, context,
                    layout
        ):

        row = layout.row(align=True)
        row.prop(self, "filter_string", text="Filter", icon="VIEWZOOM")
        row.prop(self, "filter_invert", text="", icon="ARROW_LEFTRIGHT")


        row = layout.row(align=True)
        row.label(text="Order by:")
        row.prop(self, "use_order_name", toggle=True)

        icon = 'TRIA_UP' if self.use_name_reverse else 'TRIA_DOWN'
        row.prop(self, "use_name_reverse", text="", icon=icon)

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        scene = context.scene
        scene_gr2 = scene.gr2
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            if scene:
                layout.label(text=item.shared_asset_name, icon='BOOKMARKS')
            else:
                layout.label(text='')
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)    
            
class GR2_SceneProps_SharedAssets(Panel):
    bl_label = "Shared Assets"
    bl_idname = "GR2_PT_GameVersionPanel_SharedAssets"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_parent_id = "GR2_PT_GameVersionPanel"

    def draw(self, context):
        scene = context.scene
        scene_gr2 = scene.gr2
        layout = self.layout

        layout.template_list("GR2_UL_SceneProps_SharedAssets", "", scene_gr2, "shared_assets", scene_gr2, 'shared_assets_index')
        # layout.template_list("GR2_UL_SceneProps_SharedAssets", "compact", scene_gr2, "shared_assets", scene_gr2, "shared_assets_index", type='COMPACT') # not needed

        row = layout.row()
        col = row.column(align=True)
        col.operator("gr2_shared_asset.list_add", text="Add")
        col = row.column(align=True)
        col.operator("gr2_shared_asset.list_remove", text="Remove")
        
        if len(scene_gr2.shared_assets) > 0:
            item = scene_gr2.shared_assets[scene_gr2.shared_assets_index]
            row = layout.row()
            # row.prop(item, "shared_asset_name", text='Asset Name') # debug only
            row.prop(item, "shared_asset_path", text='Path')
            row = layout.row()
            row.prop(item, "shared_asset_type", text='Type')

class GR2_List_Add_Shared_Asset(Operator):
    """ Add an Item to the UIList"""
    bl_idname = "gr2_shared_asset.list_add"
    bl_label = "Add"
    bl_description = "Add a new shared asset (sidecar) to the list."
    filename_ext = ''

    filter_glob: StringProperty(
        default="*.xml",
        options={'HIDDEN'},
        )

    filepath: StringProperty(
        name="Sidecar",
        description="Set path for the Sidecar file",
        subtype="FILE_PATH"
    )

    @classmethod
    def poll(cls, context):
        return context.scene
    
    def execute(self, context):
        scene = context.scene
        scene_gr2 = scene.gr2
        scene_gr2.shared_assets.add()
        
        path = self.filepath
        path = path.replace(GetDataPath(), '')
        scene_gr2.shared_assets[-1].shared_asset_path = path
        scene_gr2.shared_assets_index = len(scene_gr2.shared_assets) - 1
        context.area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}

class GR2_List_Remove_Shared_Asset(Operator):
    """ Remove an Item from the UIList"""
    bl_idname = "gr2_shared_asset.list_remove"
    bl_label = "Remove"
    bl_description = "Remove a shared asset (sidecar) from the list."

    @classmethod
    def poll(cls, context):
        scene = context.scene
        scene_gr2 = scene.gr2
        return context.scene and len(scene_gr2.shared_assets) > 0
    
    def execute(self, context):
        scene = context.scene
        scene_gr2 = scene.gr2
        index = scene_gr2.shared_assets_index
        scene_gr2.shared_assets.remove(index)
        return {'FINISHED'}

class GR2_Asset_ListItems(PropertyGroup):

    def GetSharedAssetName(self):
        name = self.shared_asset_path
        name = name.rpartition('\\')[2]
        name = name.rpartition('.sidecar.xml')[0]

        return name

    shared_asset_name: StringProperty(
        get=GetSharedAssetName,
    )

    shared_asset_path: StringProperty()

    shared_asset_types = [
            ('BipedAsset', 'Biped', ''),
            ('CrateAsset', 'Crate', ''),
            ('CreatureAsset', 'Creature', ''),
            ('Device_ControlAsset', 'Device Control', ''),
            ('Device_MachineAsset', 'Device Machine', ''),
            ('Device_TerminalAsset', 'Device Terminal', ''),
            ('Effect_SceneryAsset', 'Effect Scenery', ''),
            ('EquipmentAsset', 'Equipment', ''),
            ('GiantAsset', 'Giant', ''),
            ('SceneryAsset', 'Scenery', ''),
            ('VehicleAsset', 'Vehicle', ''),
            ('WeaponAsset', 'Weapon', ''),
            ('ScenarioAsset', 'Scenario', ''),
            ('Decorator_SetAsset', 'Decorator Set', ''),
            ('Particle_ModelAsset', 'Particle Model', ''),
        ]

    shared_asset_type: EnumProperty(
        name='Type',
        default='BipedAsset',
        options=set(),
        items=shared_asset_types
    )

class GR2_ScenePropertiesGroup(PropertyGroup):
    shared_assets: CollectionProperty(
        type=GR2_Asset_ListItems,
    )

    shared_assets_index: IntProperty(
        name='Index for Shared Asset',
        default=0,
        min=0,
    )
    # region: CollectionProperty(
    #     type=GR2_Region_ListItems,
    # )

    # region_index: IntProperty(
    #     name='Index for Region',
    #     default=0,
    #     min=0,
    # )


classeshalo = (
    Export_Scene_GR2,
    GR2_Asset_ListItems,
    GR2_List_Add_Shared_Asset,
    GR2_List_Remove_Shared_Asset,
    GR2_ScenePropertiesGroup,
    GR2_SceneProps,
    GR2_UL_SceneProps_SharedAssets,
    GR2_SceneProps_SharedAssets,
)

def register():
    for clshalo in classeshalo:
        bpy.utils.register_class(clshalo)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Scene.gr2 = PointerProperty(type=GR2_ScenePropertiesGroup, name="GR2 Scene Properties", description="Set properties for your scene")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Scene.gr2
    for clshalo in classeshalo:
        bpy.utils.unregister_class(clshalo)

if __name__ == "__main__":
    register()