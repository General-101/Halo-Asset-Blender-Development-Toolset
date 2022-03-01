# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

from .process_scene import process_scene
from ..global_functions import global_functions

def build_asset(context, filepath, extension, version, game_version, generate_checksum, frame_rate_value, fix_rotations, folder_structure, biped_controller, custom_scale):
    JMA = process_scene(context, version, generate_checksum, game_version, extension, custom_scale, biped_controller, fix_rotations)

    if version > 16394:
        decimal_1 = '\n%0.10f'
        decimal_2 = '\n%0.10f\t%0.10f'
        decimal_3 = '\n%0.10f\t%0.10f\t%0.10f'
        decimal_4 = '\n%0.10f\t%0.10f\t%0.10f\t%0.10f'

    else:
        decimal_1 = '\n%0.6f'
        decimal_2 = '\n%0.6f\t%0.6f'
        decimal_3 = '\n%0.6f\t%0.6f\t%0.6f'
        decimal_4 = '\n%0.6f\t%0.6f\t%0.6f\t%0.6f'

    filename = os.path.basename(filepath)

    root_directory = global_functions.get_directory(context, game_version, "animations", folder_structure, "0", False, filepath)

    file = open(root_directory + os.sep + filename + global_functions.get_true_extension(filepath, extension, False), 'w', encoding='utf_8')

    #write header
    if version >= 16394:
        file.write(
            '%s' % (version) +
            '\n%s' % (JMA.node_checksum) +
            '\n%s' % (JMA.transform_count) +
            '\n%s' % (frame_rate_value) +
            '\n%s' % (len(JMA.actor_names)) +
            '\n%s' % (JMA.actor_names[0]) +
            '\n%s' % (JMA.node_count)
            )

    else:
        file.write(
            '%s' % (version) +
            '\n%s' % (JMA.transform_count) +
            '\n%s' % (frame_rate_value) +
            '\n%s' % (len(JMA.actor_names)) +
            '\n%s' % (JMA.actor_names[0]) +
            '\n%s' % (JMA.node_count) +
            '\n%s' % (JMA.node_checksum)
            )

    if version >= 16391:
            for node in JMA.nodes:
                if version >= 16394:
                    file.write(
                        '\n%s' % (node.name) +
                        '\n%s' % (node.parent)
                        )

                else:
                    file.write('\n%s' % (node.name))
                    if version >= 16392:
                        file.write(
                            '\n%s' % (node.child) +
                            '\n%s' % (node.sibling)
                            )

    #write transforms
    for node_transform in JMA.transforms:
        for node in node_transform:
            file.write(
                decimal_3 % (node.translation[0], node.translation[1], node.translation[2]) +
                decimal_4 % (node.rotation[0], node.rotation[1], node.rotation[2], node.rotation[3]) +
                decimal_1 % (node.scale)
                )

    #H2 specific biped controller data bool value.
    if version > 16394:
        file.write('\n%s' % (int(biped_controller)))
        if biped_controller:
            for biped_transform in JMA.biped_controller_transforms:
                file.write(
                    decimal_3 % (biped_transform.translation[0], biped_transform.translation[1], biped_transform.translation[2]) +
                    decimal_4 % (biped_transform.rotation[0], biped_transform.rotation[1], biped_transform.rotation[2], biped_transform.rotation[3]) +
                    decimal_1 % (biped_transform.scale)
                    )

    file.write('\n')
    file.close()
