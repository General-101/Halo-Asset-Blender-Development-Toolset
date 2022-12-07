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

def Export(export):
    export('INVOKE_DEFAULT')
    return {'FINISHED'}

def ExportQuick(export, report, context, export_gr2_files, export_hidden, export_all_bsps, export_all_perms, export_sidecar_xml, import_to_game, import_draft, lightmap_structure, lightmap_quality_h4, lightmap_quality, lightmap_specific_bsp, lightmap_all_bsps):
    export(export_gr2_files=export_gr2_files, export_hidden=export_hidden, export_all_bsps=export_all_bsps, export_all_perms=export_all_perms, export_sidecar_xml=export_sidecar_xml, import_to_game=import_to_game, import_draft=import_draft, lightmap_structure=lightmap_structure, lightmap_quality_h4=lightmap_quality_h4, lightmap_quality=lightmap_quality, lightmap_specific_bsp=lightmap_specific_bsp, lightmap_all_bsps=lightmap_all_bsps, quick_export=True)
    report({'INFO'}, context.scene.gr2_export.final_report)
    return {'FINISHED'}

