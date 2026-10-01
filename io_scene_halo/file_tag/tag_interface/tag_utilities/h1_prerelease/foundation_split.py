import re
import os
import sys
import struct

h1_19980319_tag_groups = {
    "bitm": "bitmaps",
    "font": "fonts",
    "mesh": "meshes",
    "mode": "models",
    "str#": "strings"
    }

h1_19980403_tag_groups = {
    "moan": "animations",
    "bitm": "bitmaps",
    "font": "fonts",
    "mesh": "meshes",
    "mode": "models",
    "shad": "shadows",
    "str#": "strings"
    }

h1_19980512_tag_groups = {
    "moan": "animations",
    "bitm": "bitmaps",
    "colo": "color tables",
    "font": "fonts",
    "mesh": "meshes",
    "mode": "models",
    "plat": "platoons",
    "scen": "scenery",
    "shad": "shadows",
    "str#": "strings",
    "unit": "units",
    "bipd": "units.bipeds",
    "phys": "vehicle physics",
    "weat": "weather systems"
    }

h1_19980514_tag_groups = {
    "moan": "animations",
    "bitm": "bitmaps",
    "colo": "color tables",
    "font": "fonts",
    "mesh": "meshes",
    "mode": "models",
    "shad": "shadows",
    "str#": "strings",
    "weat": "weather systems"
    }

h1_19980624_tag_groups = {
    "bitm": "bitmaps",
    "colo": "color tables",
    "font": "fonts",
    "mesh": "meshes",
    "mode": "models",
    "antr": "models.animation graphs",
    "moan": "models.animations",
    "phys": "physics",
    "plat": "platoons",
    "scen": "scenery",
    "shad": "shadows",
    "str#": "strings",
    "unit": "units",
    "bipd": "units.bipeds",
    "hovr": "units.hovercrafts",
    "jeep": "units.jeeps",
    "tank": "units.tanks",
    "weat": "weather systems"
    }

h1_19980708_tag_groups = {
    "bitm": "bitmaps",
    "colo": "color tables",
    "font": "fonts",
    "mesh": "meshes",
    "mode": "models",
    "antr": "models.animation graphs",
    "moan": "models.animations",
    "phys": "physics",
    "plat": "platoons",
    "scen": "scenery",
    "shad": "shadows",
    "str#": "strings",
    "unit": "units",
    "bipd": "units.bipeds",
    "hovr": "units.hovercrafts",
    "jeep": "units.jeeps",
    "tank": "units.tanks",
    "weat": "weather systems"
    }

h1_19981008_tag_groups = {
    "bitm": "bitmaps",
    "coll": "collision geometries",
    "colo": "color tables",
    "cont": "contrails",
    "font": "fonts",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "phys": "physics",
    "prco": "projectile groups",
    "proj": "projectiles",
    "plyr": "saved players",
    "game": "saved players.games",
    "scen": "scenery",
    "str#": "strings",
    "unit": "units",
    "bipd": "units.bipeds",
    "boat": "units.boats",
    "hovr": "units.hovercrafts",
    "jeep": "units.jeeps",
    "tank": "units.tanks",
    "weat": "weather systems",
    "mesh": "worlds",
    "clnp": "worlds.clean pages",
    "savp": "worlds.saved pages",
    "stap": "worlds.static pages",
    "texp": "worlds.texture pages"
    }

h1_19981022_tag_groups = {
    "bitm": "bitmaps",
    "coll": "collision geometries",
    "colo": "color tables",
    "cont": "contrails",
    "effe": "effects",
    "font": "fonts",
    "ligh": "lights",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "part": "particles",
    "phys": "physics",
    "prco": "projectile groups",
    "proj": "projectiles",
    "plyr": "saved players",
    "game": "saved players.games",
    "scen": "scenery",
    "str#": "strings",
    "stru": "structures",
    "unit": "units",
    "bipd": "units.bipeds",
    "boat": "units.boats",
    "hovr": "units.hovercrafts",
    "jeep": "units.jeeps",
    "tank": "units.tanks",
    "weap": "weapons",
    "weat": "weather systems",
    "mesh": "worlds",
    "clnp": "worlds.clean pages",
    "savp": "worlds.saved pages",
    "stap": "worlds.static pages",
    "texp": "worlds.texture pages"
    }

