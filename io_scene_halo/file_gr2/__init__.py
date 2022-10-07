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

bl_info = {
    'name': 'Halo GR2 Export',
    'author': 'Generalkidd, Crisp',
    'version': (117, 343, 2552),
    'blender': (3, 3, 0),
    'location': 'File > Export',
    'category': 'Export',
    'description': 'Halo Gen4 Asset Exporter'
    }

import ctypes
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

from ..gr2_utils import (
    special_prefixes,
    GetPerm,
    IsWindows,
    CheckPath,
    ObjectValid,
    ExportPerm,
    ExportBSP,
    ResetPerm,
    GetBoneList,
    GetSceneArmature,
    SelectModelObject,
    SelectModelObjectNoPerm,
    SelectBSPObject,
    DeselectAllObjects,
)

import os
import sys
t = os.getcwd()
t += '\\scripts\\addons\\io_scene_fbx'
sys.modules[bpy.types.IMPORT_SCENE_OT_fbx.__module__].__file__
sys.path.insert(0,t)
from io_scene_fbx import export_fbx_bin

class Export_Halo_GR2(Operator, ExportHelper):
    """Exports a Halo GEN4 Asset using your Halo Editing Kit"""
    bl_idname = 'export_halo.gr2'
    bl_label = 'Export Asset'

    filename_ext = ".fbx"

    filter_glob: StringProperty(
        default='*.fbx',
        options={'HIDDEN'},
        maxlen=1024,
    )
    game_version:EnumProperty(
        name="Game Version",
        description="The game to export this asset for",
        items=[ ('REACH', "Halo Reach", "Export an asset intended for Halo Reach")]
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
    export_sidecar: BoolProperty(
        name="Export Sidecar",
        description="",
        default=True,
    )
    sidecar_type: EnumProperty(
        name='Asset Type',
        description='',
        default='MODEL',
        items=[ ('MODEL', "Model", ""), ('SCENARIO', "Scenario", "")]#, ('DECORATOR', "Decorator", ""), ('PARTICLE MODEL', "Particle Model", "") excluding these until they have been fully implemented
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
    export_specific_bsp: IntProperty(
        name='BSP',
        description='',
        default=0,
        min=0,
        max=99,
        step=5,
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
        default=False,
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

    def GetAssetPath(self):
        asset = self.filepath.rpartition('\\')[0]
        print(asset)
        return asset

    asset_path: StringProperty(
        name='',
        description="",
        get=GetAssetPath,
    )

    def GetAssetName(self):
        asset = self.asset_path.rpartition('\\')[2]
        asset = asset.replace('.fbx', '')
        print(asset)
        return asset

    asset_name: StringProperty(
        name='',
        description="",
        get=GetAssetName,
    )
    import_in_background: BoolProperty(
        name='Run In Backround',
        description="If enabled does not pause use of blender during the import process",
        default=False
    )

    def execute(self, context):
        keywords = self.as_keywords()
        from . import export_gr2, export_sidecar_xml, import_sidecar
        mode = ''
        mode_not_set = False
        if len(bpy.context.selected_objects) > 0:
            mode = bpy.context.object.mode
        else:
            mode_not_set = True

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        if self.export_hidden:
            hidden_list = []
            for ob in tuple(bpy.data.scenes[0].view_layers[0].objects):
                if not ob.visible_get():
                    hidden_list.append(ob)
            
            for ob in hidden_list:
                ob.hide_set(False)

        if self.sidecar_type == 'MODEL':
            
            model_armature = GetSceneArmature()


            if model_armature != None:

                boneslist = GetBoneList(model_armature, self.use_armature_deform_only)

                for ob in bpy.data.objects:
                        if ob.parent == model_armature:
                            if ob.parent_type == 'OBJECT':
                                if not any(m != ' ARMATURE' for m in ob.modifiers):
                                    bpy.ops.object.select_all(action='DESELECT')
                                    ob.select_set(True)
                                    bpy.context.view_layer.objects.active = model_armature
                                    if (ob.type == 'MESH' and (not ob.name.startswith(special_prefixes) or ob.name.startswith('$')) and (ob.halo_json.ObjectMesh_Type == 'PHYSICS' or ob.name.startswith('$')) and ob.halo_json.Object_Type_All == 'MESH') or (ob.type == 'MESH' and (ob.halo_json.Object_Type_All == 'MARKER' or ob.name.startswith('#'))) or ob.type == 'EMPTY' and (ob.halo_json.Object_Type_No_Mesh == 'MARKER' or ob.name.startswith('#')):
                                        bpy.ops.object.parent_set(type='BONE', keep_transform=True)
                                    else:
                                        bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)
            else:
                self.report({'ERROR'},"Model export selected but no armature in scene")
                return {'FINISHED'}

                    
        if self.show_output:
            bpy.ops.wm.console_toggle()

        if(CheckPath(self.filepath)):
            if self.sidecar_type != 'MODEL' or (self.sidecar_type == 'MODEL' and(
                self.output_biped or
                self.output_crate or
                self.output_creature or
                self.output_device_control or
                self.output_device_machine or
                self.output_device_terminal or
                self.output_effect_scenery or
                self.output_equipment or
                self.output_giant or
                self.output_scenery or
                self.output_vehicle or
                self.output_weapon)):
            
                if self.export_method == 'BATCH':

                    scene = bpy.context.scene
                    f_start = scene.frame_start
                    f_end = scene.frame_end

                    scene.frame_start = 0
                    scene.frame_end = 0

                    selection = bpy.context.selected_objects
                    active_ob = bpy.context.active_object

                    if self.sidecar_type == 'MODEL':

                        if self.export_render:
                            perm_list = []
                            for ob in bpy.data.objects:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if SelectModelRender(perm, model_armature, self.export_hidden, self.export_all_perms, self.export_specific_perm):
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'render', '', perm, model_armature, boneslist, **keywords)

                        if self.export_collision:
                            perm_list = []
                            for ob in bpy.data.objects:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if SelectModelCollision(perm, model_armature, self.export_hidden, self.export_all_perms, self.export_specific_perm):
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'collision', '', perm, model_armature, boneslist, **keywords)

                        if self.export_physics:
                            perm_list = []
                            for ob in bpy.data.objects:
                                perm = GetPerm(ob)
                                if perm not in perm_list:
                                    perm_list.append(perm)
                                    if SelectModelPhysics(perm, model_armature, self.export_hidden, self.export_all_perms, self.export_specific_perm):
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'physics', '', perm, model_armature, boneslist, **keywords)

                        if self.export_markers:
                            if SelectModelMarkers(model_armature, self.export_hidden):
                                export_fbx_bin.save(self, context, **keywords)
                                export_gr2.save(self, context, self.report, IsWindows(), 'markers', '', '', model_armature, boneslist, **keywords)

                        if SelectModelSkeleton(model_armature):
                            export_fbx_bin.save(self, context, **keywords)
                            export_gr2.save(self, context, self.report, IsWindows(), 'skeleton', '', '', model_armature, boneslist, **keywords)

                        if self.export_animations and 1<=len(bpy.data.actions):
                            if SelectModelSkeleton(model_armature):
                                bpy.context.view_layer.objects.active = model_armature
                                for action in bpy.data.actions:
                                    model_armature.animation_data.action = action
                                    if action.use_frame_range:
                                        scene.frame_start = int(action.frame_start)
                                        scene.frame_end = int(action.frame_end)
                                    else:
                                        scene.frame_start = f_start
                                        scene.frame_end = f_end
                                    export_fbx_bin.save(self, context, **keywords)
                                    export_gr2.save(self, context, self.report, IsWindows(), 'animations', '', '', model_armature, boneslist, **keywords)
                                
                    elif self.sidecar_type == 'SCENARIO':
                        
                        bsp_list = []
                        shared_bsp_exists = False

                        for ob in bpy.data.objects:
                            if not ob.halo_json.bsp_shared and (ob.halo_json.bsp_index not in bsp_list):
                                bsp_list.append(ob.halo_json.bsp_index)

                        for ob in bpy.data.objects:
                            if ob.halo_json.bsp_shared:
                                shared_bsp_exists = True
                                break
                        print('processing bsp objects')
                        for bsp in bsp_list:
                            if not ob.halo_json.bsp_shared:
                                if self.export_structure:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            print('perm appended')
                                            if SelectStructure(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                print('structure selected')
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'bsp', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_poops:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectPoops(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'poops', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_markers:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectMarkers(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'markers', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_lights:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectLights(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'lights', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_portals:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectPortals(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'portals', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_seams:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectSeams(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'seams', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_water_surfaces:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectWaterSurfaces(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'water', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_fog_planes:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectFog(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'fog', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_cookie_cutters:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectCookie(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'cookie_cutters', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_lightmap_regions:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectLightMapRegions(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'lightmap_region', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_boundary_surfaces:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectBoundarys(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'design', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_water_physics:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectWaterPhysics(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'water_physics', "{0:03}".format(bsp), perm, **keywords)

                                if self.export_rain_occluders:
                                    perm_list = []
                                    for ob in bpy.data.objects:
                                        perm = GetPerm(ob)
                                        if perm not in perm_list:
                                            perm_list.append(perm)
                                            if SelectPoopRains(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp):
                                                export_fbx_bin.save(self, context, **keywords)
                                                export_gr2.save(self, context, self.report, IsWindows(), 'rain_blockers', "{0:03}".format(bsp), perm, **keywords)



                        ############################
                        ##### SHARED STRUCTURE #####
                        ############################

                        if shared_bsp_exists:
                            if self.export_structure:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectStructure(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'bsp', 'shared', perm, **keywords)

                            if self.export_poops:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectPoops(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'poops', 'shared', perm, **keywords)

                            if self.export_markers:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectMarkers(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'markers', 'shared', perm, **keywords)

                            if self.export_lights:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectLights(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'lights', 'shared', perm, **keywords)

                            if self.export_portals:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectPortals(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'portals', 'shared', perm, **keywords)

                            if self.export_seams:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectSeams(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'seams', 'shared', perm, **keywords)

                            if self.export_water_surfaces:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectWaterSurfaces(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'water', 'shared', perm, **keywords)

                            if self.export_lightmap_regions:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectLightMapRegions(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'lightmap_region', 'shared', perm, **keywords)

                            if self.export_boundary_surfaces:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectBoundarys(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'design', 'shared', perm, **keywords)

                            if self.export_water_physics:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectWaterPhysics(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'water_physics', 'shared', perm, **keywords)

                            if self.export_rain_occluders:
                                perm_list = []
                                for ob in bpy.data.objects:
                                    perm = GetPerm(ob)
                                    if perm not in perm_list:
                                        perm_list.append(perm)
                                        SelectPoopRains(bsp, perm, self.export_hidden, self.export_all_perms, self.export_specific_perm, self.export_all_bsps, self.export_specific_bsp)
                                        export_fbx_bin.save(self, context, **keywords)
                                        export_gr2.save(self, context, self.report, IsWindows(), 'rain_blockers', 'shared', perm, **keywords)

                    elif self.sidecar_type == 'DECORATOR':
                        print('not implemented')

                    elif self.sidecar_type == 'PARTICLE MODEL':
                        print('not implemented')

                    scene.frame_start = f_start
                    scene.frame_end = f_end

                    if self.export_hidden:
                        for ob in hidden_list:
                            ob.hide_set(True)

                    for ob in selection:
                        ob.select_set(True)
                    bpy.context.view_layer.objects.active = active_ob
                
                else:
                    export_fbx_bin.save(self, context, **keywords)
                    export_gr2.save(self, context, self.report, IsWindows(), 'selected', **keywords)

                if(IsWindows()):
                    if self.export_sidecar:
                        export_sidecar_xml.save(self, context, self.report, **keywords)
                    import_sidecar.save(self, context, self.report, **keywords)
                    
            elif(not self.export_sidecar):
                export_fbx_bin.save(self, context, **keywords)
                export_gr2.save(self, context, self.report, IsWindows(), 'selected', **keywords)
            else:
                self.report({'ERROR'},"No sidecar output tags selected")


        else:
            if not CheckPath(self.filepath):
                ctypes.windll.user32.MessageBoxW(0, "Invalid Editing Kit path. Please check your editing kit path in add-on preferences and try again.", "Invalid EK Path", 0)
            else:
                ctypes.windll.user32.MessageBoxW(0, "The selected export folder is invalid, please select one within the data folder of your HEK tools.", "Invalid Export Path", 0)
        

        if self.show_output:
            bpy.ops.wm.console_toggle()
        if not mode_not_set:
            bpy.ops.object.mode_set(mode=mode, toggle=False)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        box = layout.box()
        # SETTINGS #
        box.label(text="Settings")

        col = box.column()
        col.prop(self, "game_version", text='Game Version')
        col.prop(self, "export_method", text='Export Method')
        col.prop(self, "sidecar_type", text='Asset Type')
        col.prop(self, "show_output", text='Show Output')
        sub = box.column(heading="Keep")
        sub.prop(self, "keep_fbx")
        sub.prop(self, "keep_json")
        # EXPORT CATEGORIES #
        box = layout.box()
        box.label(text="Export Categories")
        sub = box.column(heading="Export")
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
        col.separator()
        if not self.export_all_perms:
            sub.prop(self, 'export_specific_perm', text='Permutation')
        sub.prop(self, 'export_all_perms', text='All Permutations')

        # SIDECAR SETTINGS #
        box = layout.box()
        box.label(text="Sidecar Settings")
        col = box.column()
        col.prop(self, "export_sidecar")
        if self.export_sidecar:
            if self.sidecar_type == 'MODEL' and self.export_sidecar:
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
            col.prop(self, 'import_in_background')
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

        # SCENE SETTINGS #
        box = layout.box()
        box.label(text="Scene Settings")
        col = box.column()
        col.prop(self, "use_mesh_modifiers")
        col.prop(self, "use_triangles")
        col.prop(self, 'use_armature_deform_only')
        col.separator()
        col.prop(self, "global_scale")

def SelectModelRender(perm, arm, export_hidden, export_all_perms, export_specific_perm):
    return SelectModelObject(perm, arm, export_hidden, export_all_perms, export_specific_perm, 'ObRender')

def SelectModelCollision(perm, arm, export_hidden, export_all_perms, export_specific_perm):
    return SelectModelObject(perm, arm, export_hidden, export_all_perms, export_specific_perm, 'ObCollision')

def SelectModelPhysics(perm, arm, export_hidden, export_all_perms, export_specific_perm):
    return SelectModelObject(perm, arm, export_hidden, export_all_perms, export_specific_perm, 'ObPhysics')

def SelectModelMarkers(arm, export_hidden):
    return SelectModelObject(arm, export_hidden, 'ObMarker')

def SelectModelSkeleton(arm):
    DeselectAllObjects()
    arm.select_set(True)

    return True

def SelectStructure(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObStructure')

def SelectPoops(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObPoops')

def SelectMarkers(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObMarkers')

def SelectLights(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObLights')

def SelectPortals(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObPortals')

def SelectSeams(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObSeams')

def SelectWaterSurfaces(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObWaterSurfaces')

def SelectLightMapRegions(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObLightMapRegions')

def SelectFog(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObFog')

def SelectCookie(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObCookie')

def SelectBoundarys(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObBoundarys')

def SelectWaterPhysics(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObWaterPhysics')

def SelectPoopRains(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp):
    return SelectBSPObject(index, perm, export_hidden, export_all_perms, export_specific_perm, export_all_bsps, export_specific_bsp, 'ObPoopRains')

def menu_func_export(self, context):
    self.layout.operator(Export_Halo_GR2.bl_idname, text="Halo Gen4 Asset Export (.fbx .json .gr2. .xml)")

def register():
    bpy.utils.register_class(Export_Halo_GR2)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(Export_Halo_GR2)

if __name__ == "__main__":
    register()