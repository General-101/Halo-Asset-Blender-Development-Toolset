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

from datetime import datetime
import bpy
import getpass
import xml.etree.cElementTree as ET
import xml.dom.minidom
from os import path

from .nwo_utils import (
    is_design,
    valid_animation_types,
    get_data_path,
    get_perm,
    CheckType,
    is_shared,
    get_structure_from_halo_objects,
    get_design_from_halo_objects,
    get_render_from_halo_objects,
    not_bungie_game,

)


def export_xml(report, context, halo_objects, model_armature=None, lod_count=0, filePath="", sidecar_type='MODEL', asset_path='', game_version='reach',        
                output_biped=False,
                output_crate=False,
                output_creature=False,
                output_device_control=False,
                output_device_dispenser=False,
                output_device_machine=False,
                output_device_terminal=False,
                output_effect_scenery=False,
                output_equipment=False,
                output_giant=False,
                output_scenery=False,
                output_vehicle=False,
                output_weapon=False):
    full_path = filePath.rpartition('\\')[0]
    asset_path = CleanAssetPath(full_path)
    asset_name = asset_path.rpartition('\\')[2]

    BuildSidecar(halo_objects, model_armature, lod_count, asset_path, asset_name, full_path, sidecar_type, context, game_version, output_biped,output_crate,output_creature,output_device_control, output_device_dispenser, output_device_machine,output_device_terminal,output_effect_scenery,output_equipment,output_giant,output_scenery,output_vehicle,output_weapon)

    report({'INFO'},"Sidecar build complete")

def CleanAssetPath(path):
    f_path = path.replace('"','')
    f_path = path.strip('\\')
    f_path = path.replace(get_data_path(),'')

    return f_path

def BuildSidecar(halo_objects, model_armature, lod_count, asset_path, asset_name, full_path, sidecar_type, context, game_version,           
                        output_biped=False,
                        output_crate=False,
                        output_creature=False,
                        output_device_control=False,
                        output_device_dispenser=False,
                        output_device_machine=False,
                        output_device_terminal=False,
                        output_effect_scenery=False,
                        output_equipment=False,
                        output_giant=False,
                        output_scenery=False,
                        output_vehicle=False,
                        output_weapon=False, ):

    m_encoding = 'utf-8'
    m_standalone = 'yes'
    metadata = ET.Element("Metadata")
    # set a boolean to check if game is h4+ or not
    not_bungie_game = game_version in ('h4', 'h2a')
    WriteHeader(metadata)
    if sidecar_type == 'MODEL':
        GetObjectOutputTypes(context, metadata, "model", asset_path, asset_name, GetModelTags(output_biped,output_crate,output_creature,output_device_control, output_device_dispenser, output_device_machine,output_device_terminal,output_effect_scenery,output_equipment,output_giant,output_scenery,output_vehicle,output_weapon))
    elif sidecar_type == 'SCENARIO':
        GetObjectOutputTypes(context, metadata, 'scenario', asset_path, asset_name)
    elif sidecar_type == 'SKY':
        GetObjectOutputTypes(context, metadata, 'sky', asset_path, asset_name)
    elif sidecar_type == 'DECORATOR SET':
        GetObjectOutputTypes(context, metadata, 'decorator_set', asset_path, asset_name, 'decorator_set')
    elif sidecar_type == 'PARTICLE MODEL':
        GetObjectOutputTypes(context, metadata, 'particle_model', asset_path, asset_name, 'particle_model')
    elif sidecar_type == 'PREFAB':
        GetObjectOutputTypes(context, metadata, 'prefab', asset_path, asset_name, 'prefab')
    WriteFolders(metadata, not_bungie_game)
    WriteFaceCollections(metadata, sidecar_type, not_bungie_game)
    if sidecar_type == 'MODEL':
        WriteModelContents(halo_objects, model_armature, metadata, asset_path, asset_name)
    elif sidecar_type == 'SCENARIO':
        WriteScenarioContents(halo_objects, metadata, asset_path, asset_name)
    elif sidecar_type == 'SKY':
        WriteSkyContents(halo_objects, metadata, asset_path, asset_name)
    elif sidecar_type == 'DECORATOR SET':
        WriteDecoratorContents(halo_objects, metadata, asset_path, asset_name, lod_count)
    elif sidecar_type == 'PARTICLE MODEL':
        WriteParticleContents(halo_objects, metadata, asset_path, asset_name)
    elif sidecar_type == 'PREFAB':
        WritePrefabContents(halo_objects, metadata, asset_path, asset_name)

    dom = xml.dom.minidom.parseString(ET.tostring(metadata))
    xml_string = dom.toprettyxml(indent='  ')
    part1, part2 = xml_string.split('?>')
    sidecar_path = path.join(full_path, asset_name + '.sidecar.xml')
    # update sidecar path in halo launcher
    bpy.context.scene.gr2_halo_launcher.sidecar_path = sidecar_path

    with open(sidecar_path, 'w') as xfile:
        xfile.write(part1 + 'encoding=\"{}\" standalone=\"{}\"?>'.format(m_encoding, m_standalone) + part2)
        xfile.close()

