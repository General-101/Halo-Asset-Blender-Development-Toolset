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

k_o_wavelengths = [300.0, 305.0, 310.0, 315.0, 320.0,
                   325.0, 330.0, 335.0, 340.0, 345.0,
                   350.0, 355.0, 445.0, 450.0, 455.0,
                   460.0, 465.0, 470.0, 475.0, 480.0,
                   485.0, 490.0, 495.0, 500.0, 505.0,
                   510.0, 515.0, 520.0, 525.0, 530.0,
                   535.0, 540.0, 545.0, 550.0, 555.0,
                   560.0, 565.0, 570.0, 575.0, 580.0,
                   585.0, 590.0, 595.0, 600.0, 605.0,
                   610.0, 620.0, 630.0, 640.0, 650.0,
                   660.0, 670.0, 680.0, 690.0, 700.0,
                   710.0, 720.0, 730.0, 740.0, 750.0,
                   760.0, 770.0, 780.0, 790.0]

k_o_amplitudes = [10.0, 4.8, 2.7, 1.35, .8,
                  .380, .160, .075, .04, .019,
                  .007, .0, .003, .003, .004,
                  .006, .008, .009, .012, .014,
                  .017, .021, .025, .03, .035,
                  .04, .045, .048, .057, .063,
                  .07, .075, .08, .085, .095,
                  .103, .110, .12, .122, .12,
                  .118, .115, .12, .125, .130,
                  .12, .105, .09, .079, .067,
                  .057, .048, .036, .028, .023,
                  .018, .014, .011, .010, .009,
                  .007, .004, .0, .0, 0]

k_g_wavelengths = [759.0, 760.0, 770.0, 771.0]

k_g_amplitudes = [0.0, 3.0, 0.210, 0.0]

k_wa_wavelengths = [689.0, 690.0, 700.0, 710.0, 720.0,
                    730.0, 740.0, 750.0, 760.0, 770.0,
                    780.0, 790.0, 800.0]

k_wa_amplitudes = [0.0, 0.160e-1, 0.240e-1, 0.125e-1, 0.100e+1,
                   0.870, 0.610e-1, 0.100e-2, 0.100e-4, 0.100e-4,
                   0.600e-3, 0.175e-1, 0.360e-1]

sol_amplitudes = [165.5, 162.3, 211.2, 258.8, 258.2,
                  242.3, 267.6, 296.6, 305.4, 300.6,
                  306.6, 288.3, 287.1, 278.2, 271.0,
                  272.3, 263.6, 255.0, 250.6, 253.1,
                  253.5, 251.3, 246.3, 241.7, 236.8,
                  232.1, 228.2, 223.4, 219.7, 215.3,
                  211.0, 207.3, 202.4, 198.7, 194.3,
                  190.7, 186.3, 182.6]

sun_artificial_tweak_curve = [6.2, 6.2, 6.2, 6.2, 6.2,
                              6.2, 6.2, 6.2, 6.2, 6.2,
                              6.2, 6.2, 6.2, 6.2, 6.2,
                              6.2]

k_cmf_wave_length = [380.0, 385.0, 390.0, 395.0, 400.0,
                     405.0, 410.0, 415.0, 420.0, 425.0,
                     430.0, 435.0, 440.0, 445.0, 450.0,
                     455.0, 460.0, 465.0, 470.0, 475.0,
                     480.0, 485.0, 490.0, 495.0, 500.0,
                     505.0, 510.0, 515.0, 520.0, 525.0,
                     530.0, 535.0, 540.0, 545.0, 550.0,
                     555.0, 560.0, 565.0, 570.0, 575.0,
                     580.0, 585.0, 590.0, 595.0, 600.0,
                     605.0, 610.0, 615.0, 620.0, 625.0,
                     630.0, 635.0, 640.0, 645.0, 650.0,
                     655.0, 660.0, 665.0, 670.0, 675.0,
                     680.0, 685.0, 690.0, 695.0, 700.0,
                     705.0, 710.0, 715.0, 720.0, 725.0,
                     730.0, 735.0, 740.0, 745.0, 750.0,
                     755.0, 760.0, 765.0, 770.0, 775.0,
                     780.0, 785.0, 790.0, 795.0, 800.0,
                     805.0, 810.0, 815.0, 820.0, 825.0]

