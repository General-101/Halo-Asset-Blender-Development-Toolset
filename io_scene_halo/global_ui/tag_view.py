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
        Panel,
        Operator,
        PropertyGroup
        )

from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        FloatProperty,
        StringProperty,
        PointerProperty,
        FloatVectorProperty
        )

state_items=( ('0', "NONE", "NONE"),
            ('1', "Sleeping", "Sleeping"),
            ('2', "Alert", "Alert"),
            ('3', "Moving Repeat Same Position", "Moving Repeat Same Position"),
            ('4', "Moving Loop", "Moving Loop"),
            ('5', "Moving Loop Back And Forth", "Moving Loop Back And Forth"),
            ('6', "Moving Loop Randomly", "Moving Loop Randomly"),
            ('7', "Moving Randomly", "Moving Randomly"),
            ('8', "Guarding", "Guarding"),
            ('9', "Guarding At Guard Position", "Guarding At Guard Position"),
            ('10', "Searching", "Searching"),
            ('11', "Fleeing", "Fleeing"))

def atom_modifier_callback(self, context):
    items=[('0', "Default", "Default")]

    active_item = context.collection

    atom_type = int(active_item.tag_command.atom_type)
    if atom_type == 1:
        items = [
            ('0', "Stop At Point", "Stop At Point"),
            ('1', "Keep Moving", "Keep Moving")
            ]
    elif atom_type == 3:
        items = [
            ('0', "Facing Forward", "Facing Forward"),
            ('1', "Facing Left", "Facing Left"),
            ('2', "Facing Right", "Facing Right"),
            ('3', "Facing Backward", "Facing Backward"),
            ('4', "Facing Most Convenient Direction", "Facing Most Convenient Direction")
            ]
    elif atom_type == 4 or atom_type == 23 or atom_type == 24 or atom_type == 25:
        items = [
            ('0', "Idle Aim Weapon", "Idle Aim Weapon"),
            ('1', "Idle Turn Around", "Idle Turn Around"),
            ('2', "Idle Look With Head", "Idle Look With Head"),
            ('3', "Forced Exact Facing", "Forced Exact Facing"),
            ('4', "Forced Aim Weapon", "Forced Aim Weapon")
            ]
    elif atom_type == 5:
        items = [
            ('0', "Noncombat", "Noncombat"),
            ('1', "Asleep", "Asleep"),
            ('2', "Combat", "Combat"),
            ('3', "Panic", "Panic")
            ]
    elif atom_type == 6 or atom_type == 17 or atom_type == 18:
        items = [
            ('0', "Disable", "Disable"),
            ('1', "Enable", "Enable")
            ]
    elif atom_type == 8:
        items = [
            ('0', "Toss", "Toss"),
            ('1', "Lob", "Lob"),
            ('2', "Bounce", "Bounce")
            ]
    elif atom_type == 9:
        items = [
            ('0', "Any Non Driver", "Any Non Driver"),
            ('1', "Gunner", "Gunner"),
            ('2', "Passanger", "Passanger"),
            ('3', "Driver", "Driver"),
            ('4', "Any Seat", "Any Seat")
            ]
    elif atom_type == 13:
        items = [
            ('0', "Normal", "Normal"),
            ('1', "Absolute Movement", "Absolute Movement"),
            ('2', "Absolute Movement, No Collision", "Absolute Movement, No Collision"),
            ('3', "Normal, No Interpolation", "Normal, No Interpolation"),
            ('4', "Absolute Movement, No Interpolation", "Absolute Movement, No Interpolation"),
            ('5', "Absolute Movement, No Collision, No Interpolation", "Absolute Movement, No Collision, No Interpolation")
            ]
    elif atom_type == 15:
        items = [
            ('0', "Berserk", "Berserk"),
            ('1', "Surprise Front", "Surprise Front"),
            ('2', "Surprise Back", "Surprise Back"),
            ('3', "Evade Left", "Evade Left"),
            ('4', "Evade Right", "Evade Right"),
            ('5', "Dive Forward", "Dive Forward"),
            ('6', "Dive Back", "Dive Back"),
            ('7', "Dive Left", "Dive Left"),
            ('8', "Dive Right", "Dive Right"),
            ('9', "Vehicle Woohoo", "Vehicle Woohoo"),
            ('10', "Vehicle Scared", "Vehicle Scared")
            ]
    elif atom_type == 16:
        items = [
            ("0", "Idle Noncombat", "Idle Noncombat"),
            ("1", "Idle Combat", "Idle Combat"),
            ("2", "Unused 2", "Unused 2"),
            ("3", "Unused 3", "Unused 3"),
            ("4", "Unused 4", "Unused 4"),
            ("5", "Unused 5", "Unused 5"),
            ("6", "Pain Body Minor", "Pain Body Minor"),
            ("7", "Pain Body Major", "Pain Body Major"),
            ("8", "Pain Shield", "Pain Shield"),
            ("9", "Pain Falling", "Pain Falling"),
            ("10", "Scream Fear", "Scream Fear"),
            ("11", "Scream Pain", "Scream Pain"),
            ("12", "Maimed Limb", "Maimed Limb"),
            ("13", "Maimed Head", "Maimed Head"),
            ("14", "Death Quiet", "Death Quiet"),
            ("15", "Death Violent", "Death Violent"),
            ("16", "Death Falling", "Death Falling"),
            ("17", "Death Agonizing", "Death Agonizing"),
            ("18", "Death Instant", "Death Instant"),
            ("19", "Death Flying", "Death Flying"),
            ("20", "Unused 20", "Unused 20"),
            ("21", "Damaged Friend", "Damaged Friend"),
            ("22", "Damaged Friend Player", "Damaged Friend Player"),
            ("23", "Damaged Enemy", "Damaged Enemy"),
            ("24", "Damaged Enemy CM", "Damaged Enemy CM"),
            ("25", "Unused 25", "Unused 25"),
            ("26", "Unused 26", "Unused 26"),
            ("27", "Unused 27", "Unused 27"),
            ("28", "Unused 28", "Unused 28"),
            ("29", "Hurt Friend", "Hurt Friend"),
            ("30", "Hurt Friend RE", "Hurt Friend RE"),
            ("31", "Hurt Friend Player", "Hurt Friend Player"),
            ("32", "Hurt Enemy", "Hurt Enemy"),
            ("33", "Hurt Enemy RE", "Hurt Enemy RE"),
            ("34", "Hurt Enemy CM", "Hurt Enemy CM"),
            ("35", "Hurt Enemy Bullet", "Hurt Enemy Bullet"),
            ("36", "Hurt Enemy Needler", "Hurt Enemy Needler"),
            ("37", "Hurt Enemy Plasma", "Hurt Enemy Plasma"),
            ("38", "Hurt Enemy Sniper", "Hurt Enemy Sniper"),
            ("39", "Hurt Enemy Grenade", "Hurt Enemy Grenade"),
            ("40", "Hurt Enemy Explosion", "Hurt Enemy Explosion"),
            ("41", "Hurt Enemy Melee", "Hurt Enemy Melee"),
            ("42", "Hurt Enemy Flame", "Hurt Enemy Flame"),
            ("43", "Hurt Enemy Shotgun", "Hurt Enemy Shotgun"),
            ("44", "Hurt Enemy Vehicle", "Hurt Enemy Vehicle"),
            ("45", "Hurt Enemy Mounted Weapon", "Hurt Enemy Mounted Weapon"),
            ("46", "Unused 46", "Unused 46"),
            ("47", "Unused 47", "Unused 47"),
            ("48", "Unused 48", "Unused 48"),
            ("49", "Killed Friend", "Killed Friend"),
            ("50", "Killed Friend CM", "Killed Friend CM"),
            ("51", "Killed Friend Player", "Killed Friend Player"),
            ("52", "Killed Friend Player CM", "Killed Friend Player CM"),
            ("53", "Killed Enemy", "Killed Enemy"),
            ("54", "Killed Enemy CM", "Killed Enemy CM"),
            ("55", "Killed Enemy Player", "Killed Enemy Player"),
            ("56", "Killed Enemy Player CM", "Killed Enemy Player CM"),
            ("57", "Killed Enemy Covenant", "Killed Enemy Covenant"),
            ("58", "Killed Enemy Covenant CM", "Killed Enemy Covenant CM"),
            ("59", "Killed Enemy Floodcombat", "Killed Enemy Floodcombat"),
            ("60", "Killed Enemy Floodcombat CM", "Killed Enemy Floodcombat CM"),
            ("61", "Killed Enemy Floodcarrier", "Killed Enemy Floodcarrier"),
            ("62", "Killed Enemy Floodcarrier CM", "Killed Enemy Floodcarrier CM"),
            ("63", "Killed Enemy Sentinel", "Killed Enemy Sentinel"),
            ("64", "Killed Enemy Sentinel CM", "Killed Enemy Sentinel CM"),
            ("65", "Killed Enemy Bullet", "Killed Enemy Bullet"),
            ("66", "Killed Enemy Needler", "Killed Enemy Needler"),
            ("67", "Killed Enemy Plasma", "Killed Enemy Plasma"),
            ("68", "Killed Enemy Sniper", "Killed Enemy Sniper"),
            ("69", "Killed Enemy Grenade", "Killed Enemy Grenade"),
            ("70", "Killed Enemy Explosion", "Killed Enemy Explosion"),
            ("71", "Killed Enemy Melee", "Killed Enemy Melee"),
            ("72", "Killed Enemy Flame", "Killed Enemy Flame"),
            ("73", "Killed Enemy Shotgun", "Killed Enemy Shotgun"),
            ("74", "Killed Enemy Vehicle", "Killed Enemy Vehicle"),
            ("75", "Killed Enemy Mounted Weapon", "Killed Enemy Mounted Weapon"),
            ("76", "Killing Spree", "Killing Spree"),
            ("77", "Unused 77", "Unused 77"),
            ("78", "Unused 78", "Unused 78"),
            ("79", "Unused 79", "Unused 79"),
            ("80", "Player Kill CM", "Player Kill CM"),
            ("81", "Player Kill Bullet CM", "Player Kill Bullet CM"),
            ("82", "Player Kill Needler CM", "Player Kill Needler CM"),
            ("83", "Player Kill Plasma CM", "Player Kill Plasma CM"),
            ("84", "Player Kill Sniper CM", "Player Kill Sniper CM"),
            ("85", "Anyone Kill Grenade CM", "Anyone Kill Grenade CM"),
            ("86", "Player Kill Explosion CM", "Player Kill Explosion CM"),
            ("87", "Player Kill Melee CM", "Player Kill Melee CM"),
            ("88", "Player Kill Flame CM", "Player Kill Flame CM"),
            ("89", "Player Kill Shotgun CM", "Player Kill Shotgun CM"),
            ("90", "Player Kill Vehicle CM", "Player Kill Vehicle CM"),
            ("91", "Player Kill Mounted Weapon CM", "Player Kill Mounted Weapon CM"),
            ("92", "Player Killing Spree CM", "Player Killing Spree CM"),
            ("93", "Unused 93", "Unused 93"),
            ("94", "Unused 94", "Unused 94"),
            ("95", "Unused 95", "Unused 95"),
            ("96", "Friend Died", "Friend Died"),
            ("97", "Friend Player Died", "Friend Player Died"),
            ("98", "Friend Killed By Friend", "Friend Killed By Friend"),
            ("99", "Friend Killed By Friendly Player", "Friend Killed By Friendly Player"),
            ("100", "Friend Killed By Enemy", "Friend Killed By Enemy"),
            ("101", "Friend Killed By Enemy Player", "Friend Killed By Enemy Player"),
            ("102", "Friend Killed By Covenant", "Friend Killed By Covenant"),
            ("103", "Friend Killed By Flood", "Friend Killed By Flood"),
            ("104", "Friend Killed By Sentinel", "Friend Killed By Sentinel"),
            ("105", "Friend Betrayed", "Friend Betrayed"),
            ("106", "Unused 106", "Unused 106"),
            ("107", "Unused 107", "Unused 107"),
            ("108", "New Combat Alone", "New Combat Alone"),
            ("109", "New Enemy Recent Combat", "New Enemy Recent Combat"),
            ("110", "Old Enemy Sighted", "Old Enemy Sighted"),
            ("111", "Unexpected Enemy", "Unexpected Enemy"),
            ("112", "Dead Friend Found", "Dead Friend Found"),
            ("113", "Alliance Broken", "Alliance Broken"),
            ("114", "Alliance Reformed", "Alliance Reformed"),
            ("115", "Grenade Throwing", "Grenade Throwing"),
            ("116", "Grenade Startle", "Grenade Startle"),
            ("117", "Grenade Sighted", "Grenade Sighted"),
            ("118", "Grenade Danger Enemy", "Grenade Danger Enemy"),
            ("119", "Grenade Danger Self", "Grenade Danger Self"),
            ("120", "Grenade Danger Friend", "Grenade Danger Friend"),
            ("121", "Unused 121", "Unused 121"),
            ("122", "Unused 122", "Unused 122"),
            ("123", "New Combat Group RE", "New Combat Group RE"),
            ("124", "New Combat Nearby RE", "New Combat Nearby RE"),
            ("125", "Alert Friend", "Alert Friend"),
            ("126", "Alert Friend RE", "Alert Friend RE"),
            ("127", "Alert Lost Contact", "Alert Lost Contact"),
            ("128", "Alert Lost Contact RE", "Alert Lost Contact RE"),
            ("129", "Blocked Blocked RE", "Blocked Blocked RE"),
            ("130", "Search Start", "Search Start"),
            ("131", "Search Query", "Search Query"),
            ("132", "Search Query RE", "Search Query RE"),
            ("133", "Search Report", "Search Report"),
            ("134", "Search Abandon", "Search Abandon"),
            ("135", "Search Group Abandon", "Search Group Abandon"),
            ("136", "Uncover Start", "Uncover Start"),
            ("137", "Uncover Start RE", "Uncover Start RE"),
            ("138", "Advance", "Advance"),
            ("139", "Advance RE", "Advance RE"),
            ("140", "Retreat", "Retreat"),
            ("141", "Retreat RE", "Retreat RE"),
            ("142", "Cover", "Cover"),
            ("143", "Unused 143", "Unused 143"),
            ("144", "Unused 144", "Unused 144"),
            ("145", "Unused 145", "Unused 145"),
            ("146", "Sighted Friend Player", "Sighted Friend Player"),
            ("147", "Shooting", "Shooting"),
            ("148", "Shooting Vehicle", "Shooting Vehicle"),
            ("149", "Shooting Berserk", "Shooting Berserk"),
            ("150", "Shooting Group", "Shooting Group"),
            ("151", "Shooting Traitor", "Shooting Traitor"),
            ("152", "Taunt", "Taunt"),
            ("153", "Taunt RE", "Taunt RE"),
            ("154", "Flee", "Flee"),
            ("155", "Flee RE", "Flee RE"),
            ("156", "Flee Leader Died", "Flee Leader Died"),
            ("157", "Attempted Flee", "Attempted Flee"),
            ("158", "Attempted Flee RE", "Attempted Flee RE"),
            ("159", "Lost Contact", "Lost Contact"),
            ("160", "Hiding Finished", "Hiding Finished"),
            ("161", "Vehicle Entry", "Vehicle Entry"),
            ("162", "Vehicle Exit", "Vehicle Exit"),
            ("163", "Vehicle Woohoo", "Vehicle Woohoo"),
            ("164", "Vehicle Scared", "Vehicle Scared"),
            ("165", "Vehicle Collision", "Vehicle Collision"),
            ("166", "Partially Sighted", "Partially Sighted"),
            ("167", "Nothing There", "Nothing There"),
            ("168", "Pleading", "Pleading"),
            ("169", "Unused 169", "Unused 169"),
            ("170", "Unused 170", "Unused 170"),
            ("171", "Unused 171", "Unused 171"),
            ("172", "Unused 172", "Unused 172"),
            ("173", "Surprise", "Surprise"),
            ("174", "Berserk", "Berserk"),
            ("175", "Melee Attack", "Melee Attack"),
            ("176", "Dive", "Dive"),
            ("177", "Uncover Leap", "Uncover Leap"),
            ("178", "Leap Attack", "Leap Attack"),
            ("179", "Resurrection", "Resurrection")
            ]
    elif atom_type == 19:
        items = [
            ('0', "Until Alerted", "Until Alerted"),
            ('1', "Until Visible Enemy", "Until Visible Enemy"),
            ('2', "Until Told To Advance", "Until Told To Advance")
            ]
    elif atom_type == 20:
        items = [
            ('0', "Always", "Always"),
            ('1', "Only Until Told To Advance", "Only Until Told To Advance")
            ]
    elif atom_type == 21:
        items = [
            ('0', "Normally", "Normally"),
            ('1', "Silently", "Silently")
            ]
    elif atom_type == 22:
        items = [
            ('0', "Facing Forward", "Facing Forward"),
            ('1', "Facing Left", "Facing Left"),
            ('2', "Facing Right", "Facing Right"),
            ('3', "Facing Backward", "Facing Backward")
            ]

    return items