def WriteHeader(metadata):
    header = ET.SubElement(metadata, "Header")
    ET.SubElement(header, "MainRev").text = "0"
    ET.SubElement(header, "PointRev").text = "6"
    ET.SubElement(header, "Description").text = "Created using the Halo Blender Toolset"
    ET.SubElement(header, "Created").text = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    ET.SubElement(header, "By").text = getpass.getuser()
    ET.SubElement(header, 'SourceFile').text = bpy.data.filepath
    ET.SubElement(header, "DirectoryType").text = "TAE.Shared.NWOAssetDirectory"
    ET.SubElement(header, "Schema").text = "1"

def GetModelTags(       output_biped=False,
                        output_crate=False,
                        output_creature=False,
                        output_device_control=False,
                        output_device_dispenser=False,
                        output_device_machine=False,
                        output_device_terminal=False,
                        output_effect_scenery=False,
                        output_equipment=False,
                        output_giant=False,
                        output_scenery=False,
                        output_vehicle=False,
                        output_weapon=False):
    
    tags = ['model']

    if output_biped: 
        tags.append('biped')
    if output_crate:
        tags.append('crate')
    if output_creature:
        tags.append('creature')
    if output_device_control:
        tags.append('device_control') 
    if output_device_dispenser:
        tags.append('device_dispenser')
    if output_device_machine:
        tags.append('device_machine')
    if output_device_terminal:
        tags.append('device_terminal')
    if output_effect_scenery:
        tags.append('effect_scenery')
    if output_equipment:
        tags.append('equipment')
    if output_giant:
        tags.append('giant')
    if output_scenery:
        tags.append('scenery')
    if output_vehicle:
        tags.append('vehicle')
    if output_weapon:
        tags.append('weapon')

    return tags