h1_19990225_tag_groups = {
    "bitm": "bitmaps",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "effe": "effects",
    "font": "fonts",
    "mate": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damr": "objects.damage resistance",
    "item": "objects.items",
    "eqip": "objects.items.equipment",
    "proj": "objects.items.projectiles",
    "weap": "objects.items.weapons",
    "ligh": "objects.lights",
    "scen": "objects.scenery",
    "stru": "objects.structures",
    "unit": "objects.units",
    "bipd": "objects.units.bipeds",
    "vehi": "objects.units.vehicles",
    "part": "particles",
    "phys": "physics",
    "plyr": "saved players",
    "game": "saved players.games",
    "mhir": "shadows",
    "snd!": "sounds",
    "str#": "strings",
    "suit": "suit interface",
    "weat": "weather systems",
    "mesh": "worlds",
    "clnp": "worlds.clean pages",
    "savp": "worlds.saved pages",
    "stap": "worlds.static pages",
    "texp": "worlds.texture pages"
    }

h1_19990302_tag_groups = {
    "bitm": "bitmaps",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "effe": "effects",
    "font": "fonts",
    "mate": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damr": "objects.damage resistance",
    "item": "objects.items",
    "eqip": "objects.items.equipment",
    "proj": "objects.items.projectiles",
    "weap": "objects.items.weapons",
    "ligh": "objects.lights",
    "scen": "objects.scenery",
    "stru": "objects.structures",
    "unit": "objects.units",
    "bipd": "objects.units.bipeds",
    "vehi": "objects.units.vehicles",
    "part": "particles",
    "phys": "physics",
    "plyr": "saved players",
    "game": "saved players.games",
    "mhir": "shadows",
    "snd!": "sounds",
    "str#": "strings",
    "suit": "suit interface",
    "weat": "weather systems",
    "mesh": "worlds",
    "clnp": "worlds.clean pages",
    "savp": "worlds.saved pages",
    "stap": "worlds.static pages",
    "texp": "worlds.texture pages"
    }

h1_19990426_tag_groups = {
    "bitm": "bitmaps",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "effe": "effects",
    "boom": "explosions",
    "font": "fonts",
    "isla": "islands",
    "isls": "islands.scenarios",
    "islt": "islands.textures",
    "item": "items",
    "eqip": "items.equipment",
    "proj": "items.projectiles",
    "weap": "items.weapons",
    "matg": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damr": "objects.damage resistance",
    "ligh": "objects.lights",
    "plac": "objects.placeholders",
    "mhir": "objects.shadows",
    "part": "particles",
    "phys": "physics",
    "rzpf": "preferences.rasterizer",
    "scen": "scenery",
    "snd!": "sounds",
    "lsnd": "sounds.complex",
    "str#": "strings",
    "stru": "structures",
    "suit": "suit interface",
    "unit": "units",
    "bipd": "units.bipeds",
    "vehi": "units.vehicles",
    "rain": "weather particle systems",
    "weat": "weather systems",
    "ant!": "widgets.antennas",
    "flag": "widgets.flags"
    }

