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

import bpy
import os
from subprocess import Popen

from ...gr2_utils import (
    GetTagsPath,
    GetEKPath,
    GetToolPath,
    frame_prefixes,
    GetSceneArmature,
    GetPrefix,
)

def set_frame_ids():
    model_armature = GetSceneArmature()
    framelist = ImportTagXML(GetToolPath(), '')
    tag_bone_names = CleanBoneNames(framelist)
    blend_bone_names = CleanBones(model_armature.data.bones)
    blend_bones = model_armature.data.bones
    
    for blend_bone in blend_bone_names:
        for tag_bone in tag_bone_names:
            if blend_bone == tag_bone:
                ApplyFrameIDs(blend_bone, blend_bones, framelist)

    return {'FINISHED'}

def ApplyFrameIDs(bone_name, bone_names_list, framelist):
    for b in bone_names_list:
        if CleanBone(b) == bone_name:
            b.halo_json.frame_id1 = GetID(1, bone_name, framelist)
            b.halo_json.frame_id2 = GetID(2, bone_name, framelist)

def GetID(ID, name, framelist):
    frame = ''
    for x in framelist:
        b_name = CleanBoneName(x[0])
        if b_name == name:
            frame = x[ID]
    print ('frame is ' + frame)
    return frame

def CleanBoneNames(bones):
    cleanlist = []
    for b in bones:
        prefix = GetPrefix(b[0], frame_prefixes)
        cleaned_bone = b[0].removeprefix(prefix)
        cleanlist.append(cleaned_bone)
    
    return cleanlist

def CleanBones(bones):
    cleanlist = []
    for b in bones:
        prefix = GetPrefix(b.name, frame_prefixes)
        cleaned_bone = b.name.removeprefix(prefix)
        cleanlist.append(cleaned_bone)

    return cleanlist

def CleanBone(bone):
    prefix = GetPrefix(bone.name, frame_prefixes)
    cleaned_bone = bone.name.removeprefix(prefix)

    return cleaned_bone

def CleanBoneName(bone):
    prefix = GetPrefix(bone, frame_prefixes)
    cleaned_bone = bone.removeprefix(prefix)

    return cleaned_bone

def ImportTagXML(toolPath, assetPath):
    xmlPath = GetTagsPath() + "temp.xml"
    tagPath = "D:\\Games\\steamapps\\common\\HREK\\tags\\objects\\characters\\spartans\\spartans.model_animation_graph"
    toolCommand = '"{}" export-tag-to-xml "{}" "{}"'.format(toolPath, tagPath, xmlPath)
    print('\nRunning Tool command... %r' % toolCommand)
    os.chdir(GetEKPath())
    p = Popen(toolCommand)
    p.wait()
    bonelist = ParseXML(xmlPath)
    return bonelist

def ParseXML(xmlPath):
    parent = []
    import xml.etree.ElementTree as ET
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
            if(attributes.get('name') == 'frame_ID2'):
                print('HIT!')
                frameID2 = (attributes.get('value'))
        if not name == '':
            temp = [name, frameID1, frameID2]
            print(temp)
            parent.append(temp)
    return parent