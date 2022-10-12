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

from io_scene_halo.file_gr2.prepare_scene import halo_objects

from ..gr2_utils import (
    valid_animation_types,
    GetDataPath,
    GetPerm,
    sel_logic,
)


def export_xml(report, halo_objects, model_armature=None, lod_count=0, filePath="", export_sidecar_xml=False, sidecar_type='MODEL', asset_path='',        
                output_biped=False,
                output_crate=False,
                output_creature=False,
                output_device_control=False,
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

    BuildSidecar(halo_objects, model_armature, lod_count, asset_path, asset_name, full_path, sidecar_type, output_biped,output_crate,output_creature,output_device_control,output_device_machine,output_device_terminal,output_effect_scenery,output_equipment,output_giant,output_scenery,output_vehicle,output_weapon)

    report({'INFO'},"Sidecar build complete")

def CleanAssetPath(path):
    path = path.replace('"','')
    path = path.strip('\\')
    path = path.replace(GetDataPath(),'')

    return path

def BuildSidecar(halo_objects, model_armature, lod_count, asset_path, asset_name, full_path, sidecar_type,               
                        output_biped=False,
                        output_crate=False,
                        output_creature=False,
                        output_device_control=False,
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
    WriteHeader(metadata)
    if sidecar_type == 'MODEL':
        GetObjectOutputTypes(metadata, "model", asset_path, asset_name, GetModelTags(output_biped,output_crate,output_creature,output_device_control,output_device_machine,output_device_terminal,output_effect_scenery,output_equipment,output_giant,output_scenery,output_vehicle,output_weapon))
    elif sidecar_type == 'SCENARIO':
        GetObjectOutputTypes(metadata, 'scenario', asset_path, asset_name)
    elif sidecar_type == 'SKY':
        GetObjectOutputTypes(metadata, 'sky', asset_path, asset_name)
    elif sidecar_type == 'DECORATOR SET':
        GetObjectOutputTypes(metadata, 'decorator set', asset_path, asset_name, 'model')
    elif sidecar_type == 'PARTICLE MODEL':
        GetObjectOutputTypes(metadata, 'particle model', asset_path, asset_name, 'model')
    WriteFolders(metadata)
    WriteFaceCollections(metadata, sidecar_type)
    if sidecar_type == 'MODEL':
        WriteModelContents(halo_objects, model_armature, metadata, asset_path, asset_name)
    if sidecar_type == 'SCENARIO':
        WriteScenarioContents(halo_objects, metadata, asset_path, asset_name)
    if sidecar_type == 'SKY':
        WriteSkyContents(halo_objects, metadata, asset_path, asset_name)
    if sidecar_type == 'DECORATOR SET':
        WriteDecoratorContents(metadata, asset_path, asset_name, lod_count)
    if sidecar_type == 'PARTICLE MODEL':
        WriteParticleContents(metadata, asset_path, asset_name)

    dom = xml.dom.minidom.parseString(ET.tostring(metadata))
    xml_string = dom.toprettyxml(indent='  ')
    part1, part2 = xml_string.split('?>')

    with open(full_path + '\\' + asset_name + '.sidecar.xml', 'w') as xfile:
        xfile.write(part1 + 'encoding=\"{}\" standalone=\"{}\"?>'.format(m_encoding, m_standalone) + part2)
        xfile.close()

def WriteHeader(metadata):
    header = ET.SubElement(metadata, "Header")
    ET.SubElement(header, "MainRev").text = "0"
    ET.SubElement(header, "PointRev").text = "6"
    ET.SubElement(header, "Description").text = "Created using the Halo Blender Toolset"
    ET.SubElement(header, "Created").text = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
    ET.SubElement(header, "By").text = getpass.getuser()
    ET.SubElement(header, "DirectoryType").text = "TAE.Shared.NWOAssetDirectory"
    ET.SubElement(header, "Schema").text = "1"

def GetModelTags(       output_biped=False,
                        output_crate=False,
                        output_creature=False,
                        output_device_control=False,
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

def GetObjectOutputTypes(metadata, type, asset_path, asset_name, output_tags=[]):
    asset = ET.SubElement(metadata, "Asset", Name=asset_name, Type=type)
    tagcollection = ET.SubElement(asset, "OutputTagCollection")

    if type == 'model':
        for tag in output_tags: # for each output tag that that user as opted to export, add this to the sidecar
            ET.SubElement(tagcollection, "OutputTag", Type=tag).text = asset_path + '\\' + asset_name
    # models are the only sidecar type with optional high level tags exports, all others are fixed
    elif type == 'scenario':
        ET.SubElement(tagcollection, "OutputTag", Type='scenario_lightmap').text = asset_path + '\\' + asset_name + '_faux_lightmaps'
        ET.SubElement(tagcollection, "OutputTag", Type='structure_seams').text = asset_path + '\\' + asset_name
        ET.SubElement(tagcollection, "OutputTag", Type='scenario').text = asset_path + '\\' + asset_name

    elif type == 'sky':
        ET.SubElement(tagcollection, "OutputTag", Type='model').text = asset_path + '\\' + asset_name
        ET.SubElement(tagcollection, "OutputTag", Type='scenery').text = asset_path + '\\' + asset_name

    elif type == 'decorator':
        ET.SubElement(tagcollection, "OutputTag", Type='decorator').text = asset_path + '\\' + asset_name

    elif type == 'particle_model':
        ET.SubElement(tagcollection, "OutputTag", Type='particle_model').text = asset_path + '\\' + asset_name
    
    else:
        ET.SubElement(tagcollection, "OutputTag", Type='cinematic').text = asset_path + '\\' + asset_name

def WriteFolders(metadata): # Write folders to tell foundation where to look for assets. Used by Librarian
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
    ET.SubElement(folders, "Scripts").text = "\\scripts"

def WriteFaceCollections(metadata, sidecar_type): # FaceCollections is where regions and global materials are defined in the sidecar. 
        faceCollections = ET.SubElement(metadata, "FaceCollections")

        if(sidecar_type in ('MODEL', 'SKY')):
            region_list = ["default",""]
            f1 = ET.SubElement(faceCollections, "FaceCollection", Name="regions", StringTable="connected_geometry_regions_table", Description="Model regions")

            FaceCollectionsEntries = ET.SubElement(f1, "FaceCollectionEntries")
            ET.SubElement(FaceCollectionsEntries, "FaceCollectionEntry", Index="0", Name="default", Active="true")

            count = 1
            for ob in bpy.data.objects:
                region = ob.halo_json.Region_Name
                if region not in region_list:
                    ET.SubElement(FaceCollectionsEntries, "FaceCollectionEntry", Index=str(count), Name=region, Active="true")
                    region_list.append(region)
                    count += 1
        if(sidecar_type in ('MODEL', 'SCENARIO', 'SKY')):
            mat_list = ["default",""]
            f2 = ET.SubElement(faceCollections, "FaceCollection", Name="global materials override", StringTable="connected_geometry_global_material_table", Description="Global material overrides")

            FaceCollectionsEntries2 = ET.SubElement(f2, "FaceCollectionEntries")
            ET.SubElement(FaceCollectionsEntries2, "FaceCollectionEntry", Index="0", Name="default", Active="true")

            count = 1
            for ob in bpy.data.objects:
                material = ob.halo_json.Face_Global_Material
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
    for ob in halo_objects.render:
        perm = GetPerm(ob)
        if (perm not in perm_list):
            perm_list.append(perm)
            network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
            ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'render', ob.halo_json.Permutation_Name)
            ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'render', ob.halo_json.Permutation_Name)

    output = ET.SubElement(object, 'OutputTagCollection')
    ET.SubElement(output, 'OutputTag', Type='render_model').text = asset_path + '\\' + asset_name

    ##### PHYSICS #####
    if SceneHasPhysicsObject():
        object = ET.SubElement(content, 'ContentObject', Name='', Type="physics_model")

        perm_list = []
        for ob in halo_objects.physics:
            perm = GetPerm(ob)
            if (perm not in perm_list):
                perm_list.append(perm)
                network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
                ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'physics', ob.halo_json.Permutation_Name)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'physics', ob.halo_json.Permutation_Name)

        output = ET.SubElement(object, 'OutputTagCollection')
        ET.SubElement(output, 'OutputTag', Type='physics_model').text = asset_path + '\\' + asset_name

    ##### COLLISION #####    
    if SceneHasCollisionObject():
        object = ET.SubElement(content, 'ContentObject', Name='', Type="collision_model")

        perm_list = []
        for ob in halo_objects.collision:
            perm = GetPerm(ob)
            if (perm not in perm_list):
                perm_list.append(perm)
                network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
                ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'collision', ob.halo_json.Permutation_Name)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'collision', ob.halo_json.Permutation_Name)

        output = ET.SubElement(object, 'OutputTagCollection')
        ET.SubElement(output, 'OutputTag', Type='collision_model').text = asset_path + '\\' + asset_name

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
        ET.SubElement(output, 'OutputTag', Type='frame_event_list').text = asset_path + '\\' + asset_name
        ET.SubElement(output, 'OutputTag', Type='model_animation_graph').text = asset_path + '\\' + asset_name

