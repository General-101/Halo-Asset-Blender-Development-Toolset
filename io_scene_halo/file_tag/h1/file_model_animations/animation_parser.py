import io
import struct
import base64

from copy import deepcopy
from sys import float_info
from types import MethodType
from struct import unpack_from
from enum import Flag, Enum, auto
from math import sqrt, log, cos, sin, acos, atan2, asin, pi

class AnimationTypeEnum(Enum):
    base = 0
    overlay = auto()
    replacement = auto()

class FrameInfoTypeEnum(Enum):
    none = 0
    dx_dy = auto()
    dx_dy_dyaw = auto()
    dx_dy_dz_dyaw = auto()

class AnimationFlags(Flag):
    compressed_data = auto()
    world_relative = auto()
    pal_25hz = auto()

class ConstantValues():
    def __init__(self):
        self.QUAT_EPSILON = 1/32767
        self.TRANS_EPSILON = 0.005
        self.SCALE_EPSILON = 0.000001
        self.DYAW_EPSILON = 0.00000001
        self.SCALE_INTERNAL_TO_JMA = 100.0

const = ConstantValues()
POLAR_SINGULARITY_SINE = 0.999999999999

# some retail tags don't have nodes due to their
# age, so we'll hardcode them here as a fallback.
# the key is a tuple of the node count and checksum
# maps to a tuple for each nod, looking like:
#   (name, first_child, first_sibling, parent)
JMA_RETAIL_NODES = {
    # characters\cyborg\cyborg
    (19, 1828349080): (
        ["bip01 pelvis",        2, -1, -1],
        ["bip01 l thigh",        4, 3, 0],
        ["bip01 r thigh",        5, 1, 0],
        ["bip01 spine",        6, -1, 0],
        ["bip01 l calf",        8, -1, 1],
        ["bip01 r calf",        11, -1, 2],
        ["bip01 spine1",        10, -1, 3],
        ["bip01 l clavicle",        13, 9, 6],
        ["bip01 l foot",        -1, -1, 4],
        ["bip01 neck",        12, -1, 6],
        ["bip01 r clavicle",        14, 7, 6],
        ["bip01 r foot",        -1, -1, 5],
        ["bip01 head",        -1, -1, 9],
        ["bip01 l upperarm",        15, -1, 7],
        ["bip01 r upperarm",        16, -1, 10],
        ["bip01 l forearm",        17, -1, 13],
        ["bip01 r forearm",        18, -1, 14],
        ["bip01 l hand",        -1, -1, 15],
        ["bip01 r hand",        -1, -1, 16],
        ),
    # digsite\weapons\plasma_rifle\01_gs\fp
    (42, 1525243607): (
        ["frame bone24",        2, -1, -1],
        ["frame l upperarm",    3, -1,  0],
        ["frame r upperarm",    4,  1,  0],
        ["frame l forearm",     5, -1,  1],
        ["frame r forearm",     6, -1,  2],
        ["frame l wriste",     12, -1,  3],
        ["frame r wriste",      7, -1,  4],
        ["frame gun",          29, 15,  6],
        ["frame l index low",  18, -1,  5],
        ["frame l middlelow",  19,  8,  5],
        ["frame l pinky low",  20, 11,  5],
        ["frame l ring low",   21,  9,  5],
        ["frame l thumb low",  22, 10,  5],
        ["frame r index low",  23, 17,  6],
        ["frame r middle low", 24, 13,  6],
        ["frame r pinky low",  25, 16,  6],
        ["frame r ring low",   26, 14,  6],
        ["frame r thumb low",  27, -1,  6],
        ["frame l index mid",  30, -1,  8],
        ["frame l middle mid", 31, -1,  9],
        ["frame l pinky mid",  32, -1, 10],
        ["frame l ring mid",   33, -1, 11],
        ["frame l thumb mid",  34, -1, 12],
        ["frame r index mid",  35, -1, 13],
        ["frame r middle mid", 36, -1, 14],
        ["frame r pinky mid",  37, -1, 15],
        ["frame r ring mid",   38, -1, 16],
        ["frame r thumb mid",  39, -1, 17],
        ["frame rod_left",     40, -1,  7],
        ["frame rod_right",    41, 28,  7],
        ["frame l index tip",  -1, -1, 18],
        ["frame l middle tip", -1, -1, 19],
        ["frame l pinky tip",  -1, -1, 20],
        ["frame l ring tip",   -1, -1, 21],
        ["frame l thumb tip",  -1, -1, 22],
        ["frame r index tip",  -1, -1, 23],
        ["frame r middle tip", -1, -1, 24],
        ["frame r pinky tip",  -1, -1, 25],
        ["frame r ring tip",   -1, -1, 26],
        ["frame r thumb tip",  -1, -1, 27],
        ["frame wing_left",    -1, -1, 28],
        ["frame wing_right",   -1, -1, 29],
        ),
    # characters\engineer\engineer
    (25, -256390784): (
        ('frame root',            7, -1, -1),
        ('frame ltop uparm',     11,  3,  0),
        ('frame neck',            9,  6,  0),
        ('frame rtop uparm',     13,  2,  0),
        ('frame sack01',         -1,  5,  0),
        ('frame sack02',         -1,  1,  0),
        ('frame sack03',         -1, -1,  0),
        ('frame sack06',         -1,  8,  0),
        ('frame tail01',         14,  4,  0),
        ('frame head',           -1, -1,  2),
        ('frame lbottom uparm',  19, 16,  8),
        ('frame ltop forarm',    20, -1,  1),
        ('frame rbottom uparm',  21, 10,  8),
        ('frame rtop forarm',    22, -1,  3),
        ('frame sack04',         17, 15,  8),
        ('frame sack05',         18, 12,  8),
        ('frame tail02',         -1, -1,  8),
        ('frame box01',          -1, -1, 14),
        ('frame box02',          -1, -1, 15),
        ('frame lbottom forarm', 23, -1, 10),
        ('frame ltop hand',      -1, -1, 11),
        ('frame rbottom foarm',  24, -1, 12),
        ('frame rtop hand',      -1, -1, 13),
        ('frame lbottom hand',   -1, -1, 19),
        ('frame rbottom hand',   -1, -1, 21),
        ),
    # levels\a10\devices\doors\door airlock\door airlock
    (4, -921384993): (
        ("frame door airlock", 2, -1, -1),
        ("frame in bottom",   -1, -1,  0),
        ("frame in top",      -1,  3,  0),
        ("frame top",         -1,  1,  0),
        ),
    # levels\a10\devices\doors\door cryo chamber\door cryo chamber
    (3, -2130918511): (
        ("frame door cryo",    1, -1, -1),
        ("frame door cryo l", -1,  2,  0),
        ("frame door cryo r", -1, -1,  0),
        ),
    # levels\a10\devices\doors\door jeff tube\door jeff tube
    (3, 303126628): (
        ("frame door jeff tube", 2, -1, -1),
        ("frame door l",        -1, -1,  0),
        ("frame door r",        -1,  1,  0),
        ),
    # levels\a10\devices\doors\door small\door small
    # levels\a10\devices\doors\door small no glass\door small no glass
    (3, -1054070559): (
        ("frame door small", 2, -1, -1),
        ("frame in bottom", -1, -1,  0),
        ("frame in top",    -1,  1,  0),
        ),
    # levels\a30\devices\beam emitter\beam emitter
    (2, -1073502840): (
        ("frame root",  1, -1, -1),
        ("frame beam", -1, -1,  0),
        ),
    # levels\a30\devices\torpedo_bridge\torpedo_bridge
    (9, 893764757): (
        ("frame root",           1, -1, -1),
        ("frame bridgeaback",    5,  2,  0),
        ("frame bridgeafront",   6,  3,  0),
        ("frame bridgebback",    7,  4,  0),
        ("frame bridgebfront",   8, -1,  0),
        ("frame emitteraback",  -1, -1,  1),
        ("frame emitterafront", -1, -1,  2),
        ("frame emitterbback",  -1, -1,  3),
        ("frame emitterbfront", -1, -1,  4),
        ),
    # levels\a50\devices\mustering_door\mustering_door
    (3, 16992281): (
        ("frame door root",   1, -1, -1),
        ("frame left door",  -1,  2,  0),
        ("frame right door", -1, -1,  0),
        ),
    # levels\b30\devices\interior tech objects\holo control equipment\holo control equipment
    (5, -1411630910): (
        ("frame root",             2, -1, -1),
        ("frame holo circle bot", -1,  3,  0),
        ("frame holo circle top", -1,  1,  0),
        ("frame holo equip bot",  -1,  4,  0),
        ("frame holo equip top",  -1, -1,  0),
        ),
    # levels\b30\devices\interior tech objects\holo control room display\holo control room display
    (21, -1377126976): (
        ("frame root",            1, -1, 0),
        ("frame hologramb30",     5, -1, 0),
        ("frame big marker01",   -1, -1, 1),
        ("frame big marker02",   -1,  2, 1),
        ("frame big marker03",   -1,  3, 1),
        ("frame sentinel01",     -1, 20, 1),
        ("frame small marker01", -1,  4, 1),
        ("frame small marker02", -1,  6, 1),
        ("frame small marker03", -1,  7, 1),
        ("frame small marker04", -1,  8, 1),
        ("frame small marker05", -1,  9, 1),
        ("frame small marker06", -1, 10, 1),
        ("frame small marker07", -1, 11, 1),
        ("frame small marker08", -1, 12, 1),
        ("frame small marker09", -1, 13, 1),
        ("frame small marker10", -1, 14, 1),
        ("frame small marker11", -1, 15, 1),
        ("frame small marker12", -1, 16, 1),
        ("frame small marker13", -1, 17, 1),
        ("frame small marker14", -1, 18, 1),
        ("frame small marker15", -1, 19, 1),
        ),
    # levels\b30\devices\interior tech objects\holo panel\holo panel
    (2, 265626): (
        ("frame root",   1, -1, -1),
        ("frame rotor", -1, -1,  0),
        ),
    # levels\c10\devices\bridge\bridge
    (5, -802003263): (
        ("frame root",      2, -1, -1),
        ("framen_big01",    3, -1,  0),
        ("frames_big01",    4,  1,  0),
        ("framen_small01", -1, -1,  1),
        ("frames_small01", -1, -1,  2),
        ),
    # levels\c20\devices\door_large\door_large
    (3, 743432): (
        ("frame root",    2, -1, -1),
        ("frame door l", -1, -1,  0),
        ("frame door r", -1,  1,  0),
        ),
    # levels\c20\devices\holo control\holo control
    (2, 1074060612): (
        ("frame root",    1, -1, -1),
        ("frame rotate", -1, -1,  0),
        ),
    # levels\c20\devices\holo radial control\holo radial control
    (8, 1141351629): (
        ("frame root",      4, -1, -1),
        ("frame rotate01", -1, -1,  0),
        ("frame rotate02", -1,  1,  0),
        ("frame rotate03", -1,  2,  0),
        ("frame rotate04", -1,  5,  0),
        ("frame rotate05", -1,  6,  0),
        ("frame rotate06", -1,  7,  0),
        ("frame rotate07", -1,  3,  0),
        ),
    # levels\c20\devices\holo tri control\holo tri control
    (6, 16583471): (
        ("frame root",      1, -1, -1),
        ("frame rotate01", -1,  5,  0),
        ("frame rotate02", -1, -1,  0),
        ("frame rotate03", -1,  2,  0),
        ("frame rotate04", -1,  3,  0),
        ("frame rotate05", -1,  4,  0),
        ),
    # levels\test\infinity\devices\beam emitter red\beam emitter red
    (2, -1073502840): (
        ("frame root",  1, -1, -1),
        ("frame beam", -1, -1,  0),
        ),
    # scenery\lightning\lightning
    (8, 830878205): (
        ('frame root',        3, -1, -1),
        ('frame link01',      4,  2,  0),
        ('frame link05',      5, -1,  0),
        ('frame link06',     -1,  1,  0),
        ('frame link02',      7, -1,  1),
        ('frame link04',      6, -1,  2),
        ('frame link end',   -1, -1,  5),
        ('frame link end01', -1, -1,  4),
        ),
    # levels\c10\scenery\c10_bigplant\c10_bigplant
    # scenery\plants\plant_broadleaf_short\plant_broadleaf_short
    (3, 1074195833): (
        ("frame base", 1, -1, -1),
        ("frame mid",  2, -1,  0),
        ("frame end", -1, -1,  1),
        ),
    # scenery\plants\plant_broadleaf_tall\plant_broadleaf_tall
    (7, -1033375598): (
        ("frame trunk",        2, -1, -1),
        ("frame brancha",      4,  3,  0),
        ("frame branchb",      5,  1,  0),
        ("frame branchc",      6, -1,  0),
        ("frame brancha end", -1, -1,  1),
        ("frame branchb end", -1, -1,  2),
        ("frame branchc end", -1, -1,  3),
        ),
    # scenery\trees\tree_leafy_doublewide\tree_leafy_doublewide
    (4, -1849496914): (
        ("frame tree root",     1, -1, -1),
        ("frame tree mid",      2, -1,  0),
        ("frame tree top",      3, -1,  1),
        ("frame tree top end", -1, -1,  2),
        ),
    # scenery\trees\tree_leafy_medium\tree_leafy_medium
    (3, 1089048985): (
        ("frame tree root",    1, -1, -1),
        ("frame tree mid",     2, -1,  0),
        ("frame tree topend", -1, -1,  1),
        ),
    # scenery\trees\tree_pine\tree_pine
    (2, -2147257918): (
        ("frame root", 1, -1, -1),
        ("frame mid", -1, -1,  0),
        ),
    # scenery\trees\tree_pine_snow\tree_pine_snow
    # scenery\trees\tree_pine_tall\tree_pine_tall
    (4, -804395985): (
        ("frame root", 1, -1, -1),
        ("frame mid",  2, -1,  0),
        ("frame top",  3, -1,  1),
        ("frame end", -1, -1,  2),
        ),
    # vehicles\warthog
    (18, -114204588) : (
        ('frame hull',                   1,  -1,  -1),
        ('frame gun mount base',         7,   6,   0),
        ('frame left back suspension',   9,  -1,   0),
        ('frame left front suspension',  10,  4,   0),
        ('frame right back suspension',  11,  2,   0),
        ('frame right front suspension', 12,  3,   0),
        ('frame steering wheel',         -1,  5,   0),
        ('frame chain',                  -1,  8,   1),
        ('frame gun',                    13, -1,   1),
        ('frame left back engine',       14, -1,   2),
        ('frame left front engine',      15, -1,   3),
        ('frame right back engine',      16, -1,   4),
        ('frame right front engine',     17, -1,   5),
        ('frame barrels',                -1, -1,   8),
        ('frame left back tire',         -1, -1,   9),
        ('frame left front tire',        -1, -1,  10),
        ('frame right back tire',        -1, -1,  11),
        ('frame right front tire',       -1, -1,  12),
        ),
    # vehicles\ghost
    (5, -1063303411): (
        ("frame hull",        4, -1, -1),
        ("frame guns",       -1, -1,  0),
        ("frame left flap",  -1,  1,  0),
        ("frame right flap", -1,  2,  0),
        ("frame seat",       -1,  3,  0),
        )
    }

