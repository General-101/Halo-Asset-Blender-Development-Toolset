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


from ..file_tag.h1.file_scenario.format import DataTypesEnum
from bpy.types import (
        PropertyGroup,
        Panel,
        )

from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        FloatVectorProperty
        )

class HALO_PropertiesGroup(PropertyGroup):
    data_type_enum: EnumProperty(
        name="Data Tyoe",
        description="What group is this object meant to represent",
        items=( ('0', "None", "None"),
                ('1', "Cluster", "Cluster"),
                ('2', "Scenery", "Scenery"),
                ('3', "Biped", "Biped"),
                ('4', "Vehicle", "Vehicle"),
                ('5', "Equipment", "Equipment"),
                ('6', "Weapons", "Weapons"),
                ('7', "Machines", "Machines"),
                ('8', "Controls", "Controls"),
                ('9', "Light Fixtures", "Light Fixtures"),
                ('10', "Sound Scenery", "Sound Scenery"),
                ('11', "Player Starting Locations", "Player Starting Locations"),
                ('12', "Netgame Flags", "Netgame Flags"),
                ('13', "Netgame Equipment", "Netgame Equipment"),
                ('14', "Decals", "Decals"),
                ('15', "Encounters", "Encounters"),
                ('16', "Instance", "Instance"),
            )
        )

    lightmap_index: IntProperty(
        name = "Lightmap Index",
        description = "What index do we use in the referenced lightmap tag. Try not to edit this manually",
        default = -1
        )

    instance_lightmap_policy_enum: EnumProperty(
        name="Lightmap Policy",
        description="Wow the lightmapper uses the object",
        items=( ('0', "Per Pixel", "Object uses baked lighting"),
                ('1', "Per Vertex", "Object uses vertex lighting")
            )
        )

    tag_path: StringProperty(
        name = "Tag Path",
        description = "Set the referenced tag for the object"
        )

    object_name: StringProperty(
        name = "Object Name",
        description = "Set the reference name for the object"
        )

    automatically: BoolProperty(
        name ="Automatically",
        description = "Not placed automatically. Must be created via script",
        default = False,
        )

    on_easy: BoolProperty(
        name ="On Easy",
        description = "Not placed automatically on easy difficulty. Must be created via script",
        default = False,
        )

    on_normal: BoolProperty(
        name ="On Normal",
        description = "Not placed automatically on normal difficulty. Must be created via script",
        default = False,
        )

    on_hard: BoolProperty(
        name ="On Hard",
        description = "Not placed automatically on Heroic difficulty. Must be created via script",
        default = False,
        )

    use_player_appearance: BoolProperty(
        name ="Use Player Appearance",
        description = "I have no idea what this is",
        default = False,
        )

    desired_permutation: IntProperty(
        name = "Desired Permutation",
        description = "What permutation to use for the object"
        )

    appearance_player_index: IntProperty(
        name = "Appearance Player Index",
        description = "I have no idea what this is"
        )

    unit_vitality: FloatProperty(
        name="Vitality",
        description="Unit starts with percentage of health",
        min=0.0,
        max=1.0,
        )

    unit_dead: BoolProperty(
        name ="Dead",
        description = "Unit starts dead on creation",
        default = False,
        )

    multiplayer_team_index: IntProperty(
        name="Multiplayer Team Index",
        description="I have no idea what this is",
        )

    slayer_default: BoolProperty(
        name ="Slayer Default",
        description = "I have no idea what this is",
        default = False,
        )

    ctf_default: BoolProperty(
        name ="CTF Default",
        description = "I have no idea what this is",
        default = False,
        )

    king_default: BoolProperty(
        name ="King Default",
        description = "I have no idea what this is",
        default = False,
        )

    oddball_default: BoolProperty(
        name ="Oddball Default",
        description = "I have no idea what this is",
        default = False,
        )

    unused_0: BoolProperty(
        name ="Unused 0",
        description = "Unused",
        default = False,
        )

    unused_1: BoolProperty(
        name ="Unused 1",
        description = "Unused",
        default = False,
        )

    unused_2: BoolProperty(
        name ="Unused 2",
        description = "Unused",
        default = False,
        )

    unused_3: BoolProperty(
        name ="Unused 3",
        description = "Unused",
        default = False,
        )

    slayer_allowed: BoolProperty(
        name ="Slayer Allowed",
        description = "I have no idea what this is",
        default = False,
        )

    ctf_allowed: BoolProperty(
        name ="CTF Allowed",
        description = "I have no idea what this is",
        default = False,
        )

    king_allowed: BoolProperty(
        name ="King Allowed",
        description = "I have no idea what this is",
        default = False,
        )

    oddball_allowed: BoolProperty(
        name ="Oddball Allowed",
        description = "I have no idea what this is",
        default = False,
        )

    unused_4: BoolProperty(
        name ="Unused 4",
        description = "Unused",
        default = False,
        )

    unused_5: BoolProperty(
        name ="Unused 5",
        description = "Unused",
        default = False,
        )

    unused_6: BoolProperty(
        name ="Unused 6",
        description = "Unused",
        default = False,
        )

    unused_7: BoolProperty(
        name ="Unused 7",
        description = "Unused",
        default = False,
        )

    initially_at_rest: BoolProperty(
        name ="Initially At Rest",
        description = "Doesn't Fall",
        default = False,
        )

    obsolete: BoolProperty(
        name ="Obsolete",
        description = "I have no idea what this is",
        default = False,
        )

    does_accelerate: BoolProperty(
        name ="Does Accelerate",
        description = "Moves due to explosions",
        default = False,
        )

    rounds_left: IntProperty(
        name = "Rounds Left",
        description = "How many rounds left in reserve"
        )

    rounds_loaded: IntProperty(
        name = "Round Loaded",
        description = "How many rounds in the clip"
        )

    power_group: IntProperty(
        name = "Power Group",
        default = -1,
        description = "Power group index",
        min = -1
        )

    position_group: IntProperty(
        name = "Position Group",
        default = -1,
        description = "Position group index",
        min = -1
        )

    initially_open: BoolProperty(
        name ="Initially Open",
        description = "Power set to 1.0",
        default = False,
        )

    initially_off: BoolProperty(
        name ="Initially Off",
        description = "Power set to 0.0",
        default = False,
        )

    can_change_only_once: BoolProperty(
        name ="Can Change Only Once",
        description = "Device can only be set once",
        default = False,
        )

    position_reversed: BoolProperty(
        name ="Position Reversed",
        description = "Position value is inverted",
        default = False,
        )

    not_usable_from_any_side: BoolProperty(
        name ="Not Usable From Any Side",
        description = "Unable to interact with the device",
        default = False,
        )

    does_not_operate_automatically: BoolProperty(
        name ="Does Not Operate Automatically",
        description = "Automatic activation radius is ignored",
        default = False,
        )

    one_sided: BoolProperty(
        name ="One Sided",
        description = "Object is only usable from forward vector",
        default = False,
        )

    never_appears_locked: BoolProperty(
        name ="Never Appears Locked",
        description = "Machine does not use locked color data",
        default = False,
        )

    opened_by_melee_attack: BoolProperty(
        name ="Opened By Melee Attack",
        description = "Machine activates when meleed",
        default = False,
        )

    usable_from_both_sides: BoolProperty(
        name ="Usable From Both Sides",
        description = "Control ignores forward vector",
        default = False,
        )

    control_value: IntProperty(
        name = "Unknown",
        description = "Unknown",
        )

    color: FloatVectorProperty(
        name = "Color",
        description = "Color of the light emitted",
        subtype = 'COLOR',
        default = (1.0, 1.0, 1.0),
        max = 1.0,
        min = 0.0,
        )

    intensity: FloatProperty(
        name="Intensity",
        description="Strength of the light",
        min=0.0
        )

    falloff_angle: FloatProperty(
        name="Falloff Angle",
        description="I have no idea what this is",
        subtype="ANGLE"
        )

    cutoff_angle: FloatProperty(
        name="Cutoff Angle",
        description="I have no idea what this is",
        subtype="ANGLE"
        )

    team_index: IntProperty(
        name = "Team Index",
        description = "Team index",
        min = 0
        )
    
    bsp_index: IntProperty(
        name = "BSP Index",
        description = "BSP index",
        min = -1
        )

    type_options = ( ('0', "None", "None"),
                ('1', "CTF", "CTF"),
                ('2', "Slayer", "Slayer"),
                ('3', "Oddball", "Oddball"),
                ('4', "King Of The Hill", "King Of The Hill"),
                ('5', "Race", "Race"),
                ('6', "Terminator", "Terminator"),
                ('7', "Stub", "Stub"),
                ('8', "Ignored1", "Ignored1"),
                ('9', "Ignored2", "Ignored2"),
                ('10', "Ignored3", "Ignored3"),
                ('11', "Ignored4", "Ignored4"),
                ('12', "All Games", "All Games"),
                ('13', "All Except CTF", "All Except CTF"),
                ('14', "All Except Race And CTF", "All Except Race And CTF")
            )

    type_0: EnumProperty(
        name="Type 0",
        description="Type 0",
        items=type_options
        )

    type_1: EnumProperty(
        name="Type 1",
        description="Type 1",
        items=type_options
        )

    type_2: EnumProperty(
        name="Type 2",
        description="Type 2",
        items=type_options
        )

    type_3: EnumProperty(
        name="Type 3",
        description="Type 3",
        items=type_options
        )