def GetObjectOutputTypes(context, metadata, type, asset_path, asset_name, output_tags=[]):
    asset = ET.SubElement(metadata, "Asset", Name=asset_name, Type=type)
    tagcollection = ET.SubElement(asset, "OutputTagCollection")

    if type == 'model':
        for tag in output_tags: # for each output tag that that user as opted to export, add this to the sidecar
            ET.SubElement(tagcollection, "OutputTag", Type=tag).text = path.join(asset_path, asset_name)
    # models are the only sidecar type with optional high level tags exports, all others are fixed
    elif type == 'scenario':
        ET.SubElement(tagcollection, "OutputTag", Type='scenario_lightmap').text = path.join(asset_path, f'{asset_name}_faux_lightmaps')
        ET.SubElement(tagcollection, "OutputTag", Type='structure_seams').text = path.join(asset_path, asset_name)
        ET.SubElement(tagcollection, "OutputTag", Type='scenario').text = path.join(asset_path, asset_name)

    elif type == 'sky':
        ET.SubElement(tagcollection, "OutputTag", Type='model').text = path.join(asset_path, asset_name)
        ET.SubElement(tagcollection, "OutputTag", Type='scenery').text = path.join(asset_path, asset_name)

    elif type == 'decorator_set':
        ET.SubElement(tagcollection, "OutputTag", Type='decorator_set').text = path.join(asset_path, asset_name)

    elif type == 'particle_model':
        ET.SubElement(tagcollection, "OutputTag", Type='particle_model').text = path.join(asset_path, asset_name)

    elif type == 'prefab':
        ET.SubElement(tagcollection, "OutputTag", Type='prefab').text = path.join(asset_path, asset_name)
    
    else:
        ET.SubElement(tagcollection, "OutputTag", Type='cinematic').text = path.join(asset_path, asset_name)

    shared = ET.SubElement(asset, "SharedAssetCollection")
    # create a shared asset entry for each that exists
    shared_assets = context.scene.gr2.shared_assets
    for asset in shared_assets:
        ET.SubElement(shared, "SharedAsset", Type=f'TAE.Shared.{asset.shared_asset_type}').text = asset.shared_asset_path

def WriteFolders(metadata, not_bungie_game): # Write folders to tell foundation where to look for assets. Used by Librarian
    folders = ET.SubElement(metadata, "Folders")

    ET.SubElement(folders, "Reference").text = "\\reference"
    ET.SubElement(folders, "Temp").text = "\\temp"
    ET.SubElement(folders, "SourceModels").text = "\\models\\work"
    ET.SubElement(folders, "GameModels").text = "\\models"
    ET.SubElement(folders, "GamePhysicsModels").text = "\\models"
    ET.SubElement(folders, "GameCollisionModels").text = "\\models"
    ET.SubElement(folders, "ExportModels").text = "\\export\\models"
    ET.SubElement(folders, "ExportPhysicsModels").text = "\\export\\models"
    ET.SubElement(folders, "ExportCollisionModels").text = "\\export\\models"
    ET.SubElement(folders, "SourceAnimations").text = "\\animations\\work"
    ET.SubElement(folders, "AnimationsRigs").text = "\\animations\\rigs"
    ET.SubElement(folders, "GameAnimations").text = "\\animations"
    ET.SubElement(folders, "ExportAnimations").text = "\\export\\animations"
    ET.SubElement(folders, "SourceBitmaps").text = "\\bitmaps"
    ET.SubElement(folders, "GameBitmaps").text = "\\bitmaps"
    ET.SubElement(folders, "CinemaSource").text = "\\cinematics"
    ET.SubElement(folders, "CinemaExport").text = "\\export\\cinematics"
    ET.SubElement(folders, "ExportBSPs").text = "\\models"
    ET.SubElement(folders, "SourceBSPs").text = "\\models"
    ET.SubElement(folders, "RigFlags").text = "\\animations\\rigs\\flags"
    ET.SubElement(folders, "RigPoses").text = "\\animations\\rigs\\poses"
    ET.SubElement(folders, "RigRenders").text = "\\animations\\rigs\\render"
    ET.SubElement(folders, "Scripts").text = "\\scripts"
    ET.SubElement(folders, "FacePoses").text = "\\animations\\rigs\\poses\\face_poses"
    ET.SubElement(folders, "CinematicOutsource").text = "\\outsource"

    if not_bungie_game:
        ET.SubElement(folders, "Retarget").text = "\\working\\retarget"
        ET.SubElement(folders, "RetargetSourceAnimations").text = "\\working\\retarget\\binge"
        ET.SubElement(folders, "RetargetTargetAnimations").text = "\\working\\retarget\\purge"
        ET.SubElement(folders, "Export").text = "\\export"
        ET.SubElement(folders, "CinematicSceneSegments").text = "\\segments"
        ET.SubElement(folders, "SourceAnimationLibrary").text = "\\animations\\library"