def get_atom_type(self):
    return self.get("atom_type", "")

def set_atom_type(self, value):
    self["atom_type"] = value
    self["atom_modifier"] = 0
    self["atom_modifier_ui"] = 0

def get_atom_modifier(self):
    return self.get("atom_modifier", "")

def set_atom_modifier(self, value):
    self["atom_modifier"] = int(value)
    self["atom_modifier_ui"] = value

def get_group_list(value):
    group_list = []
    for char in value:
        char = char.upper()
        if char.isalpha() and not char in group_list:
            group_list.append(char)

    group_list.sort()

    return group_list

def get_attacking_groups(self):
    return self.get("attacking_groups", "")

def set_attacking_groups(self, value):
    self["attacking_groups"] = ''.join(get_group_list(value))

def get_attacking_search_groups(self):
    return self.get("attacking_search_groups", "")

def set_attacking_search_groups(self, value):
    self["attacking_search_groups"] = ''.join(get_group_list(value))

def get_attacking_guard_groups(self):
    return self.get("attacking_guard_groups", "")

def set_attacking_guard_groups(self, value):
    self["attacking_guard_groups"] = ''.join(get_group_list(value))

def get_defending_groups(self):
    return self.get("defending_groups", "")

def set_defending_groups(self, value):
    self["defending_groups"] = ''.join(get_group_list(value))

