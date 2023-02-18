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

def set_export(context, report, setting):
    if setting == 'none':
        b_var = False
    else:
        b_var = True
    # get scene armature
    for ob in context.view_layer.objects:
        if ob.type == 'ARMATURE' and not ob.name.startswith('+'):
            model_armature = ob
            break
    
    if setting == 'active':
        for action in bpy.data.actions:
            action.nwo.export_this = False
        model_armature.animation_data.action.nwo.export_this = True
        report({'INFO'},f"Enabled export only for {model_armature.animation_data.action.name}")
    else:
        for action in bpy.data.actions:
            action.nwo.export_this = b_var
            if b_var:
                report({'INFO'},"Enabled export for all animations")
            else:
                report({'INFO'},"Disabled export for all animations")

    context.area

    return {'FINISHED'}

