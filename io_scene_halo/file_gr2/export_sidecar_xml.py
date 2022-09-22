from curses import meta
from datetime import datetime
from inspect import getfile
from xml.etree.ElementTree import SubElement
import bpy
import os
from os.path import exists as file_exists
import getpass

import xml.etree.cElementTree as ET
import xml.dom.minidom

def export_xml(report, filePath="", export_sidecar=False, sidecar_type='MODEL', asset_path=''):
    print('asset path = ' + asset_path)
    if export_sidecar and asset_path != '':
        if sidecar_type == 'MODEL':
            GenerateModelSidecar(asset_path)

def GenerateModelSidecar(asset_path):
    m_encoding = 'UTF-8'

    print("beep boop I'm writing a model sidecar")

    metadata = ET.Element("Metadata")
    WriteHeader(metadata)

    GetObjectOutputTypes(metadata, "model", asset_path, GetModelTags())

    dom = xml.dom.minidom.parseString(ET.tostring(metadata))
    xml_string = dom.toprettyxml()
    part1, part2 = xml_string.split('?>')

    with open(asset_path + 'temp.sidecar.xml', 'w') as xfile:
        xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
        xfile.close()

def WriteHeader(metadata):
    header = ET.SubElement(metadata, "Header")
    ET.SubElement(header, "MainRev").text = "0"
    ET.SubElement(header, "PointRev").text = "6"
    ET.SubElement(header, "Description").text = "Created By using the Halo Blender Toolset"
    ET.SubElement(header, "Created").text = str(datetime.today().strftime('%Y-%m-%d'))
    ET.SubElement(header, "By").text = getpass.getuser()
    ET.SubElement(header, "DirectoryType").text = "TAE.Shared.NWOAssetDirectory"
    ET.SubElement(header, "Schema").text = "1"

def GetModelTags():
    # PLACEHOLDER
    tags = ['model']

    if True: 
        tags.append('biped')
    if True:
        tags.append('crate')
    if True:
        tags.append('Creature')
    if True:
        tags.append('device_control')
    if True:
        tags.append('device_machine')
    if True:
        tags.append('device_terminal')
    if True:
        tags.append('effect_scenery')
    if True:
        tags.append('equipment')
    if True:
        tags.append('giant')
    if True:
        tags.append('scenery')
    if True:
        tags.append('vehicle')
    if True:
        tags.append('weapon')

    return tags

def GetObjectOutputTypes(metadata, type, asset_path, output_tags):
    asset = ET.SubElement(metadata, "Asset", Name="example_asset", Type=type)
    tagcollection = ET.SubElement(asset, "OutputTagCollection")

    for tag in output_tags:
        ET.SubElement(tagcollection, "OutputTag", Type=tag).text = asset_path

def WriteFolders(metadata):
    folders = ET.SubElement(metadata, "Folders")

    ET.SubElement(folders, "Reference").text = "\\reference"
    ET.SubElement(folders, "Temp").text = "\\temp"
    ET.SubElement(folders, "SourceModels").text = "\\work"
    ET.SubElement(folders, "GameModels").text = "\\render"
    ET.SubElement(folders, "GamePhysicsModels").text = "\\physics"
    ET.SubElement(folders, "GameCollisionModels").text = "\\collision"
    ET.SubElement(folders, "ExportModels").text = "\\render"
    ET.SubElement(folders, "ExportPhysicsModels").text = "\\physics"
    ET.SubElement(folders, "ExportCollisionModels").text = "\\collision"
    ET.SubElement(folders, "SourceAnimations").text = "\\animations\\work"
    ET.SubElement(folders, "AnimationsRigs").text = "\\animations\\rigs"
    ET.SubElement(folders, "GameAnimations").text = "\\animations"
    ET.SubElement(folders, "ExportAnimations").text = "\\animations"
    ET.SubElement(folders, "SourceBitmaps").text = "\\bitmaps"
    ET.SubElement(folders, "GameBitmaps").text = "\\bitmaps"
    ET.SubElement(folders, "CinemaSource").text = "\\cinematics"
    ET.SubElement(folders, "CinemaExport").text = "\\cinematics"
    ET.SubElement(folders, "ExportBSPs").text = "\\"
    ET.SubElement(folders, "SourceBSPs").text = "\\"
    ET.SubElement(folders, "Scripts").text = "\\scripts"