def get_defending_search_groups(self):
    return self.get("defending_search_groups", "")

def set_defending_search_groups(self, value):
    self["defending_search_groups"] = ''.join(get_group_list(value))

def get_defending_guard_groups(self):
    return self.get("defending_guard_groups", "")

def set_defending_guard_groups(self, value):
    self["defending_guard_groups"] = ''.join(get_group_list(value))

def get_pursuing_groups(self):
    return self.get("pursuing_groups", "")

def set_pursuing_groups(self, value):
    self["pursuing_groups"] = ''.join(get_group_list(value))

class Scenario_SceneProps(Panel):
    bl_label = "Tag Scene Properties"
    bl_idname = "HALO_PT_ScenarioTag"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenePropertiesPanel"

    def draw(self, context):
        scene = context.scene

        layout = self.layout
        scenario = context.scene.tag_scenario

        col = layout.column(align=True)
        row = col.row()
        row.label(text='Scenario Path:')
        row.prop(scenario, "scenario_path", text='')
        row = col.row()
        row.label(text='Global Lightmap Multiplier:')
        row.prop(scenario, "global_lightmap_multiplier", text='')
        row = col.row()
        row.label(text='H2V Scenario:')
        row.prop(scenario, "is_h2v", text='')
        row = col.row()
        row.prop_search(scenario, 'dont_use', scene, 'tag_palatte')
        row = col.row()
        row.prop_search(scenario, 'wont_use', scene, 'tag_palatte')
        row = col.row()
        row.prop_search(scenario, 'cant_use', scene, 'tag_palatte')
        row = col.row()
        row.label(text='Scenario Type:')
        row.prop(scenario, "scenario_type_enum", text='')

        box_flags = layout.box()
        box_flags.label(text="Flags")
        col_flags = box_flags.column(align=True)
        row_flags = col_flags.row()
        row_flags.prop(scenario, "cortana_hack")
        row_flags = col_flags.row()
        row_flags.prop(scenario, "use_demo_ui")
        row_flags = col_flags.row()
        row_flags.prop(scenario, "color_correction")
        row_flags = col_flags.row()
        row_flags.prop(scenario, "disable_tag_patches")

        box = layout.split()
        col = box.column(align=True)
        row = col.row()
        row.label(text='Local North:')
        row.prop(scenario, "local_north", text='')
        row = col.row()
        row.prop_search(scenario, 'custom_object_names', scene, 'tag_palatte')
        row = col.row()
        row.prop_search(scenario, 'ingame_help_text', scene, 'tag_palatte')
        row = col.row()
        row.prop_search(scenario, 'hud_messages', scene, 'tag_palatte')

class HaloScenarioPropertiesGroup(PropertyGroup):
    scenario_path: StringProperty(
            name = "Scenario Path",
            description="Where to place the generated scenario file for this level",
            default="",
            maxlen=1024,
            subtype='FILE_PATH'
    )

    global_lightmap_multiplier: IntProperty(
        name="Global Lightmap Multiplier",
        description="Takes lightmap resolution for each image and multiplies it by set value",
        default=1,
        min=1
    )

    is_h2v: BoolProperty(
        name ="Is H2V",
        description = "Generates a bitmap for H2V if set. If not set then it's for MCC",
        default = False,
    )

    dont_use: StringProperty(
        name = "Dont Use",
        description = "Unused structure_bsp tag reference"
        )

    wont_use: StringProperty(
        name = "Wont Use",
        description = "Unused structure_bsp tag reference"
        )

    cant_use: StringProperty(
        name = "Cant Use",
        description = "Unused sky tag reference"
        )

    scenario_type_enum: EnumProperty(
        name="Scenario Type",
        description="The type of scenario",
        items=( ('0', "Solo", "Solo"),
                ('1', "Multiplayer", "Multiplayer"),
                ('2', "Main Menu", "Main Menu")
            )
        )

    cortana_hack: BoolProperty(
        name ="Cortana Hack",
        description = "Sort Cortana in front of other transparent geometry",
        default = False,
        )

    use_demo_ui: BoolProperty(
        name ="Use Demo UI",
        description = "Use alternate UI collection for the demo",
        default = False,
        )

    color_correction: BoolProperty(
        name ="Color Correction",
        description = "Enable NTSC to SRGB color space conversion",
        default = False,
        )

    disable_tag_patches: BoolProperty(
        name="Do Not Apply Bungie Campaign Tag Patches",
        description="Inhibit the hard coded balance patch changes made specific for original campaign maps",
        default = False,
        )

    local_north: FloatProperty(
        name="Local North",
        description="The direction the compass will point to for north",
        subtype="ANGLE"
        )

    custom_object_names: StringProperty(
        name = "Custom Object Names",
        description = "A unicode_string tag reference"
        )

    ingame_help_text: StringProperty(
        name = "Ingame Help Text",
        description = "A unicode_string tag reference"
        )

    hud_messages: StringProperty(
        name = "HUD Messages",
        description = "A hud_message tag reference"
        )

class HaloGeometryPropertiesGroup(PropertyGroup):
    lightmap_index: IntProperty(
        name = "Lightmap Index",
        description = "What index do we use in the referenced lightmap tag. Try not to edit this manually",
        default = -1
        )

    image_multiplier: IntProperty(
        name="Image Multiplier",
        description="Takes image resolution for the mesh and multiplies it by set value",
        default=1,
        min=1
    )

    instance_lightmap_policy_enum: EnumProperty(
        name="Lightmap Policy",
        description="Determines how the object is lit.",
        items=( ('0', "Per Pixel", "Object uses baked lighting"),
                ('1', "Per Vertex", "Object uses vertex lighting")
            )
        )

class HaloSkyPropertiesGroup(PropertyGroup):
    sky_path: StringProperty(
        name = "Sky Path",
        description = "A sky tag reference"
        )

class HaloObjectPropertiesGroup(PropertyGroup):
    tag_path: StringProperty(
        name = "Tag Path",
        description = "An object tag reference"
        )

    object_name: StringProperty(
        name = "Object Name",
        description = "Set the script name for the object"
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
        description = "???",
        default = False,
        )

    desired_permutation: IntProperty(
        name = "Desired Permutation",
        description = "What permutation to use for the object"
        )

    appearance_player_index: IntProperty(
        name = "Appearance Player Index",
        description = "???"
        )