k_cmf_X = [2.689900e-003, 5.310500e-003, 1.078100e-002, 2.079200e-002, 3.798100e-002,
           6.315700e-002, 9.994100e-002, 1.582400e-001, 2.294800e-001, 2.810800e-001,
           3.109500e-001, 3.307200e-001, 3.333600e-001, 3.167200e-001, 2.888200e-001,
           2.596900e-001, 2.327600e-001, 2.099900e-001, 1.747600e-001, 1.328700e-001,
           9.194400e-002, 5.698500e-002, 3.173100e-002, 1.461300e-002, 4.849100e-003,
           2.321500e-003, 9.289900e-003, 2.927800e-002, 6.379100e-002, 1.108100e-001,
           1.669200e-001, 2.276800e-001, 2.926900e-001, 3.622500e-001, 4.363500e-001,
           5.151300e-001, 5.974800e-001, 6.812100e-001, 7.642500e-001, 8.439400e-001,
           9.163500e-001, 9.770300e-001, 1.023000e+000, 1.051300e+000, 1.055000e+000,
           1.036200e+000, 9.923900e-001, 9.286100e-001, 8.434600e-001, 7.398300e-001,
           6.328900e-001, 5.335100e-001, 4.406200e-001, 3.545300e-001, 2.786200e-001,
           2.148500e-001, 1.616100e-001, 1.182000e-001, 8.575300e-002, 6.307700e-002,
           4.583400e-002, 3.205700e-002, 2.218700e-002, 1.561200e-002, 1.109800e-002,
           7.923300e-003, 5.653100e-003, 4.003900e-003, 2.825300e-003, 1.994700e-003,
           1.399400e-003, 9.698000e-004, 6.684700e-004, 4.614100e-004, 3.207300e-004,
           2.257300e-004, 1.597300e-004, 1.127500e-004, 7.951300e-005, 5.608700e-005,
           3.954100e-005, 2.785200e-005, 1.959700e-005, 1.377000e-005, 9.670000e-006,
           6.791800e-006, 4.770600e-006, 3.355000e-006, 2.353400e-006, 1.637700e-006]

k_cmf_Y = [2.000000e-004, 3.955600e-004, 8.000000e-004, 1.545700e-003, 2.800000e-003,
           4.656200e-003, 7.400000e-003, 1.177900e-002, 1.750000e-002, 2.267800e-002,
           2.730000e-002, 3.258400e-002, 3.790000e-002, 4.239100e-002, 4.680000e-002,
           5.212200e-002, 6.000000e-002, 7.294200e-002, 9.098000e-002, 1.128400e-001,
           1.390200e-001, 1.698700e-001, 2.080200e-001, 2.580800e-001, 3.230000e-001,
           4.054000e-001, 5.030000e-001, 6.081100e-001, 7.100000e-001, 7.951000e-001,
           8.620000e-001, 9.150500e-001, 9.540000e-001, 9.800400e-001, 9.949500e-001,
           1.000100e+000, 9.950000e-001, 9.787500e-001, 9.520000e-001, 9.155800e-001,
           8.700000e-001, 8.162300e-001, 7.570000e-001, 6.948300e-001, 6.310000e-001,
           5.665400e-001, 5.030000e-001, 4.417200e-001, 3.810000e-001, 3.205200e-001,
           2.650000e-001, 2.170200e-001, 1.750000e-001, 1.381200e-001, 1.070000e-001,
           8.165200e-002, 6.100000e-002, 4.432700e-002, 3.200000e-002, 2.345400e-002,
           1.700000e-002, 1.187200e-002, 8.210000e-003, 5.772300e-003, 4.102000e-003,
           2.929100e-003, 2.091000e-003, 1.482200e-003, 1.047000e-003, 7.401500e-004,
           5.200000e-004, 3.609300e-004, 2.492000e-004, 1.723100e-004, 1.200000e-004,
           8.462000e-005, 6.000000e-005, 4.244600e-005, 3.000000e-005, 2.121000e-005,
           1.498900e-005, 1.058400e-005, 7.465600e-006, 5.259200e-006, 3.702800e-006,
           2.607600e-006, 1.836500e-006, 1.295000e-006, 9.109200e-007, 6.356400e-007]