def WriteFaceCollections(metadata, regions=False, materials=False):
    if(regions or materials):
        faceCollections = ET.SubElement(metadata, "FaceCollections")

        if(regions):
            temp = ["default"]
            f1 = ET.SubElement(faceCollections, "FaceCollection", Name="regions", StringTable="connected_geometry_regions_table", Description="model regions")

            FaceCollectionsEntries = ET.SubElement(f1, "FaceCollectionEntries")
            ET.SubElement(FaceCollectionsEntries, "FaceCollectionEntry", Index="0", Name="default", Active="true")

            count = 1
            for name in temp:
                if(not bpy.types.Object.halo_json.Region_Name == name):
                    for i in bpy.types.Object.halo_json.Region_Name:
                        ET.SubElement(FaceCollectionsEntries, "FaceCollectionEntry", Index=str(count), Name=i, Active="true")
                        temp.add(i)
                        count += 1
        if(materials):
            temp = ["default"]
            f2 = ET.SubElement(faceCollections, "FaceCollection", Name="global materials overrides", StringTable="connected_geometry_global_material_table", Description="Global material overrides")

            FaceCollectionsEntries2 = ET.SubElement(f2, "FaceCollectionEntries")
            ET.SubElement(FaceCollectionsEntries2, "FaceCollectionEntry", Index="0", Name="default", Active="true")

            count = 1
            for name in temp:
                if(not bpy.types.Object.halo_json.Region_Name == name):
                    for i in bpy.types.Object.halo_json.Face_Global_Material:
                        ET.SubElement(FaceCollectionsEntries2, "FaceCollectionEntry", Index=str(count), Name=i, Active="true")
                        temp.add(i)
                        count += 1

def IntermediateFileExists(folderName):
    filePath = "fullPath" + "\\" + folderName

    for fname in os.listdir(filePath):
        if fname.endswith('.gr2'):
            return True
        else:
            return False

def GetModelContentObjects(metadata):
    temp = []
    ContentObjects = ET.SubElement(metadata, "Content", Name="assetName", Type="model")

    if(IntermediateFileExists("render")):
        CreateContentObject(ContentObjects, "render")

    if(IntermediateFileExists("physics")):
        CreateContentObject(ContentObjects, "physics")

    if(IntermediateFileExists("collision")):
        CreateContentObject(ContentObjects, "collision")

    if(IntermediateFileExists("markers")):
        CreateContentObject(ContentObjects, "markers")

    if(IntermediateFileExists("skeleton")):
        CreateContentObject(ContentObjects, "skeleton")

    if(IntermediateFileExists("animations\\JMM") or IntermediateFileExists("animations\\JMA") or IntermediateFileExists("animations\\JMT") or IntermediateFileExists("animations\\JMZ") or IntermediateFileExists("animations\\JMV")
        or IntermediateFileExists("animations\\JMO (Keyframe)") or IntermediateFileExists("animations\\JMO (Pose)") or IntermediateFileExists("animations\\JMR (Object)") or IntermediateFileExists("animations\\JMR (Local)")):
        animations = ET.SubElement(ContentObjects, "ContentObject", Name="", Type="model_animation_graph")

        if(IntermediateFileExists("animations\\JMM")):
            CreateContentObject(animations, "animations\\JMM", "Base", "ModelAnimationMovementData", "None", "", "")

        if(IntermediateFileExists("animations\\JMA")):
            CreateContentObject(animations, "animations\\JMA", "Base", "ModelAnimationMovementData", "XY", "", "")

        if(IntermediateFileExists("animations\\JMT")):
            CreateContentObject(animations, "animations\\JMT", "Base", "ModelAnimationMovementData", "XYYaw", "", "")

        if(IntermediateFileExists("animations\\JMZ")):
            CreateContentObject(animations, "animations\\JMZ", "Base", "ModelAnimationMovementData", "XYZYaw", "", "")

        if(IntermediateFileExists("animations\\JMV")):
            CreateContentObject(animations, "animations\\JMV", "Base", "ModelAnimationMovementData", "XYZFullRotation", "", "")

        if(IntermediateFileExists("animations\\JMO (Keyframe)")):
            CreateContentObject(animations, "animations\\JMO (Keyframe)", "Overlay", "ModelAnimationOverlayType", "Keyframe", "ModelAnimationOverlayBlending", "Additive")

        if(IntermediateFileExists("animations\\JMO (Pose)")):
            CreateContentObject(animations, "animations\\JMO (Pose)", "Overlay", "ModelAnimationOverlayType", "Pose", "ModelAnimationOverlayBlending", "Additive")

        if(IntermediateFileExists("animations\\JMR (Local)")):
            CreateContentObject(animations, "animations\\JMR (Local)", "Overlay", "ModelAnimationOverlayType", "keyframe", "ModelAnimationOverlayBlending", "ReplacementLocalSpace")

        if(IntermediateFileExists("animations\\JMR (Object)")):
            CreateContentObject(animations, "animations\\JMR (Object)", "Overlay", "ModelAnimationOverlayType", "keyframe", "ModelAnimationOverlayBlending", "ReplacementObjectSpace")

        r2 = ET.SubElement(animations, "OutputTagCollection")
        ET.SubElement(r2, "OutputTag", Type="frame_event_list").text = "dataPath" + "\\" + "assetName"
        ET.SubElement(r2, "OutputTag", Type="model_animation_graph").text = "dataPath" + "\\" + "assetName"