def render_cluster(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Lightmap Index:')
    row.prop(tag_view, "lightmap_index", text='')

def render_instance(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Lightmap Policy:')
    row.prop(tag_view, "instance_lightmap_policy_enum", text='')

def render_object(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Tag Path')
    row.prop(tag_view, "tag_path", text='')
    row = col.row()
    row.label(text='Object Name')
    row.prop(tag_view, "object_name", text='')

    box_flags = layout.box()
    box_flags.label(text="Not Placed")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "automatically")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "on_easy")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "on_normal")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "on_hard")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "use_player_appearance")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Desired Permutation')
    row.prop(tag_view, "desired_permutation", text='')

def render_scenery(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(tag_view, "appearance_player_index", text='')

def render_unit(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(tag_view, "appearance_player_index", text='')
    row = col.row()
    row.label(text='Vitality')
    row.prop(tag_view, "unit_vitality", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "unit_dead")

def render_vehicle(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Multiplayer Team Index')
    row.prop(tag_view, "multiplayer_team_index", text='')

    box_flags = layout.box()
    box_flags.label(text="Multiplayer Spawn Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "slayer_default")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "ctf_default")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "king_default")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "oddball_default")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "unused_0")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "unused_1")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "unused_2")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "unused_3")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "slayer_allowed")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "ctf_allowed")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "king_allowed")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "oddball_allowed")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "unused_4")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "unused_5")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "unused_6")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "unused_7")

def render_equipment(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)

    box_flags = layout.box()
    box_flags.label(text="Misc Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "initially_at_rest")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "obsolete")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "does_accelerate")

    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(tag_view, "appearance_player_index", text='')

def render_weapon(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(tag_view, "appearance_player_index", text='')
    row = col.row()
    row.label(text='Rounds Left')
    row.prop(tag_view, "rounds_left", text='')
    row = col.row()
    row.label(text='Rounds Loaded')
    row.prop(tag_view, "rounds_loaded", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "initially_at_rest")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "obsolete")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "does_accelerate")

def render_device(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(tag_view, "appearance_player_index", text='')
    row = col.row()
    row.label(text='Power Group')
    row.prop(tag_view, "power_group", text='')
    row = col.row()
    row.label(text='Position Group')
    row.prop(tag_view, "position_group", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "initially_open")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "initially_off")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "can_change_only_once")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "position_reversed")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "not_usable_from_any_side")

def render_machine(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "does_not_operate_automatically")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "one_sided")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "never_appears_locked")
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "opened_by_melee_attack")

