from ctypes import *
from enum import IntEnum


#incldue<math.h>
# define M_E            2.7182818284590452354   /* e */
# define M_LOG2E        1.4426950408889634074   /* log_2 e */
# define M_LOG10E       0.43429448190325182765  /* log_10 e */
# define M_LN2          0.69314718055994530942  /* log_e 2 */
# define M_LN10         2.30258509299404568402  /* log_e 10 */
# define M_PI           3.14159265358979323846  /* pi */
# define M_PI_2         1.57079632679489661923  /* pi/2 */
# define M_PI_4         0.78539816339744830962  /* pi/4 */
# define M_1_PI         0.31830988618379067154  /* 1/pi */
# define M_2_PI         0.63661977236758134308  /* 2/pi */
# define M_2_SQRTPI     1.12837916709551257390  /* 2/sqrt(pi) */
# define M_SQRT2        1.41421356237309504880  /* sqrt(2) */
# define M_SQRT1_2      0.70710678118654752440  /* 1/sqrt(2) */

M_E        = 2.7182818284590452354
M_LOG2E    = 1.4426950408889634074
M_LOG10E   = 0.43429448190325182765
M_LN2      = 0.69314718055994530942
M_LN10     = 2.30258509299404568402
M_PI       = 3.14159265358979323846
M_PI_2     = 1.57079632679489661923
M_PI_4     = 0.78539816339744830962
M_1_PI     = 0.31830988618379067154
M_2_PI     = 0.63661977236758134308
M_2_SQRTPI = 1.12837916709551257390
M_SQRT2    = 1.41421356237309504880
M_SQRT1_2  = 0.70710678118654752440

# Define the kinematics Radian Types
K_PI = c_double(M_PI)
K_2PI = c_double(K_PI.value * 2.0)
K_PI_2 = c_double(M_PI_2)
K_PI_4 = c_double(M_PI_4)

def type_str(obj):
    return "%s" % obj.value

c_int.__str__ = type_str
c_double.__str__ = type_str
c_uint.__str__ = type_str


class KineStructure(Structure):
    def format_field(self, field):
        return getattr(self, field)

    def __str__(self):
        s = "".join([self.__class__.__name__, '('])
        first = True
        for field in self._fields_:
            s1 = "%s=%s" % (field[0], self.format_field(field[0]))
            if first:
                first = False
            else:
                s1 = "".join([',', s1])
            if ((len(s) + len(s1))  // 45 > len(s) // 45) or s[-1] in '()':
                s = "\n".join([s, s1])
            else:
                s = " ".join([s, s1])
        s = "".join([s, ')'])
        return s


# Type SpeedT defines a speed which is expressed in knots
class SppedT(c_double):
    pass

# Type MachT defines a speed which is expressed in Mach
class MachT(c_double):
    pass

DEGREES_IN_CIRCLE       = c_double(360.0)
DEGREES_IN_HALF_CIRCLE   = c_double(180.0)
DEGREES_IN_QUARTER_OF_CIRCLE   = c_double(DEGREES_IN_CIRCLE.value/4.0)
DEGREES_IN_3QUARTER_OF_CIRCLE  = c_double (DEGREES_IN_CIRCLE.value*0.75)
DEGREE_TO_RADIAN        = c_double(K_PI.value/DEGREES_IN_HALF_CIRCLE.value)
RADIAN_TO_DEGREE        = c_double(DEGREES_IN_HALF_CIRCLE.value/K_PI.value)
NM_TO_METER         = c_double(1852.000)
METER_TO_NM         = c_double (1.0/NM_TO_METER.value)
TEN_DEGREES_TO_DEGREES  = c_double(0.1)
NM32_TO_NM          = c_double(1.0/32.0)
FEET_TO_METER       = c_double(0.3048)
METER_TO_FEET       = c_double(1.0/FEET_TO_METER.value)
FEET_TO_NM          = c_double(FEET_TO_METER.value/NM_TO_METER.value)
NM_TO_FEET          = c_double(NM_TO_METER.value/FEET_TO_METER.value)
NM_TO_KM            = c_double(NM_TO_METER.value/1000.0)
KM_TO_NM            = c_double(1.0/NM_TO_KM.value)

def FeetToNM(f):
    return f * FEET_TO_NM.value

KNOT_TO_M_PER_S = c_double(NM_TO_METER.value/3600.0)
M_PER_S_TO_KNOT = c_double(1.0/KNOT_TO_M_PER_S.value)


MAX_NB_OF_MAG_GRID_PT_IN_LAT = 100
MAX_NB_OF_MAG_GRID_PT_IN_LONG = 360
MAX_GRID_PT_NBER  = MAX_NB_OF_MAG_GRID_PT_IN_LAT * MAX_NB_OF_MAG_GRID_PT_IN_LONG

MAX_NB_OF_POINT_ON_A_GREAT_CIRCLE = 420

#class ConvResultT(IntEnum):
#    Ok = 0
#    EarthNotInit             = 1
#    CenterNotInit            = 2
#    EarthYetInit             = 3
#    PointOutsideMagneticGrid = 4
#    RadarNotInit             = 5
#    RadarBiasNotInit         = 6
#    PolygonError             = 7
#    InvalidSouthWestMagPoint = 8
#    IncrementTooSmall        = 9
#    PrecisionTooHigh         = 10
#    ReferenceError           = 11
#    MemoryError              = 253
#    UndefinedError           = 254
#    NumericError             = 255
#    #_fields_ = []

ConvResultT = {    0: "Ok",
    1: "EarthNotInit",
    2: "CenterNotInit",
    3: "EarthYetInit",
    4: "PointOutsideMagneticGrid",
    5: "RadarNotInit",
    6: "RadarBiasNotInit",
    7: "PolygonError",
    8: "InvalidSouthWestMagPoint",
    9: "IncrementTooSmall",
    10: "PrecisionTooHigh",
    11: "ReferenceError",
    253: "MemoryError",
    254: "UndefinedError",
    255: "NumericError", }

# Type AltitudeT defines an altitude which is expressed in feet
class AltitudeT(c_double):
    pass

class DistanceT(c_double):
    pass

#  Type MeterAltitudeT defines an altitude which is expressed in metres
class MeterAltitudeT(c_double):
    pass

# A point can be defined from cartesian coordinates expressed in
class  StereographicCoordinatesT(KineStructure):
    _fields_ = [("x", c_double),   # Nm
                ("y", c_double)]   # Nm

# The StereoSpeed type defines a speed with cartesian vector
# expressed in knots
class StereoSpeedT(KineStructure):
    _fields_ = [("U_speed", c_double),  # knot
                ("V_speed", c_double)]  # knot

# The GeodesicPositionT type defines the position of an aircraft by
# latitude, longitude  (expressed in decimal degrees).
# height               (expressed in meters)
class GeodesicPositionT(KineStructure):
    _fields_ = [("latitude", c_double),  # latitude
                ("longitude", c_double), # longitude
                ('h', MeterAltitudeT)]   # height

# The GeographicCoordinateT a position on the earth by
# latitude, longitude, (expressed in decimal degrees).
# This type is especially used for great circle calculations
class GeographicCoordinateT(KineStructure):
    _fields_ = [("latitude", c_double),
                ("longitude", c_double)]