class HaloUnitPropertiesGroup(PropertyGroup):
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
        description="???",
        )

    slayer_default: BoolProperty(
        name ="Slayer Default",
        description = "???",
        default = False,
        )

    ctf_default: BoolProperty(
        name ="CTF Default",
        description = "???",
        default = False,
        )

    king_default: BoolProperty(
        name ="King Default",
        description = "???",
        default = False,
        )

    oddball_default: BoolProperty(
        name ="Oddball Default",
        description = "???",
        default = False,
        )

    unused_0: BoolProperty(
        name ="Unused 0",
        description = "???",
        default = False,
        )

    unused_1: BoolProperty(
        name ="Unused 1",
        description = "???",
        default = False,
        )

    unused_2: BoolProperty(
        name ="Unused 2",
        description = "???",
        default = False,
        )

    unused_3: BoolProperty(
        name ="Unused 3",
        description = "???",
        default = False,
        )

    slayer_allowed: BoolProperty(
        name ="Slayer Allowed",
        description = "???",
        default = False,
        )

    ctf_allowed: BoolProperty(
        name ="CTF Allowed",
        description = "???",
        default = False,
        )

    king_allowed: BoolProperty(
        name ="King Allowed",
        description = "???",
        default = False,
        )

    oddball_allowed: BoolProperty(
        name ="Oddball Allowed",
        description = "???",
        default = False,
        )

    unused_4: BoolProperty(
        name ="Unused 4",
        description = "???",
        default = False,
        )

    unused_5: BoolProperty(
        name ="Unused 5",
        description = "???",
        default = False,
        )

    unused_6: BoolProperty(
        name ="Unused 6",
        description = "???",
        default = False,
        )

    unused_7: BoolProperty(
        name ="Unused 7",
        description = "???",
        default = False,
        )

class HaloItemPropertiesGroup(PropertyGroup):
    initially_at_rest: BoolProperty(
        name ="Initially At Rest",
        description = "Doesn't Fall",
        default = False,
        )
    obsolete: BoolProperty(
        name ="Obsolete",
        description = "???",
        default = False,
        )

    does_accelerate: BoolProperty(
        name ="Does Accelerate",
        description = "Affected by physics such as explosives.",
        default = False,
        )

class HaloWeaponPropertiesGroup(PropertyGroup):
    rounds_left: IntProperty(
        name = "Rounds Left",
        description = "How many rounds left in reserve"
        )

    rounds_loaded: IntProperty(
        name = "Round Loaded",
        description = "How many rounds in the clip"
        )

class HaloDevicePropertiesGroup(PropertyGroup):
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

class HaloMachinePropertiesGroup(PropertyGroup):
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

class HaloControlPropertiesGroup(PropertyGroup):
    usable_from_both_sides: BoolProperty(
        name ="Usable From Both Sides",
        description = "Control ignores forward vector",
        default = False,
        )

    control_value: IntProperty(
        name = "Unknown",
        description = "???",
        )

class HaloLightFixturePropertiesGroup(PropertyGroup):
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
        description="???",
        subtype="ANGLE"
        )

    cutoff_angle: FloatProperty(
        name="Cutoff Angle",
        description="???",
        subtype="ANGLE"
        )