h1_19990608_tag_groups = {
    "bitm": "bitmaps",
    "trak": "camera tracks",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "effe": "effects",
    "font": "fonts",
    "isla": "islands",
    "isls": "islands.scenarios",
    "islt": "islands.textures",
    "item": "items",
    "eqip": "items.equipment",
    "proj": "items.projectiles",
    "weap": "items.weapons",
    "matg": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damr": "objects.damage resistance",
    "ligh": "objects.lights",
    "plac": "objects.placeholders",
    "mhir": "objects.shadows",
    "part": "particles",
    "phys": "physics",
    "rzpf": "preferences.rasterizer",
    "sdpf": "preferences.sound",
    "scen": "scenery",
    "lsnd": "sounds.complex",
    "snd!": "sounds.definitions",
    "snpm": "sounds.samples",
    "boom": "spheroids",
    "str#": "strings",
    "stru": "structures",
    "suit": "suit interface",
    "unit": "units",
    "bipd": "units.bipeds",
    "vehi": "units.vehicles",
    "rain": "weather particle systems",
    "weat": "weather systems",
    "ant!": "widgets.antennas",
    "flag": "widgets.flags",
    "glw!": "widgets.glow"
    }

h1_19990623_tag_groups = {
    "bitm": "bitmaps",
    "trak": "camera tracks",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "effe": "effects",
    "font": "fonts",
    "isla": "islands",
    "isls": "islands.scenarios",
    "islt": "islands.textures",
    "item": "items",
    "eqip": "items.equipment",
    "proj": "items.projectiles",
    "weap": "items.weapons",
    "matg": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damr": "objects.damage resistance",
    "ligh": "objects.lights",
    "plac": "objects.placeholders",
    "mhir": "objects.shadows",
    "butt": "particle systems",
    "part": "particles",
    "phys": "physics",
    "rzpf": "preferences.rasterizer",
    "sdpf": "preferences.sound",
    "scen": "scenery",
    "lsnd": "sounds.complex",
    "snd!": "sounds.definitions",
    "snpm": "sounds.samples",
    "boom": "spheroids",
    "str#": "strings",
    "stru": "structures",
    "suit": "suit interface",
    "unit": "units",
    "bipd": "units.bipeds",
    "vehi": "units.vehicles",
    "rain": "weather particle systems",
    "weat": "weather systems",
    "ant!": "widgets.antennas",
    "flag": "widgets.flags",
    "glw!": "widgets.glow"
    }

h1_19990730_tag_groups = {
    "bitm": "bitmaps",
    "trak": "camera tracks",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "effe": "effects",
    "font": "fonts",
    "isla": "islands",
    "isls": "islands.scenarios",
    "islt": "islands.textures",
    "item": "items",
    "eqip": "items.equipment",
    "proj": "items.projectiles",
    "weap": "items.weapons",
    "matg": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damr": "objects.damage resistance",
    "ligh": "objects.lights",
    "plac": "objects.placeholders",
    "mhir": "objects.shadows",
    "part": "particles",
    "phys": "physics",
    "rzpf": "preferences.rasterizer",
    "sdpf": "preferences.sound",
    "scen": "scenery",
    "moov": "scripts",
    "lsnd": "sounds.complex",
    "snd!": "sounds.definitions",
    "snpm": "sounds.samples",
    "boom": "spheroids",
    "str#": "strings",
    "stru": "structures",
    "suit": "suit interface",
    "unit": "units",
    "bipd": "units.bipeds",
    "vehi": "units.vehicles",
    "rain": "weather particle systems",
    "weat": "weather systems",
    "ant!": "widgets.antennas",
    "flag": "widgets.flags",
    "glw!": "widgets.glow"
    }