class JmaNodeState:
    __slots__ = (
        "pos_x", "pos_y", "pos_z",
        "rot_i", "rot_j", "rot_k", "rot_w",
        "scale",
        )
    def __init__(self, pos_x=0.0, pos_y=0.0, pos_z=0.0,
                 rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0, scale=1.0):
        self.rot_i = rot_i
        self.rot_j = rot_j
        self.rot_k = rot_k
        self.rot_w = rot_w
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.scale = scale

    @property
    def quat(self):
        return Quaternion((self.rot_i, self.rot_j, self.rot_k, self.rot_w))

    def __repr__(self):
        return """JmaNodeState(
    x=%s, y=%s, z=%s,
    i=%s, j=%s, k=%s, w=%s,
    scale=%s
)""" % (self.pos_x, self.pos_y, self.pos_z,
        self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.scale)

    def __eq__(self, other):
        if (not isinstance(other, JmaNodeState)                 or
            abs(self.rot_i - other.rot_i) > const.QUAT_EPSILON  or
            abs(self.rot_j - other.rot_j) > const.QUAT_EPSILON  or
            abs(self.rot_k - other.rot_k) > const.QUAT_EPSILON  or
            abs(self.rot_w - other.rot_w) > const.QUAT_EPSILON  or
            abs(self.pos_x - other.pos_x) > const.TRANS_EPSILON or
            abs(self.pos_y - other.pos_y) > const.TRANS_EPSILON or
            abs(self.pos_z - other.pos_z) > const.TRANS_EPSILON or
            abs(self.scale - other.scale) > const.SCALE_EPSILON
            ):
            return False
        return True

    def __sub__(self, other):
        if not isinstance(other, JmaNodeState):
            raise TypeError("Cannot subtract %s from %s" %
                            (type(other), type(self)))
        return JmaNodeState(
            self.pos_x - other.pos_x, self.pos_y - other.pos_y,
            self.pos_z - other.pos_z, self.rot_i - other.rot_i,
            self.rot_j - other.rot_j, self.rot_k - other.rot_k,
            self.rot_w - other.rot_w, self.scale - other.scale,
            )
    
