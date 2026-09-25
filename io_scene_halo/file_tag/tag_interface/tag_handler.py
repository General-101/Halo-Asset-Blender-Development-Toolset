import os
import sys
import json
import tag_common
from tag_interface import read_file, write_file, obfuscation_buffer_prepare
from tag_definitions import h1, h2, common
from tag_postprocessing.h1 import postprocess_functions as h1_postprocess_functions
from tag_postprocessing.h2 import postprocess_functions as h2_postprocess_functions, create_function
from tag_upgrading.h1 import upgrade_functions as h1_upgrade_functions
from tag_upgrading.h2 import upgrade_functions as h2_upgrade_functions

def import_tag(file_path):
    output_dir = os.path.join(os.path.dirname(tag_common.h1_20000525_defs_directory), "h1_20000525_merged_output")
    merged_defs = h1.generate_defs(tag_common.h1_20000525_defs_directory, output_dir, tag_common.h1_20000525_tag_groups, tag_common.h1_20000525_tag_extensions)

    tag_dict = read_file(merged_defs, "", file_path, engine_tag=tag_common.EngineTag.H1Latest.value, engine_version=tag_common.H1Versions._20000525)
    with open(os.path.join(os.path.dirname(file_path), "%s.json" % os.path.basename(file_path).rsplit(".", 1)[0]), 'w', encoding ='utf8') as json_file:
        json.dump(tag_dict, json_file, ensure_ascii = True, indent=4)

def export_tag(file_path):
    output_dir = os.path.join(os.path.dirname(tag_common.h1_20000525_defs_directory), "h1_20000525_merged_output")
    merged_defs = h1.generate_defs(tag_common.h1_20000525_defs_directory, output_dir, tag_common.h1_20000525_tag_groups, tag_common.h1_20000525_tag_extensions)


    output_path = file_path.rsplit(".", 1)[0]
    with open(file_path, "r", encoding="utf8") as json_file:
        tag_dict = json.load(json_file)

        write_file(merged_defs, tag_dict, obfuscation_buffer_prepare(), output_path, engine_tag=tag_common.EngineTag.H1Latest.value, engine_version=tag_common.H1Versions._20000525)

def main():
    if len(sys.argv) < 2:
        print("Drag a file onto this script.")
        return
    for file_path in sys.argv[1:]:
        if not os.path.isfile(file_path):
            continue
        if file_path.lower().endswith(".json"):
            export_tag(file_path)
        else:
            import_tag(file_path)

if __name__ == "__main__":
    try:
        main()
        input("\nPress Enter to close...")
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}\n")
        input("\nPress Enter to close...")