class HaloPlayerStartingLocationPropertiesGroup(PropertyGroup):
    team_index: IntProperty(
        name = "Team Index",
        description = "Team index",
        min = 0
        )
    
    bsp_index: IntProperty(
        name = "BSP Index",
        description = "BSP index",
        default=-1,
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

class HaloNetgameFlagsPropertiesGroup(PropertyGroup):
    netgame_type: EnumProperty(
        name="Type",
        description="Type",
        items = ( ('0', "CTF - Flag", "CTF - Flag"),
                    ('1', "Unused1", "Unused1"),
                    ('2', "Oddball - Ball Spawn", "Oddball - Ball Spawn"),
                    ('3', "Race - Track", "Race - Track"),
                    ('4', "Race - Vehicle", "Race - Vehicle"),
                    ('5', "Unused5", "Unused5"),
                    ('6', "Teleport From", "Teleport From"),
                    ('7', "Teleport To", "Teleport To"),
                    ('8', "Hill - Flag", "Hill - Flag"),
                )
        )

    usage_id: IntProperty(
        name = "Usage ID",
        description = "Usage ID",
        min = 0
        )
    
    weapon_group: StringProperty(
        name = "Weapon Group",
        description = "Set the tag reference for the object"
        )

class HaloNetgameEquipmentPropertiesGroup(PropertyGroup):
    levitate: BoolProperty(
        name ="Levitate",
        description = "Levitate",
        default = False,
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

    team_index: IntProperty(
        name = "Team Index",
        description = "Team index",
        min = 0
        )

    spawn_time: IntProperty(
        name="Spawn Time",
        description="Spawn Time"
        )

    item_collection: StringProperty(
        name = "Item Collection",
        description = "Set the tag reference for the element"
        )

class HaloCollectionPropertiesGroup(PropertyGroup):
    parent: PointerProperty(
        name="Parent", 
        type=bpy.types.Collection
        )

class HaloEncounterPropertiesGroup(PropertyGroup):
    name: StringProperty(
        name = "Name",
        description = "Set the name for the element"
        )

    not_initially_created: BoolProperty(
        name ="Not Initially Created",
        description = "???",
        default = False,
        )

    respawn_enabled: BoolProperty(
        name ="Respawn Enabled",
        description = "???",
        default = False,
        )

    initially_blind: BoolProperty(
        name ="Initially Blind",
        description = "???",
        default = False,
        )

    initially_deaf: BoolProperty(
        name ="Initially Deaf",
        description = "???",
        default = False,
        )

    initially_braindead: BoolProperty(
        name ="Initially Braindead",
        description = "???",
        default = False,
        )

    firing_positions: BoolProperty(
        name ="Firing Positions 3D",
        description = "???",
        default = False,
        )

    manual_bsp_index_specified: BoolProperty(
        name ="Manual BSP Index Specified",
        description = "???",
        default = False,
        )

    team_index: EnumProperty(
        name="Team Index",
        description="???",
        items=( ('0', "Default By Unit", "Default By Unit"),
                ('1', "Player", "Player"),
                ('2', "Human", "Human"),
                ('3', "Covenant", "Covenant"),
                ('4', "Flood", "Flood"),
                ('5', "Sentinel", "Sentinel"),
                ('6', "Unused 6", "Unused 6"),
                ('7', "Unused 7", "Unused 7"),
                ('8', "Unused 8", "Unused 8"),
                ('9', "Unused 9", "Unused 9")
            )
        )

    search_behavior: EnumProperty(
        name="Search Behavior",
        description="???",
        items=( ('0', "Normal", "Normal"),
                ('1', "Never", "Never"),
                ('2', "Tenacious", "Tenacious")
            )
        )

    manual_bsp_index: IntProperty(
        name = "Manual BSP Index",
        description = "???",
        default=-1,
        min = -1
        )

    respawn_delay_min: FloatProperty(
        name="Respawn Delay Min",
        description="???"
        )

    respawn_delay_max: FloatProperty(
        name="Respawn Delay Max",
        description="???"
        )

class HaloSquadPropertiesGroup(PropertyGroup):
    name: StringProperty(
        name = "Name",
        description = "Set the name for the element"
        )

    actor_type: StringProperty(
        name = "Actor Type",
        description = "???"
        )

    platoon: PointerProperty(
        name="Platoon", 
        type=bpy.types.Collection
        )

    initial_state: EnumProperty(
        name="Initial State",
        description="???",
        items=state_items
        )

    return_state: EnumProperty(
        name="Return State",
        description="???",
        items=state_items
        )

    unused: BoolProperty(
        name ="Unused",
        description = "???",
        default = False,
        )

    never_search: BoolProperty(
        name ="Never Search",
        description = "???",
        default = False,
        )

    start_timer_immediately: BoolProperty(
        name ="Start Timer Immediately",
        description = "???",
        default = False,
        )

    no_timer_delay_forever: BoolProperty(
        name ="No Timer Delay Forever",
        description = "???",
        default = False,
        )

    magic_sight_after_timer: BoolProperty(
        name ="Magic Sight After Timer",
        description = "???",
        default = False,
        )

    automatic_migration: BoolProperty(
        name ="Automatic Migration",
        description = "???",
        default = False,
        )

    unique_leader_type: EnumProperty(
        name="Unique Leader Type",
        description="???",
        items=( ('0', "Normal", "Normal"),
                ('1', "NONE", "NONE"),
                ('2', "Random", "Random"),
                ('3', "SGT Johnson", "SGT Johnson"),
                ('4', "SGT Lehto", "SGT Lehto")
            )
        )

    maneuver_to_squad: PointerProperty(
        name="Maneuver To Squad", 
        type=bpy.types.Collection
        )

    squad_delay_time: FloatProperty(
        name="Squad Delay Time",
        description="???"
        )

    attacking_groups: StringProperty(
        name = "Attacking",
        description = "???",
        get=get_attacking_groups,
        set=set_attacking_groups
        )

    attacking_search_groups: StringProperty(
        name = "Attacking Search",
        description = "???",
        get=get_attacking_search_groups,
        set=set_attacking_search_groups
        )
    
    attacking_guard_groups: StringProperty(
        name = "Attacking Search",
        description = "???",
        get=get_attacking_guard_groups,
        set=set_attacking_guard_groups
        )
    
    defending_groups: StringProperty(
        name = "Defending",
        description = "???",
        get=get_defending_groups,
        set=set_defending_groups
        )

    defending_search_groups: StringProperty(
        name = "Defending Search",
        description = "???",
        get=get_defending_search_groups,
        set=set_defending_search_groups
        )
    
    defending_guard_groups: StringProperty(
        name = "Defending Search",
        description = "???",
        get=get_defending_guard_groups,
        set=set_defending_guard_groups
        )

    pursuing_groups: StringProperty(
        name = "Pursuing",
        description = "???",
        get=get_pursuing_groups,
        set=set_pursuing_groups
        )

    normal_diff_count: IntProperty(
        name="Normal Difficulty Count",
        description="Spawn Time"
        )
    
    insane_diff_count: IntProperty(
        name="Insane Difficulty Count",
        description="Spawn Time"
        )

    major_upgrade: EnumProperty(
        name="Major Upgrade",
        description="???",
        items=( ('0', "Normal", "Normal"),
                ('1', "Few", "Few"),
                ('2', "Many", "Many"),
                ('3', "NONE", "NONE"),
                ('4', "All", "All")
            )
        )

    respawn_min_actors: IntProperty(
        name="Respawn Minimum Actors",
        description="???"
        )
    
    respawn_max_actors: IntProperty(
        name="Respawn Maximum Actors",
        description="???"
        )

    respawn_total: IntProperty(
        name="Respawn Total",
        description="???"
        )

    respawn_delay_min: FloatProperty(
        name="Respawn Delay Min",
        description="???"
        )

    respawn_delay_max: FloatProperty(
        name="Respawn Delay Max",
        description="???"
        )

class HaloMovePositionPropertiesGroup(PropertyGroup):
    weight: FloatProperty(
        name="Weight",
        description="???"
        )

    time_min: FloatProperty(
        name="Time Minimum",
        description="???"
        )

    time_max: FloatProperty(
        name="Time Maximum",
        description="???"
        )

    animation_index: IntProperty(
        name="Animation",
        description="???"
        )

    sequence_id: IntProperty(
        name="Sequence ID",
        description="???"
        )

    surface_index: IntProperty(
        name="Surface Index",
        description="???"
        )
    
class HaloStartingLocationPropertiesGroup(PropertyGroup):
    sequence_id: IntProperty(
        name="Sequence ID",
        description="???"
        )

    required: BoolProperty(
        name ="Unused",
        description = "???",
        default = False,
        )

    initial_state: EnumProperty(
        name="Initial State",
        description="???",
        items=state_items
        )

    return_state: EnumProperty(
        name="Return State",
        description="???",
        items=state_items
        )

    actor_type: StringProperty(
        name = "Actor Type",
        description = "???"
        )

    command_list: PointerProperty(
        name="Command List", 
        type=bpy.types.Collection
        )

class HaloPlatoonPropertiesGroup(PropertyGroup):
    name: StringProperty(
        name = "Name",
        description = "Set the name for the element"
        )

    flee_when_maneuvering: BoolProperty(
        name ="Flee When Maneuvering",
        description = "???",
        default = False,
        )

    say_advancing_when_maneuver: BoolProperty(
        name="Say Advancing When Maneuver",
        description = "???",
        default = False,
        )

    start_in_defending_state: BoolProperty(
        name ="Start In Defending State",
        description = "???",
        default = False,
        )
    
    state_items=( ('0', "Never", "Never"),
                ('1', "Less 75 Percent Strength", "Less 75 Percent Strength"),
                ('2', "Less 50 Percent Strength", "Less 50 Percent Strength"),
                ('3', "Less 25 Percent Strength", "Less 25 Percent Strength"),
                ('4', "Anybody Dead", "Anybody Dead"),
                ('5', "25 Percent Dead", "25 Percent Dead"),
                ('6', "50 Percent Dead", "50 Percent Dead"),
                ('7', "75 Percent Dead", "75 Percent Dead"),
                ('8', "All But One Dead", "All But One Dead"),
                ('9', "All Dead", "All Dead"))

    change_attacking_defending_state: EnumProperty(
        name="Change Attacking/Defending State",
        description="???",
        items=state_items
        )

    happens_to_a: PointerProperty(
        name="Happens To A", 
        type=bpy.types.Collection
        )

    maneuver_when: EnumProperty(
        name="Maneuver When",
        description="???",
        items=state_items
        )

    happens_to_b: PointerProperty(
        name="Happens To B", 
        type=bpy.types.Collection
        )

class HaloFiringPositionPropertiesGroup(PropertyGroup):
    group_index: EnumProperty(
        name="Group Index",
        description="???",
        items=( ('0', "A", "A"),
                ('1', "B", "B"),
                ('2', "C", "C"),
                ('3', "D", "D"),
                ('4', "E", "E"),
                ('5', "F", "F"),
                ('6', "G", "G"),
                ('7', "H", "H"),
                ('8', "I", "I"),
                ('9', "J", "J"),
                ('10', "K", "K"),
                ('11', "L", "L"),
                ('12', "M", "M"),
                ('13', "N", "N"),
                ('14', "O", "O"),
                ('15', "P", "P"),
                ('16', "Q", "Q"),
                ('17', "R", "R"),
                ('18', "S", "S"),
                ('19', "T", "T"),
                ('20', "U", "U"),
                ('21', "V", "V"),
                ('22', "W", "W"),
                ('23', "X", "X"),
                ('24', "Y", "Y"),
                ('25', "Z", "Z"))
        )

class HaloDecalPropertiesGroup(PropertyGroup):
    decal_type: StringProperty(
        name = "Decal Type",
        description = "???"
        )

    yaw: IntProperty(
        name="Yaw",
        description="???"
        )
    
    pitch: IntProperty(
        name="Pitch",
        description="???"
        )

class HaloCommandListPropertiesGroup(PropertyGroup):
    name: StringProperty(
        name = "Name",
        description = "???"
        )

    allow_initiative: BoolProperty(
        name ="Allow Initiative",
        description = "???",
        default = False,
        )

    allow_targeting: BoolProperty(
        name="Allow Targeting",
        description = "???",
        default = False,
        )

    disable_looking: BoolProperty(
        name ="Disable Looking",
        description = "???",
        default = False,
        )

    disable_communication: BoolProperty(
        name ="Disable Communication",
        description = "???",
        default = False,
        )

    disable_falling_damage: BoolProperty(
        name="Disable Falling Damage",
        description = "???",
        default = False,
        )

    manual_bsp_index_flag: BoolProperty(
        name ="Manual BSP Index",
        description = "???",
        default = False,
        )
    
    manual_bsp_index: IntProperty(
        name = "Manual BSP Index",
        description = "???",
        default=-1,
        min = -1
        )

class HaloCommandPropertiesGroup(PropertyGroup):
    atom_type: EnumProperty(
        name="Atom Type",
        description="???",
        items=( ('0', "Pause", "Pause"),
                ('1', "Go To", "Go To"),
                ('2', "Go To And Face", "Go To And Face"),
                ('3', "Move In Direction", "Move In Direction"),
                ('4', "Look", "Look"),
                ('5', "Animation Mode", "Animation Mode"),
                ('6', "Crouch", "Crouch"),
                ('7', "Shoot", "Shoot"),
                ('8', "Grenade", "Grenade"),
                ('9', "Vehicle", "Vehicle"),
                ('10', "Running Jump", "Running Jump"),
                ('11', "Targeted Jump", "Targeted Jump"),
                ('12', "Script", "Script"),
                ('13', "Animate", "Animate"),
                ('14', "Recording", "Recording"),
                ('15', "Action", "Action"),
                ('16', "Vocalize", "Vocalize"),
                ('17', "Targeting", "Targeting"),
                ('18', "Initiative", "Initiative"),
                ('19', "Wait", "Wait"),
                ('20', "Loop", "Loop"),
                ('21', "Die", "Die"),
                ('22', "Move Immediate", "Move Immediate"),
                ('23', "Look Random", "Look Random"),
                ('24', "Look Player", "Look Player"),
                ('25', "Look Object", "Look Object"),
                ('26', "Set Radius", "Set Radius"),
                ('27', "Teleport", "Teleport")
                ),
        get=get_atom_type,
        set=set_atom_type
    )

    atom_modifier: IntProperty(
        name = "Atom Modifier",
        description = "???"
        )

    atom_modifier_ui: EnumProperty(
        name = "Atom Modifier",
        description = "???",
        items=atom_modifier_callback,
        get=get_atom_modifier,
        set=set_atom_modifier
        )

    parameter_1: FloatProperty(
        name="Parameter 1",
        description="???"
        )

    parameter_2: FloatProperty(
        name="Parameter 2",
        description="???"
        )

    point_1: PointerProperty(
        name="Point 1", 
        type=bpy.types.Object
        )

    point_2: PointerProperty(
        name="Point 2", 
        type=bpy.types.Object
        )

    animation_index: IntProperty(
        name = "Animation Index",
        description = "???",
        )

    script_index: IntProperty(
        name = "Script Index",
        description = "???",
        )

    recording_index: IntProperty(
        name = "Recording Index",
        description = "???",
        )

    command_index: PointerProperty(
        name="Command", 
        type=bpy.types.Collection
        )

    object_name: StringProperty(
        name = "Object Name",
        description = "Set the reference name for the command"
        )

class HaloCutsceneFlagGroup(PropertyGroup):
    name: StringProperty(
        name = "Name",
        description = "???"
        )

class HaloCutsceneCameraGroup(PropertyGroup):
    name: StringProperty(
        name = "Name",
        description = "???"
        )
    
class HaloCutsceneTitleGroup(PropertyGroup):
    name: StringProperty(
        name = "Name",
        description = "???"
        )
    
    top_bound: IntProperty(
        name = "Top Bound",
        description = "???",
        )
    
    left_bound: IntProperty(
        name = "Left Bound",
        description = "???",
        )
    
    bottom_bound: IntProperty(
        name = "Bottom Bound",
        description = "???",
        )
    
    right_bound: IntProperty(
        name = "Right Bound",
        description = "???",
        )
    
    string_index: IntProperty(
        name = "String Index",
        description = "???",
        )
    
    style: EnumProperty(
        name="Style",
        description="???",
        items=( ('0', "Plain", "Plain"),
                ('1', "Bold", "Bold"),
                ('2', "Italics", "Italics"),
                ('3', "Condensed", "Condensed"),
                ('4', "Underlined", "Underlined")
                )
    )

    justification: EnumProperty(
        name="Style",
        description="???",
        items=( ('0', "Left", "Left"),
                ('1', "Right", "Right"),
                ('2', "Center", "Center")
                )
    )

    wrap_horizontally: BoolProperty(
        name ="Wrap Horizontally",
        description = "???",
        default = False,
        )

    wrap_vertically: BoolProperty(
        name ="Wrap Vertically",
        description = "???",
        default = False,
        )

    center_vertically: BoolProperty(
        name ="Center Vertically",
        description = "???",
        default = False,
        )

    bottom_justify: BoolProperty(
        name ="Bottom Justify",
        description = "???",
        default = False,
        )

    text_color: FloatVectorProperty(
        name = "Text Color",
        subtype='COLOR', 
        size=4,
        description="???"
        )

    shadow_color: FloatVectorProperty(
        name = "Shadow Color",
        subtype='COLOR', 
        size=4,
        description="???"
        )

    fade_in_time: FloatProperty(
        name="Fade In Time",
        description="???"
        )

    up_time: FloatProperty(
        name="Up time",
        description="???"
        )

    fade_out_time: FloatProperty(
        name="Fade Out Time",
        description="???"
        )

def render_cluster(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Lightmap Index:')
    row.prop(active_item.tag_mesh, "lightmap_index", text='')

def render_instance(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Lightmap Policy:')
    row.prop(active_item.tag_mesh, "instance_lightmap_policy_enum", text='')

def render_sky(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.prop_search(active_item.tag_sky, 'sky_path', scene, 'tag_palatte')

def render_object(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.prop_search(active_item.tag_object, 'tag_path', scene, 'tag_palatte')

    row = col.row()
    row.prop_search(active_item.tag_object, 'object_name', scene, 'object_names')

    box_flags = layout.box()
    box_flags.label(text="Not Placed")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_object, "automatically")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_object, "on_easy")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_object, "on_normal")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_object, "on_hard")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_object, "use_player_appearance")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Desired Permutation')
    row.prop(active_item.tag_object, "desired_permutation", text='')

def render_scenery(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(active_item.tag_object, "appearance_player_index", text='')

def render_unit(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(active_item.tag_object, "appearance_player_index", text='')
    row = col.row()
    row.label(text='Vitality')
    row.prop(active_item.tag_unit, "unit_vitality", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "unit_dead")

def render_vehicle(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Multiplayer Team Index')
    row.prop(active_item.tag_unit, "multiplayer_team_index", text='')

    box_flags = layout.box()
    box_flags.label(text="Multiplayer Spawn Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "slayer_default")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "ctf_default")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "king_default")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "oddball_default")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "unused_0")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "unused_1")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "unused_2")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "unused_3")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "slayer_allowed")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "ctf_allowed")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "king_allowed")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "oddball_allowed")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "unused_4")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "unused_5")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "unused_6")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_unit, "unused_7")

def render_equipment(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)

    box_flags = layout.box()
    box_flags.label(text="Misc Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_item, "initially_at_rest")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_item, "obsolete")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_item, "does_accelerate")

    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(active_item.tag_object, "appearance_player_index", text='')

def render_weapon(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(active_item.tag_object, "appearance_player_index", text='')
    row = col.row()
    row.label(text='Rounds Left')
    row.prop(active_item.tag_weapon, "rounds_left", text='')
    row = col.row()
    row.label(text='Rounds Loaded')
    row.prop(active_item.tag_weapon, "rounds_loaded", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_item, "initially_at_rest")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_item, "obsolete")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_item, "does_accelerate")

def render_device(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Appearance Player Index')
    row.prop(active_item.tag_object, "appearance_player_index", text='')
    row = col.row()
    row.label(text='Power Group')
    row.prop(active_item.tag_device, "power_group", text='')
    row = col.row()
    row.label(text='Position Group')
    row.prop(active_item.tag_device, "position_group", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_device, "initially_open")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_device, "initially_off")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_device, "can_change_only_once")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_device, "position_reversed")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_device, "not_usable_from_any_side")

def render_machine(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_machine, "does_not_operate_automatically")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_machine, "one_sided")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_machine, "never_appears_locked")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_machine, "opened_by_melee_attack")