class JmaRootNodeState:
    __slots__ = (
        "dx", "dy", "dz", "dyaw",
        "x", "y", "z", "yaw",
        )
    def __init__(self, dx=0.0, dy=0.0, dz=0.0, dyaw=0.0,
                 x=0.0, y=0.0, z=0.0, yaw=0.0):
        self.dx, self.dy, self.dz, self.dyaw = dx, dy, dz, dyaw
        self.x,  self.y,  self.z,  self.yaw  =  x,  y,  z,  yaw

    def __repr__(self):
        return """JmaRootNodeState(
    dx=%s, dy=%s, dz=%s, dyaw=%s,
    x=%s, y=%s, z=%s, yaw=%s,
)""" % (self.dx, self.dy, self.dz, self.dyaw,
        self.x, self.y, self.z, self.yaw)

    def __eq__(self, other):
        if (not isinstance(other, JmaRootNodeState)           or
            abs(self.dx - other.dx)     > const.TRANS_EPSILON or
            abs(self.dy - other.dy)     > const.TRANS_EPSILON or
            abs(self.dz - other.dz)     > const.TRANS_EPSILON or
            abs(self.dyaw - other.dyaw) > const.DYAW_EPSILON
            ):
            return False
        return True

class CannotRowReduce(ValueError): pass
class MatrixNotInvertable(ValueError): pass
class QuaternionNotInvertable(ValueError): pass

class Vector(list):
    __slots__ = ()
    '''Implements the minimal methods required for messing with matrix rows'''
    def __neg__(self):
        return type(self)(-x for x in self)
    def __add__(self, other):
        new = type(self)(self)
        for i in range(len(other)): new[i] += other[i]
        return new
    def __sub__(self, other):
        new = type(self)(self)
        for i in range(len(other)): new[i] -= other[i]
        return new
    def __mul__(self, other):
        if isinstance(other, type(self)):
            return sum(self[i]*other[i] for i in range(len(self)))
        new = type(self)(self)
        for i in range(len(self)): new[i] *= other
        return new
    def __truediv__(self, other):
        if isinstance(other, type(self)):
            return cross_product(self, other)
        new = type(self)(self)
        for i in range(len(self)): new[i] /= other
        return new
    def __eq__(self, other):
        return are_vectors_equal(self, other)
    def __iadd__(self, other):
        for i in range(len(other)): self[i] += other[i]
        return self
    def __isub__(self, other):
        for i in range(len(other)): self[i] -= other[i]
        return self
    def __imul__(self, other):
        if isinstance(other, type(self)):
            raise NotImplementedError
        for i in range(len(self)): self[i] *= other
        return self
    def __itruediv__(self, other):
        if isinstance(other, type(self)):
            raise NotImplementedError
        for i in range(len(self)): self[i] /= other
        return self

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

class Ray(Vector):
    __slots__ = ()
    @property
    def is_zero(self): return not sum(bool(val) for val in self)
    @property
    def normalized(self):
        ray = type(self)(self)
        ray.normalize()
        return ray
    @property
    def magnitude_sq(self): return sum(v**2 for v in self)
    @property
    def magnitude(self): return sqrt(sum(v**2 for v in self))
    mag_sq = magnitude_sq
    mag = magnitude

    @classmethod
    def cross(cls, v0, v1):
        assert len(v0) >= 3
        assert len(v1) >= 3
        return cls(cross_product(v0, v1))
    @classmethod
    def dot(cls, v0, v1):
        assert len(v0) == len(v1)
        return dot_product(v0, v1)

    def cross_with(self, other):
        return self.cross(self, other)

    def dot_with(self, other):
        return self.dot(self, other)

    def normalize(self):
        div = self.magnitude
        if div:
            for i in range(len(self)): self[i] /= div

class FixedLengthList(list):
    __slots__ = ()
    def append(self, val):          raise NotImplementedError
    def extend(self, vals):         raise NotImplementedError
    def insert(self, index, val):   raise NotImplementedError
    def pop(self):                  raise NotImplementedError
    def __delitem__(self, index):   raise NotImplementedError
    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            if start > stop:
                start, stop = stop, start
            if start == stop:
                return
            elif step < 0:
                step = -step

            slice_size = (stop - start) // step

            if slice_size != len(val):
                raise ValueError(("attempt to assign sequence of size %s to "
                                  "slice of size %s") % (len(val), slice_size))

        list.__setitem__(self, index, val)

class MatrixRow(FixedLengthList, Vector):
    __slots__ = ()

    def append(self, val):
        raise ValueError("Cannot append on %s" % type(self))
    def extend(self, vals):
        raise ValueError("Cannot extend on %s" % type(self))
    def insert(self, index, val):
        raise ValueError("Cannot insert on %s" % type(self))
    def pop(self):
        raise ValueError("Cannot pop on %s" % type(self))
    def __delitem__(self, index):
        raise ValueError("Cannot delete in %s" % type(self))

class Matrix(list):
    width = 1
    height = 1

    def __init__(self, matrix=None, width=1, height=1, identity=False):
        if matrix is None:
            self.width = width
            self.height = height
            list.__init__(self, (MatrixRow((0,)*width) for i in range(height)))

            if identity and width <= height:
                # place the identity matrix into the inverse
                for i in range(self.width):
                    self[i][i] = 1.0
            return

        matrix_rows = []
        self.height = max(1, len(matrix))
        self.width = -1
        for row in matrix:
            if not hasattr(row, '__iter__'):
                row = [row]
            self.width = max(self.width, len(row))
            assert self.width and len(row) == self.width
            matrix_rows.append(MatrixRow(row[:]))
        list.__init__(self, matrix_rows)

    def __setitem__(self, index, new_row):
        assert len(new_row) == self.width
        list.__setitem__(self, index, MatrixRow(new_row))

    def __delitem__(self, index):
        self[index][:] = (0,)*self.width

    def __str__(self):
        matrix_str = "Matrix([\n%s])"
        insert_str = ''
        for row in self:
            insert_str += '%s,\n' % (row,)
        return matrix_str % insert_str

    def __neg__(self):
        return Matrix([-row for row in self])

    def __add__(self, other):
        assert isinstance(other, Matrix)
        assert self.width == other.width and self.height == other.height
        new = Matrix(self)
        for i in range(len(other)): new[i] += other[i]
        return new

    def __sub__(self, other):
        assert isinstance(other, Matrix)
        assert self.width == other.width and self.height == other.height
        new = Matrix(self)
        for i in range(len(other)): new[i] -= other[i]
        return new

    def __mul__(self, other):
        assert isinstance(other, (Matrix, int, float))
        if not isinstance(other, Matrix):
            new = Matrix(self)
            for row in new:
                row *= other
            return new

        assert self.width == other.height
        # transpose the matrix so its easier to work with
        new = Matrix(width=other.width, height=self.height)
        other = other.transpose

        # loop over each row in the new matrix
        for i in range(new.height):
            # loop over each column in the new matrix
            for j in range(new.width):
                # set the element equal to the dot product of the matrix rows
                new[i][j] = self[i]*other[j]

        return new

    def __truediv__(self, other):
        assert isinstance(other, (Matrix, int, float))
        if not isinstance(other, Matrix):
            new = Matrix(self)
            for row in new:
                row /= other
            return new
        assert self.width == other.height
        return self * other.inverse

    __repr__ = __str__
    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

    def __iadd__(self, other):
        assert isinstance(other, Matrix)
        assert self.width == other.width and self.height == other.height
        for i in range(len(other)): self[i] += other[i]
        return self

    def __isub__(self, other):
        assert isinstance(other, Matrix)
        assert self.width == other.width and self.height == other.height
        for i in range(len(other)): self[i] -= other[i]
        return self

    def __imul__(self, other):
        assert isinstance(other, (Matrix, int, float))
        if not isinstance(other, Matrix):
            for row in self:
                row *= other
            return self

        assert self.width == other.height
        # transpose the matrix so its easier to work with
        new = Matrix(width=other.width, height=self.height)
        other = other.transpose

        # loop over each row in the new matrix
        for i in range(new.height):
            # loop over each column in the new matrix
            for j in range(new.width):
                # set the element equal to the dot product of the matrix rows
                new[i][j] = self[i]*other[j]

        # replace the values in this matrix with those in the new matrix
        self.width = 0
        self.height = new.height
        for i in range(self.height):
            self.width = len(self[i])
            self[i] = new[i]

        return self

    def __itruediv__(self, other):
        assert isinstance(other, (Matrix, int, float))
        if not isinstance(other, Matrix):
            for row in self:
                row /= other
            return self
        self *= other.inverse
        return self

    def to_quaternion(self):
        assert self.width == 3
        assert self.height == 3
        return Quaternion(matrix_to_quaternion(self))

    @property
    def determinant(self):
        assert self.width == self.height, "Non-square matrices do not have determinants."
        if self.width == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]

        d = 0
        sub_matrix = Matrix(width=self.width - 1, height=self.height - 1)
        for i in range(self.width):
            for j in range(sub_matrix.height):
                for k in range(sub_matrix.width):
                    sub_matrix[j][k] = self[j+1][(i + k + 1) % self.width]
            d += self[0][i] * sub_matrix.determinant

        return d

    @property
    def transpose(self):
        transpose = Matrix(width=self.height, height=self.width)
        for r in range(self.height):
            for c in range(self.width):
                transpose[c][r] = self[r][c]
        return transpose

    @property
    def inverse(self):
        # cannot invert non-square matrices. check for that
        if self.width != self.height:
            raise MatrixNotInvertable("Cannot invert non-square matrix.")
        elif not self.determinant:
            raise MatrixNotInvertable("Matrix is non-invertible.")

        regular, inverse = self.row_reduce(
            Matrix(width=self.width, height=self.height, identity=True),
            find_best_reduction=True
            )

        return inverse

    def row_reduce(self, other, find_best_reduction=True):
        # cant row-reduce if number of columns is greater than number of rows
        assert self.width <= self.height

        # WIDTH NOTE: We will loop over the width rather than height for
        #     several things here, as we do not care about any rows that
        #     don't intersect the columns at a diagonal. Essentially we're
        #     treating a potentially non-square matrix as square(we're
        #     ignoring the higher numbered rows) by rearranging the rows.

        new_row_order = self.get_row_reduce_order(find_best_reduction)
        if new_row_order is None:
            raise CannotRowReduce(
                "Impossible to rearrange rows to row-reduce:\n%s" % self)

        reduced = Matrix(self)
        orig_other = list(other)
        # rearrange rows so diagonals are all non-zero
        for i in range(len(new_row_order)):
            reduced[i] = self[new_row_order[i]]
            other[i] = orig_other[new_row_order[i]]

        orig_reduced = Matrix(reduced)  # TEMP
        for i in range(self.width):  # read note about looping over width
            # divide both matrices by their diagonal values
            div = reduced[i][i]
            if not div:
                raise CannotRowReduce("Impossible to row-reduce.")

            reduced[i] /= div
            other[i] /= div

            # make copies of the rows that we can multiply for subtraction
            reduced_diff = MatrixRow(reduced[i])
            other_diff = MatrixRow(other[i])

            # loop over the rows NOT intersecting the column at the diagonal
            for j in range(self.width):
                if i == j:
                    continue
                # get the value that needs to be subtracted from
                # where this row intersects the current column
                mul = reduced[j][i]

                # subtract the difference row from each of the
                # rows above it to set everything in the column
                # above an below the diagonal intersection to 0
                reduced[j] -= reduced_diff*mul
                other[j] -= other_diff*mul

        return reduced, other

    def get_row_reduce_order(self, find_best_reduction=True):
        nonzero_diag_row_indices = list(set() for i in range(self.width))
        valid_row_orders = {}

        # determine which rows have a nonzero value on each diagonal
        for i in range(self.height):
            for j in range(self.width):
                if self[i][j]:
                    nonzero_diag_row_indices[j].add(i)

        self._get_valid_diagonal_row_orders(
            nonzero_diag_row_indices, valid_row_orders, find_best_reduction)

        # get the highest weighted row order
        test_matrix = Matrix(width=self.width, height=self.width)
        for weight in reversed(sorted(valid_row_orders)):
            for row_order in valid_row_orders[weight]:
                for i in range(len(row_order)):
                    test_matrix[i][:] = self[row_order[i]]

                # make sure the determinant of the matrix made from the
                # row order isn't zero. if it is, the matrix isnt solvable
                if test_matrix.determinant:
                    return row_order

        return None

    def _get_valid_diagonal_row_orders(self, row_indices, row_orders,
                                       choose_best=True, row_order=(),
                                       curr_column=0):
        row_order = list(row_order)
        column_count = len(row_indices)
        if not row_order:
            row_order = [None] * column_count

        # loop over each row with a non-zero value on this diagonal
        for i in row_indices[curr_column]:
            if row_orders and not choose_best:
                # found a valid row arrangement, don't keep checking
                break
            elif i in row_order:
                continue

            row_order[curr_column] = i
            if curr_column + 1 == column_count:
                weight = 1.0
                for j in range(len(row_order)):
                    weight *= abs(self[row_order[j]][j])

                # freeze this row order in place
                row_orders.setdefault(weight, []).append(tuple(row_order))
            else:
                # check the rest of the rows
                self._get_valid_diagonal_row_orders(
                    row_indices, row_orders, choose_best,
                    row_order, curr_column + 1)