def WriteScenarioContents(halo_objects, metadata, asset_path, asset_name):
    contents = ET.SubElement(metadata, "Contents", BuiltByImportFarm="True")
    ##### STRUCTURE #####
    if SceneHasBSP(halo_objects):
        bsp_list = []
        shared_bsp_exists = False

        for ob in bpy.data.objects:
            if not ob.halo_json.bsp_shared and (ob.halo_json.bsp_index not in bsp_list):
                bsp_list.append(ob.halo_json.bsp_index)

        for ob in bpy.data.objects:
            if ob.halo_json.bsp_shared:
                shared_bsp_exists = True
                break

        shared_structure_perm = []
        shared_poop_perm = []
        shared_marker_perm = []
        shared_light_perm = []
        shared_portal_perm = []
        shared_seam_perm = []
        shared_water_perm = []
        shared_lightmap_perm = []
        shared_cookie_perm = []

        if shared_bsp_exists:
            for ob in halo_objects.structure:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_structure_perm):
                        shared_structure_perm.append(perm)
            for ob in halo_objects.poops:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_poop_perm):
                        shared_poop_perm.append(perm)

            for ob in halo_objects.markers:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_marker_perm):
                        shared_marker_perm.append(perm)

            for ob in halo_objects.lights:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_light_perm):
                        shared_light_perm.append(perm)

            for ob in halo_objects.portals:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_portal_perm):
                        shared_portal_perm.append(perm)

            for ob in halo_objects.seams:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_seam_perm):
                        shared_seam_perm.append(perm)

            for ob in halo_objects.water_surfaces:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_water_perm):
                        shared_water_perm.append(perm)

            for ob in halo_objects.lightmap_regions:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_lightmap_perm):
                        shared_lightmap_perm.append(perm)

            for ob in halo_objects.cookie_cutters:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_cookie_perm):
                        shared_cookie_perm.append(perm)

        for bsp in bsp_list:
            content = ET.SubElement(contents, "Content", Name=asset_name + '_' + "{0:03}".format(bsp), Type='bsp', BspErrorPolicy='auto_generated_physics')
            object = ET.SubElement(content, 'ContentObject', Name='', Type="scenario_structure_bsp")
            structure_perm = []
            poop_perm = []
            marker_perm = []
            light_perm = []
            portal_perm = []
            seam_perm = []
            water_perm = []
            lightmap_perm = []
            cookie_perm = []
            for ob in halo_objects.structure:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in structure_perm):
                        structure_perm.append(perm)

            for ob in halo_objects.poops:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in poop_perm):
                        poop_perm.append(perm)

            for ob in halo_objects.markers:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in marker_perm):
                        marker_perm.append(perm)

            for ob in halo_objects.lights:
                if ob.halo_json.bsp_index == bsp:
                    print('we found a light!')
                    perm = GetPerm(ob)
                    if (perm not in light_perm):
                        light_perm.append(perm)
                        print('we appended the light as a perm!')

            for ob in halo_objects.portals:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in portal_perm):
                        portal_perm.append(perm)

            for ob in halo_objects.seams:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in seam_perm):
                        seam_perm.append(perm)

            for ob in halo_objects.water_surfaces:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in water_perm):
                        water_perm.append(perm)

            for ob in halo_objects.lightmap_regions:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in lightmap_perm):
                        lightmap_perm.append(perm)

            for ob in halo_objects.cookie_cutters:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in cookie_perm):
                        cookie_perm.append(perm)

            for perm in structure_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'bsp', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'bsp', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'bsp', perm)
            for perm in poop_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'poops', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name,  "{0:03}".format(bsp), 'poops', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'poops', perm)
            for perm in marker_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'markers', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'markers', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'markers', perm)
            for perm in light_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'lights', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'lights', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'lights', perm)
            for perm in portal_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'portals', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'portals', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'portals', perm)
            for perm in seam_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'seams', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'seams', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'seams', perm)
            for perm in water_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'water', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'water', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'water', perm)
            for perm in lightmap_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'lightmap_region', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'lightmap_region', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'lightmap_region', perm)
            for perm in cookie_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'cookie_cutters', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'cookie_cutters', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'cookie_cutters', perm)

            for perm in shared_structure_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'bsp', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'bsp', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'bsp', perm)
            for perm in shared_poop_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'poops', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name,  'shared', 'poops', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'poops', perm)
            for perm in shared_marker_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'markers', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'markers', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'markers', perm)
            for perm in shared_light_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'lights', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'lights', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'lights', perm)
            for perm in shared_portal_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'portals', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'portals', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'portals', perm)
            for perm in shared_seam_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'seams', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'seams', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'seams', perm)
            for perm in shared_water_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'water', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'water', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'water', perm)
            for perm in shared_lightmap_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'lightmap_region', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'lightmap_region', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'lightmap_region', perm)
            for perm in shared_cookie_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'cookie_cutters', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'cookie_cutters', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'cookie_cutters', perm)

            output = ET.SubElement(object, 'OutputTagCollection')
            ET.SubElement(output, 'OutputTag', Type='scenario_structure_bsp').text = asset_path + '\\' + asset_name + '_' + "{0:03}".format(bsp)
            ET.SubElement(output, 'OutputTag', Type='scenario_structure_lighting_info').text = asset_path + '\\' + asset_name + '_' + "{0:03}".format(bsp)
        
    ##### STRUCTURE DESIGN #####
    if SceneHasDesign(halo_objects):
        bsp_list = []
        shared_bsp_exists = False

        for ob in bpy.data.objects:
            if not ob.halo_json.bsp_shared and (ob.halo_json.bsp_index not in bsp_list) and (sel_logic.ObBoundarys(ob) or sel_logic.ObWaterPhysics(ob) or sel_logic.ObPoopRains(ob) or sel_logic.ObFog(ob)):
                bsp_list.append(ob.halo_json.bsp_index)

        for ob in bpy.data.objects:
            if ob.halo_json.bsp_shared:
                shared_bsp_exists = True
                break

        shared_boundary_perm = []
        shared_water_physics_perm = []
        shared_rain_perm = []
        shared_fog_perm = []

        if shared_bsp_exists:
            for ob in halo_objects.boundary_surfaces:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_boundary_perm):
                        shared_boundary_perm.append(perm)

            for ob in halo_objects.water_physics:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_water_physics_perm):
                        shared_water_physics_perm.append(perm)
       
            for ob in halo_objects.rain_occluders:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_rain_perm):
                        shared_rain_perm.append(perm)

            for ob in halo_objects.fog:
                if ob.halo_json.bsp_shared:
                    perm = GetPerm(ob)
                    if (perm not in shared_fog_perm):
                        shared_fog_perm.append(perm)
        
        for bsp in bsp_list:
            content = ET.SubElement(contents, "Content", Name=asset_name + '_' + "{0:03}".format(bsp) + '_structure_design', Type='design')
            object = ET.SubElement(content, 'ContentObject', Name='', Type="structure_design")

            boundary_perm = []
            water_physics_perm = []
            rain_perm = []
            fog_perm = []

            for ob in halo_objects.boundary_surfaces:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in boundary_perm):
                        boundary_perm.append(perm)

            for ob in halo_objects.water_physics:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in water_physics_perm):
                        water_physics_perm.append(perm)

            for ob in halo_objects.rain_occluders:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in rain_perm):
                        rain_perm.append(perm)

            for ob in halo_objects.fog:
                if ob.halo_json.bsp_index == bsp:
                    perm = GetPerm(ob)
                    if (perm not in fog_perm):
                        fog_perm.append(perm)

            for perm in boundary_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'design', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'design')
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'design')
            
            for perm in water_physics_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'water_physics', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'water_physics')
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'water_physics')

            for perm in rain_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'rain_blockers', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'rain_blockers')
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'rain_blockers')

            for perm in fog_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'fog', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'fog', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, "{0:03}".format(bsp), 'fog', perm)

            for perm in shared_boundary_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'design', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'design')
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'design')

            for perm in shared_water_physics_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'water_physics', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'water_physics')
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'water_physics')

            for perm in shared_rain_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'rain_blockers', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'rain_blockers')
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'rain_blockers')

            for perm in shared_fog_perm:
                network = ET.SubElement(object, 'ContentNetwork' ,Name=GetAssetPathBSP(asset_path, asset_name, 'shared', 'fog', perm))
                ET.SubElement(network, 'InputFile').text = GetInputFilePathBSP(asset_path, asset_name, 'shared', 'fog', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePathBSP(asset_path, asset_name, 'shared', 'fog', perm)

            output = ET.SubElement(object, 'OutputTagCollection')
            ET.SubElement(output, 'OutputTag', Type='structure_design').text = asset_path + '\\' + asset_name + '_' + "{0:03}".format(bsp) + '_structure_design'

def WriteSkyContents(halo_objects, metadata, asset_path, asset_name):
    contents = ET.SubElement(metadata, "Contents")
    content = ET.SubElement(contents, "Content", Name=asset_name, Type='model')
    object = ET.SubElement(content, 'ContentObject', Name='', Type="render_model")

    perm_list = []
    for ob in halo_objects.render:
        perm = GetPerm(ob)
        if (perm not in perm_list):
            perm_list.append(perm)
            network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
            ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'render', ob.halo_json.Permutation_Name)
            ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'render', ob.halo_json.Permutation_Name)

    perm_list = []
    for ob in halo_objects.lights:
        perm = GetPerm(ob)
        if (perm not in perm_list):
            perm_list.append(perm)
            network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
            ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'lights', ob.halo_json.Permutation_Name)
            ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'lights', ob.halo_json.Permutation_Name)

    output = ET.SubElement(object, 'OutputTagCollection')
    ET.SubElement(output, 'OutputTag', Type='render_model').text = asset_path + '\\' + asset_name

