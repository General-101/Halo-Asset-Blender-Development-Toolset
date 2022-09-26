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
from xml.etree.ElementTree import SubElement
import bpy
import getpass

import xml.etree.cElementTree as ET
import xml.dom.minidom

EKPath = bpy.context.preferences.addons['io_scene_halo'].preferences.hrek_path

#clean editing kit path
EKPath = EKPath.replace('"','')
EKPath = EKPath.strip('\\')

valid_animation_types = ('JMM', 'JMA', 'JMT', 'JMZ', 'JMV', 'JMO', 'JMOX', 'JMR', 'JMRX')

special_prefixes = ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_','#','+soft_ceiling','+soft_kill','+slip_surface', '@','+cookie','+decorator','+flair', '%', '$','+fog','+portal', '+seam','+water', '\'')

def export_xml(report, filePath="", export_sidecar=False, sidecar_type='MODEL', asset_path='',        
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
    print('full path = ' + filePath)
    asset_path = CleanAssetPath(full_path)
    asset_name = asset_path.rpartition('\\')[2]

    if export_sidecar and asset_path != '':
        if sidecar_type == 'MODEL':
            GenerateModelSidecar(asset_path, asset_name, full_path,output_biped,output_crate,output_creature,output_device_control,output_device_machine,output_device_terminal,output_effect_scenery,output_equipment,output_giant,output_scenery,output_vehicle,output_weapon)
        elif sidecar_type == 'SCENARIO':
            GenerateStructureSidecar(asset_path, asset_name, full_path)
        elif sidecar_type == 'SCENARIO':
            GenerateDecoratorSidecar(asset_path, asset_name, full_path)
        else:
            GenerateParticleSidecar(asset_path, asset_name, full_path)

def CleanAssetPath(path):
    path = path.replace('"','')
    path = path.strip('\\')
    path = path.replace(EKPath + '\\data\\','')

    return path

def GenerateModelSidecar(asset_path, asset_name, full_path,                
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

    m_encoding = 'utf-8'
    m_standalone = 'yes'

    print("beep boop I'm writing a model sidecar")

    metadata = ET.Element("Metadata")
    WriteHeader(metadata)
    GetObjectOutputTypes(metadata, "model", asset_path, asset_name, GetModelTags(output_biped,output_crate,output_creature,output_device_control,output_device_machine,output_device_terminal,output_effect_scenery,output_equipment,output_giant,output_scenery,output_vehicle,output_weapon))
    WriteFolders(metadata)
    WriteFaceCollections(metadata, True, True)
    WriteModelContents(metadata, asset_path, asset_name)

    dom = xml.dom.minidom.parseString(ET.tostring(metadata))
    xml_string = dom.toprettyxml(indent='  ') # indent='\t', encoding='utf-8', standalone='yes'
    part1, part2 = xml_string.split('?>')

    with open(full_path + '\\' + asset_name + '.sidecar.xml', 'w') as xfile:
        xfile.write(part1 + 'encoding=\"{}\" standalone=\"{}\"?>'.format(m_encoding, m_standalone) + part2)
        xfile.close()

def GenerateStructureSidecar(asset_path, asset_name, full_path):
    print(asset_path)
    m_encoding = 'UTF-8'

    metadata = ET.Element("Metadata")
    WriteHeader(metadata)
    GetObjectOutputTypes(metadata, "scenario", asset_path, asset_name, ['scenario_lightmap','structure_seams','scenario'])
    WriteFolders(metadata)
    WriteFaceCollections(metadata, False, True)
    WriteStructureContents(metadata, asset_path, asset_name)

    dom = xml.dom.minidom.parseString(ET.tostring(metadata))
    xml_string = dom.toprettyxml(indent='\t', encoding='utf-8', standalone='yes')
    part1, part2 = xml_string.split('?>')

    with open(asset_path + 'temp.sidecar.xml', 'w') as xfile:
        xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
        xfile.close()

def GenerateDecoratorSidecar(asset_path, asset_name, full_path):
    print(asset_path)

def GenerateParticleSidecar(asset_path, asset_name, full_path):
    print(asset_path)

def WriteHeader(metadata):
    header = ET.SubElement(metadata, "Header")
    ET.SubElement(header, "MainRev").text = "0"
    ET.SubElement(header, "PointRev").text = "6"
    ET.SubElement(header, "Description").text = "Created using the Halo Blender Toolset"
    ET.SubElement(header, "Created").text = str(datetime.today().strftime('%Y-%m-%d'))
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

def GetObjectOutputTypes(metadata, type, asset_path, asset_name, output_tags):
    asset = ET.SubElement(metadata, "Asset", Name=asset_name, Type=type)
    tagcollection = ET.SubElement(asset, "OutputTagCollection")

    for tag in output_tags:
        ET.SubElement(tagcollection, "OutputTag", Type=tag).text = asset_path + '\\' + asset_name

def WriteFolders(metadata):
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

def WriteFaceCollections(metadata, regions=False, materials=False):
    if(regions or materials):
        faceCollections = ET.SubElement(metadata, "FaceCollections")

        if(regions):
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
        if(materials):
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

def WriteModelContents(metadata, asset_path, asset_name):
    ##### RENDER #####
    contents = ET.SubElement(metadata, "Contents")
    content = ET.SubElement(contents, "Content", Name=asset_name, Type='model')
    object = ET.SubElement(content, 'ContentObject', Name='', Type="render_model")

    perm_list = []
    for ob in bpy.data.objects:
        if ob.halo_json.Permutation_Name == '':
            perm = 'default'
        else:
            perm = ob.halo_json.Permutation_Name
        if (perm not in perm_list) and RenderPermExists(perm):
            perm_list.append(perm)
            network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
            ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'render', perm)
            ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'render', perm)

    output = ET.SubElement(object, 'OutputTagCollection')
    ET.SubElement(output, 'OutputTag', Type='render_model').text = asset_path + '\\' + asset_name

    ##### PHYSICS #####
    if SceneHasPhysicsObject():
        object = ET.SubElement(content, 'ContentObject', Name='', Type="physics_model")

        perm_list = []
        for ob in bpy.data.objects:
            if ob.halo_json.Permutation_Name == '':
                perm = 'default'
            else:
                perm = ob.halo_json.Permutation_Name
            if (perm not in perm_list) and PhysicsPermExists(perm):
                perm_list.append(perm)
                network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
                ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'physics', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'physics', perm)

        output = ET.SubElement(object, 'OutputTagCollection')
        ET.SubElement(output, 'OutputTag', Type='physics_model').text = asset_path + '\\' + asset_name

    ##### COLLISION #####    
    if SceneHasCollisionObject():
        object = ET.SubElement(content, 'ContentObject', Name='', Type="collision_model")

        perm_list = []
        for ob in bpy.data.objects:
            if ob.halo_json.Permutation_Name == '':
                perm = 'default'
            else:
                perm = ob.halo_json.Permutation_Name
            if (perm not in perm_list) and CollisionPermExists(perm):
                perm_list.append(perm)
                network = ET.SubElement(object, 'ContentNetwork' ,Name=perm, Type="")
                ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, asset_name, 'collision', perm)
                ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, asset_name, 'collision', perm)

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
                case 'JMM':
                    network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Base', ModelAnimationMovementData='None')
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
                case 'JMR':
                    network = ET.SubElement(object, 'ContentNetwork' , Name=anim_name, Type='Overlay', ModelAnimationOverlayType='Keyframe', ModelAnimationOverlayBlending='ReplacementLocalSpace')

            ET.SubElement(network, 'InputFile').text = GetInputFilePath(asset_path, anim_name, 'model_animation_graph')
            ET.SubElement(network, 'IntermediateFile').text = GetIntermediateFilePath(asset_path, anim_name, 'model_animation_graph')

        output = ET.SubElement(object, 'OutputTagCollection')
        ET.SubElement(output, 'OutputTag', Type='frame_event_list').text = asset_path + '\\' + asset_name
        ET.SubElement(output, 'OutputTag', Type='model_animation_graph').text = asset_path + '\\' + asset_name