class Quaternion(FixedLengthList, Ray):
    __slots__ = ()
    def __init__(self, initializer=(0, 0, 0, 1)):
        assert len(initializer) == 4
        list.__init__(self, initializer)
    def append(self, val):
        raise ValueError("Cannot append on %s" % type(self))
    def extend(self, vals):
        raise ValueError("Cannot extend on %s" % type(self))
    def insert(self, index, val):
        raise ValueError("Cannot insert on %s" % type(self))
    def pop(self):
        raise ValueError("Cannot pop on %s" % type(self))
    def __delitem__(self, index):
        raise ValueError("Cannot delete in %s" % type(self))

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            new = Quaternion(multiply_quaternions(self, other))
        else:
            new = Ray(self)
            for i in range(len(self)): new[i] *= other
        return new
    def __imul__(self, other):
        if isinstance(other, Quaternion):
            return Quaternion(multiply_quaternions(self, other))
        for i in range(len(self)): self[i] *= other
        return self
    __rmul__ = __mul__

    @property
    def i(self): return self[0]
    @i.setter
    def i(self, new_val): self[0] = float(new_val)
    @property
    def j(self): return self[1]
    @j.setter
    def j(self, new_val): self[1] = float(new_val)
    @property
    def k(self): return self[2]
    @k.setter
    def k(self, new_val): self[2] = float(new_val)
    @property
    def w(self): return self[3]
    @w.setter
    def w(self, new_val): self[3] = float(new_val)

    @property
    def to_euler(self):
        return Vector(quaternion_to_euler(*self))
    @property
    def to_axis_angle(self):
        return Vector(quaternion_to_axis_angle(*self))
    @property
    def to_matrix(self):
        return quaternion_to_matrix(*self)
    @property
    def inverse(self):
        copy = Quaternion(self)
        copy.invert()
        return copy

    def invert(self):
        div = self.i**2 + self.j**2 + self.k**2 + self.w**2
        if not div:
            raise QuaternionNotInvertable("%s is not invertable." % self)

        div = sqrt(div)
        self.i = -self.i / div
        self.j = -self.j / div
        self.k = -self.k / div
        self.w =  self.w / div

def decompress_quaternion48(word_0, word_1, word_2):
    '''Decompress a ones-signed 6byte quaternion to floats'''
    comp_rot = (word_2 & 0xFFff) | ((word_1 & 0xFFff)<<16) | ((word_0 & 0xFFff)<<32)
    w =  comp_rot & 4095
    k = (comp_rot >> 12) & 4095
    j = (comp_rot >> 24) & 4095
    i = (comp_rot >> 36) & 4095
    # avoid division by zero
    if i | j | k | w:
        if i & 0x800: i -= 4095
        if j & 0x800: j -= 4095
        if k & 0x800: k -= 4095
        if w & 0x800: w -= 4095
        length = 1.0 / sqrt(i**2 + j**2 + k**2 + w**2)
        return i * length, j * length, k * length, w * length
    return 0.0, 0.0, 0.0, 1.0

def lerp_blend_vectors(v0, v1, ratio):
    r1 = max(0.0, min(1.0, ratio))
    r0 = 1.0 - r1
    return [a*r0 + b*r1 for a, b in zip(v0, v1)]

def nlerp_blend_quaternions(q0, q1, ratio):
    r1 = max(0.0, min(1.0, ratio))
    r0 = 1.0 - ratio

    i0, j0, k0, w0 = q0
    i1, j1, k1, w1 = q1

    cos_half_theta = i0*i1 + j0*j1 + k0*k1 + w0*w1
    if cos_half_theta < 0:
        # need to change the vector rotations to be 2pi - rot
        r1 = -r1

    return [i0*r0 + i1*r1, j0*r0 + j1*r1, k0*r0 + k1*r1, w0*r0 + w1*r1]

def multiply_quaternions(q0, q1):
    i =  q0[0] * q1[3] + q0[1] * q1[2] - q0[2] * q1[1] + q0[3] * q1[0]
    j = -q0[0] * q1[2] + q0[1] * q1[3] + q0[2] * q1[0] + q0[3] * q1[1]
    k =  q0[0] * q1[1] - q0[1] * q1[0] + q0[2] * q1[3] + q0[3] * q1[2]
    w = -q0[0] * q1[0] - q0[1] * q1[1] - q0[2] * q1[2] + q0[3] * q1[3]
    div = i**2 + j**2 + k**2 + w**2
    if not div:
        # not sure if we should raise an error.
        # this multiplication makes no sense.
        i = j = k = 0.0
        w = 1.0
    else:
        div = sqrt(div)
        i /= div
        j /= div
        k /= div
        w /= div

    return type(q0)((i, j, k, w))