def WriteDecoratorContents(halo_objects, metadata, asset_path, asset_name, lod_count):
    contents = ET.SubElement(metadata, "Contents")
    content = ET.SubElement(contents, "Content", Name=asset_name, Type='decorator_set')
    if len(halo_objects.decorator) > 0:
        count = 0
        while lod_count > count: # count is treated as an index here, wheras lod_count is a range of 1-4. So for a lod_count of 4 the count will be 3 while make its final loop
            object = ET.SubElement(content, 'ContentObject', Name=str(count), Type="render_model", LOD=str(count))
            network = ET.SubElement(object, 'ContentNetwork' ,Name='default', Type="")
            ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'render')
            ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'render')

            output = ET.SubElement(object, 'OutputTagCollection')
            ET.SubElement(output, 'OutputTag', Type='render_model').text = asset_path + '\\' + asset_name + '_lod' + str(count + 1) # we add 1 here by convention. This results in a tag name that matches the lod value, rather than index
            count += 1

def WriteParticleContents(halo_objects, metadata, asset_path, asset_name):
    contents = ET.SubElement(metadata, "Contents")
    content = ET.SubElement(contents, "Content", Name=asset_name, Type='particle_model')
    object = ET.SubElement(content, 'ContentObject', Name='', Type="particle_model")

    if len(halo_objects.render) > 0:
        network = ET.SubElement(object, 'ContentNetwork' ,Name=asset_name, Type="")
        ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'particle_model')
        ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'particle_model')

    output = ET.SubElement(object, 'OutputTagCollection')
    ET.SubElement(output, 'OutputTag', Type='render_model').text = asset_path + '\\' + asset_name

