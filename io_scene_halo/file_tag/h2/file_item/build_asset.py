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

import struct

def write_predicted_bitmaps(output_stream, TAG, predicted_bitmaps, predicted_bitmaps_header):
    if len(predicted_bitmaps) > 0:
        predicted_bitmaps_header.write(output_stream, TAG, True)
        for predicted_bitmap_element in predicted_bitmaps:
            predicted_bitmap_element.write(output_stream, False, True)

        for predicted_bitmap_element in predicted_bitmaps:
            predicted_bitmap_length = len(predicted_bitmap_element.name)
            if predicted_bitmap_length > 0:
                output_stream.write(struct.pack('<%ssx' % predicted_bitmap_length, TAG.string_to_bytes(predicted_bitmap_element.name, False)))
