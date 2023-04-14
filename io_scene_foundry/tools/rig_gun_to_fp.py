# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Crisp
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

from io_scene_foundry.utils.nwo_utils import deselect_all_objects, set_active_object

def deselect_all_edit_bones(armature):
    for bone in armature.data.edit_bones:
        bone.select = False

def deselect_all_pose_bones(armature):
    for bone in armature.pose.bones:
        bone.select = False

def get_halo_bone_name(armature, pbone): # ('b ', 'b_', 'frame ', 'frame_','bip ','bip_','bone ','bone_')
    if armature.data.bones[pbone.name].nwo.name_override == '':
        name = pbone.name
    else:
        name = armature.data.bones[pbone.name].nwo.name_override
    if name.startswith('b '):
        return name.rpartition('b ')[2]
    elif name.startswith('b_'):
        return name.rpartition('b_')[2]
    elif name.startswith('frame '):
        return name.rpartition('frame ')[2]
    elif name.startswith('frame_'):
        return name.rpartition('frame_')[2]
    elif name.startswith('bip '):
        return name.rpartition('bip ')[2]
    elif name.startswith('bip_'):
        return name.rpartition('bip_')[2]
    elif name.startswith('bone '):
        return name.rpartition('bone ')[2]
    elif name.startswith('bone_'):
        return name.rpartition('bone_')[2]
    else:
        return name