def GetInputFilePath(asset_path, asset_name, type, perm=''):
    if type == 'model_animation_graph':
        path = asset_path + '\\animations\\' + asset_name
    else:
        path = asset_path + '\\models\\' + asset_name
    if type != 'skeleton' and type != 'markers' and type != 'model_animation_graph':
        if perm != 'default':
            path = path + '_' + perm
    if type == 'model_animation_graph':
        path = path + '.fbx'
    else:
        path = path + '_' + type + '.fbx'

    return path

def GetIntermediateFilePath(asset_path, asset_name, type, perm=''):
    if type == 'model_animation_graph':
        path = asset_path + '\\export\\animations\\' + asset_name
    else:
        path = asset_path + '\\export\\models\\' + asset_name
    if type != 'skeleton' and type != 'markers' and type != 'model_animation_graph':
        if perm != 'default':
            path = path + '_' + perm
    if type == 'model_animation_graph':
        path = path + '.gr2'
    else:
        path = path + '_' + type + '.gr2'

    return path

def SceneHasCollisionObject():
    boolean = False

    for ob in bpy.data.objects:
        if ob.name.startswith('@') or ob.halo_json.ObjectMesh_Type == 'COLLISION':
            boolean = True
    
    return boolean

def SceneHasPhysicsObject():
    boolean = False

    for ob in bpy.data.objects:
        if ob.name.startswith('$') or ob.halo_json.ObjectMesh_Type == 'PHYSICS':
            boolean = True
    
    return boolean