def WriteFaceCollections(metadata, sidecar_type, not_bungie_game): # FaceCollections is where regions and global materials are defined in the sidecar. 
        faceCollections = ET.SubElement(metadata, "FaceCollections")

        if sidecar_type == 'SCENARIO' and not_bungie_game:
            bsp_list = ["default",""]
            f1 = ET.SubElement(faceCollections, "FaceCollection", Name="connected_geometry_bsp_table", StringTable="connected_geometry_bsp_table", Description="BSPs")

            FaceCollectionsEntries = ET.SubElement(f1, "FaceCollectionEntries")
            using_default_bsp = False
            for ob in bpy.context.view_layer.objects:
                if ob.nwo.bsp_name_locked == '':
                    bsp = ob.nwo.bsp_name
                else:
                    bsp = ob.nwo.bsp_name_locked
                if bsp == 'default':
                    using_default_bsp = True
                    break

            ET.SubElement(FaceCollectionsEntries, "FaceCollectionEntry", Index="0", Name="default", Active=str(using_default_bsp).lower())

            count = 1
            for ob in bpy.context.view_layer.objects:
                if ob.nwo.bsp_name_locked == '':
                    bsp = ob.nwo.bsp_name
                else:
                    bsp = ob.nwo.bsp_name_locked
                if bsp not in bsp_list:
                    ET.SubElement(FaceCollectionsEntries, "FaceCollectionEntry", Index=str(count), Name=bsp, Active="true")
                    bsp_list.append(bsp)
                    count += 1     

        if(sidecar_type in ('MODEL', 'SKY')):
            region_list = ["default",""]
            f1 = ET.SubElement(faceCollections, "FaceCollection", Name="regions", StringTable="connected_geometry_regions_table", Description="Model regions")

            FaceCollectionsEntries = ET.SubElement(f1, "FaceCollectionEntries")
            ET.SubElement(FaceCollectionsEntries, "FaceCollectionEntry", Index="0", Name="default", Active="true")

            count = 1
            for ob in bpy.context.view_layer.objects:
                if ob.nwo.Region_Name_Locked == '':
                    region = ob.nwo.Region_Name
                else:
                    region = ob.nwo.Region_Name_Locked
                if region not in region_list:
                    ET.SubElement(FaceCollectionsEntries, "FaceCollectionEntry", Index=str(count), Name=region, Active="true")
                    region_list.append(region)
                    count += 1
        if(sidecar_type in ('MODEL', 'SCENARIO', 'PREFAB', 'SKY')):
            mat_list = ["default",""]
            f2 = ET.SubElement(faceCollections, "FaceCollection", Name="global materials override", StringTable="connected_geometry_global_material_table", Description="Global material overrides")

            FaceCollectionsEntries2 = ET.SubElement(f2, "FaceCollectionEntries")
            ET.SubElement(FaceCollectionsEntries2, "FaceCollectionEntry", Index="0", Name="default", Active="true")

            count = 1
            for ob in bpy.context.view_layer.objects:
                material = ob.nwo.Face_Global_Material
                if material not in mat_list:
                        ET.SubElement(FaceCollectionsEntries2, "FaceCollectionEntry", Index=str(count), Name=material, Active="true")
                        mat_list.append(material)
                        count += 1