def render_control(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_control, "usable_from_both_sides")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.prop(active_item.tag_control, "control_value")

def render_light_fixture(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Color')
    row.prop(active_item.tag_light_fixture, "color", text='')
    row = col.row()
    row.label(text='Intensity')
    row.prop(active_item.tag_light_fixture, "intensity", text='')
    row = col.row()
    row.label(text='Falloff Angle')
    row.prop(active_item.tag_light_fixture, "falloff_angle", text='')
    row = col.row()
    row.label(text='Cutoff Angle')
    row.prop(active_item.tag_light_fixture, "cutoff_angle", text='')

def render_player_starting_location(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Team Index')
    row.prop(active_item.tag_player_starting_location, "team_index", text='')
    row = col.row()
    row.label(text='BSP Index')
    row.prop(active_item.tag_player_starting_location, "bsp_index", text='')
    row = col.row()
    row.label(text='Type 0')
    row.prop(active_item.tag_player_starting_location, "type_0", text='')
    row = col.row()
    row.label(text='Type 1')
    row.prop(active_item.tag_player_starting_location, "type_1", text='')
    row = col.row()
    row.label(text='Type 2')
    row.prop(active_item.tag_player_starting_location, "type_2", text='')
    row = col.row()
    row.label(text='Type 3')
    row.prop(active_item.tag_player_starting_location, "type_3", text='')

def render_netgame_flags(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Type')
    row.prop(active_item.tag_netgame_flag, "netgame_type", text='')
    row = col.row()
    row.label(text='Usage ID')
    row.prop(active_item.tag_netgame_flag, "usage_id", text='')
    row = col.row()
    row.prop_search(active_item.tag_netgame_flag, 'weapon_group', scene, 'tag_palatte')

def render_netgame_equipment(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_netgame_equipment, "levitate")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Type 0')
    row.prop(active_item.tag_netgame_equipment, "type_0", text='')
    row = col.row()
    row.label(text='Type 1')
    row.prop(active_item.tag_netgame_equipment, "type_1", text='')
    row = col.row()
    row.label(text='Type 2')
    row.prop(active_item.tag_netgame_equipment, "type_2", text='')
    row = col.row()
    row.label(text='Type 3')
    row.prop(active_item.tag_netgame_equipment, "type_3", text='')
    row = col.row()
    row.label(text='Team Index')
    row.prop(active_item.tag_netgame_equipment, "team_index", text='')
    row = col.row()
    row.label(text='Spawn Time')
    row.prop(active_item.tag_netgame_equipment, "spawn_time", text='')
    row = col.row()
    row.prop_search(active_item.tag_netgame_equipment, 'item_collection', scene, 'tag_palatte')

def render_collection(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Parent')
    row.prop(active_item.tag_collection, "parent", text='')

def render_decal(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.prop_search(active_item.tag_decal, 'decal_type', scene, 'tag_palatte')
    row = col.row()
    row.label(text='Yaw')
    row.prop(active_item.tag_decal, "yaw", text='')
    row = col.row()
    row.label(text='Pitch')
    row.prop(active_item.tag_decal, "pitch", text='')

def render_encounter(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Name')
    row.prop(active_item.tag_encounter, "name", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_encounter, "not_initially_created")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_encounter, "respawn_enabled")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_encounter, "initially_blind")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_encounter, "initially_deaf")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_encounter, "initially_braindead")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_encounter, "firing_positions")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_encounter, "manual_bsp_index_specified")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Team Index')
    row.prop(active_item.tag_encounter, "team_index", text='')
    row = col.row()
    row.label(text='Search Behavior')
    row.prop(active_item.tag_encounter, "search_behavior", text='')
    row = col.row()
    row.label(text='Manual BSP Index')
    row.prop(active_item.tag_encounter, "manual_bsp_index", text='')
    row = col.row()
    row.label(text='Respawn Delay')
    row.prop(active_item.tag_encounter, "respawn_delay_min", text='')
    row.prop(active_item.tag_encounter, "respawn_delay_max", text='')