def GetAssetPathBSP(asset_path, asset_name, bsp, type, perm=''):
    if perm == '' or perm == 'default':
        name = asset_name + '_' + bsp + '_' + type
    else:
        name = asset_name + '_' + bsp + '_' + type + '_' + perm

    return name

def GetInputFilePathBSP(asset_path, asset_name, bsp, type, perm=''):
    if perm == '' or perm == 'default':
        path = asset_path + '\\models\\' + asset_name + '_' + bsp + '_' + type + '.fbx'
    else:
        path = asset_path + '\\models\\' + asset_name + '_' + bsp + '_' + type + '_' + perm + '.fbx'

    return path

def GetIntermediateFilePathBSP(asset_path, asset_name, bsp, type, perm=''):
    if perm == '' or perm == 'default':
        path = asset_path + '\\export\\models\\' + asset_name + '_' + bsp + '_' + type + '.gr2'
    else:
        path = asset_path + '\\export\\models\\' + asset_name + '_' + bsp + '_' + type + '_' + perm + '.gr2'

    return path

def SceneHasBSP(halo_objects):
    bsp_objects = halo_objects.structure
    return len(bsp_objects) > 0

def SceneHasDesign(halo_objects):
    design_objects = halo_objects.boundary_surfaces + halo_objects.water_physics + halo_objects.rain_occluders + halo_objects.fog
    return len(design_objects) > 0