h1_19990924_tag_groups = {
    "bitm": "bitmaps",
    "camr": "camera parameters",
    "trak": "camera tracks",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "ditl": "dialog templates",
    "effe": "effects",
    "font": "fonts",
    "isla": "islands",
    "isls": "islands.scenarios",
    "islt": "islands.textures",
    "item": "items",
    "eqip": "items.equipment",
    "proj": "items.projectiles",
    "weap": "items.weapons",
    "matg": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damr": "objects.damage resistance",
    "ligh": "objects.lights",
    "plac": "objects.placeholders",
    "mhir": "objects.shadows",
    "pctl": "particle systems",
    "part": "particles",
    "phys": "physics",
    "rzpf": "preferences.rasterizer",
    "sdpf": "preferences.sound",
    "scen": "scenery",
    "moov": "scripts",
    "lsnd": "sounds.complex",
    "snd!": "sounds.definitions",
    "snpm": "sounds.samples",
    "boom": "spheroids",
    "str#": "strings",
    "stru": "structures",
    "suit": "suit interface",
    "unit": "units",
    "bipd": "units.bipeds",
    "vehi": "units.vehicles",
    "rain": "weather particle systems",
    "weat": "weather systems",
    "ant!": "widgets.antennas",
    "flag": "widgets.flags",
    "glw!": "widgets.glow"
    }

h1_19990930_tag_groups = {
    "bitm": "bitmaps",
    "camr": "camera parameters",
    "trak": "camera tracks",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "ditl": "dialog templates",
    "effe": "effects",
    "font": "fonts",
    "isla": "islands",
    "isls": "islands.scenarios",
    "islt": "islands.textures",
    "item": "items",
    "eqip": "items.equipment",
    "proj": "items.projectiles",
    "weap": "items.weapons",
    "matg": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damr": "objects.damage resistance",
    "ligh": "objects.lights",
    "plac": "objects.placeholders",
    "mhir": "objects.shadows",
    "pctl": "particle systems",
    "part": "particles",
    "phys": "physics",
    "rzpf": "preferences.rasterizer",
    "sdpf": "preferences.sound",
    "scen": "scenery",
    "moov": "scripts",
    "lsnd": "sounds.complex",
    "snd!": "sounds.definitions",
    "snpm": "sounds.samples",
    "stsl": "sounds.streaming.loops",
    "boom": "spheroids",
    "str#": "strings",
    "stru": "structures",
    "suit": "suit interface",
    "unit": "units",
    "bipd": "units.bipeds",
    "vehi": "units.vehicles",
    "rain": "weather particle systems",
    "weat": "weather systems",
    "ant!": "widgets.antennas",
    "flag": "widgets.flags",
    "glw!": "widgets.glow"
    }

h1_19991021_tag_groups = {
    "bitm": "bitmaps",
    "camr": "camera parameters",
    "trak": "camera tracks",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "ditl": "dialog templates",
    "effe": "effects",
    "font": "fonts",
    "isla": "islands",
    "isls": "islands.scenarios",
    "islt": "islands.textures",
    "item": "items",
    "eqip": "items.equipment",
    "proj": "items.projectiles",
    "weap": "items.weapons",
    "matg": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damg": "objects.damage",
    "damr": "objects.damage resistance",
    "ligh": "objects.lights",
    "plac": "objects.placeholders",
    "mhir": "objects.shadows",
    "pctl": "particle systems",
    "part": "particles",
    "phys": "physics",
    "rzpf": "preferences.rasterizer",
    "sdpf": "preferences.sound",
    "scen": "scenery",
    "moov": "scripts",
    "lsnd": "sounds.complex",
    "snd!": "sounds.definitions",
    "snpm": "sounds.samples",
    "stsl": "sounds.streaming.loops",
    "boom": "spheroids",
    "str#": "strings",
    "stru": "structures",
    "suit": "suit interface",
    "unit": "units",
    "bipd": "units.bipeds",
    "vehi": "units.vehicles",
    "rain": "weather particle systems",
    "weat": "weather systems",
    "ant!": "widgets.antennas",
    "flag": "widgets.flags",
    "glw!": "widgets.glow"
    }