def cross_product(ray_a, ray_b):
    return ((ray_a[1]*ray_b[2] - ray_a[2]*ray_b[1],
             ray_a[2]*ray_b[0] - ray_a[0]*ray_b[2],
             ray_a[0]*ray_b[1] - ray_a[1]*ray_b[0]))

def dot_product(v0, v1):
    return sum(a*b for a, b in zip(v0, v1))

def are_vectors_equal(vector_0, vector_1, use_double_rounding=False,
                      round_adjust=0):
    mantissa_len = (53 if use_double_rounding else 23)
    for val_0, val_1 in zip(vector_0, vector_1):
        # take into account rounding errors for 32bit floats
        val = max(abs(val_0), abs(val_1))
        delta_max = 2**(
            int(log(val + float_info.epsilon, 2)) -
            mantissa_len) + abs(round_adjust)
        if abs(val_1 - val_0) > delta_max:
            return False
    return True

def euler_to_quaternion(y, p, r):
    '''Angles are expected to be in radians.'''
    c0, c1, c2 = cos(y / 2), cos(p / 2), cos(r / 2)
    s0, s1, s2 = sin(y / 2), sin(p / 2), sin(r / 2)
    return (s0*s1*c2 + c0*c1*s2, s0*c1*c2 + c0*s1*s2,
            c0*s1*c2 - s0*c1*s2, c0*c1*c2 - s0*s1*s2)

def quaternion_to_axis_angle(i, j, k, w):
    '''Angle returned is in radians.'''
    ray_len = sqrt(i**2 + j**2 + k**2 + w**2)
    i /= ray_len
    j /= ray_len
    k /= ray_len
    w /= ray_len

    length = sqrt(1 - w**2)
    if length == 0.0:
        return i, j, k, 0
    return i / length, j / length, k / length, 2 * acos(w)

def quaternion_to_matrix(i, j, k, w):
    return Matrix([
        (2*(0.5 - j*j - k*k),   2*(i*j + k*w),         2*(i*k - j*w)),
        (2*(i*j - k*w),         2*(0.5 - k*k - i*i),   2*(j*k + i*w)),
        (2*(i*k + j*w),         2*(j*k - i*w),         2*(0.5 - i*i - j*j)),
    ])

def matrix_to_quaternion(matrix):
    m00, m10, m20 = matrix[0]
    m01, m11, m21 = matrix[1]
    m02, m12, m22 = matrix[2]
    tr = m00 + m11 + m22

    if tr > 0:
        s = sqrt(tr+1.0) * 2
        i = (m21 - m12) / s
        j = (m02 - m20) / s
        k = (m10 - m01) / s
        w = 0.25 * s
    elif m00 > m11 and m00 > m22:
        s = sqrt(1.0 + m00 - m11 - m22) * 2
        i = 0.25 * s
        j = (m01 + m10) / s
        k = (m02 + m20) / s
        w = (m21 - m12) / s
    elif m11 > m22:
        s = sqrt(1.0 + m11 - m00 - m22) * 2
        i = (m01 + m10) / s
        j = 0.25 * s
        k = (m12 + m21) / s
        w = (m02 - m20) / s
    else:
        s = sqrt(1.0 + m22 - m00 - m11) * 2
        i = (m02 + m20) / s
        j = (m12 + m21) / s
        k = 0.25 * s
        w = (m10 - m01) / s

    return i, j, k, w

def quaternion_to_euler(i, j, k, w):
    '''Angles returned are in radians.'''
    p_sin = 2*(i * j + k * w)
    # check for singularities at north and south poles
    if abs(p_sin) < POLAR_SINGULARITY_SINE:
        y = atan2(2*(j*w - i*k), 1 - 2*(j**2 + k**2))
        p = asin(p_sin)
        r = atan2(2*(i*w - j*k), 1 - 2*(i**2 + k**2))
    else:
        y, p, r = (2*atan2(i, w), pi/2, 0)
        if p_sin < 0:
            y, p = -y, -p

    return y, p, r

def get_anim_flags(anim):
    rot_flags, trans_flags, scale_flags = [], [], []
    for flags, flags_int in (
        [rot_flags,   anim["node rotation flag data"]   | (anim["node rotation flag data_1"]<<32)  ],
        [trans_flags, anim["node transform flag data"] | (anim["node transform flag data_1"]<<32)],
        [scale_flags, anim["node scale flag data"] | (anim["node scale flag data_1"]<<32)],
        ):
        flags.extend(bool(flags_int & (1 << i)) for i in range(anim["node count"]))

    return rot_flags, trans_flags, scale_flags

def get_base_anim_for_overlay(animation_idx, animation_data):
    # NOTE: this function is quite a bit of best-guess-work and
    #       hopes and prayers. There's not really a simple way
    #       to figure out what base animation is best to use for
    #       an overlay, so this was hand-tuned till it worked out
    unit_anims = animation_data["units"]
    fp_sets    = animation_data["first person weapons"]
    anims      = animation_data["animations"]
    to_check   = set(range(len(anims)))

    o_anim, b_anim = anims[animation_idx], None
    fallback_anim_1 = fallback_anim_2 = None
    o_name = o_anim["name"].lower()
    o_name_parts = o_name.split(" ") + ["", ""]

    # check for all indices in permutation chains
    o_anim_indices = set([animation_idx])
    for i, anim in enumerate(anims):
        anim_chain = set([i])
        while anim["next animation"] in to_check:
            anim_chain.add(anim["next animation"])
            anim = anims[anim["next animation"]]

        if animation_idx in anim_chain:
            o_anim_indices.update(anim_chain)

    anim_sets = [
        [anim["animation"] for anim in anim_set["animations"]
         if anim["animation"] in to_check]
        for anim_set in fp_sets
        ]

    is_weap = False
    for unit in unit_anims:
        unit_anim_sets = []

        for uw_anim in unit["weapons"]:
            unit_anim_sets.append([])
            unit_anim_sets[-1].extend(
                anim["animation"] for anim in uw_anim["animations"]
                if anim["animation"] in to_check
                )
            for weap_type in uw_anim["weapon types"]:
                unit_anim_sets[-1].extend(
                    anim["animation"] for anim in weap_type["animations"]
                    if anim["animation"] in to_check
                    )
            is_weap |= (unit["label"].lower() in o_name_parts[0] and
                        o_name_parts[1] in uw_anim["name"].lower())

        unit_anim_set = []
        [unit_anim_set.extend(anim_set) for anim_set in unit_anim_sets]
        unit_anim_set.extend(
            anim["animation"] for anim in unit["animations"]
            if anim["animation"] in to_check
            )

        anim_sets.extend([*unit_anim_sets, unit_anim_set])

    for indices in anim_sets:
        # find an idle animation that matches this(and a fallback)
        if b_anim:
            break
        elif not o_anim_indices.intersection(indices):
            continue

        for i in indices:
            anim = anims[i] if i in to_check else None
            to_check.discard(i)

            # find the first valid base animation we can use
            if not anim:
                continue
            else:
                animation_type = AnimationTypeEnum(anim["type"]["value"])
                if not animation_type != AnimationTypeEnum.base:
                    continue
                    
            b_name = anim["name"].lower()
            b_name_parts = b_name.split(" ") + ["", ""]

            if "idle" not in b_name:
                fallback_anim_2 = anim
            elif b_name_parts[0] == o_name_parts[0]:
                b_anim = anim
                if is_weap and b_name_parts[1] == o_name_parts[1]:
                    break
            else:
                fallback_anim_1 = anim

    for anim in (() if b_anim else anims):
        # find a useful base if we can't find a more fitting one
        animation_type = AnimationTypeEnum(anim["type"]["value"])
        if animation_type != AnimationTypeEnum.base:
            continue

        b_name = anim["name"].lower()
        b_name_parts = b_name.split(" ") + ["", ""]

        if "idle" not in b_name:
            continue
        elif ((("stand" in b_name or "alert" in b_name) and
               ("stand" in o_name or "alert" in o_name or
                o_name.startswith("h-ping") or
                o_name.startswith("s-ping"))
               )   or
              ("crouch"  in o_name and "crouch"  in b_name) or
              ("flee"    in o_name and "flee"    in b_name) or
              ("flaming" in o_name and "flaming" in b_name)):
            b_anim = anim
            if is_weap and b_name_parts[1] == o_name_parts[1]:
                break
        elif not fallback_anim_1:
            fallback_anim_1 = anim

    b_anim = b_anim or fallback_anim_1 or fallback_anim_2

    return b_anim