def GetInputFilePath(asset_path, asset_name, type, perm=''):
    if type == 'model_animation_graph':
        path = asset_path + '\\animations\\' + asset_name + '.fbx'
    elif type == 'particle_model':
        path = asset_path + '\\models\\' + asset_name + '.fbx'
    else:
        if perm == '':
            path = asset_path + '\\models\\' + asset_name  + '_' + type + '.fbx'
        else:
            path = asset_path + '\\models\\' + asset_name + '_'  + perm  + '_' + type + '.fbx'

    return path

def GetIntermediateFilePath(asset_path, asset_name, type, perm=''):
    if type == 'model_animation_graph':
        path = asset_path + '\\export\\animations\\' + asset_name + '.gr2'
    elif type == 'particle_model':
        path = asset_path + '\\export\\models\\' + asset_name + '.gr2'
    else:
        if perm == '':
            path = asset_path + '\\export\\models\\' + asset_name + '_' + type + '.gr2'
        else:
            path = asset_path + '\\export\\models\\' + asset_name + '_'  + perm  + '_' + type + '.gr2'

    return path

def SceneHasCollisionObject():
    boolean = False

    for ob in bpy.data.objects:
        if sel_logic.ObCollision(ob):
            boolean = True
            break
    
    return boolean

def SceneHasPhysicsObject():
    boolean = False

    for ob in bpy.data.objects:
        if sel_logic.ObPhysics(ob):
            boolean = True
            break
    
    return boolean

def SceneHasMarkers():
    boolean = False

    for ob in bpy.data.objects:
        if sel_logic.ObMarkers(ob):
            boolean = True
            break
    
    return boolean

def export_sidecar(operator, context, report, asset_path, halo_objects, model_armature=None, lod_count=0,
        filepath="",
        export_sidecar_xml=False,
        sidecar_type='MODEL',
        output_biped=False,
        output_crate=False,
        output_creature=False,
        output_device_control=False,
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
    if export_sidecar_xml and asset_path != '': # if the user has opted to export a sidecar and a valid asset path exists, proceed
        export_xml(report, halo_objects, model_armature, lod_count, filepath, export_sidecar_xml, sidecar_type, asset_path,output_biped,output_crate,output_creature,output_device_control,output_device_machine,output_device_terminal,output_effect_scenery,output_equipment,output_giant,output_scenery,output_vehicle,output_weapon)
    return {'FINISHED'}