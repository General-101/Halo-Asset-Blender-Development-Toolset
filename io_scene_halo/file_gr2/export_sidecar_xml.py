from datetime import datetime
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
            WriteSidecar_Model(asset_path)

def WriteSidecar_Model(asset_path):
    m_encoding = 'UTF-8'

    print("beep boop I'm writing a model sidecar")

    metadata = ET.Element("Metadata")
    WriteHeader(metadata)

    GetObjectOutputTypes(metadata, "model", asset_path, getModelTags())

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

def getModelTags():
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

# def WriteHeader():
#     header = ET.Element("Header")
    
#     MainRev = ET.SubElement(header, "MainRev")
#     MainRev.text = "0"
#     PointRev = ET.SubElement(header, "PointRev")
#     PointRev.text = "6"
#     Description = ET.SubElement(header, "Description")
#     Description.text = "Description", "Created By Osoyoos SideCar Gen v1.0"
#     Created = ET.SubElement(header, "Created")
#     Created.text = datetime.now()
#     By = ET.SubElement(header, "By")
#     By.text = os.getlogin()
#     DirectoryType = ET.SubElement(header, "DirectoryType")
#     DirectoryType.text = "TAE.Shared.NWOAssetDirectory"
#     SchemaText = ET.SubElement(header, "Schema")
#     SchemaText.text = "1"

#     return header

# def GetObjectOutputTypes():
#     OutputTags = xml.Element("OutputTagCollection")
#     return OutputTags

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

# def WriteFaceCollections(regions=False, materials=False):
#     if(regions or materials):
#         faceCollections = xml.Element("FaceCollections")

#         if(regions):
#             temp = ["default"]
#             f1 = xml.Element
#             f1.set("Name", "regions")
#             f1.set("StringTable", "connected_geometry_regions_table")
#             f1.set("Description", "Model regions")

#             FaceCollectionsEntries = xml.Element("FaceCollectionEntries")

#             FaceCollectionEntry = xml.Element("FaceCollectionEntry")
#             FaceCollectionEntry.set("Index", "0")
#             FaceCollectionEntry.set("Name", "default") 
#             FaceCollectionEntry.set("Active", "true")
#             FaceCollectionsEntries.append(FaceCollectionEntry)
#             f1.append(FaceCollectionsEntries)
#             faceCollections.append(f1)

#             count = 1
#             for name in temp:
#                 if(not bpy.types.Object.halo_json.Region_Name == name):
#                     for i in bpy.types.Object.halo_json.Region_Name:
#                         FaceCollectionEntry = xml.Element("FaceCollectionEntry")
#                         FaceCollectionEntry.set("Index", count)
#                         FaceCollectionEntry.set("Name", i) 
#                         FaceCollectionEntry.set("Active", "true")
#                         FaceCollectionsEntries.append(FaceCollectionEntry)
#                         f1.append(FaceCollectionsEntries)
#                         faceCollections.append(f1)
#                         temp.add(i)
#                         count += 1
#         if(materials):
#             temp = ["default"]
#             f2 = xml.Element
#             f2.set("Name", "global materials override")
#             f2.set("StringTable", "connected_geometry_global_material_table")
#             f2.set("Description", "Global material overrides")

#             FaceCollectionsEntries2 = xml.Element("FaceCollectionEntries")
#             FaceCollectionEntry2 = xml.Element("FaceCollectionEntry")
#             FaceCollectionEntry2.set("Index", "0")
#             FaceCollectionEntry2.set("Name", "default") 
#             FaceCollectionEntry2.set("Active", "true")
#             FaceCollectionsEntries2.append(FaceCollectionEntry2)
#             f2.append(FaceCollectionsEntries2)
#             faceCollections.append(f2)

#             count = 1
#             for name in temp:
#                 if(not bpy.types.Object.halo_json.Region_Name == name):
#                     for i in bpy.types.Object.halo_json.Face_Global_Material:
#                         FaceCollectionEntry = xml.Element("FaceCollectionEntry")
#                         FaceCollectionEntry.set("Index", count)
#                         FaceCollectionEntry.set("Name", i) 
#                         FaceCollectionEntry.set("Active", "true")
#                         FaceCollectionsEntries.append(FaceCollectionEntry)
#                         f1.append(FaceCollectionsEntries)
#                         faceCollections.append(f1)
#                         temp.add(i)
#                         count += 1

#             return faceCollections
#         else:
#             return None

# def IntermediateFileExists(folderName):
#     filePath = "fullPath" + "\\" + folderName

#     for fname in os.listdir(filePath):
#         if fname.endswith('.gr2'):
#             return True
#         else:
#             return False

# def GenerateModelSidecar(assetName=""):
#     #root = minidom.Document()

#     #xml = root.createElement("Metadata")
#     #root.appendChild(xml)

#     m_encoding = 'UTF-8'

#     root = ET.Element("Metadata")
#     #root.append(WriteHeader())
#     ET.SubElement(root, WriteHeader())

#     dom = xml.dom.minidom.parseString(ET.tostring(root))
#     xml_string = dom.toprettyxml()
#     part1, part2 = xml_string.split('?>')

#     with open("C:\\Users\\plasm\\Documents\\Temp\\gfg.xml", 'w') as xfile:
#         xfile.write(part1 + 'encoding=\"{}\"?>\n'.format(m_encoding) + part2)
#         xfile.close()

#     #tree = xml.ElementTree(root)
#     #dir_path = "C:\Users\plasm\Documents\Temp\gfg.xml"
#     #tree.write(f'{}/test_new_2.xml', xml_declaration=True)
#     #with open (dir_path, "wb") as files :
#     #    tree.write(str(files))

#     #tree.write(open(r'C:\\Users\\plasm\\Documents\\Temp\\gfg.xml', 'w', encoding='utf-8'))