def render_squad(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Name')
    row.prop(active_item.tag_squad, "name", text='')
    row = col.row()
    row.prop_search(active_item.tag_squad, 'actor_type', scene, 'tag_palatte')
    row = col.row()
    row.label(text='Platoon')
    row.prop(active_item.tag_squad, "platoon", text='')
    row = col.row()
    row.label(text='Initial State')
    row.prop(active_item.tag_squad, "initial_state", text='')
    row = col.row()
    row.label(text='Return State')
    row.prop(active_item.tag_squad, "return_state", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_squad, "unused")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_squad, "never_search")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_squad, "start_timer_immediately")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_squad, "no_timer_delay_forever")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_squad, "magic_sight_after_timer")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_squad, "automatic_migration")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Unique Leader Type')
    row.prop(active_item.tag_squad, "unique_leader_type", text='')
    row = col.row()
    row.label(text='Maneuver To Squad')
    row.prop(active_item.tag_squad, "maneuver_to_squad", text='')
    row = col.row()
    row.label(text='Squad Delay Time')
    row.prop(active_item.tag_squad, "squad_delay_time", text='')
    row = col.row()
    row.label(text='Attacking')
    row.prop(active_item.tag_squad, "attacking_groups", text='')
    row = col.row()
    row.label(text='Attacking Search')
    row.prop(active_item.tag_squad, "attacking_search_groups", text='')
    row = col.row()
    row.label(text='Attacking Guard')
    row.prop(active_item.tag_squad, "attacking_guard_groups", text='')
    row = col.row()
    row.label(text='Defending')
    row.prop(active_item.tag_squad, "defending_groups", text='')
    row = col.row()
    row.label(text='Defending Search')
    row.prop(active_item.tag_squad, "defending_search_groups", text='')
    row = col.row()
    row.label(text='Defending Guard')
    row.prop(active_item.tag_squad, "defending_guard_groups", text='')
    row = col.row()
    row.label(text='Pursuing')
    row.prop(active_item.tag_squad, "pursuing_groups", text='')
    row = col.row()
    row.label(text='Normal Difficulty Count')
    row.prop(active_item.tag_squad, "normal_diff_count", text='')
    row = col.row()
    row.label(text='Insane Difficulty Count')
    row.prop(active_item.tag_squad, "insane_diff_count", text='')
    row = col.row()
    row.label(text='Major Upgrade')
    row.prop(active_item.tag_squad, "major_upgrade", text='')
    row = col.row()
    row.label(text='Respawn Minimum Actors')
    row.prop(active_item.tag_squad, "respawn_min_actors", text='')
    row = col.row()
    row.label(text='Respawn Maximum Actors')
    row.prop(active_item.tag_squad, "respawn_max_actors", text='')
    row = col.row()
    row.label(text='Respawn Total')
    row.prop(active_item.tag_squad, "respawn_total", text='')
    row = col.row()
    row.label(text='Respawn Delay')
    row.prop(active_item.tag_squad, "respawn_delay_min", text='')
    row.prop(active_item.tag_squad, "respawn_delay_max", text='')

def render_move_position(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Weight')
    row.prop(active_item.tag_move_position, "weight", text='')
    row = col.row()
    row.label(text='Time')
    row.prop(active_item.tag_move_position, "time_min", text='')
    row.prop(active_item.tag_move_position, "time_max", text='')
    row = col.row()
    row.label(text='Animation')
    row.prop(active_item.tag_move_position, "animation_index", text='')
    row = col.row()
    row.label(text='Sequence ID')
    row.prop(active_item.tag_move_position, "sequence_id", text='')
    row = col.row()
    row.label(text='Surface Index')
    row.prop(active_item.tag_move_position, "surface_index", text='')

def render_starting_location(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Sequence ID')
    row.prop(active_item.tag_starting_location, "sequence_id", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_starting_location, "required")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Initial State')
    row.prop(active_item.tag_starting_location, "initial_state", text='')
    row = col.row()
    row.label(text='Return State')
    row.prop(active_item.tag_starting_location, "return_state", text='')
    row = col.row()
    row.prop_search(active_item.tag_starting_location, 'actor_type', scene, 'tag_palatte')
    row = col.row()
    row.label(text='Command List')
    row.prop(active_item.tag_starting_location, "command_list", text='')

def render_platoon(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Name')
    row.prop(active_item.tag_platoon, "name", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_platoon, "flee_when_maneuvering")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_platoon, "say_advancing_when_maneuver")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_platoon, "start_in_defending_state")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Change Attacking/Defending State')
    row.prop(active_item.tag_platoon, "change_attacking_defending_state", text='')
    row = col.row()
    row.label(text='Happens To A')
    row.prop(active_item.tag_platoon, "happens_to_a", text='')
    row = col.row()
    row.label(text='Maneuver When')
    row.prop(active_item.tag_platoon, "maneuver_when", text='')
    row = col.row()
    row.label(text='Happens To B')
    row.prop(active_item.tag_platoon, "happens_to_b", text='')

def render_firing_point(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Group Index')
    row.prop(active_item.tag_firing_position, "group_index", text='')

def render_command_list(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Team Index')
    row.prop(active_item.tag_command_list, "name", text='')

    box_flags = layout.box()
    box_flags.label(text="Flags")
    col_flags = box_flags.column(align=True)
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_command_list, "allow_initiative")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_command_list, "allow_targeting")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_command_list, "disable_looking")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_command_list, "disable_communication")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_command_list, "disable_falling_damage")
    row_flags = col_flags.row()
    row_flags.prop(active_item.tag_command_list, "manual_bsp_index_flag")

    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='BSP Index')
    row.prop(active_item.tag_command_list, "manual_bsp_index", text='')