def get_frame_from_keyframe_data(
        frame_index, keyframes_start, keyframes_end, keyframes,
        frame_0, keyframe_data, blender
        ):
    if keyframes_start >= keyframes_end or frame_index == 0:
        # first frame OR only default data stored for this node
        return frame_0

    last_kf  = keyframes[keyframes_end]
    if frame_index == last_kf:
        # frame is the last keyframe. repeat it to the end
        return keyframe_data[keyframes_end]

    first_kf = keyframes[keyframes_start]
    if frame_index < first_kf:
        # frame is before the first stored keyframe.
        # blend from default data to first keyframe.
        frame_b = keyframe_data[keyframes_start]
        ratio   = frame_index / first_kf
        return blender(frame_0, frame_b, ratio)

    # frame is at/past the first stored keyframe.
    # don't need to use default data at all.

    # find the keyframes this frame is between
    for kf_i in range(keyframes_start, keyframes_end):
        # TODO: make this more efficent using a binary search
        if (keyframes[kf_i]  <= frame_index and
            keyframes[kf_i+1] > frame_index):
            break

        # NOTE: unless the animation is broken, this will never
        #       be hit. commenting out for speed, as there's not
        #       really a good reason to keep it in
        #elif kf_i == keyframes_end:
        #    raise ValueError(f"No keyframes pairs containing frame {frame_index}")

    frame_a = keyframe_data[kf_i]
    if frame_index == keyframes[kf_i]:
        # this keyframe is the frame we want.
        # no blending required
        return frame_a

    frame_b = keyframe_data[kf_i+1]
    ratio   = ((      frame_index - keyframes[kf_i]) /
               (keyframes[kf_i+1] - keyframes[kf_i]))

    return blender(frame_a, frame_b, ratio)

class CompressedFrames:
    def __init__(self, rotation_offsets=None, translation_offsets=None, scale_offsets=None, rotation=None, translation=None, scale=None):
        self.rotation_offsets = rotation_offsets
        self.translation_offsets = translation_offsets
        self.scale_offsets = scale_offsets
        self.rotation = rotation
        self.translation = translation
        self.scale = scale

class FrameData:
    def __init__(self, keyframe_head=None, keyframes=None, default_data=None, keyframe_data=None):
        self.keyframe_head = keyframe_head
        self.keyframes = keyframes
        self.default_data = default_data
        self.keyframe_data = keyframe_data

def get_keyframe_data(animation, channel, channel_flags, input_stream, channel_type, data_size):
    unpack_string = '<HHH'
    unpack_length = 6
    if channel_type == "r":
        unpack_string = '<HHH'
        unpack_length = 6
    elif channel_type == "t":
        unpack_string = '<fff'
        unpack_length = 12
    elif channel_type == "s":
        unpack_string = '<f'
        unpack_length = 4

    node_count = animation["node count"]
    channel.keyframe_head = []
    channel.keyframes = []
    channel.default_data = []
    channel.keyframe_data = []
    for node_idx in range(node_count):
        if channel_flags[node_idx] == True:
            if (data_size - input_stream.tell()) >= 4:
                keyframe_head = struct.unpack('<I', input_stream.read(4))[0]
                channel.keyframe_head.append(keyframe_head)

    kf_index = 0
    for node_idx in range(node_count):
        if channel_flags[node_idx] == True:
            keyframe_value = channel.keyframe_head[kf_index]
            keyframe_count = keyframe_value & 4095
            keyframe_count2 = keyframe_value >> 12
            for keyframe_idx in range(keyframe_count):
                if (data_size - input_stream.tell()) >= 2:
                    channel.keyframes.append(struct.unpack('<H', input_stream.read(2))[0])
            kf_index += 1

    for node_idx in range(node_count):
        valid_index = True
        if channel_type == "s":
            valid_index = channel_flags[node_idx]

        if valid_index:
            if (data_size - input_stream.tell()) >= unpack_length:
                results = struct.unpack(unpack_string, input_stream.read(unpack_length))
                for result in results:
                    channel.default_data.append(result)

    kfd_index = 0
    for node_idx in range(node_count):
        if channel_flags[node_idx] == True:
            keyframe_value = channel.keyframe_head[kfd_index]
            keyframe_count = keyframe_value & 4095
            keyframe_count2 = keyframe_value >> 12
            for keyframe_idx in range(keyframe_count):
                if (data_size - input_stream.tell()) >= unpack_length:
                    results = struct.unpack(unpack_string, input_stream.read(unpack_length))
                    for result in results:
                        channel.keyframe_data.append(result)
                else:
                    print('were out of space')
        

            kfd_index += 1

def deserialize_comp_frame_data(anim, get_default_data=False, include_extra_base_frame=True, pos_scale=1.0):
    r_kfs_by_nodes = []
    t_kfs_by_nodes = []
    s_kfs_by_nodes = []

    keyframes = (r_kfs_by_nodes, t_kfs_by_nodes, s_kfs_by_nodes)
    animation_flags = AnimationFlags(anim["flags"])
    if AnimationFlags.compressed_data not in animation_flags:
        return keyframes, ()

    decomp_quat = decompress_quaternion48
    blend_trans = lerp_blend_vectors
    blend_quats = nlerp_blend_quaternions
    blend_scale = lambda scale_0, scale_1, ratio: (
        scale_0 * (1 - ratio) + scale_1 * ratio
        )
    pos_scale  *= const.SCALE_INTERNAL_TO_JMA

    frame_count = 1 if get_default_data else anim["frame count"]

    # make a bunch of frames we can fill in below
    frames = [[JmaNodeState() for n in range(anim["node count"])]
              for f in range(frame_count)]

    r_flags, t_flags, s_flags = get_anim_flags(anim)

    try:
        # parse the compressed animation block
        frame_data_data = io.BytesIO(base64.b64decode(anim["frame data"]["encoded"]))
        data_offset = anim["offset to compressed data"]
        frame_data_data.seek(data_offset, 0)
        data_size = len(frame_data_data.getbuffer())

        rotation_offsets = FrameData()
        translation_offsets = FrameData()
        scale_offsets = FrameData()
        rotation = FrameData()
        translation = FrameData()
        scale = FrameData()

        cab = CompressedFrames()
        cab.rotation_offsets = rotation_offsets
        cab.translation_offsets = translation_offsets
        cab.scale_offsets = scale_offsets
        cab.rotation = rotation
        cab.translation = translation
        cab.scale = scale

        rotation_offsets.keyframe_head = 0
        rotation_offsets.keyframes = struct.unpack('<I', frame_data_data.read(4))[0]
        rotation_offsets.default_data = struct.unpack('<I', frame_data_data.read(4))[0]
        rotation_offsets.keyframe_data = struct.unpack('<I', frame_data_data.read(4))[0]

        translation_offsets.keyframe_head = struct.unpack('<I', frame_data_data.read(4))[0]
        translation_offsets.keyframes = struct.unpack('<I', frame_data_data.read(4))[0]
        translation_offsets.default_data = struct.unpack('<I', frame_data_data.read(4))[0]
        translation_offsets.keyframe_data = struct.unpack('<I', frame_data_data.read(4))[0]

        scale_offsets.keyframe_head = struct.unpack('<I', frame_data_data.read(4))[0]
        scale_offsets.keyframes = struct.unpack('<I', frame_data_data.read(4))[0]
        scale_offsets.default_data = struct.unpack('<I', frame_data_data.read(4))[0]
        scale_offsets.keyframe_data = struct.unpack('<I', frame_data_data.read(4))[0]

        rotation_offset = data_offset + 44
        frame_data_data.seek(rotation_offset, 0)
        get_keyframe_data(anim, rotation, r_flags, frame_data_data, "r", data_size)

        translation_offset = data_offset + translation_offsets.keyframe_head
        frame_data_data.seek(translation_offset, 0)
        get_keyframe_data(anim, translation, t_flags, frame_data_data, "t", data_size)

        scale_offset = data_offset + scale_offsets.keyframe_head
        frame_data_data.seek(scale_offset, 0)
        get_keyframe_data(anim, scale, s_flags, frame_data_data, "s", data_size)
    except Exception:
        cab = None

    if not cab:
        raise Exception("Failed to parse compressed animations "
                        "block. It may be corrupt.")

    # shorthands
    cab_r, cab_t, cab_s = cab.rotation, cab.translation, cab.scale

    # get the keyframe counts and keyframe offsets
    r_kf_headers, t_kf_headers, s_kf_headers = [
        [(v&4095, v>>12) for v in block.keyframe_head]
        for block in (cab_r, cab_t, cab_s)
        ]

    r_kfs, t_kfs, s_kfs = cab_r.keyframes, cab_t.keyframes, cab_s.keyframes

    r_ddata, r_fdata = cab_r.default_data, cab_r.keyframe_data
    t_ddata, t_fdata = cab_t.default_data, cab_t.keyframe_data
    s_ddata, s_fdata = cab_s.default_data, cab_s.keyframe_data

    def_node_states = [JmaNodeState() for n in range(anim["node count"])]

    # convert keyframe data into lists of component sets
    r_fdata = [decomp_quat(*r_fdata[i: i+3])
               for i in range(0, len(r_fdata), 3)]
    t_fdata = [t_fdata[i: i+3] for i in range(0, len(t_fdata), 3)]

    animation_type = AnimationTypeEnum(anim["type"]["value"])
    is_overlay = AnimationTypeEnum.overlay == animation_type
    ri = ti = si = 0
    for ni, def_ns in enumerate(def_node_states):
        r_def = decomp_quat(*r_ddata[3*ni: 3*(ni + 1)])
        t_def = t_ddata[3*ni: 3*(ni + 1)]
        s_def = s_ddata[si] if s_flags[ni] else 1.0

        def_ns.rot_i = r_def[0]
        def_ns.rot_j = r_def[1]
        def_ns.rot_k = r_def[2]
        def_ns.rot_w = r_def[3]

        def_ns.pos_x = t_def[0] * pos_scale
        def_ns.pos_y = t_def[1] * pos_scale
        def_ns.pos_z = t_def[2] * pos_scale

        def_ns.scale = s_def

        ri, r_kf_ct, r_kf_off = ((ri+1, *r_kf_headers[ri])
                                 if r_flags[ni] else (ri, 0, 0))
        ti, t_kf_ct, t_kf_off = ((ti+1, *t_kf_headers[ti])
                                 if t_flags[ni] else (ti, 0, 0))
        si, s_kf_ct, s_kf_off = ((si+1, *s_kf_headers[si])
                                 if s_flags[ni] else (si, 0, 0))

        # add this nodes keyframes to the keyframe lists in the jma_anim
        for kf_ct, kf_off, all_kfs, kfs_by_nodes in (
                (r_kf_ct, r_kf_off, r_kfs, r_kfs_by_nodes),
                (t_kf_ct, t_kf_off, t_kfs, t_kfs_by_nodes),
                (s_kf_ct, s_kf_off, s_kfs, s_kfs_by_nodes)):
            kfs_by_nodes.append(list(all_kfs[kf_off: kf_off + kf_ct]))

        r_kf_end = r_kf_off + r_kf_ct - 1
        t_kf_end = t_kf_off + t_kf_ct - 1
        s_kf_end = s_kf_off + s_kf_ct - 1
        for fi in range(frame_count):
            node_frame = frames[fi][ni]

            # decompress rotation
            qi, qj, qk, qw = get_frame_from_keyframe_data(
                fi, r_kf_off, r_kf_end, r_kfs,
                r_def, r_fdata, blend_quats
                )
            mag         = qi**2 + qj**2 + qk**2 + qw**2
            qw, q_scale = (qw, 1/sqrt(mag)) if mag else (1.0, 1)

            node_frame.rot_i = qi * q_scale
            node_frame.rot_j = qj * q_scale
            node_frame.rot_k = qk * q_scale
            node_frame.rot_w = qw * q_scale

            # decompress position
            x, y, z = get_frame_from_keyframe_data(
                fi, t_kf_off, t_kf_end, t_kfs,
                t_def, t_fdata, blend_trans
                )
            node_frame.pos_x = x * pos_scale
            node_frame.pos_y = y * pos_scale
            node_frame.pos_z = z * pos_scale

            # decompress scale
            node_frame.scale = get_frame_from_keyframe_data(
                fi, s_kf_off, s_kf_end, s_kfs,
                s_def, s_fdata, blend_scale
                )

    if include_extra_base_frame and not get_default_data:
        # overlay animations start with frame 0 being
        # in the same state as the default node states
        is_overlay and frames.insert(0, def_node_states)

        # non-overlays duplicate the first frame to the last frame
        is_overlay or  frames.append(deepcopy(frames[0]))

    return keyframes, frames