#     #header = root.createElement(WriteHeader())
#     #xml.appendChild(header)

#     # asset = root.createElement("Asset")
#     # asset.setAttribute("Name", assetName)
#     # asset.setAttribute("Type", "model")
#     # objectTypes = root.createElement(GetObjectOutputTypes())
#     # asset.appendChild(objectTypes)
#     # xml.appendChild(asset)

#     # writeFolders = root.createElement(WriteFolders())
#     # xml.appendChild(writeFolders)
#     #faceCollections = root.createElement(WriteFaceCollections(True,True))
#     #xml.appendChild(faceCollections)

#     #contentObjects = root.createElement(GetModelContentObjects())
#     #content = root.createElement("Contents")
#     #content.appendChild(contentObjects)
#     #xml.appendChild(content)

#     # xmlstr = minidom.parseString(root).toprettyxml(indent="   ")

#     # save_path_file = "sidecar.xml"
  
#     # with open(save_path_file, "w") as f:
#     #     f.write(xmlstr) 

#     # root2 = minidom.Document()
  
#     # xml2 = root2.createElement('root') 
#     # root2.appendChild(xml2)
    
#     # productChild = root2.createElement('product')
#     # productChild.setAttribute('name', 'Geeks for Geeks')
    
#     # xml2.appendChild(productChild)
    
#     # xml_str = root.toprettyxml(indent ="\t") 
    
#     # save_path_file = "C:\\Users\\plasm\\Documents\\Temp\\gfg.xml"
    
#     # with open(save_path_file, "w") as f:
#     #     f.write(xml_str) 

# def GetModelContentObjects():
#     temp = []

#     if(IntermediateFileExists("render")):
#         temp.append(CreateContentObject("render"))

#     if(IntermediateFileExists("physics")):
#         temp.append(CreateContentObject("physics"))

#     if(IntermediateFileExists("collision")):
#         temp.append(CreateContentObject("collision"))

#     if(IntermediateFileExists("markers")):
#         temp.append(CreateContentObject("markers"))

#     if(IntermediateFileExists("skeleton")):
#         temp.append(CreateContentObject("skeleton"))

#     if(IntermediateFileExists("animations\\JMM") or IntermediateFileExists("animations\\JMA") or IntermediateFileExists("animations\\JMT") or IntermediateFileExists("animations\\JMZ") or IntermediateFileExists("animations\\JMV")
#         or IntermediateFileExists("animations\\JMO (Keyframe)") or IntermediateFileExists("animations\\JMO (Pose)") or IntermediateFileExists("animations\\JMR (Object)") or IntermediateFileExists("animations\\JMR (Local)")):
#         animations = xml.Element("ContentObject")
#         animations.set("Name", "")
#         animations.set("Type" "model_animation_graph")

#         if(IntermediateFileExists("animations\\JMM")):
#             animations.append(CreateContentObject("animations\\JMM", "Base", "ModelAnimationMovementData", "None", "", ""))

#         if(IntermediateFileExists("animations\\JMA")):
#             animations.append(CreateContentObject("animations\\JMA", "Base", "ModelAnimationMovementData", "XY", "", ""))

#         if(IntermediateFileExists("animations\\JMT")):
#             animations.append(CreateContentObject("animations\\JMT", "Base", "ModelAnimationMovementData", "XYYaw", "", ""))

#         if(IntermediateFileExists("animations\\JMZ")):
#             animations.append(CreateContentObject("animations\\JMZ", "Base", "ModelAnimationMovementData", "XYZYaw", "", ""))

#         if(IntermediateFileExists("animations\\JMV")):
#             animations.append(CreateContentObject("animations\\JMV", "Base", "ModelAnimationMovementData", "XYZFullRotation", "", ""))

#         if(IntermediateFileExists("animations\\JMO (Keyframe)")):
#             animations.append(CreateContentObject("animations\\JMO (Keyframe)", "Overlay", "ModelAnimationOverlayType", "Keyframe", "ModelAnimationOverlayBlending", "Additive"))

#         if(IntermediateFileExists("animations\\JMO (Pose)")):
#             animations.append(CreateContentObject("animations\\JMO (Pose)", "Overlay", "ModelAnimationOverlayType", "Pose", "ModelAnimationOverlayBlending", "Additive"))

#         if(IntermediateFileExists("animations\\JMR (Local)")):
#             animations.append(CreateContentObject("animations\\JMR (Local)", "Overlay", "ModelAnimationOverlayType", "keyframe", "ModelAnimationOverlayBlending", "ReplacementLocalSpace"))

#         if(IntermediateFileExists("animations\\JMR (Object)")):
#             animations.append(CreateContentObject("animations\\JMR (Object)", "Overlay", "ModelAnimationOverlayType", "keyframe", "ModelAnimationOverlayBlending", "ReplacementObjectSpace"))

#         r2 = xml.Element("OutputTagCollection")
#         outputTag1 = xml.SubElement(r2, "OutputTag")
#         outputTag1.set("Type", "frame_event_list")
#         outputTag1.text = "dataPath" + "\\" + "assetName"
#         outputTag2 = xml.SubElement(r2, "OutputTag")
#         outputTag2.set("Type", "model_animation_graph")
#         outputTag2.text = "dataPath" + "\\" + "assetName"

#         animations.append(r2)
#         temp.append(animations)

#     ContentObjects = xml.Element("Content")
#     ContentObjects.set("Name", "assetName")
#     ContentObjects.set("Type", "model")

#     for e in temp:
#         ContentObjects.append(e)

#     return ContentObjects

# def CreateContentObject(type):
#     print("")

# def CreateContentObject(type1, type2, type3, type4, type5, type6):
#     print("")


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