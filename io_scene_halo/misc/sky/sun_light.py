# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2021 Steven Garcia
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

import math

from .sky_math import (
        SpectralCurve,
        k_o_wavelengths,
        k_o_amplitudes,
        k_g_wavelengths,
        k_g_amplitudes,
        k_wa_wavelengths,
        k_wa_amplitudes,
        sol_amplitudes,
        sun_artificial_tweak_curve,
        ColorRGB,
        ColorxyY,
        ColorXYZ
        )

normalization_factor = 0.0175
sun_solid_angle = 0.00001 * 2.0 * math.pi

def clamp_positive(value):
    clamped_value = 0.0
    if value > 0.0:
        clamped_value = value

    return clamped_value

def convert_RGB_to_XYZ(src):
    XYZ = ColorXYZ()

    XYZ.X = 0.412424 * src.R + 0.357579 * src.G + 0.180464 * src.B
    XYZ.Y = 0.212656 * src.R + 0.715158 * src.G + 0.0721856 * src.B
    XYZ.Z = 0.0193324 * src.R + 0.119193 * src.G + 0.950444 * src.B

    return XYZ

def convert_XYZ_to_xyY(src):
    xyY = ColorxyY()

    xyY.x = src.X
    xyY.Y = src.Y
    xyY.y = src.Y
    if src.X > 0.0:
        xyY.x = src.X/(src.X + src.Y + src.Z)

    if src.Y > 0.0:
        xyY.y = src.Y/(src.X + src.Y + src.Z)

    return xyY

def convert_RGB_to_xyY(rgb):
    XYZ = convert_RGB_to_XYZ(rgb)
    xyY = convert_XYZ_to_xyY(XYZ)

    return xyY

def convert_xyY_to_XYZ(src):
    XYZ = ColorXYZ()

    XYZ.X = src.x * (src.Y / src.y)
    XYZ.Y = src.Y
    XYZ.Z = (1.0 - src.x - src.y)* (src.Y/src.y)

    return XYZ

def convert_XYZ_to_RGB(src):
    RGB = ColorRGB()

    RGB.R = 3.240479 * src.X - 1.537150 * src.Y - 0.498535 * src.Z
    RGB.G = -0.969256 * src.X + 1.875991 * src.Y + 0.041556 * src.Z
    RGB.B = 0.055648 * src.X - 0.204043 * src.Y + 1.057311 * src.Z

    return RGB

def convert_xyY_to_RGB(src):
    XYZ = convert_xyY_to_XYZ(src)
    RGB = convert_XYZ_to_RGB(XYZ)

    return RGB

def set_control_point(control_point, value):
    control_point.y = value
    control_point.v = [control_point.x, value, 0.0, 0.0]

    return control_point

class SunLight():
    def __init__(self):
        self.sun_spectral_curve = SpectralCurve().regular_curve(350, 800, 0, 91)

    def initialize_spectral_curve(self, sun_theta, turpidity):
        k_o_curve = SpectralCurve().irregular_curve(k_o_wavelengths, k_o_amplitudes, 64)
        k_g_curve = SpectralCurve().irregular_curve(k_g_wavelengths, k_g_amplitudes, 4)
        k_wa_curve = SpectralCurve().irregular_curve(k_wa_wavelengths, k_wa_amplitudes, 13)
        sol_curve = SpectralCurve().regular_curve(380, 750, sol_amplitudes, 38)
        artificial_tweak_curve = SpectralCurve().regular_curve(0.0, 1.5, sun_artificial_tweak_curve, 16)

        beta = 0.04608365822050 * turpidity - 0.04586025928522
        
        m = 1.0 / (math.cos(sun_theta) + 0.15 * math.pow(93.885 - sun_theta / math.pi * 180.0, -1.253))

        curve_value = 350.0
        for i in range(91):
            tau_r = math.exp(-m * 0.008735 * pow(curve_value / 1000.0, -4.08))
            alpha = 1.3
            tau_a = math.exp(-m * beta * pow(curve_value / 1000.0, -alpha))
            l_ozone = .35
            tau_o = math.exp(-m * clamp_positive(k_o_curve.get_value(curve_value)) * l_ozone)
            kg = clamp_positive(k_g_curve.get_value(curve_value))
            tau_g = math.exp(-1.41 * kg * m / math.pow(1.0 + 118.93 * kg * m, 0.45))
            w = 2.0
            wa = clamp_positive(k_wa_curve.get_value(curve_value))
            tau_wa = math.exp(-0.2385 * wa * w * m / math.pow(1.0 + 20.07 * wa * w * m, 0.45))
            amplitude = 100.0 * clamp_positive(sol_curve.get_value(curve_value)) * tau_r * tau_a * tau_o * tau_g * tau_wa

            if sun_theta < 0.0:
                sun_theta = 0.0

            elif sun_theta> 1.5:
                sun_theta = 1.5

            amplitude *= artificial_tweak_curve.get_value(sun_theta)

            self.sun_spectral_curve.control_points[i] = set_control_point(self.sun_spectral_curve.control_points[i], amplitude)

            curve_value += 5.0

    def get_sun_light_rgb(self, sky_halo):
        red, green, blue = self.sun_spectral_curve.convert_to_RGB()

        sr = red
        sg = green
        sb = blue
        if sky_halo.sun_color_overide_bool:
            rgb = ColorRGB()
            rgb.set(red, green, blue)
            xyY0 = convert_RGB_to_xyY(rgb)
            rgb.set(sky_halo.sun_color_override[0], sky_halo.sun_color_override[1], sky_halo.sun_color_override[2])
            xyY1 = convert_RGB_to_xyY(rgb)

            xyY1.Y = xyY0.Y
            rgb = convert_xyY_to_RGB(xyY1)
            sr = rgb.R
            sg = rgb.G
            sb = rgb.B

        sr *= normalization_factor
        sg *= normalization_factor
        sb *= normalization_factor

        return sr, sg, sb