def _deserialize_uncomp_frame_data(anim, get_default_data=False, def_node_states=(), endian=">", pos_scale=1.0):
    unpack_rot   = MethodType(unpack_from, endian + "4h")
    unpack_trans = MethodType(unpack_from, endian + "3f")
    unpack_scale = MethodType(unpack_from, endian +  "f")
    pos_scale   *= const.SCALE_INTERNAL_TO_JMA

    r_flags, t_flags, s_flags = get_anim_flags(anim)
    r_incs = [8  * (f != get_default_data) for f in r_flags]
    t_incs = [12 * (f != get_default_data) for f in t_flags]
    s_incs = [4  * (f != get_default_data) for f in s_flags]

    default_data_data = base64.b64decode(anim["default data"]["encoded"])
    frame_data_data = base64.b64decode(anim["frame data"]["encoded"])

    data, frame_count = ((default_data_data, 1) if get_default_data else (frame_data_data, anim["frame count"]))
    all_node_states = [[JmaNodeState() for n in range(anim["node count"])] for f in range(frame_count)]

    if get_default_data or not def_node_states:
        def_node_states = all_node_states[0]

    assert len(def_node_states) == anim["node count"]

    i = 0
    for f, node_states in enumerate(all_node_states):
        for r_inc, t_inc, s_inc, def_ns, ns in zip(
                r_incs, t_incs, s_incs,
                def_node_states, node_states
                ):
            if r_inc:
                qi, qj, qk, qw = unpack_rot(data, i)

                mag = qi**2 + qj**2 + qk**2 + qw**2
                qw, q_scale    = (qw, 1/sqrt(mag)) if mag else (1.0, 1)

                qi, qj, qk, qw = (qi*q_scale, qj*q_scale,
                                  qk*q_scale, qw*q_scale)
                i  += r_inc
            else:
                qi, qj, qk, qw = (def_ns.rot_i, def_ns.rot_j,
                                  def_ns.rot_k, def_ns.rot_w)

            x, y, z = (
                (v*pos_scale for v in unpack_trans(data, i)) if t_inc else
                (def_ns.pos_x, def_ns.pos_y, def_ns.pos_z)
                )
            i += t_inc

            s = unpack_scale(data, i)[0] if s_inc else def_ns.scale
            i += s_inc

            ns.rot_i = qi
            ns.rot_j = qj
            ns.rot_k = qk
            ns.rot_w = qw
            ns.pos_x = x
            ns.pos_y = y
            ns.pos_z = z
            ns.scale = s

    return all_node_states

def deserialize_uncomp_frame_data(anim, def_node_states=None, include_extra_base_frame=True, endian=">", pos_scale=1.0):
    animation_type = AnimationTypeEnum(anim["type"]["value"])
    is_overlay = AnimationTypeEnum.overlay == animation_type
    if def_node_states is None:
        def_node_states = _deserialize_uncomp_frame_data(anim, True, (), endian, pos_scale)[0]

    frame_data = _deserialize_uncomp_frame_data(anim, False, def_node_states, endian, pos_scale)
    if include_extra_base_frame:
        # overlay animations start with frame 0 being
        # in the same state as the default node states
        is_overlay and frame_data.insert(0, def_node_states)

        # non-overlays duplicate the first frame to the last frame
        is_overlay or frame_data.append(deepcopy(frame_data[0]))

    return frame_data

def deserialize(anim, endian=">", pos_scale=1.0):
    animation_flags = AnimationFlags(anim["flags"])
    if AnimationFlags.compressed_data in animation_flags:
        # decompress compressed animations
        kfs, frames = deserialize_comp_frame_data(anim, False, True, pos_scale)
    else:
        # create the node states from the frame_data and default_data
        frames = deserialize_uncomp_frame_data(anim, None, True, endian, pos_scale)
        kfs = [], [], []

    return kfs, frames

def deserialize_frame_info(anim, include_extra_base_frame=False, endian=">", pos_scale=1.0):
    i = 0
    dx = dy = dz = dyaw = x = y = z = yaw = 0.0

    root_node_info = [JmaRootNodeState() for i in range(anim["frame count"])]
    frame_info = base64.b64decode(anim["frame info"]["encoded"])
    pos_scale *= const.SCALE_INTERNAL_TO_JMA

    # write to the data
    fite = FrameInfoTypeEnum(anim["frame info type"]["value"])
    if fite == FrameInfoTypeEnum.dx_dy_dz_dyaw:
        unpack = MethodType(unpack_from, endian + "4f")
        for f in range(anim["frame count"]):
            dx, dy, dz, dyaw = unpack(frame_info, i)
            dx *= pos_scale; dy *= pos_scale; dz *= pos_scale

            info = root_node_info[f]
            info.dx = dx; info.dy = dy; info.dz = dz; info.dyaw = dyaw
            info.x  = x;  info.y  = y;  info.z  = z;  info.yaw  = yaw

            x += dx; y += dy; z += dz; yaw += dyaw
            i += 16

    elif fite == FrameInfoTypeEnum.dx_dy_dyaw:
        unpack = MethodType(unpack_from, endian + "3f")
        for f in range(anim["frame count"]):
            dx, dy, dyaw = unpack(frame_info, i)
            dx *= pos_scale; dy *= pos_scale

            info = root_node_info[f]
            info.dx = dx; info.dy = dy; info.dyaw = dyaw
            info.x  = x;  info.y  = y;  info.yaw  = yaw

            x += dx; y += dy; yaw += dyaw
            i += 12

    elif fite == FrameInfoTypeEnum.dx_dy:
        unpack = MethodType(unpack_from, endian + "2f")
        for f in range(anim["frame count"]):
            dx, dy = unpack(frame_info, i)
            dx *= pos_scale; dy *= pos_scale

            info = root_node_info[f]
            info.dx = dx; info.dy = dy
            info.x  = x;  info.y  = y

            x += dx; y += dy
            i += 8

    if include_extra_base_frame and root_node_info:
        # duplicate the last frame and apply the change
        # that frame to the total change at that frame.
        last_root_node_info = deepcopy(root_node_info[-1])
        last_root_node_info.x += last_root_node_info.dx
        last_root_node_info.y += last_root_node_info.dy
        last_root_node_info.z += last_root_node_info.dz
        last_root_node_info.yaw += last_root_node_info.dyaw

        # no delta on last frame. zero it out
        last_root_node_info.dx = 0.0
        last_root_node_info.dy = 0.0
        last_root_node_info.dz = 0.0
        last_root_node_info.dyaw = 0.0

        root_node_info.append(last_root_node_info)

    return root_node_info