def WriteModelContents(halo_objects, model_armature, metadata, asset_path, asset_name):
    ##### RENDER #####
    contents = ET.SubElement(metadata, "Contents")
    content = ET.SubElement(contents, "Content", Name=asset_name, Type='model')
    object = ET.SubElement(content, 'ContentObject', Name='', Type="render_model")

    perm_list = []
    for ob in get_render_from_halo_objects(halo_objects):
        perm = get_perm(ob)
        if (perm not in perm_list):
            perm_list.append(perm)
            network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
            ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'render', perm)
            ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'render', perm)

    output = ET.SubElement(object, 'OutputTagCollection')
    ET.SubElement(output, 'OutputTag', Type='render_model').text = path.join(asset_path, asset_name)

    ##### PHYSICS #####
    if SceneHasPhysicsObject():
        object = ET.SubElement(content, 'ContentObject', Name='', Type="physics_model")

        perm_list = []
        for ob in halo_objects.physics:
            perm = get_perm(ob)
            if (perm not in perm_list):
                perm_list.append(perm)
                network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
                ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'physics', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'physics', perm)

        output = ET.SubElement(object, 'OutputTagCollection')
        ET.SubElement(output, 'OutputTag', Type='physics_model').text = path.join(asset_path, asset_name)

    ##### COLLISION #####    
    if SceneHasCollisionObject():
        object = ET.SubElement(content, 'ContentObject', Name='', Type="collision_model")

        perm_list = []
        for ob in halo_objects.collision:
            perm = get_perm(ob)
            if (perm not in perm_list):
                perm_list.append(perm)
                network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
                ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'collision', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'collision', perm)

        output = ET.SubElement(object, 'OutputTagCollection')
        ET.SubElement(output, 'OutputTag', Type='collision_model').text = path.join(asset_path, asset_name)

    ##### SKELETON #####
    object = ET.SubElement(content, 'ContentObject', Name='', Type="skeleton")
    network = ET.SubElement(object, 'ContentNetwork' , Name='default', Type="")
    ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'skeleton')
    ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'skeleton')

    output = ET.SubElement(object, 'OutputTagCollection')
    
    ##### MARKERS #####
    if SceneHasMarkers():
        object = ET.SubElement(content, 'ContentObject', Name='', Type="markers")
        network = ET.SubElement(object, 'ContentNetwork' , Name='default', Type="")
        ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'markers')
        ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'markers')
        
        output = ET.SubElement(object, 'OutputTagCollection')

    ##### ANIMATIONS #####
    if 1<=len(bpy.data.actions):
        object = ET.SubElement(content, 'ContentObject', Name='', Type="model_animation_graph")

        for anim in bpy.data.actions:
            try:
                model_armature.animation_data.action == anim # causes an assert if action is not in armature
                if anim.name.rpartition('.')[0] != '':
                    anim_name = anim.name.rpartition('.')[0]
                    anim_type = anim.name.rpartition('.')[2]
                    anim_type = anim_type.upper()
                else:
                    anim_name = anim.name
                    anim_type = 'JMM'
                
                if anim_type not in valid_animation_types:
                    anim_type = 'JMM'
                
                match anim_type:
                    case 'JMA':
                        network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Base', ModelAnimationMovementData='XY')
                    case 'JMT':
                        network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Base', ModelAnimationMovementData='XYYaw')
                    case 'JMZ':
                        network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Base', ModelAnimationMovementData='XYZYaw')
                    case 'JMV':
                        network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Base', ModelAnimationMovementData='XYZFullRotation')
                    case 'JMO':
                        network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Overlay', ModelAnimationOverlayType='Keyframe', ModelAnimationOverlayBlending='Additive')
                    case 'JMOX':
                        network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Overlay', ModelAnimationOverlayType='Pose', ModelAnimationOverlayBlending='Additive')
                    case 'JMR':
                        network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Overlay', ModelAnimationOverlayType='Keyframe', ModelAnimationOverlayBlending='ReplacementObjectSpace')
                    case 'JMRX':
                        network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Overlay', ModelAnimationOverlayType='Keyframe', ModelAnimationOverlayBlending='ReplacementLocalSpace')
                    case _:
                        network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Base', ModelAnimationMovementData='None')

                ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, anim_name, 'model_animation_graph')
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, anim_name, 'model_animation_graph')
            except:
                print('Animation ' + anim.name + ' not written to sidecar because it does not exist in the armature')

        output = ET.SubElement(object, 'OutputTagCollection')
        ET.SubElement(output, 'OutputTag', Type='frame_event_list').text = path.join(asset_path, asset_name)
        ET.SubElement(output, 'OutputTag', Type='model_animation_graph').text = path.join(asset_path, asset_name)