k_cmf_Z = [1.226000e-002, 2.422200e-002, 4.925000e-002, 9.513500e-002, 1.740900e-001,
           2.901300e-001, 4.605300e-001, 7.316600e-001, 1.065800e+000, 1.314600e+000,
           1.467200e+000, 1.579600e+000, 1.616600e+000, 1.568200e+000, 1.471700e+000,
           1.374000e+000, 1.291700e+000, 1.235600e+000, 1.113800e+000, 9.422000e-001,
           7.559600e-001, 5.864000e-001, 4.466900e-001, 3.411600e-001, 2.643700e-001,
           2.059400e-001, 1.544500e-001, 1.091800e-001, 7.658500e-002, 5.622700e-002,
           4.136600e-002, 2.935300e-002, 2.004200e-002, 1.331200e-002, 8.782300e-003,
           5.857300e-003, 4.049300e-003, 2.921700e-003, 2.277100e-003, 1.970600e-003,
           1.806600e-003, 1.544900e-003, 1.234800e-003, 1.117700e-003, 9.056400e-004,
           6.946700e-004, 4.288500e-004, 3.181700e-004, 2.559800e-004, 1.567900e-004,
           9.769400e-005, 6.894400e-005, 5.116500e-005, 3.601600e-005, 2.423800e-005,
           1.691500e-005, 1.190600e-005, 8.148900e-006, 5.600600e-006, 3.954400e-006,
           2.791200e-006, 1.917600e-006, 1.313500e-006, 9.151900e-007, 6.476700e-007,
           4.635200e-007, 3.330400e-007, 2.382300e-007, 1.702600e-007, 1.220700e-007,
           8.710700e-008, 6.145500e-008, 4.316200e-008, 3.037900e-008, 2.155400e-008,
           1.549300e-008, 1.120400e-008, 8.087300e-009, 5.834000e-009, 4.211000e-009,
           3.038300e-009, 2.190700e-009, 1.577800e-009, 1.134800e-009, 8.156500e-010,
           5.862600e-010, 4.213800e-010, 3.031900e-010, 2.175300e-010, 1.547600e-010]

S0Amplitudes = [0.04, 6.0, 29.6, 55.3, 57.3,
                61.8, 61.5, 68.8, 63.4, 65.8,
                94.8, 104.8, 105.9, 96.8, 113.9,
                125.6, 125.5, 121.3, 121.3, 113.5,
                113.1, 110.8, 106.5, 108.8, 105.3,
                104.4, 100.0, 96.0, 95.1, 89.1,
                90.5, 90.3, 88.4, 84.0, 85.1,
                81.9, 82.6, 84.9, 81.3, 71.9,
                74.3, 76.4, 63.3, 71.7, 77.0,
                65.2, 47.7, 68.6, 65.0, 66.0,
                61.0, 53.3, 58.9, 61.9]

S1Amplitudes = [0.02, 4.5, 22.4, 42.0, 40.6,
                41.6, 38.0, 42.4, 38.5, 35.0,
                43.4, 46.3, 43.9, 37.1, 36.7,
                35.9, 32.6, 27.9, 24.3, 20.1,
                16.2, 13.2, 8.6, 6.1, 4.2,
                1.9, 0.0, -1.6, -3.5, -3.5,
                -5.8, -7.2, -8.6, -9.5, -10.9,
                -10.7, -12.0, -14.0, -13.6, -12.0,
                -13.3, -12.9, -10.6, -11.6, -12.2,
                -10.2, -7.8, -11.2, -10.4, -10.6,
                -9.7, -8.3, -9.3, -9.8]

S2Amplitudes = [0.0, 2.0, 4.0, 8.5, 7.8,
                6.7, 5.3, 6.1, 3.0, 1.2,
                -1.1, -0.5, -0.7, -1.2, -2.6,
                -2.9, -2.8, -2.6, -2.6, -1.8,
                -1.5, -1.3, -1.2, -1.0, -0.5,
                -0.3, 0.0, 0.2, 0.5, 2.1,
                3.2, 4.1, 4.7, 5.1, 6.7,
                7.3, 8.6, 9.8, 10.2, 8.3,
                9.6, 8.5, 7.0, 7.6, 8.0,
                6.7, 5.2, 7.4, 6.8, 7.0,
                6.4, 5.5, 6.1, 6.5]