h1_20000525_tag_groups = {
    "alph": "aleph",
    "ant!": "antennas",
    "damg": "area_of_effect_damage",
    "bipd": "bipeds",
    "bitm": "bitmaps",
    "cafx": "camera_effects",
    "trak": "camera_track",
    "camr": "cameras",
    "devo": "cellular_automata",
    "whip": "cellular_automata2d",
    "colo": "color_tables",
    "cont": "contrails",
    "damr": "damage_resistance",
    "deta": "detail_objects",
    "devi": "devices",
    "ctrl": "devices_controls",
    "mach": "devices_machines",
    "pane": "devices_panes",
    "sens": "devices_sensors",
    "stat": "devices_stations",
    "ditl": "dialog_template",
    "effe": "effects",
    "envi": "environment",
    "eqip": "equipment",
    "flag": "flags",
    "font": "fonts",
    "glw!": "glow",
    "isla": "islands",
    "isls": "islands_scenarios",
    "item": "items",
    "ligh": "lights",
    "matg": "materials",
    "mode": "models",
    "antr": "models_animations",
    "col2": "models_collision_geometry",
    "coll": "models_old_collision_geometry",
    "obje": "objects",
    "pctl": "particle_systems",
    "part": "particles",
    "phys": "physics",
    "plac": "placeholders",
    "pphy": "point_physics",
    "ngpr": "preferences_network_game",
    "rzpf": "preferences_rasterizer",
    "sdpf": "preferences_sound",
    "proj": "projectiles",
    "scen": "scenery",
    "moov": "scripts",
    "mhir": "shadows",
    "snd!": "sounds",
    "lsnd": "sounds_looping",
    "stst": "structure_styles",
    "boom": "spheroids",
    "str#": "string_lists",
    "suit": "suit_interface",
    "team": "teams",
    "turr": "turrets",
    "unit": "units",
    "vehi": "vehicles",
    "weap": "weapons",
    "rain": "weather_particle_systems"
    }

h1_20001005_tag_groups = {
    "bitm": "bitmaps",
    "camr": "camera parameters",
    "trak": "camera tracks",
    "coll": "collision models",
    "colo": "color tables",
    "cont": "contrails",
    "deta": "detail objects",
    "ditl": "dialog templates",
    "effe": "effects",
    "font": "fonts",
    "isla": "islands",
    "isls": "islands.scenarios",
    "islt": "islands.textures",
    "item": "items",
    "eqip": "items.equipment",
    "proj": "items.projectiles",
    "weap": "items.weapons",
    "matg": "materials",
    "mode": "models",
    "antr": "models.animations",
    "obje": "objects",
    "damg": "objects.damage",
    "damr": "objects.damage resistance",
    "ligh": "objects.lights",
    "plac": "objects.placeholders",
    "mhir": "objects.shadows",
    "pctl": "particle systems",
    "part": "particles",
    "phys": "physics",
    "rzpf": "preferences.rasterizer",
    "sdpf": "preferences.sound",
    "scen": "scenery",
    "moov": "scripts",
    "lsnd": "sounds.complex",
    "snd!": "sounds.definitions",
    "snpm": "sounds.samples",
    "stsl": "sounds.streaming.loops",
    "boom": "spheroids",
    "str#": "strings",
    "stru": "structures",
    "suit": "suit interface",
    "unit": "units",
    "bipd": "units.bipeds",
    "vehi": "units.vehicles",
    "rain": "weather particle systems",
    "weat": "weather systems",
    "ant!": "widgets.antennas",
    "flag": "widgets.flags",
    "glw!": "widgets.glow"
    }