def WriteScenarioContents(halo_objects, metadata, asset_path, asset_name):
    contents = ET.SubElement(metadata, "Contents")
    ##### STRUCTURE #####
    if SceneHasBSP(halo_objects):
        bsp_list = []
        shared_bsp_exists = False

        for ob in bpy.context.view_layer.objects:
            if ob.nwo.bsp_name_locked != '':
                if ob.nwo.bsp_name_locked != 'shared' and (ob.nwo.bsp_name_locked not in bsp_list) and not is_design(ob):
                    bsp_list.append(ob.nwo.bsp_name_locked)
            else:
                if ob.nwo.bsp_name != 'shared' and (ob.nwo.bsp_name not in bsp_list) and not is_design(ob):
                    bsp_list.append(ob.nwo.bsp_name)

        # # sort bsp list alphanumerically
        bsp_list.sort()

        for ob in bpy.context.view_layer.objects:
            if ob.nwo.bsp_name_locked != '':
                if ob.nwo.bsp_name_locked == 'shared':
                    shared_bsp_exists = True
                    break
            else:
                if ob.nwo.bsp_name == 'shared':
                    shared_bsp_exists = True
                    break

        shared_permutations = []

        if shared_bsp_exists:
            for ob in get_structure_from_halo_objects(halo_objects):
                if is_shared(ob):
                    perm = get_perm(ob)
                    if (perm not in shared_permutations):
                        shared_permutations.append(perm)
   
        for bsp in bsp_list:
            content = ET.SubElement(contents, "Content", Name=asset_name + '_' + bsp, Type='bsp')
            object = ET.SubElement(content, 'ContentObject', Name='', Type="scenario_structure_bsp")
            permutations = []

            for ob in get_structure_from_halo_objects(halo_objects):
                if ob.nwo.bsp_name_locked == bsp or ob.nwo.bsp_name == bsp and not is_shared(ob):
                    perm = get_perm(ob)
                    if (perm not in permutations):
                        permutations.append(perm)

            for perm in permutations:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_name, bsp, perm), Type="")
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, bsp, perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, bsp, perm)

            for perm in shared_permutations:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_name, 'shared', perm), Type="")
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', perm)

            output = ET.SubElement(object, 'OutputTagCollection')
            ET.SubElement(output, 'OutputTag', Type='scenario_structure_bsp').text = f'{path.join(asset_path, asset_name)}_{bsp}'
            ET.SubElement(output, 'OutputTag', Type='scenario_structure_lighting_info').text = f'{path.join(asset_path, asset_name)}_{bsp}'
        
    ##### STRUCTURE DESIGN #####
    if SceneHasDesign(halo_objects):
        bsp_list = []

        for ob in bpy.context.view_layer.objects:
            if ob.nwo.bsp_name_locked != '':
                if (ob.nwo.bsp_name_locked not in bsp_list) and is_design(ob):
                    bsp_list.append(ob.nwo.bsp_name_locked)
            else:
                if (ob.nwo.bsp_name not in bsp_list) and is_design(ob):
                    bsp_list.append(ob.nwo.bsp_name)

        # sort bsp list alphanumerically
        bsp_list.sort()
        
        for bsp in bsp_list:
            content = ET.SubElement(contents, "Content", Name=f'{asset_name}_{bsp}_structure_design', Type='design')
            object = ET.SubElement(content, 'ContentObject', Name='', Type="structure_design")

            permutations = []

            for ob in get_design_from_halo_objects(halo_objects):
                if ob.nwo.bsp_name_locked == bsp or ob.nwo.bsp_name == bsp:
                    perm = get_perm(ob)
                    if (perm not in permutations):
                        permutations.append(perm)

            for perm in permutations:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_name, bsp, perm, True), Type="")
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, bsp, perm, True)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, bsp, perm, True)

            output = ET.SubElement(object, 'OutputTagCollection')
            ET.SubElement(output, 'OutputTag', Type='structure_design').text = f'{path.join(asset_path, asset_name)}_{bsp}_structure_design'

