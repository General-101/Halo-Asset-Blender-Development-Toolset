# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

from .format import FunctionScaleEnum, get_valid_h1_object_functions
from ....file_tag.h1.file_weapon.format import get_valid_h1_weapon_functions
def get_function_list(H1_ASSET, function_list, keyword, FunctionsEnum):
    if "Object" == keyword:
        a_scale_function = FunctionsEnum(H1_ASSET.object_a_in)
        b_scale_function = FunctionsEnum(H1_ASSET.object_b_in)
        c_scale_function = FunctionsEnum(H1_ASSET.object_c_in)
        d_scale_function = FunctionsEnum(H1_ASSET.object_d_in)
        if a_scale_function != FunctionsEnum.none:
            function_list[0] = get_valid_h1_object_functions(a_scale_function.name)
        if b_scale_function != FunctionsEnum.none:
            function_list[1] = get_valid_h1_object_functions(b_scale_function.name)
        if c_scale_function != FunctionsEnum.none:
            function_list[2] = get_valid_h1_object_functions(c_scale_function.name)
        if d_scale_function != FunctionsEnum.none:
            function_list[3] = get_valid_h1_object_functions(d_scale_function.name)
    elif "Weapon" == keyword:
        a_scale_function = FunctionsEnum(H1_ASSET.weapon_a_in)
        b_scale_function = FunctionsEnum(H1_ASSET.weapon_b_in)
        c_scale_function = FunctionsEnum(H1_ASSET.weapon_c_in)
        d_scale_function = FunctionsEnum(H1_ASSET.weapon_d_in)
        if a_scale_function != FunctionsEnum.none:
            function_list[0] = get_valid_h1_weapon_functions(a_scale_function.name)
        if b_scale_function != FunctionsEnum.none:
            function_list[1] = get_valid_h1_weapon_functions(b_scale_function.name)
        if c_scale_function != FunctionsEnum.none:
            function_list[2] = get_valid_h1_weapon_functions(c_scale_function.name)
        if d_scale_function != FunctionsEnum.none:
            function_list[3] = get_valid_h1_weapon_functions(d_scale_function.name)

def get_scale_function(function_tag_block, function_index, function_list):
    scale_name = ""
    function_count = len(function_tag_block)
    function_element = function_tag_block[function_index]
    scale_function = FunctionScaleEnum(function_element.scale_function_by)
    if scale_function != FunctionScaleEnum.none and scale_function.value < 5:
        if scale_function.value == 1 and function_count >= 1:
            scale_name = function_list[0]
        elif scale_function.value == 2 and function_count >= 2:
            scale_name = function_list[1]
        elif scale_function.value == 3 and function_count >= 3:
            scale_name = function_list[2]
        elif scale_function.value == 4 and function_count >= 4:
            scale_name = function_list[3]

    return scale_name

def convert_attachment_scale(H1_ASSET, function_channel, function_keywords):
    function_list = ["", "", "", ""]
    for function_keyword in function_keywords:
        get_function_list(H1_ASSET, function_list, function_keyword[0], function_keyword[1])

    scale_name = ""
    function_tag_block = H1_ASSET.functions
    function_count = len(function_tag_block)
    if function_channel == 1 and function_count >= 1:
        scale_name = get_scale_function(function_tag_block, 0, function_list)
    elif function_channel == 2 and function_count >= 2:
        scale_name = get_scale_function(function_tag_block, 1, function_list)
    elif function_channel == 3 and function_count >= 3:
        scale_name = get_scale_function(function_tag_block, 2, function_list)
    elif function_channel == 4 and function_count >= 4:
        scale_name = get_scale_function(function_tag_block, 3, function_list)

    return scale_name

def generate_attachments(H1_ASSET, TAG, ASSET, function_keywords):
    for attachment_element in H1_ASSET.attachments:
        attachment = ASSET.Attachment()
        attachment.attachment_type = attachment_element.attachment_type
        attachment.marker = attachment_element.marker
        attachment.marker_length = len(attachment.marker)
        attachment.primary_scale = convert_attachment_scale(H1_ASSET, attachment_element.primary_scale, function_keywords)
        attachment.primary_scale_length = len(attachment.primary_scale)
        attachment.secondary_scale = convert_attachment_scale(H1_ASSET, attachment_element.secondary_scale, function_keywords)
        attachment.secondary_scale_length = len(attachment.secondary_scale)

        ASSET.attachments.append(attachment)

    attachment_count = len(ASSET.attachments)
    ASSET.attachments_header = TAG.TagBlockHeader("tbfd", 0, attachment_count, 32)

    return TAG.TagBlock(attachment_count)

def generate_widgets(H1_ASSET, TAG, ASSET):
    for widget_element in H1_ASSET.widgets:
        ASSET.widgets.append(widget_element)

    widget_count = len(ASSET.widgets)
    ASSET.widgets_header = TAG.TagBlockHeader("tbfd", 0, widget_count, 16)

    return TAG.TagBlock(widget_count)

def generate_change_colors(H1_ASSET, TAG, ASSET, function_keywords):
    for change_color_element in H1_ASSET.change_colors:
        change_color = ASSET.ChangeColor()
        change_color.initial_permutations = []
        for permutation_element in change_color_element.permutations:
            initial_permutation = ASSET.InitialPermutations()
            initial_permutation.weight = permutation_element.weight
            initial_permutation.color_lower_bound = permutation_element.color_lower_bound
            initial_permutation.color_upper_bound = permutation_element.color_upper_bound

            change_color.initial_permutations.append(initial_permutation)

        initial_permutation_count = len(change_color.initial_permutations)
        change_color.initial_permutations_header = TAG.TagBlockHeader("tbfd", 0, initial_permutation_count, 32)
        change_color.initial_permutations_tag_block = TAG.TagBlock(initial_permutation_count)

        change_color.functions = []
        color_function = ASSET.Function()
        color_function.scale_flags = change_color_element.scale_flags
        color_function.color_lower_bound = change_color_element.color_lower_bound
        color_function.color_upper_bound = change_color_element.color_upper_bound
        color_function.darken_by = convert_attachment_scale(H1_ASSET, change_color_element.darken_by, function_keywords)
        color_function.scale_by = convert_attachment_scale(H1_ASSET, change_color_element.scale_by, function_keywords)
        color_function.darken_by_length = len(color_function.darken_by)
        color_function.scale_by_length = len(color_function.scale_by)

        change_color.functions.append(color_function)

        function_count = len(change_color.functions)
        change_color.functions_header = TAG.TagBlockHeader("tbfd", 0, function_count, 40)
        change_color.functions_tag_block = TAG.TagBlock(function_count)

        ASSET.change_colors.append(change_color)

    change_color_count = len(ASSET.change_colors)
    ASSET.change_colors_header = TAG.TagBlockHeader("tbfd", 0, change_color_count, 24)

    return TAG.TagBlock(change_color_count)