h1_20001116_tag_groups = {
    "actr": "actors",
    "alph": "aleph",
    "ant!": "antennas",
    "damg": "area_of_effect_damage",
    "bipd": "bipeds",
    "bitm": "bitmaps",
    "cafx": "camera_effects",
    "trak": "camera_track",
    "camr": "cameras",
    "devo": "cellular_automata",
    "whip": "cellular_automata2d",
    "colo": "color_tables",
    "cont": "contrails",
    "joy!": "controller_response_function",
    "ctrl": "devices_controls",
    "mach": "devices_machines",
    "ditl": "dialog_template",
    "effe": "effects",
    "senv": "environment_shaders",
    "eqip": "equipment",
    "flag": "flags",
    "font": "fonts",
    "glw!": "glow",
    "lens": "lens_flare",
    "ligh": "lights",
    "matg": "materials",
    "sobj": "model_shaders",
    "mode": "models",
    "antr": "models_animations",
    "coll": "models_collision_geometry",
    "obje": "objects",
    "pctl": "particle_systems",
    "part": "particles",
    "phys": "physics",
    "plac": "placeholders",
    "pphy": "point_physics",
    "ngpr": "preferences_network_game",
    "sdpf": "preferences_sound",
    "proj": "projectiles",
    "scnr": "scenario",
    "scen": "scenery",
    "moov": "scripts",
    "shdr": "shaders",
    "mhir": "shadows",
    "sky ": "sky",
    "soso": "solid_model_shaders",
    "snde": "sound_environment",
    "snd!": "sounds",
    "lsnd": "sounds_looping",
    "boom": "spheroids",
    "str#": "string_lists",
    "sbsp": "structure_bsp",
    "suit": "suit_interface",
    "sotr": "transparent_model_shaders",
    "vehi": "vehicles",
    "weap": "weapons",
    "rain": "weather_particle_systems",
    "wind": "wind"
    }

def read_int16(input_stream, file_endian=">", is_signed=True):
    struct_string = "%sh" % file_endian
    if not is_signed:
        struct_string = uppercase_struct_letters(struct_string)

    return struct.unpack(struct_string, input_stream.read(2))[0]

def read_int32(input_stream, file_endian=">", is_signed=True):
    struct_string = "%si" % file_endian
    if not is_signed:
        struct_string = uppercase_struct_letters(struct_string)
    
    return struct.unpack(struct_string, input_stream.read(4))[0]

def read_byte(input_stream, file_endian=">", is_signed=True):
    struct_string = "%sb" % file_endian
    if not is_signed:
        struct_string = uppercase_struct_letters(struct_string)
    
    return struct.unpack(struct_string, input_stream.read(1))[0]

def read_string(input_stream, length, clean_string= True):
    string = None
    data = input_stream.read(length)
    if clean_string:
        string = data.decode('ascii', errors='replace').split('\x00', 1)[0].strip('\x20')
    else:
        string = data.decode('ascii', errors='replace')
    return string

def read_tag_header(input_stream):
    header = {}

    header["unk1"] = read_int16(input_stream)
    header["flags"] = read_byte(input_stream)
    header["type"] = read_byte(input_stream)

    header["name"] = read_string(input_stream, 32)

    header["tag_group"] = read_string(input_stream, 4, False)

    header["checksum"] = read_int32(input_stream, is_signed=False)
    header["data_offset"] = read_int32(input_stream, is_signed=False)
    header["data_length"] = read_int32(input_stream, is_signed=False)

    header["unk"] = read_int32(input_stream, is_signed=False)

    header["version"] = read_int16(input_stream, is_signed=False)
    header["destination"] = read_byte(input_stream)
    header["plugin_handle"] = read_byte(input_stream, is_signed=False)

    header["blam_tag"] = read_string(input_stream, 4, False)

    return header

def uppercase_struct_letters(struct_string):
    struct_letters = 'bhiqnl'
    result = []
    for char in struct_string:
        if char in struct_letters:
            result.append(char.upper())
        else:
            result.append(char)
    return ''.join(result)