def WriteSkyContents(halo_objects, metadata, asset_path, asset_name):
    contents = ET.SubElement(metadata, "Contents")
    content = ET.SubElement(contents, "Content", Name=asset_name, Type='model')
    object = ET.SubElement(content, 'ContentObject', Name='', Type="render_model")

    perm_list = []
    for ob in halo_objects.default:
        perm = get_perm(ob)
        if (perm not in perm_list):
            perm_list.append(perm)
            network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
            ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'render', perm)
            ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'render', perm)

    output = ET.SubElement(object, 'OutputTagCollection')
    ET.SubElement(output, 'OutputTag', Type='render_model').text = path.join(asset_path, asset_name)

def WriteDecoratorContents(halo_objects, metadata, asset_path, asset_name, lod_count):
    contents = ET.SubElement(metadata, "Contents")
    content = ET.SubElement(contents, "Content", Name=asset_name, Type='decorator_set')
    if len(halo_objects.decorators) > 0:
        count = 0
        while lod_count > count: # count is treated as an index here, wheras lod_count is a range of 1-4. So for a lod_count of 4 the count will be 3 while make its final loop
            object = ET.SubElement(content, 'ContentObject', Name=str(count), Type="render_model", LOD=str(count))
            network = ET.SubElement(object, 'ContentNetwork' ,Name='default', Type="")
            ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'render')
            ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'render')

            output = ET.SubElement(object, 'OutputTagCollection')
            ET.SubElement(output, 'OutputTag', Type='render_model').text = f'{path.join(asset_path, asset_name)}_lod{str(count + 1)}' # we add 1 here by convention. This results in a tag name that matches the lod value, rather than index
            count += 1

    output = ET.SubElement(object, 'OutputTagCollection')

def WriteParticleContents(halo_objects, metadata, asset_path, asset_name):
    contents = ET.SubElement(metadata, "Contents")
    content = ET.SubElement(contents, "Content", Name=asset_name, Type='particle_model')
    object = ET.SubElement(content, 'ContentObject', Name='', Type="particle_model")

    if len(halo_objects.default) > 0:
        network = ET.SubElement(object, 'ContentNetwork' ,Name=asset_name, Type="")
        ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'particle_model')
        ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'particle_model')

    ET.SubElement(object, 'OutputTagCollection')

def WritePrefabContents(halo_objects, metadata, asset_path, asset_name):
    contents = ET.SubElement(metadata, "Contents")
    content = ET.SubElement(contents, "Content", Name=asset_name, Type='prefab')
    object = ET.SubElement(content, 'ContentObject', Name='', Type="scenario_structure_bsp")

    if len(get_structure_from_halo_objects(halo_objects)) > 0:
        network = ET.SubElement(object, 'ContentNetwork' ,Name=asset_name, Type="")
        ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'prefab')
        ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'prefab')

    output = ET.SubElement(object, 'OutputTagCollection')
    ET.SubElement(output, 'OutputTag', Type='scenario_structure_bsp').text = f'{path.join(asset_path, asset_name)}'
    ET.SubElement(output, 'OutputTag', Type='scenario_structure_lighting_info').text = f'{path.join(asset_path, asset_name)}'

def GetAssetPathBSP(asset_name, bsp, perm='', is_design = False):
    if is_design:
        if perm == 'default':
            name = f'{asset_name}_design_{bsp}'
        else:
            name = f'{asset_name}_design_{bsp}_{perm}'
    else:
        if perm == 'default':
            name = f'{asset_name}_{bsp}'
        else:
            name = f'{asset_name}_{bsp}_{perm}'

    return name

def GetInputFilePathBSP(asset_path, asset_name, bsp, perm='', is_design = False):
    if is_design:
        if perm == 'default':
            f_path = f'{path.join(asset_path, "models", asset_name)}_design_{bsp}.fbx'
        else:
            f_path = f'{path.join(asset_path, "models", asset_name)}_design_{bsp}_{perm}.fbx'
    else:
        if perm == 'default':
            f_path = f'{path.join(asset_path, "models", asset_name)}_{bsp}.fbx'
        else:
            f_path = f'{path.join(asset_path, "models", asset_name)}_{bsp}_{perm}.fbx'

    return f_path

