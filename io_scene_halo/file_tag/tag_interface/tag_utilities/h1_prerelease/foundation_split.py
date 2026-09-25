import re
import os
import sys
import struct

h1_20000525_tag_groups = {
    "ant!": "antennas",
    "antr": "models_animations",
    "bipd": "bipeds",
    "bitm": "bitmaps",
    "boom": "spheroids",
    "cafx": "camera_effects",
    "camr": "cameras",
    "col2": "models_collision_geometry",
    "coll": "models_old_collision_geometry",
    "colo": "color_tables",
    "cont": "contrails",
    "damg": "area_of_effect_damage",
    "damr": "damage_resistance",
    "deta": "detail_objects",
    "devo": "cellular_automata",
    "effe": "effects",
    "envi": "environment",
    "eqip": "equipment",
    "flag": "flags",
    "font": "fonts",
    "glw!": "glow",
    "isla": "islands",
    "isls": "islands_scenarios",
    "ligh": "lights",
    "mach": "devices_machines",
    "matg": "materials",
    "mode": "models",
    "part": "particles",
    "pctl": "particle_systems",
    "phys": "physics",
    "plac": "placeholders",
    "pphy": "point_physics",
    "proj": "projectiles",
    "rain": "weather_particle_systems",
    "scen": "scenery",
    "snd!": "sounds",
    "str#": "string_lists",
    "stst": "structure_styles",
    "suit": "suit_interface",
    "trak": "camera_track",
    "turr": "turrets",
    "vehi": "vehicles",
    "weap": "weapons",
    "whip": "cellular_automata2d",
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

def dump_foundation(foundation_file):
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

        for tag_idx in range(tag_count):
            tag_header = read_tag_header(input_stream)
            print(tag_header)

            tag_group = tag_header["tag_group"]

            output_folder = os.path.join(os.path.join(os.path.dirname(foundation_file), "output"), h1_20000525_tag_groups.get(tag_group))
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
    for file_path in sys.argv[1:]:
        dump_foundation(file_path)

if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to close...")
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}\n")
        input("\nPress Enter to close...")
