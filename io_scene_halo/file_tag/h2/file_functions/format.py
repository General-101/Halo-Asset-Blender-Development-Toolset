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

class FunctionTypeEnum(Enum):
    identity = 0
    constant = auto()
    transition = auto()
    periodic = auto()
    linear = auto()
    linear_key = auto()
    multi_linear_key = auto()
    spline = auto()
    multi_spline = auto()
    exponent = auto()
    spline2 = auto()

class OutputTypeFlags(Flag):
    scalar_intensity = 0
    _range = 1
    constant = 16
    _2_color = 32
    _3_color = 48
    _4_color = 64

class TransitionExponentEnum(Enum):
    linear = 0
    early = auto()
    very_early = auto()
    late = auto()
    very_late = auto()
    cosine = auto()
    one = auto()
    zero = auto()

class Function():
    def __init__(self, SCFN_header=None, MAPP_header=None, function_header=None, function_type=0, output_type=0, lower_bound=0.0, upper_bound=0.0, 
                 color_a=(0.0, 0.0, 0.0, 1.0), color_b=(0.0, 0.0, 0.0, 1.0), color_c=(0.0, 0.0, 0.0, 1.0), color_d=(0.0, 0.0, 0.0, 1.0), input_function_data=None, 
                 range_function_data=None):
        self.SCFN_header = SCFN_header
        self.MAPP_header = MAPP_header
        self.function_header = function_header
        self.function_type = function_type
        self.output_type = output_type
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.color_a = color_a
        self.color_b = color_b
        self.color_c = color_c
        self.color_d = color_d
        self.input_function_data = input_function_data
        self.range_function_data = range_function_data

class FunctionData:
    def __init__(self, function_min=0.0, function_max=1.0, exponent=0, frequency=1.0, phase=0.0, points=None):
        self.function_min = function_min
        self.function_max = function_max
        self.exponent = exponent
        self.frequency = frequency
        self.phase = phase
        self.points = points