def root_node_info_frame_size(frame_info_type_value):
    fite = FrameInfoTypeEnum(frame_info_type_value)
    if fite == FrameInfoTypeEnum.dx_dy_dz_dyaw:
        return 16
    elif fite == FrameInfoTypeEnum.dx_dy_dyaw:
        return 12
    elif fite == FrameInfoTypeEnum.dx_dy:
        return 8
    return 0

def frame_data_frame_size(trans_flags, rot_flags, scale_flags):
    return (12 * sum(trans_flags) + 8 * sum(rot_flags) + 4 * sum(scale_flags))

def default_data_size(node_count, trans_flags, rot_flags, scale_flags):
    return node_count * 24 - frame_data_frame_size(trans_flags, rot_flags, scale_flags)

def trans_flags_bools(trans_flags_int, node_count):
    return [bool(trans_flags_int & (1 << i))
            for i in range(node_count)]

def rot_flags_bools(rot_flags_int, node_count):
    return [bool(rot_flags_int & (1 << i))
            for i in range(node_count)]

def scale_flags_bools(scale_flags_int, node_count):
    return [bool(scale_flags_int & (1 << i))
            for i in range(node_count)]

def has_frame_info(frame_info_type_value):
    result = False
    fite = FrameInfoTypeEnum(frame_info_type_value)
    if fite == FrameInfoTypeEnum.dx_dy_dz_dyaw:
        result = True
    elif fite == FrameInfoTypeEnum.dx_dy_dyaw:
        result = True
    elif fite == FrameInfoTypeEnum.dx_dy:
        result = True
    return result

def apply_root_node_info_to_states(anim, undo=False):
    apply = not undo
    if bool(anim["root_node_info_applied"]) == apply:
        # do nothing if the root node info is already applied
        # and we are being told to apply it, or its not applied
        # and we are being told to undo its application.
        return

    if has_frame_info(anim["frame info type"]["value"]):
        delta = 1 if apply else -1
        for f in range(anim["frame count"]):
            # apply the total change in the root nodes
            # frame_info for this frame to the frame_data
            node_info = anim["root_node_info"][f]
            node_state = anim["frames"][f][0]

            q0 = Ray(euler_to_quaternion(0, 0, -node_info.yaw * delta))
            q1 = Ray((node_state.rot_i, node_state.rot_j,
                        node_state.rot_k, node_state.rot_w))
            q0.normalize()
            q1.normalize()

            i, j, k, w = multiply_quaternions(q0, q1)

            node_state.pos_x += node_info.x * delta
            node_state.pos_y += node_info.y * delta
            node_state.pos_z += node_info.z * delta
            node_state.rot_i = i
            node_state.rot_j = j
            node_state.rot_k = k
            node_state.rot_w = w

    anim["root_node_info_applied"] = has_frame_info(anim["frame info type"]["value"]) and apply

def apply_base_pose_to_states(animation, undo=False):
    apply = not undo
    animation_type = AnimationTypeEnum(animation["type"]["value"])
    if bool(animation["overlay_base_applied"]) == apply:
        # do nothing if the base is already applied and
        # we are being told to apply it, or its not and
        # we are being told to undo its application.
        return

    # using the base frame, apply each overlay frame onto it
    for n, b_node in enumerate(animation["frames"][0] if AnimationTypeEnum.overlay == animation_type else []):
        b_s                = b_node.scale
        b_x, b_y, b_z      = b_node.pos_x, b_node.pos_y, b_node.pos_z
        b_i, b_j, b_k, b_w = [b_node.rot_i, b_node.rot_j,
                                b_node.rot_k, b_node.rot_w]

        if undo:
            b_s           = 1/b_s if b_s else 1
            b_x, b_y, b_z = -b_x, -b_y, -b_z
            b_i, b_j, b_k = -b_i, -b_j, -b_k

        b_quat = Ray([b_i, b_j, b_k, b_w])
        b_quat.normalize()
        for frame in animation["frames"][1:]:
            o_node = frame[n]
            o_quat = Ray([o_node.rot_i, o_node.rot_j,
                            o_node.rot_k, o_node.rot_w])
            o_quat.normalize()

            q_i, q_j, q_k, q_w = multiply_quaternions(o_quat, b_quat)
            o_node.pos_x += b_x
            o_node.pos_y += b_y
            o_node.pos_z += b_z
            o_node.scale *= b_s
            o_node.rot_i  = q_i
            o_node.rot_j  = q_j
            o_node.rot_k  = q_k
            o_node.rot_w  = q_w

    animation["overlay_base_applied"] = AnimationTypeEnum.overlay == animation_type and apply

def extract_animation(armature, animation_idx, animation, animation_data):
    trans_flags = trans_flags_bools((animation["node transform flag data"] | (animation["node transform flag data_1"] << 32)), animation["node count"])
    rot_flags = rot_flags_bools((animation["node rotation flag data"] | (animation["node rotation flag data_1"] << 32)), animation["node count"])
    scale_flags = scale_flags_bools((animation["node scale flag data"] | (animation["node scale flag data_1"] << 32)), animation["node count"])
    frame_info_data = base64.b64decode(animation["frame info"]["encoded"])
    default_data_data = base64.b64decode(animation["default data"]["encoded"])
    frame_data_data = base64.b64decode(animation["frame data"]["encoded"])
    animation_flags = AnimationFlags(animation["flags"])
    animation_type = AnimationTypeEnum(animation["type"]["value"])
    if len(frame_info_data) < root_node_info_frame_size(animation["frame info type"]["value"]) * animation["frame count"]:
        print("Skipping animation with less frame_info data "
              "than it is expected to contain: '%s'" % animation["name"])
        return
    elif AnimationFlags.compressed_data in animation_flags:
        # checks below don't apply to compressed animations
        pass
    elif len(default_data_data) < default_data_size(animation["node count"], trans_flags, rot_flags, scale_flags):
        print("Skipping animation with less default_data "
              "than it is expected to contain: '%s'" % animation["name"])
        return
    elif len(frame_data_data) < frame_data_frame_size(trans_flags, rot_flags, scale_flags) * animation["frame count"]:
        print("Skipping animation with less frame_data "
              "than it is expected to contain: '%s'" % animation["name"])
        return

    # if this is an overlay, try to determine a base
    # animation that it can be applied to, and apply
    # the overlay onto it so it looks good when imported
    base_frame = None
    if AnimationTypeEnum.overlay == animation_type:
        b_animation = get_base_anim_for_overlay(animation_idx, animation_data)
        base_frame = [] if not b_animation else deserialize(b_animation)[1][0]
        anim_name = animation["name"]
        if base_frame:
            b_anim_name = b_animation["name"]
            print(f"'{b_anim_name}' used as base for '{anim_name}'")
        else:
            print(f"No base anim found for '{anim_name}'. May not look correct when imported.")

    # sum the frame info changes for each frame from the frame_info
    root_node_info = deserialize_frame_info(animation, True)

    kfs, frames = deserialize(animation)
    rot_kfs, trans_kfs, scale_kfs = kfs

    animation["root_node_info"] = root_node_info
    animation["frames"] = frames
    animation["rot_keyframes"] = rot_kfs
    animation["trans_keyframes"] = trans_kfs
    animation["scale_keyframes"] = scale_kfs
    animation["overlay_base_applied"] = True

    if has_frame_info(animation["frame info type"]["value"]):
        # this is set to True on instantiation.
        # set it to False since we had to provide root node info
        animation["root_node_info_applied"] = False
        apply_root_node_info_to_states(animation)

    elif AnimationTypeEnum.overlay == animation_type and base_frame:
        # remove whatever base is applied so we can apply a new one
        apply_base_pose_to_states(animation, True)

        # replace the first frame with the chosen base pose
        animation["frames"][0] = base_frame
        apply_base_pose_to_states(animation)