def CreateContentObject(ContentObjects, type):
    files = []
    path = "fullPath" + "\\" + type
    
    for (root, dirs, file) in os.walk(path):
        for fi in file:
            if '.gr2' in fi:
                files.add(fi)
    
    if(type == "markers" or type == "skeleton"):
        ET.SubElement(ContentObjects, "ContentObject", Name="", Type=type)
    else:
        ET.SubElement(ContentObjects, "ContentObject", Name="", Type=str(type + "_model"))

    for f in files:
        r1 = ET.SubElement(ContentObjects, "ContentNetwork", Name=getFileNames(f), Type="")
        ET.SubElement(r1, "InputFile").text = "dataPath" + "\\" + type + "\\" + getFileNames(f) + "inputFileType"
        ET.SubElement(r1, "IntermediateFile").text = "dataPath" + "\\" + type + "\\" + getFileNames(f)
    
    if(type == "markers" or type == "skeleton"):
        ET.SubElement(ContentObjects, "OutputTagCollection")
    else:
        r2 = ET.SubElement(ContentObjects, "OutputTagCollection")
        ET.SubElement(r2, "OutputTag", Type=str(type + "_model")).text = "dataPath" + "\\" + "assetName"

def CreateContentObject(animations, type1, type2, type3, type4, type5, type6):
    files = []
    path = "fullPath" + "\\" + type
    
    for (root, dirs, file) in os.walk(path):
        for fi in file:
            if '.gr2' in fi:
                files.add(fi)
    
    for f in files:
        if(type5 == "" or type6 == ""):
            r1 = ET.SubElement(animations, "ContentNetwork", Name=getFileNames(f), Type=type2, type3=type4)
            ET.SubElement(r1, "InputFile").text = "dataPath" + "\\" + type1 + "\\" + getFileNames(f) + "inputFileType"
            ET.SubElement(r1, "IntermediateFile").text = "dataPath" + "\\" + type1 + "\\" + getFileNames(f)
        else:
            r1 = ET.SubElement(animations, "ContentNetwork", Name=getFileNames(f), Type=type2, type3=type4, type5=type6)
            ET.SubElement(r1, "InputFile").text = "dataPath" + "\\" + type1 + "\\" + getFileNames(f) + "inputFileType"
            ET.SubElement(r1, "IntermediateFile").text = "dataPath" + "\\" + type1 + "\\" + getFileNames(f)

def getFileNames(file):
    return ""


def save(operator, context, report,
        filepath="",
        use_selection=False,
        use_visible=False,
        use_active_collection=False,
        batch_mode='OFF',
        use_batch_own_dir=False,
        export_sidecar=False,
        sidecar_type='MODEL',
        asset_path='',
        **kwargs
        ):
    export_xml(report, filepath, export_sidecar, sidecar_type, asset_path)
    return {'FINISHED'}