def dump_foundation(foundation_file, game_version=None):
    with open(foundation_file, "rb") as input_stream:
        foundation_type = read_int16(input_stream)
        version = read_int16(input_stream)
        name = read_string(input_stream, 32)
        
        input_stream.read(64) # URL
        
        entry_point_count = read_int16(input_stream)
        tag_count = read_int16(input_stream)
        checksum = read_int32(input_stream, is_signed=False)
        flags = read_int32(input_stream, is_signed=False)
        size = read_int32(input_stream)
        header_checksum = read_int32(input_stream)
        
        input_stream.read(4) # Padding
        
        signature = read_string(input_stream, 4, False)

        print("Foundation:")
        print(f"  Name:       {name}")
        print(f"  Version:    {version}")
        print(f"  Tag Count:  {tag_count}")
        print(f"  Signature:  {signature}")
        print()

        tag_groups = None
        if game_version == 19980319:
            tag_groups = h1_19980319_tag_groups
        elif game_version == 19980403:
            tag_groups = h1_19980403_tag_groups
        elif game_version == 19980512:
            tag_groups = h1_19980512_tag_groups
        elif game_version == 19980514:
            tag_groups = h1_19980514_tag_groups
        elif game_version == 19980624:
            tag_groups = h1_19980624_tag_groups
        elif game_version == 19980708:
            tag_groups = h1_19980708_tag_groups
        elif game_version == 19981008:
            tag_groups = h1_19981008_tag_groups
        elif game_version == 19981022:
            tag_groups = h1_19981022_tag_groups
        elif game_version == 19990225:
            tag_groups = h1_19990225_tag_groups
        elif game_version == 19990302:
            tag_groups = h1_19990302_tag_groups
        elif game_version == 19990426:
            tag_groups = h1_19990426_tag_groups
        elif game_version == 19990608:
            tag_groups = h1_19990608_tag_groups
        elif game_version == 19990623:
            tag_groups = h1_19990623_tag_groups
        elif game_version == 19990730:
            tag_groups = h1_19990730_tag_groups
        elif game_version == 19990924:
            tag_groups = h1_19990924_tag_groups
        elif game_version == 19990930:
            tag_groups = h1_19990930_tag_groups
        elif game_version == 19991021:
            tag_groups = h1_19991021_tag_groups
        elif game_version == 20000525:
            tag_groups = h1_20000525_tag_groups
        elif game_version == 20001005:
            tag_groups = h1_20001005_tag_groups
        elif game_version == 20001116:
            tag_groups = h1_20001116_tag_groups

        for tag_idx in range(tag_count):
            tag_header = read_tag_header(input_stream)
            print(tag_header)

            tag_group = tag_header["tag_group"]

            tag_extension = tag_group
            if tag_groups is not None:
                result = tag_groups.get(tag_group)
                if result is not None:
                    tag_extension = result

            output_folder = os.path.join(os.path.join(os.path.dirname(foundation_file), "output"), tag_extension)
            os.makedirs(output_folder, exist_ok=True)
            output_file = os.path.join(output_folder, tag_header["name"])

            current_pos = input_stream.tell()
            input_stream.seek(tag_header["data_offset"], os.SEEK_SET)

            tag_data = input_stream.read(tag_header["data_length"])

            with open(output_file, "wb") as tag_file:
                tag_file.write(struct.pack(">hBB", tag_header["unk1"], tag_header["flags"], 0))
                name_bytes = tag_header["name"].encode("ascii")
                tag_file.write(name_bytes.ljust(32, b"\0"))
                tag_file.write(tag_group.encode("ascii"))
                tag_file.write(
                    struct.pack(
                        ">IIIIH Bb",
                        tag_header["checksum"],
                        64,  # Data offset
                        tag_header["data_length"],
                        tag_header["unk"],
                        tag_header["version"],
                        tag_header["destination"],
                        -1   # Plugin handle
                    )
                )

                tag_file.write(tag_header["blam_tag"].encode("ascii"))
                tag_file.write(tag_data)
                
            input_stream.seek(current_pos)

def main():
    if len(sys.argv) < 2:
        print("Drag a file onto this script.")
        return

    file_path = sys.argv[1]
    game_version = None
    if len(sys.argv) >= 3:
        game_version = int(sys.argv[2])

    dump_foundation(file_path, game_version)

if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to close...")
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}\n")
        input("\nPress Enter to close...")