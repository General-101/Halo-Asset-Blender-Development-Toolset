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

from enum import Flag, Enum, auto

class MaterialTypeEnum(Enum):
    dirt = 0
    sand = auto()
    stone = auto()
    snow = auto()
    wood = auto()
    metal_hollow = auto()
    metal_thin = auto()
    metal_thick = auto()
    rubber = auto()
    glass = auto()
    force_field = auto()
    grunt = auto()
    hunter_armor = auto()
    hunter_skin = auto()
    elite = auto()
    jackal = auto()
    jackal_energy_shield = auto()
    engineer_skin = auto()
    enngineer_force_field = auto()
    flood_combat_form = auto()
    flood_carrier_form = auto()
    cyborg_armor = auto()
    cyborg_energy_shield = auto()
    human_armor = auto()
    human_skin = auto()
    sentinel = auto()
    monitor = auto()
    plastic = auto()
    water = auto()
    leaves = auto()
    elite_energy_shield = auto()
    ice = auto()
    hunter_shield = auto()

def get_material_name(material_type):
    h1_material = MaterialTypeEnum(material_type)
    h2_name = ""
    if h1_material == MaterialTypeEnum.dirt:
        h2_name = "tough_terrain_dirt"
    elif h1_material == MaterialTypeEnum.sand:
        h2_name = "tough_terrain_sand"
    elif h1_material == MaterialTypeEnum.stone:
        h2_name = "hard_terrain_stone"
    elif h1_material == MaterialTypeEnum.snow:
        h2_name = "soft_terrain_snow"
    elif h1_material == MaterialTypeEnum.wood:
        h2_name = "tough_organic_wood"
    elif h1_material == MaterialTypeEnum.metal_hollow:
        h2_name = "hard_metal_solid"
    elif h1_material == MaterialTypeEnum.metal_thin:
        h2_name = "hard_metal_thin"
    elif h1_material == MaterialTypeEnum.metal_thick:
        h2_name = "hard_metal_thick"
    elif h1_material == MaterialTypeEnum.rubber:
        h2_name = "tough_inorganic_rubber"
    elif h1_material == MaterialTypeEnum.glass:
        h2_name = "brittle_glass"
    elif h1_material == MaterialTypeEnum.force_field:
        h2_name = "energy_shield_invincible"
    elif h1_material == MaterialTypeEnum.grunt:
        h2_name = "soft_organic_flesh_grunt"
    elif h1_material == MaterialTypeEnum.hunter_armor:
        h2_name = "hard_metal_solid_cov_hunter"
    elif h1_material == MaterialTypeEnum.hunter_skin:
        h2_name = "soft_organic_flesh_hunter"
    elif h1_material == MaterialTypeEnum.elite:
        h2_name = "soft_organic_flesh_elite"
    elif h1_material == MaterialTypeEnum.jackal:
        h2_name = "soft_organic_flesh_jackal"
    elif h1_material == MaterialTypeEnum.jackal_energy_shield:
        h2_name = "energy_shield_thick_cov_jackal"
    elif h1_material == MaterialTypeEnum.engineer_skin:
        h2_name = "soft_organic_flesh_elite"
    elif h1_material == MaterialTypeEnum.enngineer_force_field:
        h2_name = "energy_shield_thick_cov_jackal"
    elif h1_material == MaterialTypeEnum.flood_combat_form:
        h2_name = "tough_floodflesh_combatform"
    elif h1_material == MaterialTypeEnum.flood_carrier_form:
        h2_name = "tough_floodflesh_carrierform"
    elif h1_material == MaterialTypeEnum.cyborg_armor:
        h2_name = "hard_metal_thin_hum_masterchief"
    elif h1_material == MaterialTypeEnum.cyborg_energy_shield:
        h2_name = "energy_shield_thin_hum_masterchief"
    elif h1_material == MaterialTypeEnum.human_armor:
        h2_name = "tough_inorganic_armor_hum"
    elif h1_material == MaterialTypeEnum.human_skin:
        h2_name = "soft_organic_flesh_human"
    elif h1_material == MaterialTypeEnum.sentinel:
        h2_name = "hard_metal_thin_for_sentinel_aggressor"
    elif h1_material == MaterialTypeEnum.monitor:
        h2_name = "hard_metal_thin_for_monitor"
    elif h1_material == MaterialTypeEnum.plastic:
        h2_name = "tough_inorganic_plastic"
    elif h1_material == MaterialTypeEnum.water:
        h2_name = "liquid_thin_water"
    elif h1_material == MaterialTypeEnum.leaves:
        h2_name = "soft_organic_plant_leafy"
    elif h1_material == MaterialTypeEnum.elite_energy_shield:
        h2_name = "energy_shield_thin_cov_elite"
    elif h1_material == MaterialTypeEnum.ice:
        h2_name = "hard_terrain_ice"
    elif h1_material == MaterialTypeEnum.hunter_shield:
        h2_name = "hard_metal_solid_cov_hunter"

    return h2_name
