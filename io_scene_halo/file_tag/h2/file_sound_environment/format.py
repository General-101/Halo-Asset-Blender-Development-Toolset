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

class SoundEnvironmentAsset():
    def __init__(self, header=None, body_header=None, priority=0, room_intensity=0.0, room_intensity_hf=0.0, room_rolloff=0.0, decay_time=0.0, decay_hf_ratio=0.0, 
                 reflections_intensity=0.0, reflections_delay=0.0, reverb_intensity=0.0, reverb_delay=0.0, diffusion=0.0, density=0.0, hf_reference=0.0, reflection_type="", 
                 reflection_type_length=0):
        self.header = header
        self.body_header = body_header
        self.priority = priority
        self.room_intensity = room_intensity
        self.room_intensity_hf = room_intensity_hf
        self.room_rolloff = room_rolloff
        self.decay_time = decay_time
        self.decay_hf_ratio = decay_hf_ratio
        self.reflections_intensity = reflections_intensity
        self.reflections_delay = reflections_delay
        self.reverb_intensity = reverb_intensity
        self.reverb_delay = reverb_delay
        self.diffusion = diffusion
        self.density = density
        self.hf_reference = hf_reference
        self.reflection_type = reflection_type
        self.reflection_type_length = reflection_type_length