def SceneHasMarkers():
    boolean = False

    for ob in bpy.data.objects:
        if ob.name.startswith('#') or ob.halo_json.Object_Type_All == 'MARKER' or ob.halo_json.Object_Type_No_Mesh == 'MARKER':
            boolean = True
    
    return boolean


def WriteStructureContents(metadata, asset_path, asset_name):
    print ('null')

def RenderPermExists(perm):
    exists = False
    for ob in bpy.data.objects:
        halo_mesh = ob.halo_json
        halo_mesh_name = ob.name
        if halo_mesh.Permutation_Name != perm and perm == 'default':
            perm = ''
        if (ob.type == 'MESH' and (not halo_mesh_name.startswith(special_prefixes)) and halo_mesh.Object_Type_All == 'MESH' and halo_mesh.ObjectMesh_Type == 'DEFAULT' and halo_mesh.Permutation_Name == perm):
            exists = True
    return exists

def PhysicsPermExists(perm):
    exists = False
    for ob in bpy.data.objects:
        halo_mesh = ob.halo_json
        halo_mesh_name = ob.name
        if halo_mesh.Permutation_Name != perm and perm == 'default':
            perm = ''
        if (ob.type == 'MESH' and (not halo_mesh_name.startswith(special_prefixes) or halo_mesh_name.startswith('$')) and (halo_mesh.ObjectMesh_Type == 'PHYSICS' or halo_mesh_name.startswith('$')) and halo_mesh.Object_Type_All == 'MESH' and halo_mesh.Permutation_Name == perm):
            exists = True
    return exists

def CollisionPermExists(perm):
    exists = False
    for ob in bpy.data.objects:
        halo_mesh = ob.halo_json
        halo_mesh_name = ob.name
        if halo_mesh.Permutation_Name != perm and perm == 'default':
            perm = ''
        if (ob.type == 'MESH' and (not halo_mesh_name.startswith(special_prefixes) or halo_mesh_name.startswith('@')) and (halo_mesh.ObjectMesh_Type == 'COLLISION' or halo_mesh_name.startswith('@')) and halo_mesh.Object_Type_All == 'MESH' and halo_mesh.Permutation_Name == perm):
            exists = True
    return exists

# def IntermediateFileExists(folderName):
#     filePath = "fullPath" + "\\" + folderName

#     for fname in os.listdir(filePath):
#         if fname.endswith('.gr2'):
#             return True
#         else:
#             return False

# def GetModelContentObjects(metadata):
#     temp = []
#     ContentObjects = ET.SubElement(metadata, "Content", Name="assetName", Type="model")

#     if(IntermediateFileExists("render")):
#         CreateContentObject(ContentObjects, "render")

#     if(IntermediateFileExists("physics")):
#         CreateContentObject(ContentObjects, "physics")

#     if(IntermediateFileExists("collision")):
#         CreateContentObject(ContentObjects, "collision")

#     if(IntermediateFileExists("markers")):
#         CreateContentObject(ContentObjects, "markers")

#     if(IntermediateFileExists("skeleton")):
#         CreateContentObject(ContentObjects, "skeleton")

#     if(IntermediateFileExists("animations\\JMM") or IntermediateFileExists("animations\\JMA") or IntermediateFileExists("animations\\JMT") or IntermediateFileExists("animations\\JMZ") or IntermediateFileExists("animations\\JMV")
#         or IntermediateFileExists("animations\\JMO (Keyframe)") or IntermediateFileExists("animations\\JMO (Pose)") or IntermediateFileExists("animations\\JMR (Object)") or IntermediateFileExists("animations\\JMR (Local)")):
#         animations = ET.SubElement(ContentObjects, "ContentObject", Name="", Type="model_animation_graph")

#         if(IntermediateFileExists("animations\\JMM")):
#             CreateContentObject(animations, "animations\\JMM", "Base", "ModelAnimationMovementData", "None", "", "")

#         if(IntermediateFileExists("animations\\JMA")):
#             CreateContentObject(animations, "animations\\JMA", "Base", "ModelAnimationMovementData", "XY", "", "")

#         if(IntermediateFileExists("animations\\JMT")):
#             CreateContentObject(animations, "animations\\JMT", "Base", "ModelAnimationMovementData", "XYYaw", "", "")

#         if(IntermediateFileExists("animations\\JMZ")):
#             CreateContentObject(animations, "animations\\JMZ", "Base", "ModelAnimationMovementData", "XYZYaw", "", "")

