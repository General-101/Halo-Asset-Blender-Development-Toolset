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

import bpy

from bpy.types import (
        PropertyGroup,
        Operator,
        UIList,
        Panel,
        Menu
        )

from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        StringProperty,
        PointerProperty,
        CollectionProperty
        )

from ...global_functions import global_functions
from ...file_tag.tag_interface.tag_common import h1_tag_groups, h1_tag_extensions, h1_tag_groups_tuple, h2_tag_groups, h2_tag_extensions, h2_tag_groups_tuple

def get_tag_groups(self, context):
    items = ()
    if bpy.context.scene.halo.game_title == 'halo1':
        items = h1_tag_groups_tuple
    elif bpy.context.scene.halo.game_title == 'halo2':
        items = h2_tag_groups_tuple

    return items

def tag_add(self, name="NONE", tag_path="", tag_group="actr"):
    tag_element = self.tag_palatte.add()
    tag_element.name = name
    tag_element.tag_path = tag_path
    tag_element.tag_group = tag_group
    self.active_tag = 0

def set_tag_name(self, context):
    tag_group = self.tag_group
    tag_path = self.tag_path

    tag_path = tag_path.rsplit(".", 1)[0]
    tag_groups = None
    if bpy.context.scene.halo.game_title == 'halo1':
        tag_groups = h1_tag_groups
    elif bpy.context.scene.halo.game_title == 'halo2':
        tag_groups = h2_tag_groups

    if not global_functions.string_empty_check(tag_path) and tag_groups:
        tag_path = "%s.%s" % (tag_path, tag_groups.get(tag_group))
    else:
        tag_path = "NONE"

    self["name"] = tag_path

def get_tag_path(self):
    return self.get("tag_path", "")

def set_tag_path(self, value):
    tag_group = self.tag_group
    tag_path = value.lower()
    config_tag_path = ""
    tag_groups = None
    tag_extensions = None
    if bpy.context.scene.halo.game_title == 'halo1':
        tag_groups = h1_tag_groups
        tag_extensions = h1_tag_extensions
        config_tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path.lower()
    elif bpy.context.scene.halo.game_title == 'halo2':
        tag_groups = h2_tag_groups
        tag_extensions = h2_tag_extensions
        config_tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path.lower()
    
    if not global_functions.string_empty_check(config_tag_path):
        tag_path = tag_path.split(config_tag_path)
        if len(tag_path) >= 2:
            tag_path = tag_path[1]
        else:
            tag_path = tag_path[0]

    tag_path = tag_path.rsplit(".", 1)
    if len(tag_path) >= 2 and tag_extensions:
        tag_group = tag_extensions.get(tag_path[1])
        tag_path = tag_path[0]
    else:
        tag_path = tag_path[0]

    for ob in bpy.context.scene.objects:
        if tag_groups:
            tag_name = "%s.%s" % (self.tag_path, tag_groups.get(self.tag_group))
            if hasattr(ob, 'tag_object') and ob.tag_object.tag_path == tag_name:
                if not global_functions.string_empty_check(tag_path):
                    ob.tag_object.tag_path = "%s.%s" % (tag_path, tag_groups.get(tag_group))
                else:
                    ob.tag_object.tag_path = "NONE"
            if hasattr(ob, 'tag_netgame_flag') and ob.tag_netgame_flag.weapon_group == tag_name:
                if not global_functions.string_empty_check(tag_path):
                    ob.tag_netgame_flag.weapon_group = "%s.%s" % (tag_path, tag_groups.get(tag_group))
                else:
                    ob.tag_netgame_flag.weapon_group = "NONE"
            if hasattr(ob, 'tag_netgame_equipment') and ob.tag_netgame_equipment.item_collection == tag_name:
                if not global_functions.string_empty_check(tag_path):
                    ob.tag_netgame_equipment.item_collection = "%s.%s" % (tag_path, tag_groups.get(tag_group))
                else:
                    ob.tag_netgame_equipment.item_collection = "NONE"

    self["tag_path"] = tag_path
    self.tag_group = tag_group

class TagItem(PropertyGroup):
    name: StringProperty(
        name = "Name"
    )

    tag_group: EnumProperty(
        name="Tag Group",
        description="The tag group for this item",
        items= get_tag_groups,
        update=set_tag_name
        )

    tag_path: StringProperty(
           name="Tag Path",
           description="The tag path for this item",
           subtype="FILE_PATH",
           update=set_tag_name,
           get=get_tag_path,
           set=set_tag_path
           )

class TAG_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text="", icon='FACE_MAPS')
            layout.prop(item, "tag_group", text="", emboss=True)
            layout.prop(item, "tag_path", text="", emboss=True)

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class Halo_OT_TagAdd(Operator):
    """Add a new tag to the scene"""
    bl_idname = "tag_palatte.tag_add"
    bl_label = "Add a tag"

    def execute(self, context):
        scene = context.scene

        scene.tag_add()
        scene.active_tag = len(scene.tag_palatte) - 1

        return{'FINISHED'}

class Halo_OT_TagRemove(Operator):
    """Remove a tag from the scene"""
    bl_idname = "tag_palatte.tag_remove"
    bl_label = "Remove a tag"

    @classmethod
    def poll(cls, context):
        valid = False
        scene = context.scene
        if scene and len(scene.tag_palatte) > 0:
            valid = True

        return valid

    def execute(self, context):
        scene = context.scene

        tag_palatte = scene.tag_palatte
        active_tag = scene.active_tag

        tag_palatte.remove(active_tag)
        scene.active_tag = min(max(0, active_tag), len(tag_palatte) - 1)

        return{'FINISHED'}

class Halo_OT_TagMove(Operator):
    """Move the active tag up/down in the list"""
    bl_idname = "tag_palatte.tag_move"
    bl_label = "Move tag"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""), ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        valid = False
        scene = context.scene
        if scene and len(scene.tag_palatte) > 0:
            valid = True

        return valid

    def move_index(self, scene):
        list_length = len(scene.tag_palatte) - 1
        new_index = scene.active_tag + (-1 if self.direction == 'UP' else 1)

        scene.active_tag = max(0, min(new_index, list_length))

    def execute(self, context):
        scene = context.scene

        tag_palatte = scene.tag_palatte
        active_tag = scene.active_tag

        neighbor = active_tag + (-1 if self.direction == 'UP' else 1)
        tag_palatte.move(neighbor, active_tag)
        self.move_index(scene)

        return{'FINISHED'}

class Halo_TagPanel(Panel):
    bl_label = "Halo Tag References"
    bl_idname = "HALO_PT_Tag"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenarioTag"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tag_count = len(scene.tag_palatte)

        row = layout.row()
        row.template_list("TAG_UL_List", "Tag_List", scene, "tag_palatte", scene, "active_tag")

        col = row.column(align=True)
        col.operator("tag_palatte.tag_add", icon='ADD', text="")
        col.operator("tag_palatte.tag_remove", icon='REMOVE', text="")

        if tag_count >= 2:
            col.separator()
            col.operator("tag_palatte.tag_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("tag_palatte.tag_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        #col.separator()
        #col.menu("REGION_MT_context_menu", icon='DOWNARROW_HLT', text="")