def GetIntermediateFilePathBSP(asset_path, asset_name, bsp, perm='', is_design = False):
    if is_design:
        if perm == 'default':
            f_path = f'{path.join(asset_path, "export", "models", asset_name)}_design_{bsp}.gr2'
        else:
            f_path = f'{path.join(asset_path, "export", "models", asset_name)}_design_{bsp}_{perm}.gr2'
    else:
        if perm == 'default':
            f_path = f'{path.join(asset_path, "export", "models", asset_name)}_{bsp}.gr2'
        else:
            f_path = f'{path.join(asset_path, "export", "models", asset_name)}_{bsp}_{perm}.gr2'

    return f_path

def SceneHasBSP(halo_objects):
    bsp_objects = get_structure_from_halo_objects(halo_objects)
    return len(bsp_objects) > 0

def SceneHasDesign(halo_objects):
    design_objects = get_design_from_halo_objects(halo_objects)
    return len(design_objects) > 0

def GetInputFilePath(asset_path, asset_name, type, perm=''):
    if type == 'model_animation_graph':
        f_path = f'{path.join(asset_path, "animations", asset_name)}.fbx'
    elif type == 'particle_model' or type == 'prefab':
        f_path = f'{path.join(asset_path, "models", asset_name)}.fbx'
    else:
        if perm == '' or perm == 'default':
            f_path = f'{path.join(asset_path, "models", asset_name)}_{type}.fbx'
        else:
            f_path = f'{path.join(asset_path, "models", asset_name)}_{perm}_{type}.fbx'

    return f_path

def GetIntermediateFilePath(asset_path, asset_name, type, perm=''):
    if type == 'model_animation_graph':
        f_path = f'{path.join(asset_path, "export", "animations", asset_name)}.gr2'
    elif type == 'particle_model' or type == 'prefab':
        f_path = f'{path.join(asset_path, "export", "models", asset_name)}.gr2'
    else:
        if perm == '' or perm == 'default':
            f_path = f'{path.join(asset_path, "export", "models", asset_name)}_{type}.gr2'
        else:
            f_path = f'{path.join(asset_path, "export", "models", asset_name)}_{perm}_{type}.gr2'

    return f_path

def SceneHasCollisionObject():
    boolean = False

    for ob in bpy.context.view_layer.objects:
        if CheckType.collision(ob):
            boolean = True
            break
    
    return boolean

def SceneHasPhysicsObject():
    boolean = False

    for ob in bpy.context.view_layer.objects:
        if CheckType.physics(ob):
            boolean = True
            break
    
    return boolean

def SceneHasMarkers():
    boolean = False

    for ob in bpy.context.view_layer.objects:
        if CheckType.marker(ob):
            boolean = True
            break
    
    return boolean

def export_sidecar(operator, context, report, asset_path, halo_objects, model_armature=None, lod_count=0,
        filepath="",
        export_sidecar_xml=False,
        sidecar_type='MODEL',
        game_version='reach',
        output_biped=False,
        output_crate=False,
        output_creature=False,
        output_device_control=False,
        output_device_dispenser=False,
        output_device_machine=False,
        output_device_terminal=False,
        output_effect_scenery=False,
        output_equipment=False,
        output_giant=False,
        output_scenery=False,
        output_vehicle=False,
        output_weapon=False,
        **kwargs
        ):
    if game_version not in ('h4','h2a'):
        output_device_dispenser = False # force this off in case user is not exporting for H4/H2A
        
    if export_sidecar_xml and asset_path != '': # if the user has opted to export a sidecar and a valid asset path exists, proceed
        export_xml(report, context, halo_objects, model_armature, lod_count, filepath, sidecar_type, asset_path, game_version, output_biped, output_crate,output_creature,output_device_control, output_device_dispenser, output_device_machine,output_device_terminal,output_effect_scenery,output_equipment,output_giant,output_scenery,output_vehicle,output_weapon)
    return {'FINISHED'}