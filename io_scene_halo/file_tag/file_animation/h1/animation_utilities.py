# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
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

unit_animation_names = (
    'airborne-dead', 'landing-dead',
    'acc-front-back', 'acc-left-right', 'acc-up-down',
    'push', 'twist', 'enter', 'exit', 'look', 'talk', 'emotions', 'unused0',
    'user0', 'user1', 'user2', 'user3', 'user4',
    'user5', 'user6', 'user7', 'user8', 'user9',
    'flying-front', 'flying-back', 'flying-left', 'flying-right',
    'opening', 'closing', 'hovering'
    )
unit_weapon_animation_names = (
    'idle', 'gesture', 'turn-left', 'turn-right',
    'dive-front', 'dive-back', 'dive-left', 'dive-right',
    'move-front', 'move-back', 'move-left', 'move-right',
    'slide-front', 'slide-back', 'slide-left', 'slide-right',
    'airborne', 'land-soft', 'land-hard', 'unused0', 'throw-grenade',
    'disarm', 'drop', 'ready', 'put-away', 'aim-still', 'aim-move',
    'surprise-front', 'surprise-back', 'berserk',
    'evade-left', 'evade-right', 'signal-move', 'signal-attack', 'warn',
    'stunned-front', 'stunned-back', 'stunned-left', 'stunned-right',
    'melee', 'celebrate', 'panic', 'melee-airborne', 'flaming',
    'resurrect-front', 'resurrect-back', 'melee-continuous',
    'feeding', 'leap-start', 'leap-airborne', 'leap-melee',
    'zapping', 'unused1', 'unused2', 'unused3'
    )
unit_weapon_type_animation_names = (
    'reload-1', 'reload-2', 'chamber-1', 'chamber-2',
    'fire-1', 'fire-2', 'charged-1', 'charged-2',
    'melee', 'overheat'
    )

def animation_settings_transfer(H1_ASSET, DONOR_TAG, patch_txt_path, tag_format, report):
    TAG = tag_format.TagAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)
    animation_names = []
    for animation in DONOR_TAG.animations:
        animation_names.append(animation.name)

    for animation in H1_ASSET.animations:
        anim_name = tag_format.get_patched_name(TAG.upgrade_patches, animation.name)
        if anim_name in animation_names:
            animation_index = animation_names.index(anim_name)
            animation.loop_frame_index = DONOR_TAG.animations[animation_index].loop_frame_index
            animation.weight = DONOR_TAG.animations[animation_index].weight
            animation.key_frame_index = DONOR_TAG.animations[animation_index].key_frame_index
            animation.second_key_frame_index = DONOR_TAG.animations[animation_index].second_key_frame_index
            animation.sound = DONOR_TAG.animations[animation_index].sound
            animation.sound_frame_index = DONOR_TAG.animations[animation_index].sound_frame_index
            animation.left_foot_frame_index = DONOR_TAG.animations[animation_index].left_foot_frame_index
            animation.right_foot_frame_index = DONOR_TAG.animations[animation_index].right_foot_frame_index

    return H1_ASSET

def find_tag_block(tag_block, name):
    tag_element = None
    if not tag_block == None:
        for element in tag_block:
            if element.label == name:
                tag_element = element
                break

    return tag_element

def find_animation_index(tag_block, rename_string):
    animation_element_index = -1
    if not tag_block == None:
        for animation_idx, animation in enumerate(tag_block.animations):
            if animation.name == rename_string:
                animation_element_index = animation_idx

    return animation_element_index

def animation_rename(H1_ASSET, patch_txt_path, tag_format, report):
    TAG = tag_format.TagAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    if not TAG.upgrade_patches == None:
        for patch in TAG.upgrade_patches:
            invalid_rename = True
            unit_path = patch[0]
            rename_string = patch[1]
            rename_string_count = len(rename_string)
            if rename_string_count < 32:
                split_name = unit_path.split(" ")
                tag_element = find_tag_block(H1_ASSET.units, split_name[0])

                split_name_count = len(split_name)
                if split_name_count == 2 and not tag_element == None and not len(tag_element.animations) == 0:
                    try:
                        animation_index = unit_animation_names.index(split_name[1])
                        if animation_index < len(tag_element.animations):
                            if rename_string_count == 0:
                                tag_element.animations[animation_index] = -1
                                invalid_rename = False
                                print("Rename string '%s' was empty so we set the animation to null" % unit_path)

                            elif not animation_index == -1:
                                animation_element_index = find_animation_index(H1_ASSET, rename_string)
                                if not animation_element_index == -1:
                                    tag_element.animations[animation_index] = animation_element_index
                                    invalid_rename = False

                    except:
                        print('%s triggered an exception' % unit_path)
                        pass


                elif split_name_count == 3 and not tag_element == None and not len(tag_element.weapons) == 0:
                    tag_element = find_tag_block(tag_element.weapons, split_name[1])
                    if not tag_element == None and not len(tag_element.animations) == 0:
                        try:
                            animation_index = unit_weapon_animation_names.index(split_name[2])
                            if animation_index < len(tag_element.animations):
                                if rename_string_count == 0:
                                    tag_element.animations[animation_index] = -1
                                    invalid_rename = False
                                    print("Rename string '%s' was empty so we set the animation to null" % unit_path)

                                elif not animation_index == -1:
                                    animation_element_index = find_animation_index(H1_ASSET, rename_string)
                                    if not animation_element_index == -1:
                                        tag_element.animations[animation_index] = animation_element_index
                                        invalid_rename = False

                        except:
                            print('%s triggered an exception' % unit_path)
                            pass

                elif split_name_count == 4 and not tag_element == None and not len(tag_element.weapons) == 0:
                    tag_element = find_tag_block(tag_element.weapons, split_name[1])
                    if not tag_element == None and not len(tag_element.weapons) == 0:
                        tag_element = find_tag_block(tag_element.weapons, split_name[2])
                        if not tag_element == None and not len(tag_element.animations) == 0:
                            try:
                                animation_index = unit_weapon_type_animation_names.index(split_name[3])
                                if animation_index < len(tag_element.animations):
                                    if rename_string_count == 0:
                                        tag_element.animations[animation_index] = -1
                                        invalid_rename = False
                                        print("Rename string '%s' was empty so we set the animation to null" % unit_path)

                                    elif not animation_index == -1:
                                        animation_element_index = find_animation_index(H1_ASSET, rename_string)
                                        if not animation_element_index == -1:
                                            tag_element.animations[animation_index] = animation_element_index
                                            invalid_rename = False

                            except:
                                print('%s triggered an exception' % unit_path)
                                pass


                if invalid_rename:
                    print('%s was not found in the Units tag block' % unit_path)

            else:
                print("%s is greater than 31 characters" % rename_string)

    return H1_ASSET
