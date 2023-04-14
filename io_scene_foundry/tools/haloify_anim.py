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

def haloify_anim(context, rename, new, suffix, anim_mode, anim_class, anim_type, anim_state, anim_damage, anim_direction, anim_region, anim_mode_2, anim_state_2, animation = None):
    # Add a fake user to the animation (to ensure it is not deleted on closing the blend file)
    animation.use_fake_user = True
    animation_name = ''
    if rename or new:
        pass
        # code to add the name
    # set the animation type by adding the animation suffix
    else:
        # get the current animation less anything after the final '.'
        animation_name = max(animation.name.rpartition('.')[0], animation.name)
    
    animation_name_full = f'{animation_name}.{suffix}'

    if new:
        bpy.ops.action.new()
        animation = context.object.animation_data.action
    
    animation.name = animation_name_full

    return {'FINISHED'}