class XMVECTOR():
    def __init__(self, x = 0.0, y = 0.0, z = 0.0, w = 0.0, u = [0.0, 0.0, 0.0, 0.0], v = [0.0, 0.0, 0.0, 0.0]):
        self.x= x
        self.y= y
        self.z= z
        self.w= w
        self.u= u
        self.v= v

    def XMVectorMultiply(V1, V2):
        result = XMVECTOR()

        x = (V1.v[0] * V2.v[0])
        y = (V1.v[1] * V2.v[1])
        z = (V1.v[2] * V2.v[2])
        w = (V1.v[3] * V2.v[3])

        result.x = x
        result.y = y
        result.z = z
        result.w = w

        result.v = [x, y, z, w]

        return result

    def XMVectorMultiplyAdd(V1, V2, V3):
        result = XMVECTOR()

        x = (V1.v[0] * V2.v[0] + V3.v[0])
        y = (V1.v[1] * V2.v[1] + V3.v[1])
        z = (V1.v[2] * V2.v[2] + V3.v[2])
        w = (V1.v[3] * V2.v[3] + V3.v[3])

        result.x = x
        result.y = y
        result.z = z
        result.w = w

        result.v = [x, y, z, w]

        return result

    def XMVectorReplicate(Value):
        result = XMVECTOR()

        result.x = Value
        result.y = Value
        result.z = Value
        result.w = Value

        result.v = [Value, Value, Value, Value]

        return result

    def XMVectorSubtract(V1, V2):
        result = XMVECTOR()

        x = (V1.v[0] - V2.v[0])
        y = (V1.v[1] - V2.v[1])
        z = (V1.v[2] - V2.v[2])
        w = (V1.v[3] - V2.v[3])

        result.x = x
        result.y = y
        result.z = z
        result.w = w

        result.v = [x, y, z, w]

        return result

    def XMVectorLerp(V0, V1, t):
        scale = XMVECTOR.XMVectorReplicate(t)
        length = XMVECTOR.XMVectorSubtract(V1, V0)
        result = XMVECTOR.XMVectorMultiplyAdd(length, scale, V0)

        return result

    def XMVectorCatmullRom(Position0, Position1, Position2, Position3, t):
        t2 = t * t
        t3 = t * t2

        P0 = XMVECTOR.XMVectorReplicate((-t3 + 2.0 * t2 - t) * 0.5)
        P1 = XMVECTOR.XMVectorReplicate((3.0 * t3 - 5.0 * t2 + 2.0) * 0.5)
        P2 = XMVECTOR.XMVectorReplicate((-3.0 * t3 + 4.0 * t2 + t) * 0.5)
        P3 = XMVECTOR.XMVectorReplicate((t3 - t2) * 0.5)

        result = XMVECTOR.XMVectorMultiply(P0, Position0)
        result = XMVECTOR.XMVectorMultiplyAdd(P1, Position1, result)
        result = XMVECTOR.XMVectorMultiplyAdd(P2, Position2, result)
        result = XMVECTOR.XMVectorMultiplyAdd(P3, Position3, result)

        return result

class SkyHalo(object):
    def __init__(self):
        self.sun_theta = 0
        self.sun_phi = 0
        self.turpidity = 0
        self.sky_type = 0
        self.cie_sky_number = 0
        self.sky_intensity = 0
        self.sun_intensity = 0
        self.luminance_only = 0
        self.exposure = 0
        self.sun_cone_angle = 0
        self.sun_color_overide_bool = False
        self.sun_color_override = (0, 0, 0)
        self.sky_dome_radius = 0
        self.zenith_color = (0, 0, 0)
        self.haze_color = (0, 0, 0)
        self.zenith_color_override_bool = False
        self.horizon_color_override_bool = False
        self.horizon_haze_height = 0
        self.sun_blur = 0

