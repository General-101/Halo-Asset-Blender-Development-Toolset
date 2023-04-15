# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Generalkidd & Crisp
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

import os
import ctypes
import xml.etree.ElementTree as ET
from subprocess import Popen

from io_scene_foundry.utils.nwo_utils import (
    get_tags_path,
    get_ek_path,
    get_tool_path,
    frame_prefixes,
    get_prefix,
    run_tool,
    dot_partition,
    comma_partition,
)

def reset_frame_ids(context, report):
    model_armature = GetArmature(context, report)
    if model_armature != None:
        blend_bones = model_armature.data.bones
        for b in blend_bones:
            b.nwo.frame_id1 = ''
            b.nwo.frame_id2 = ''
        
        report({'INFO'},"Frame IDs Reset")
    
    return {'FINISHED'}
    
def set_frame_ids(context, report):
    model_armature = GetArmature(context, report)
    frame_count = 0
    if model_armature != None:
        try:
            framelist = ImportTagXML(context, report)
            if(not framelist == None):
                tag_bone_names = CleanBoneNames(framelist)
                blend_bone_names = CleanBones(model_armature.data.bones)
                blend_bones = model_armature.data.bones
                
                for blend_bone in blend_bone_names:
                    for tag_bone in tag_bone_names:
                        if blend_bone == tag_bone:
                            ApplyFrameIDs(blend_bone, blend_bones, framelist)
                            frame_count += 1

                report({'INFO'},"Updated Frame IDs for " + str(frame_count) + ' bones')
        except:
            report({'WARNING'},"Failed to parse exported tag XML")

    return {'FINISHED'}

def ApplyFrameIDs(bone_name, bone_names_list, framelist):
    for b in bone_names_list:
        if CleanBone(b) == bone_name:
            b.nwo.frame_id1 = GetID(1, bone_name, framelist)
            b.nwo.frame_id2 = GetID(2, bone_name, framelist)

def GetID(ID, name, framelist):
    frame = ''
    for x in framelist:
        b_name = CleanBoneName(x[0])
        if b_name == name:
            frame = x[ID]
    return frame

def CleanBoneNames(bones):
    cleanlist = []
    for b in bones:
        prefix = get_prefix(b[0], frame_prefixes)
        cleaned_bone = b[0].removeprefix(prefix)
        cleanlist.append(cleaned_bone)
    
    return cleanlist

def CleanBones(bones):
    cleanlist = []
    for b in bones:
        prefix = get_prefix(b.name, frame_prefixes)
        cleaned_bone = b.name.removeprefix(prefix)
        cleanlist.append(cleaned_bone)

    return cleanlist

def CleanBone(bone):
    prefix = get_prefix(bone.name, frame_prefixes)
    cleaned_bone = bone.name.removeprefix(prefix)

    return cleaned_bone

def CleanBoneName(bone):
    prefix = get_prefix(bone, frame_prefixes)
    cleaned_bone = bone.removeprefix(prefix)

    return cleaned_bone

def ImportTagXML(context, report):
    # try:
    xml_path = get_tags_path() + "temp.xml"
    tag_path = GetGraphPath(context)
    print(os.path.join(get_ek_path(), tag_path))
    if not os.path.exists(os.path.join(get_ek_path(), tag_path)):
        report({'WARNING'},"Could not find file that exists at this path. Are your Editing Kit path and animation graph path correct?")
        return None
    os.chdir(get_ek_path())
    run_tool(['export-tag-to-xml', f'\\{tag_path}', xml_path])
    if not os.path.exists(xml_path):
        report({'WARNING'},"Failed to convert supplied tag path to XML. Did you enter a valid tag path?")
        return None
    bonelist = ParseXML(xml_path, context)
    os.remove(xml_path)
    return bonelist
    # except:
    #     ctypes.windll.user32.MessageBoxW(0, "Tool.exe failed to get tag XML for FrameIDs. Please check the path to your .model_animation_graph tag.", "GET FRAMEIDS FAILED", 0)
    #     return None

def GetGraphPath(context):
    path = context.scene.nwo_frame_ids.anim_tag_path
    # path cleaning
    path = path.strip('\\')
    path = path.replace(get_tags_path(), '')
    path = os.path.join('tags', path)
    path = dot_partition(path)
    path = comma_partition(path)
    path = f'{path}.model_animation_graph'

    return path

def ParseXML(xmlPath, context):
    parent = []
    scene = context.scene
    scene_nwo = scene.nwo_global

    if scene_nwo.game_version in ('h4','h2a'):
        tree = ET.parse(xmlPath, parser = ET.XMLParser(encoding = 'iso-8859-5'))
        root = tree.getroot()
        for b in root.findall('block'):
            for e in b.findall('element'):
                name = ''
                frameID1 = ''
                frameID2 = ''
                for f in e.findall('field'):
                    attributes = f.attrib
                    if(attributes.get('name') == 'frame_ID1'):
                        name = (e.get('name'))
                        frameID1 = (attributes.get('value'))
                    elif(attributes.get('name') == 'frame_ID2'):
                        frameID2 = (attributes.get('value'))
                if not name == '':
                    temp = [name, frameID1, frameID2]
                    parent.append(temp)
    else: 
        tree = ET.parse(xmlPath)
        root = tree.getroot()
        for e in root.findall('element'):
            name = ''
            frameID1 = ''
            frameID2 = ''
            for f in e.findall('field'):
                attributes = f.attrib
                if(attributes.get('name') == 'frame_ID1'):
                    name = (e.get('name'))
                    frameID1 = (attributes.get('value'))
                elif(attributes.get('name') == 'frame_ID2'):
                    frameID2 = (attributes.get('value'))
            if not name == '':
                temp = [name, frameID1, frameID2]
                parent.append(temp)

    return parent

def GetArmature(context, report):
    model_armature = None
    for ob in context.scene.objects:
        if ob.type == 'ARMATURE' and not ob.name.startswith('+'): # added a check for a '+' prefix in armature name, to support special animation control armatures in the future
            model_armature = ob
            break
    if model_armature == None:
        report({'WARNING'},"Could not find any valid armature in the scene. Frame ID operation aborted")

    return model_armature