def render_command(context, layout, active_item):
    scene = context.scene

    box = layout.split()
    col = box.column(align=True)

    row = col.row()
    row.label(text='Atom Type')
    row.prop(active_item.tag_command, "atom_type", text='')
    row = col.row()
    atom_type = int(active_item.tag_command.atom_type)
    if atom_type == 0:
        row = col.row()
        row.label(text='Pause Time')
        row.prop(active_item.tag_command, "parameter_1", text='')
    elif atom_type == 1:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Destination')
        row.prop(active_item.tag_command, "point_1", text='')
    elif atom_type == 2:
        row = col.row()
        row.label(text='Destination')
        row.prop(active_item.tag_command, "point_1", text='')
        row = col.row()
        row.label(text='Facing At')
        row.prop(active_item.tag_command, "point_2", text='')
    elif atom_type == 3:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Distance')
        row.prop(active_item.tag_command, "parameter_1", text='')
        row = col.row()
        row.label(text='Angle')
        row.prop(active_item.tag_command, "parameter_2", text='')
        row = col.row()
        row.label(text='Move Towards')
        row.prop(active_item.tag_command, "point_1", text='')
    elif atom_type == 4:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Duration')
        row.prop(active_item.tag_command, "parameter_1", text='')
        row = col.row()
        row.label(text='Look At')
        row.prop(active_item.tag_command, "point_1", text='')
    elif atom_type == 5:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
    elif atom_type == 6:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
    elif atom_type == 7:
        row = col.row()
        row.label(text='Burst Fire Length')
        row.prop(active_item.tag_command, "parameter_1", text='')
        row = col.row()
        row.label(text='Shoot At')
        row.prop(active_item.tag_command, "point_1", text='')
    elif atom_type == 8:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Throw At')
        row.prop(active_item.tag_command, "point_1", text='')
    elif atom_type == 9:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Vehicle Distance')
        row.prop(active_item.tag_command, "parameter_1", text='')
    elif atom_type == 11:
        row = col.row()
        row.label(text='Horizontal Velocity')
        row.prop(active_item.tag_command, "parameter_1", text='')
        row = col.row()
        row.label(text='Vertical Velocity')
        row.prop(active_item.tag_command, "parameter_2", text='')
    elif atom_type == 12:
        row = col.row()
        row.label(text='Script')
        row.prop(active_item.tag_command, "script_index", text='')
    elif atom_type == 13:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Animation')
        row.prop(active_item.tag_command, "animation_index", text='')
    elif atom_type == 14:
        row = col.row()
        row.label(text='Recording')
        row.prop(active_item.tag_command, "recording_index", text='')
    elif atom_type == 15:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
    elif atom_type == 16:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
    elif atom_type == 17:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
    elif atom_type == 18:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
    elif atom_type == 19:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
    elif atom_type == 20:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Command')
        row.prop(active_item.tag_command, "command_index", text='')
    elif atom_type == 21:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Command')
        row.prop(active_item.tag_command, "command_index", text='')
    elif atom_type == 22:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Time')
        row.prop(active_item.tag_command, "parameter_1", text='')
    elif atom_type == 23:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Duration Min')
        row.prop(active_item.tag_command, "parameter_1", text='')
        row = col.row()
        row.label(text='Duration Max')
        row.prop(active_item.tag_command, "parameter_2", text='')
        row = col.row()
        row.label(text='First Look Point')
        row.prop(active_item.tag_command, "point_1", text='')
        row = col.row()
        row.label(text='Last Look Point')
        row.prop(active_item.tag_command, "point_2", text='')
    elif atom_type == 24:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Duration')
        row.prop(active_item.tag_command, "parameter_1", text='')
    elif atom_type == 25:
        row = col.row()
        row.label(text='Modifier')
        row.prop(active_item.tag_command, "atom_modifier_ui", text='')
        row = col.row()
        row.label(text='Duration')
        row.prop(active_item.tag_command, "parameter_1", text='')
        row = col.row()
        row.prop_search(active_item.tag_command, 'object_name', scene, 'object_names')
    elif atom_type == 26:
        row = col.row()
        row.label(text='Duration')
        row.prop(active_item.tag_command, "parameter_1", text='')
    elif atom_type == 27:
        row = col.row()
        row.label(text='Target Point')
        row.prop(active_item.tag_command, "point_1", text='')
        row = col.row()
        row.label(text='Face Towards Point')
        row.prop(active_item.tag_command, "point_2", text='')

def render_cutscene_flag(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Name')
    row.prop(active_item.tag_cutscene_flag, "name", text='')

def render_cutscene_camera(context, layout, active_item):
    box = layout.split()
    col = box.column(align=True)
    row = col.row()
    row.label(text='Name')
    row.prop(active_item.tag_cutscene_camera, "name", text='')

def get_data_type(ui, context, is_collection=False):
    layout = ui.layout
    
    if is_collection:
        active_item = context.collection
        parent_collection = active_item.tag_collection.parent
        item_collection_names = []
        if parent_collection:
            item_collection_names = [parent_collection.name.lower().replace(" ", "_")]

        render_collection(context, layout, active_item)

    else:
        active_item = context.object
        item_collection_names = [collection.name.lower().replace(" ", "_") for collection in active_item.users_collection]

    if "skies" in item_collection_names:
        render_sky(context, layout, active_item)
    elif "scenery" in item_collection_names or "sound_scenery" in item_collection_names:
        render_object(context, layout, active_item)
        render_scenery(context, layout, active_item)
    elif "bipeds" in item_collection_names:
        render_object(context, layout, active_item)
        render_unit(context, layout, active_item)
    elif "vehicles" in item_collection_names:
        render_object(context, layout, active_item)
        render_unit(context, layout, active_item)
        render_vehicle(context, layout, active_item)
    elif "equipment" in item_collection_names:
        render_object(context, layout, active_item)
        render_equipment(context, layout, active_item)
    elif "weapons" in item_collection_names:
        render_object(context, layout, active_item)
        render_weapon(context, layout, active_item)
    elif "machines" in item_collection_names:
        render_object(context, layout, active_item)
        render_device(context, layout, active_item)
        render_machine(context, layout, active_item)
    elif "controls" in item_collection_names:
        render_object(context, layout, active_item)
        render_device(context, layout, active_item)
        render_control(context, layout, active_item)
    elif "light_fixtures" in item_collection_names:
        render_object(context, layout, active_item)
        render_device(context, layout, active_item)
        render_light_fixture(context, layout, active_item)
    elif "player_starting_locations" in item_collection_names:
        render_player_starting_location(context, layout, active_item)
    elif "netgame_flags" in item_collection_names:
        render_netgame_flags(context, layout, active_item)
    elif "netgame_equipment" in item_collection_names:
        render_netgame_equipment(context, layout, active_item)
    elif "decals" in item_collection_names:
        render_decal(context, layout, active_item)
    elif "encounters" in item_collection_names:
        render_encounter(context, layout, active_item)
    elif "cutscene_flags" in item_collection_names:
        render_cutscene_flag(context, layout, active_item)
    elif "cutscene_cameras" in item_collection_names:
        render_cutscene_camera(context, layout, active_item)
    else:
        for collection_name in item_collection_names:
            if collection_name.endswith("clusters"):
                render_cluster(context, layout, active_item)
            elif collection_name.endswith("instances"):
                render_instance(context, layout, active_item)
            elif collection_name.startswith("squads"):
                render_squad(context, layout, active_item)
            elif collection_name.startswith("move_positions"):
                render_move_position(context, layout, active_item)
            elif collection_name.startswith("starting_locations"):
                render_starting_location(context, layout, active_item)
            elif collection_name.startswith("platoons"):
                render_platoon(context, layout, active_item)
            elif collection_name.startswith("firing_points"):
                render_firing_point(context, layout, active_item)
            elif collection_name.startswith("player_starting_locations"):
                render_player_starting_location(context, layout, active_item)
            elif collection_name.startswith("command_list"):
                render_command_list(context, layout, active_item)
            elif collection_name.startswith("command"):
                render_command(context, layout, active_item)

class Halo_ObjectTagView(Panel):
    bl_label = "Halo Tag View"
    bl_idname = "HALO_PT_ObjectTagView"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ObjectDetailsPanel"

    def draw(self, context):
        get_data_type(self, context)

class Halo_CollectionTagView(Panel):
    bl_label = "Halo Tag View"
    bl_idname = "HALO_PT_CollectionTagView"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        get_data_type(self, context, True)
