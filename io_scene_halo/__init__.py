# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Steven Garcia
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

bl_info = {
    "name": "Halo Asset Blender Development Toolset",
    "author": "General_101",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "File > Import-Export",
    "description": "Import-Export Halo CE/2/3 Jointed Model Skeleton File (.jms), Import-Export Halo CE/2/3 Jointed Model Animation File (.jma), Import-Export Halo 2/3 Amalgam Scene Specification File (.ass), Import Halo CE Virtual Reality Modeling Language File (.wrl), and Export Halo 2 Vista H2Codez lightmap UV (.luv). Originally by Cyboryxmen with changes by Fulsy + MosesofEgypt + con for JMS portion. Initial ASS exporter by Dave Barnes (Aerial Dave). WRL importing originally by Con".,
    "warning": "",
    "wiki_url": "https://c20.reclaimers.net/tools/jointed-model-blender-toolset/",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

from . import global_ui
from . import file_ass
from . import file_jma
from . import file_jmi
from . import file_jms
from . import file_wrl
from . import misc

modules = [
    global_ui,
    file_ass,
    file_jma,
    file_jmi,
    file_jms,
    file_wrl,
    misc
]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in reversed(modules):
        module.unregister()

if __name__ == '__main__':
    register()
