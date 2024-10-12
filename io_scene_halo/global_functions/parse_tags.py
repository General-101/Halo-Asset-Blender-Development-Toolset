# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia & Jadeon Sheppard
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

import os

from .. import config

from ..file_tag.h1.file_scenario.process_file import process_file as process_h1_scenario
from ..file_tag.h1.file_scenario_structure_bsp.process_file import process_file as process_h1_structure_bsp
from ..file_tag.h1.file_actor_variant.process_file import process_file as process_actor_variant
from ..file_tag.h1.file_model.process_file import process_file as process_mode
from ..file_tag.h1.file_gbxmodel.process_file import process_file as process_mod2
from ..file_tag.h1.file_scenery.process_file import process_file as process_h1_scenery
from ..file_tag.h1.file_biped.process_file import process_file as process_biped
from ..file_tag.h1.file_vehicle.process_file import process_file as process_vehicle
from ..file_tag.h1.file_equipment.process_file import process_file as process_equipment
from ..file_tag.h1.file_device_machine.process_file import process_file as process_machine
from ..file_tag.h1.file_device_control.process_file import process_file as process_control
from ..file_tag.h1.file_sound_scenery.process_file import process_file as process_sound_scenery
from ..file_tag.h1.file_device_light_fixture.process_file import process_file as process_light_fixture
from ..file_tag.h1.file_bitmap.process_file import process_file as process_bitmap
from ..file_tag.h1.file_weapon.process_file import process_file as process_weapon
from ..file_tag.h1.file_item_collection.process_file import process_file as process_item_collection
from ..file_tag.h1.file_sky.process_file import process_file as process_sky

from ..file_tag.h1.file_shader_environment.process_file import process_file as process_shader_environment
from ..file_tag.h1.file_shader_model.process_file import process_file as process_shader_model
from ..file_tag.h1.file_shader_transparent_chicago.process_file import process_file as process_shader_transparent_chicago
from ..file_tag.h1.file_shader_transparent_chicago_extended.process_file import process_file as process_shader_transparent_chicago_extended
from ..file_tag.h1.file_shader_transparent_generic.process_file import process_file as process_shader_transparent_generic
from ..file_tag.h1.file_shader_transparent_glass.process_file import process_file as process_shader_transparent_glass
from ..file_tag.h1.file_shader_transparent_meter.process_file import process_file as process_shader_transparent_meter
from ..file_tag.h1.file_shader_transparent_plasma.process_file import process_file as process_shader_transparent_plasma
from ..file_tag.h1.file_shader_transparent_water.process_file import process_file as process_shader_transparent_water

from ..file_tag.h2.file_sky.process_file import process_file as process_h2_sky
from ..file_tag.h2.file_scenario_structure_bsp.process_file import process_file as process_h2_structure_bsp
from ..file_tag.h2.file_scenario_structure_lightmap.process_file import process_file as process_h2_structure_lightmap
from ..file_tag.h2.file_bitmap.process_file import process_file as process_h2_bitmap
from ..file_tag.h2.file_shader.process_file import process_file as process_h2_shader
from ..file_tag.h2.file_model.process_file import process_file as process_h2_model
from ..file_tag.h2.file_render_model.process_file import process_file as process_h2_render
from ..file_tag.h2.file_scenery.process_file import process_file as process_h2_scenery
from ..file_tag.h2.file_crate.process_file import process_file as process_h2_crate
from ..file_tag.h2.file_biped.process_file import process_file as process_h2_biped
from ..file_tag.h2.file_vehicle.process_file import process_file as process_h2_vehicle
from ..file_tag.h2.file_equipment.process_file import process_file as process_h2_equipment
from ..file_tag.h2.file_weapon.process_file import process_file as process_h2_weapon
from ..file_tag.h2.file_machine.process_file import process_file as process_h2_machine
from ..file_tag.h2.file_control.process_file import process_file as process_h2_control
from ..file_tag.h2.file_sound_scenery.process_file import process_file as process_h2_sound_scenery
from ..file_tag.h2.file_item_collection.process_file import process_file as process_h2_item_collection
from ..file_tag.h2.file_vehicle_collection.process_file import process_file as process_h2_vehicle_collection
from ..file_tag.h2.file_scenario_scenery_resource.process_file import process_file as process_h2_scenario_scenery_resource

def parse_tag(tagref, report, game_title, game_version):
    ASSET = None
    if game_title == "halo1":
        if tagref.tag_group == "actv":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.actor_variant" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_actor_variant(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "sky ":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.sky" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_sky(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "bitm":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.bitmap" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_bitmap(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "scen":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.scenery" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h1_scenery(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "bipd":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.biped" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_biped(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "vehi":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.vehicle" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_vehicle(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "mach":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.device_machine" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_machine(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "ctrl":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.device_control" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_control(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "lifi":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.device_light_fixture" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_light_fixture(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "ssce":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.sound_scenery" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_sound_scenery(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "eqip":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.equipment" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_equipment(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "weap":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.weapon" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_weapon(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "itmc":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.item_collection" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_item_collection(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "mod2" or tagref.tag_group == "mode":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.gbxmodel" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_mod2(input_stream, report)
                input_stream.close()
            else:
                input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.model" % tagref.name)
                if os.path.exists(input_file):
                    input_stream = open(input_file, 'rb')
                    ASSET = process_mode(input_stream, report)
                    input_stream.close()

        elif tagref.tag_group == "sbsp":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.scenario_structure_bsp" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h1_structure_bsp(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "senv":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.shader_environment" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_shader_environment(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "soso":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.shader_model" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_shader_model(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "schi":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.shader_transparent_chicago" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_shader_transparent_chicago(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "scex":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.shader_transparent_chicago_extended" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_shader_transparent_chicago_extended(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "sotr":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.shader_transparent_generic" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_shader_transparent_generic(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "sgla":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.shader_transparent_glass" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_shader_transparent_glass(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "smet":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.shader_transparent_meter" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_shader_transparent_meter(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "spla":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.shader_transparent_plasma" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_shader_transparent_plasma(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "swat":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.shader_transparent_water" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_shader_transparent_water(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "scnr":
            input_file = os.path.join(config.HALO_1_TAG_PATH, "%s.scenario" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h1_scenario(input_stream, report)
                input_stream.close()

    elif game_title == "halo2":
        if tagref.tag_group == "sky ":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.sky" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_sky(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "sbsp":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.scenario_structure_bsp" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_structure_bsp(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "ltmp":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.scenario_structure_lightmap" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_structure_lightmap(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "bitm":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.bitmap" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_bitmap(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "shad":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.shader" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_shader(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "hlmt":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.model" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_model(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "mode":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.render_model" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_render(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "scen":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.scenery" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_scenery(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "bloc":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.crate" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_crate(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "bipd":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.biped" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_biped(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "vehi":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.vehicle" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_vehicle(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "eqip":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.equipment" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_equipment(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "weap":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.weapon" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_weapon(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "mach":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.device_machine" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_machine(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "ctrl":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.device_control" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_control(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "ssce":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.sound_scenery" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_sound_scenery(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "itmc":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.item_collection" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_item_collection(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "vehc":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.vehicle_collection" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_vehicle_collection(input_stream, report)
                input_stream.close()

        elif tagref.tag_group == "*cen":
            input_file = os.path.join(config.HALO_2_TAG_PATH, "%s.scenario_scenery_resource" % tagref.name)
            if os.path.exists(input_file):
                input_stream = open(input_file, 'rb')
                ASSET = process_h2_scenario_scenery_resource(input_stream, report)
                input_stream.close()

    return ASSET