#         if(IntermediateFileExists("animations\\JMV")):
#             CreateContentObject(animations, "animations\\JMV", "Base", "ModelAnimationMovementData", "XYZFullRotation", "", "")

#         if(IntermediateFileExists("animations\\JMO (Keyframe)")):
#             CreateContentObject(animations, "animations\\JMO (Keyframe)", "Overlay", "ModelAnimationOverlayType", "Keyframe", "ModelAnimationOverlayBlending", "Additive")

#         if(IntermediateFileExists("animations\\JMO (Pose)")):
#             CreateContentObject(animations, "animations\\JMO (Pose)", "Overlay", "ModelAnimationOverlayType", "Pose", "ModelAnimationOverlayBlending", "Additive")

#         if(IntermediateFileExists("animations\\JMR (Local)")):
#             CreateContentObject(animations, "animations\\JMR (Local)", "Overlay", "ModelAnimationOverlayType", "keyframe", "ModelAnimationOverlayBlending", "ReplacementLocalSpace")

#         if(IntermediateFileExists("animations\\JMR (Object)")):
#             CreateContentObject(animations, "animations\\JMR (Object)", "Overlay", "ModelAnimationOverlayType", "keyframe", "ModelAnimationOverlayBlending", "ReplacementObjectSpace")

#         r2 = ET.SubElement(animations, "OutputTagCollection")
#         ET.SubElement(r2, "OutputTag", Type="frame_event_list").text = "dataPath" + "\\" + "assetName"
#         ET.SubElement(r2, "OutputTag", Type="model_animation_graph").text = "dataPath" + "\\" + "assetName"

# def CreateContentObject(ContentObjects, type):
#     files = []
#     path = "fullPath" + "\\" + type
    
#     for (root, dirs, file) in os.walk(path):
#         for fi in file:
#             if '.gr2' in fi:
#                 files.add(fi)
    
#     if(type == "markers" or type == "skeleton"):
#         ET.SubElement(ContentObjects, "ContentObject", Name="", Type=type)
#     else:
#         ET.SubElement(ContentObjects, "ContentObject", Name="", Type=str(type + "_model"))

#     for f in files:
#         r1 = ET.SubElement(ContentObjects, "ContentNetwork", Name=getFileNames(f), Type="")
#         ET.SubElement(r1, "InputFile").text = "dataPath" + "\\" + type + "\\" + getFileNames(f) + "inputFileType"
#         ET.SubElement(r1, "IntermediateFile").text = "dataPath" + "\\" + type + "\\" + getFileNames(f)
    
#     if(type == "markers" or type == "skeleton"):
#         ET.SubElement(ContentObjects, "OutputTagCollection")
#     else:
#         r2 = ET.SubElement(ContentObjects, "OutputTagCollection")
#         ET.SubElement(r2, "OutputTag", Type=str(type + "_model")).text = "dataPath" + "\\" + "assetName"

# def CreateContentObject(animations, type1, type2, type3, type4, type5, type6):
#     files = []
#     path = "fullPath" + "\\" + type
    
#     for (root, dirs, file) in os.walk(path):
#         for fi in file:
#             if '.gr2' in fi:
#                 files.add(fi)
    
#     for f in files:
#         if(type5 == "" or type6 == ""):
#             r1 = ET.SubElement(animations, "ContentNetwork", Name=getFileNames(f), Type=type2, type3=type4)
#             ET.SubElement(r1, "InputFile").text = "dataPath" + "\\" + type1 + "\\" + getFileNames(f) + "inputFileType"
#             ET.SubElement(r1, "IntermediateFile").text = "dataPath" + "\\" + type1 + "\\" + getFileNames(f)
#         else:
#             r1 = ET.SubElement(animations, "ContentNetwork", Name=getFileNames(f), Type=type2, type3=type4, type5=type6)
#             ET.SubElement(r1, "InputFile").text = "dataPath" + "\\" + type1 + "\\" + getFileNames(f) + "inputFileType"
#             ET.SubElement(r1, "IntermediateFile").text = "dataPath" + "\\" + type1 + "\\" + getFileNames(f)

# def getFileNames(file):
#     t = []
#     return ""


def save(operator, context, report,
        filepath="",
        export_sidecar=False,
        sidecar_type='MODEL',
        asset_path='',
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
    export_xml(report, filepath, export_sidecar, sidecar_type, asset_path,output_biped,output_crate,output_creature,output_device_control,output_device_machine,output_device_terminal,output_effect_scenery,output_equipment,output_giant,output_scenery,output_vehicle,output_weapon)
    return {'FINISHED'}