def build_rig(report, selected_objects):
    # check that the user has selected two armatures
    for ob in selected_objects:
        if ob.type != 'ARMATURE':
            ob.select_set(False)
            selected_objects.remove(ob)

    if len(selected_objects) != 2:
        if len(selected_objects) < 2:
            report({'WARNING'}, 'Two armatures have not been selected. Aborting operation')
            return {'CANCELLED'}

        else:
            report({'WARNING'}, 'More than two armatures have been selected. Aborting operation')
            return {'CANCELLED'}
        
    # assign the fp and gun armatures to variables
    if get_halo_bone_name(selected_objects[0], selected_objects[0].pose.bones[0]) == 'gun':
        gun_armature = selected_objects[0]
        fp_armature = selected_objects[1]
    else:
        gun_armature = selected_objects[1]
        fp_armature = selected_objects[0]

    print(gun_armature)
    print(fp_armature)
    
    # verify both rigs are valid
    for pbone in fp_armature.pose.bones:
        if pbone.parent is None and get_halo_bone_name(fp_armature, pbone) == 'pedestal':
            deform_pedestal = pbone
            # once pedestal verified, check for r_hand bone
            for bone in pbone.children_recursive:
                if get_halo_bone_name(fp_armature, bone) == 'r_hand':
                    deform_r_hand = bone
                    break
            else:
                report({'WARNING'}, 'FP armature does not contain r_hand bone. Aborting operation')
                return {'CANCELLED'}
            for bone in pbone.children_recursive:
                if get_halo_bone_name(fp_armature, bone) == 'l_hand':
                    deform_l_hand = bone
                    break
            else:
                report({'WARNING'}, 'FP armature does not contain l_hand bone. Aborting operation')
                return {'CANCELLED'}
            
            break
    else:
        report({'WARNING'}, 'FP armature does not contain root pedestal bone. Aborting operation')
        return {'CANCELLED'}
    
    for pbone in gun_armature.pose.bones:
        if pbone.parent is None and get_halo_bone_name(gun_armature, pbone) == 'gun':
            deform_gun = pbone
            break
    else:
        report({'WARNING'}, 'Gun armature does not contain root gun bone. Aborting operation')
        return {'CANCELLED'}
    # check if gun armature contains a magazine bone
    deform_magazine = None
    for pbone in gun_armature.pose.bones:
        if get_halo_bone_name(gun_armature, pbone) == 'magazine':
            deform_magazine = pbone
            break
    else:
        print('Gun armature has no magazine bone')
    # check if fp armature contains a control pedestal bone
    control_pedestal = None
    control_ik_hand_r = None
    control_ik_hand_l = None
    for pbone in fp_armature.pose.bones:
        if pbone.parent is None and not fp_armature.data.bones[pbone.name].use_deform and 'pedestal' in pbone.name and pbone != deform_pedestal:
            control_pedestal = pbone
            for bone in pbone.children_recursive:
                if not fp_armature.data.bones[bone.name].use_deform and 'hand' in bone.name.lower() and 'ik' in bone.name.lower() and bone.name.upper().endswith('R') and bone != deform_r_hand:
                    control_ik_hand_r = bone
                    break
            for bone in pbone.children_recursive:
                if not fp_armature.data.bones[bone.name].use_deform and 'hand' in bone.name.lower() and 'ik' in bone.name.lower() and bone.name.upper().endswith('L') and bone != deform_l_hand:
                    control_ik_hand_l = bone
                    break

            break
    else:
        print('FP armature does not contain pedestal control bone, skipping set up of gun control rig')

    # get all child objects of armatures
    child_objects = []
    for ob in fp_armature.children:
        child_objects.append(ob)
    for ob in gun_armature.children:
        child_objects.append(ob)

    # begin rigging
    deselect_all_objects()
    gun_armature.select_set(True)
    fp_armature.select_set(True)
    set_active_object(fp_armature)
    # join the two armatures
    bpy.ops.object.join()
    # parent gun bone to r_hand
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    edit_deform_gun = fp_armature.data.edit_bones[deform_gun.name]
    edit_deform_r_hand = fp_armature.data.edit_bones[deform_r_hand.name]

    edit_deform_gun.parent = edit_deform_r_hand

    # set up control rig if valid
    if control_pedestal is not None:
        edit_control_pedestal = fp_armature.data.edit_bones[control_pedestal.name]
        
        edit_control_gun = fp_armature.data.edit_bones.new('CTRL_gun')
        edit_control_gun.length = edit_deform_gun.length
        edit_control_gun.matrix = edit_deform_gun.matrix.copy()
        edit_control_gun.use_deform = False
        edit_control_gun.parent = edit_control_pedestal

        # add magazine control bone if a deform magazine bone exists
        if deform_magazine is not None:
            edit_deform_magazine = fp_armature.data.edit_bones[deform_magazine.name]
            edit_control_magazine = fp_armature.data.edit_bones.new('CTRL_magazine')
            edit_control_magazine.length = edit_deform_magazine.length
            edit_control_magazine.matrix = edit_deform_magazine.matrix.copy()
            edit_control_magazine.use_deform = False
            edit_control_magazine.parent = edit_control_gun

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    # set up control rig constraints
    if control_pedestal is not None:
        # set copy transform constraint
        control_gun = fp_armature.pose.bones['CTRL_gun']
        constraint = deform_gun.constraints.new('COPY_TRANSFORMS')
        constraint.target = fp_armature
        constraint.subtarget = control_gun.name

        # and for magazine if it exists
        if deform_magazine is not None:
            control_magazine = fp_armature.pose.bones['CTRL_magazine']
            constraint = deform_magazine.constraints.new('COPY_TRANSFORMS')
            constraint.target = fp_armature
            constraint.subtarget = control_magazine.name

        # set up child of constraints for hands IK
        if control_ik_hand_r is not None:
            constraint = control_ik_hand_r.constraints.new('CHILD_OF')
            constraint.target = fp_armature
            constraint.subtarget = control_gun.name
        # constraint left hand to the magazine control if it exists
        if control_ik_hand_l is not None:
            constraint = control_ik_hand_l.constraints.new('CHILD_OF')
            constraint.target = fp_armature
            if deform_magazine is not None:
                constraint.subtarget = control_magazine.name
            else:
                constraint.subtarget = control_gun.name
            
        
    # parent meshes back to armature
    deselect_all_objects()
    for ob in child_objects:
        ob.select_set(True)
    fp_armature.select_set(True)
    set_active_object(fp_armature)
    bpy.ops.object.parent_set(type='ARMATURE')

    return {'FINISHED'}