def render_control(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(tag_view, "usable_from_both_sides")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.prop(tag_view, "control_value")

def render_light_fixture(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Color')
    row.prop(tag_view, "color", text='')
    row = col.row()
    row.label(text='Intensity')
    row.prop(tag_view, "intensity", text='')
    row = col.row()
    row.label(text='Falloff Angle')
    row.prop(tag_view, "falloff_angle", text='')
    row = col.row()
    row.label(text='Cutoff Angle')
    row.prop(tag_view, "cutoff_angle", text='')

def render_player_starting_location(layout, tag_view):
    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Team Index')
    row.prop(tag_view, "team_index", text='')
    row = col.row()
    row.label(text='BSP Index')
    row.prop(tag_view, "bsp_index", text='')
    row = col.row()
    row.label(text='Type 0')
    row.prop(tag_view, "type_0", text='')
    row = col.row()
    row.label(text='Type 1')
    row.prop(tag_view, "type_1", text='')
    row = col.row()
    row.label(text='Type 2')
    row.prop(tag_view, "type_2", text='')
    row = col.row()
    row.label(text='Type 3')
    row.prop(tag_view, "type_3", text='')

class Halo_TagView(Panel):
    bl_label = "Halo Tag View"
    bl_idname = "HALO_PT_TagView"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ObjectDetailsPanel"

    def draw(self, context):
        layout = self.layout
        tag_view = context.object.tag_view

        box = layout.split()
        col = box.column(align=True)
        row = col.row()
        row.label(text='Data Type:')
        row.prop(tag_view, "data_type_enum", text='')

        data_type_value = int(tag_view.data_type_enum)
        if data_type_value == DataTypesEnum.clusters.value:
            if context.scene.halo.game_title == 'halo1':
                render_cluster(layout, tag_view)
        elif data_type_value == DataTypesEnum.scenery.value or data_type_value == DataTypesEnum.sound_scenery.value:
            render_object(layout, tag_view)
            render_scenery(layout, tag_view)
        elif data_type_value == DataTypesEnum.bipeds.value:
            render_object(layout, tag_view)
            render_unit(layout, tag_view)
        elif data_type_value == DataTypesEnum.vehicles.value:
            render_object(layout, tag_view)
            render_unit(layout, tag_view)
            render_vehicle(layout, tag_view)
        elif data_type_value == DataTypesEnum.equipment.value:
            render_object(layout, tag_view)
            render_equipment(layout, tag_view)
        elif data_type_value == DataTypesEnum.weapons.value:
            render_object(layout, tag_view)
            render_weapon(layout, tag_view)
        elif data_type_value == DataTypesEnum.machines.value:
            render_object(layout, tag_view)
            render_device(layout, tag_view)
            render_machine(layout, tag_view)
        elif data_type_value == DataTypesEnum.controls.value:
            render_object(layout, tag_view)
            render_device(layout, tag_view)
            render_control(layout, tag_view)
        elif data_type_value == DataTypesEnum.light_fixtures.value:
            render_object(layout, tag_view)
            render_device(layout, tag_view)
            render_light_fixture(layout, tag_view)
        elif data_type_value == DataTypesEnum.player_starting_locations.value:
            render_player_starting_location(layout, tag_view)
        elif data_type_value == DataTypesEnum.instances.value:
            render_instance(layout, tag_view)