def find_t(value, start, end):
    t = None
    if (value - start) <= 0.00001:
        t = 0.0

    else:
        t = (value - start) / (end - start)

    return t

class ColorxyY(object):
    def __init__(self, x = 0.0, y = 0.0, Y = 0.0):
        self.x = x
        self.y = y
        self.Y = Y

class ColorXYZ(object):
    def __init__(self, X = 0.0, Y = 0.0, Z = 0.0):
        self.X = X
        self.Y = Y
        self.Z = Z

class ColorRGB(object):
    def __init__(self, R = 0.0, G = 0.0, B = 0.0):
        self.R = R
        self.G = G
        self.B = B

    def set(self, R, G, B):
        self.R = R
        self.G = G
        self.B = B

class SpectralCurve():
    def __init__(self):
        self.control_points = []
        self.num_control_points = 0

    def populate_curve(self, num_of_points):
        self.control_points = [XMVECTOR() for i in range(91)]
        self.num_control_points = num_of_points

    def irregular_curve(self, wave_length, value, num_of_points):
        self.populate_curve(num_of_points)
        for i in range(num_of_points):
            x_value = 0.0
            if isinstance(value, float):
                x_value = wave_length

            elif isinstance(value, list):
                x_value = wave_length[i]

            y_value = 0.0
            if isinstance(value, float):
                y_value = value

            elif isinstance(value, list):
                y_value = value[i]

            self.control_points[i].x = x_value
            self.control_points[i].y = y_value
            self.control_points[i].z = 0.0
            self.control_points[i].w = 0.0
            self.control_points[i].v = [x_value, y_value, 0.0, 0.0]

        return self

    def regular_curve(self, start, end, value, num_of_points):
        self.populate_curve(num_of_points)
        for i in range(num_of_points):
            y_value = 0.0
            if isinstance(value, float):
                y_value = value

            elif isinstance(value, list):
                y_value = value[i]

            x_value = start + (end-start)/(num_of_points-1) * i

            self.control_points[i].x = x_value
            self.control_points[i].y = y_value
            self.control_points[i].z = 0.0
            self.control_points[i].w = 0.0
            self.control_points[i].v = [x_value, y_value, 0.0, 0.0]

        return self

    def get_value(self, wave_length):
        if wave_length >= self.control_points[self.num_control_points-1].x:
            return self.control_points[self.num_control_points-1].y

        if wave_length <= self.control_points[0].x:
            return self.control_points[0].y

        result = XMVECTOR()

        start = 0
        for i in range(self.num_control_points-1):
            if wave_length >= self.control_points[i].x and wave_length < self.control_points[i+1].x:
                start = i
                break

        t = find_t(wave_length, self.control_points[start].x, self.control_points[start+1].x)
        if start > 0 and start < self.num_control_points-2:
            result = XMVECTOR.XMVectorCatmullRom(self.control_points[start-1], self.control_points[start], self.control_points[start+1], self.control_points[start+2], t)

        else:
            result = XMVECTOR.XMVectorLerp(self.control_points[start], self.control_points[start+1], t)

        return result.y

    def convert_XYZ_to_RGB(self, src):
        RGB = ColorRGB()

        RGB.R = 3.240479 * src.X - 1.537150 * src.Y - 0.498535 * src.Z
        RGB.G = -0.969256 * src.X + 1.875991 * src.Y + 0.041556 * src.Z
        RGB.B = 0.055648 * src.X - 0.204043 * src.Y + 1.057311 * src.Z

        return RGB

    def convert_to_XYZ(self):
        XYZ = ColorXYZ()

        for wi in range(90):
            lambda_keyword_conflict = k_cmf_wave_length[wi]
            spectral = self.get_value(lambda_keyword_conflict)

            XYZ.X += spectral * k_cmf_X[wi]
            XYZ.Y += spectral * k_cmf_Y[wi]
            XYZ.Z += spectral * k_cmf_Z[wi]

        return XYZ

    def convert_to_RGB(self):
        XYZ = self.convert_to_XYZ()
        RGB = self.convert_XYZ_to_RGB(XYZ)

        return RGB.R, RGB.G, RGB.B
