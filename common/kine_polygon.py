from ctypes import *
from common.kinematics import *
from enum import IntEnum


# the max number of volumic polygons allowed    - This has an Ada equivalent
MAX_NB_OF_VOLUMIC_POLYGONS     = 1200
# the max number of points in a volumic polygon - This has an Ada equivalent
MAX_NB_OF_POINTS_IN_VOLUMIC_POLYGON = 500
# the max number of allowed intersection points - This has an Ada equivalent
MAX_NB_OF_INTERSECTIONS  = 400
# the maximum number of polygon arrays that can be defined for a process    
MAX_NB_OF_POLYGON_SETS   = MAX_NB_OF_VOLUMIC_POLYGONS
# the maximum number of sloping planes for polygon floor and ceiling        
# This is only required in the Ada code - no imposed limit in C or Java     
MAX_NB_OF_POLYGON_PLANES = MAX_NB_OF_VOLUMIC_POLYGONS * 2
# the maximum number of masks for polygons - used for say sector processing 
# This is only required in the Ada code - no imposed limit in C or Java     
MAX_NB_OF_POLYGON_MASKS  = MAX_NB_OF_VOLUMIC_POLYGONS

#class T_PolygonPreparationResults(IntEnum):
#    POLYGON_PREPARED_OK = 0
#    POLYGON_NOT_CLOSED = 1
#    POLYGON_NULL_SEGMENT = 2
#    POLYGON_SEGMENTS_CROSS = 3
#    POLYGON_TOO_HIGH = 4
#    POLYGON_FLOOR_INVALID = 5
#    POLYGON_CEILING_INVALID = 6
#    POLYGON_CEILING_BELOW_FLOOR = 7
#    POLYGON_NEEDS_POINT_AT_POLE = 8
#    POLYGON_AMBIGUOUS_POLE = 9
#    POLYGON_FILTER_ERROR = 10
#    POLYGON_INTERNAL_ERROR = 11
T_PolygonPreparationResults = {
        0: "POLYGON_PREPARED_OK",
        1: "POLYGON_NOT_CLOSED",
        2: "POLYGON_NULL_SEGMENT",
        3: "POLYGON_SEGMENTS_CROSS",
        4: "POLYGON_TOO_HIGH",
        5: "POLYGON_FLOOR_INVALID",
        6: "POLYGON_CEILING_INVALID",
        7: "POLYGON_CEILING_BELOW_FLOOR",
        8: "POLYGON_NEEDS_POINT_AT_POLE",
        9: "POLYGON_AMBIGUOUS_POLE",
        10: "POLYGON_FILTER_ERROR",
        11: "POLYGON_INTERNAL_ERROR",
}

class PolygonAddressOffsetT(c_int):
    pass

class AltitudePlaneNumberT(c_int):
    pass

class PolygonMaskNumberT(c_int):
    pass

class PolygonHandleT(c_int):
    pass

class PolygonPointDefinitionT(KineStructure):
    _fields_ = [("max_polygon_number", c_int),
                ("max_point_number", c_int),
                ("offset_to_data", PolygonAddressOffsetT),
                ("offset_to_points", PolygonAddressOffsetT)]

class PolygonicVolumeDefinitionT(KineStructure):
    _fields_ = [("max_polygon_number", c_int),
                ("max_point_number", c_int),
                ("max_plane_number", PolygonMaskNumberT),
                ("max_mask_number", PolygonAddressOffsetT),
                ("last_plane_number", AltitudePlaneNumberT),
                ("polygons_initialised", c_int),
                ("offset_to_data", PolygonAddressOffsetT),
                ("offset_to_points", PolygonAddressOffsetT),
                ("offset_to_segments", PolygonAddressOffsetT),
                ("offset_to_planes", PolygonAddressOffsetT),
                ("offset_to_masks", PolygonAddressOffsetT),
                ("offset_reserved", PolygonAddressOffsetT),
                ]

# -- A plane is defined by the the equation a*x + b*y + c*z + d = 0 where
# -- S(x, y, z) is a point on the plane in 3 dimensions.
# -- Since we are solving for the height z,  the terms a, b and d can be
# -- divided by -c and we can reduce the equation to z = A*x + B*y + D
class AltitudePlaneT(KineStructure):
    _fields_ = [("A", c_double),
                ("B", c_double),
                ("D", c_double)]

class PolygonDataT(KineStructure):
    _fields_ = [("floor", AltitudeT),
                ("ceiling", AltitudeT),
                ("polygon_number", c_int),
                ("number_of_points", c_int),
                ("floor_plane", AltitudePlaneT),
                ("ceiling_plane", AltitudePlaneT)]

PolygonDataArrayT = PolygonDataT * MAX_NB_OF_VOLUMIC_POLYGONS

GeographicCoordinateArrayT = GeographicCoordinateT * MAX_NB_OF_VOLUMIC_POLYGONS
GeographicCoordinateArrayTT = GeographicCoordinateArrayT * MAX_NB_OF_POINTS_IN_VOLUMIC_POLYGON

# Three unique geodesic positions are required to define a 3D plane
class PlaneDefinitionT(KineStructure):
    _fields_ = [("S1", GeodesicPositionT),
                ("S2", GeodesicPositionT),
                ("S3", GeodesicPositionT)]

PlaneDefinitionArrayT = PlaneDefinitionT * MAX_NB_OF_VOLUMIC_POLYGONS

class T_GridPolarRegion(IntEnum):
    E_GridNotPolar = 0
    E_GridSouthPolar = 1
    E_GridNorthPolar = 2

class T_GridFill32(c_int):
    pass

class T_GridLatitude(c_double):
    pass

class T_GridLongitude(c_double):
    pass

class T_GridPositionOffset(KineStructure):
    _fields_ = [("latitude", T_GridLatitude),
                ("longitude", T_GridLongitude)]

class T_GeographicGrid(KineStructure):
    _fields_ = [ #("polarRegion", T_GridPolarRegion),
                ("polarRegion", c_int),  # T_GridPolarRegion
                ("align", T_GridFill32),
                ("southWestOffset", T_GridPositionOffset),
                ("northEastOffset", T_GridPositionOffset)]
    def format_field(self, field):
        val = getattr(self, field)
        if field == "polarRegion":
            return T_GridPolarRegion[getattr(val, 'value') if hasattr(val, 'value') else val]
        return val

class PreparedPolygonDataT(KineStructure):
    _fields_ = [("floor", AltitudeT),
                ("ceiling", AltitudeT),
                ("boundary_grid", T_GeographicGrid),
                ("polygon_number", c_int),
                ("number_of_points", c_int),
                ("active", c_int),
                ("concave", c_int),
                ("floorPlane", AltitudePlaneNumberT),
                ("ceilingPlane", AltitudePlaneNumberT)]

class PolygonAddressT(c_uint):
    pass

PolygonNumbers = c_int * MAX_NB_OF_VOLUMIC_POLYGONS

class VolumicSegmentT(KineStructure):
    _fields_ = [("start_point", GeographicCoordinateT),
                ("start_altitude", AltitudeT),
                ("end_point", GeographicCoordinateT),
                ("end_altitude", AltitudeT)]

#typedef enum {
#  POLYGON_IN       = 0,
#  POLYGON_OUT      = 1,
#  POLYGON_ENTRY    = 2,
#  POLYGON_EXIT     = 3,
#  POLYGON_BOUNDARY = 4,
#  POLYGON_ERROR    = 5
#} PolygonIntersectionTypeT;

PolygonIntersectionTypeT = {
    0: "POLYGON_IN",
    1: "POLYGON_OUT",
    2: "POLYGON_ENTRY",
    3: "POLYGON_EXIT",
    4: "POLYGON_BOUNDARY",
    5: "POLYGON_ERROR",
}

#  typedef enum {
#    FLOOR   = 0,
#    CEILING = 1,
#    SIDE    = 2,
#    BORDER  = 3,
#    CORNER  = 4,
#    NONE    = 5
#  } PointBelongsToT;
PointBelongsToT = {
    0: "FLOOR",
    1: "CEILING",
    2: "SIDE",
    3: "BORDER",
    4: "CORNER",
    5: "NONE",
}

class PolygonIntersectionT(KineStructure):
    _fields_ = [("point", GeographicCoordinateT),
                ("altitude", AltitudeT),
                ("distance", c_double),
                ("type", c_int),   # PolygonIntersectionTypeT
                ("polygon_number", c_int),
                ("segment_number", c_int),
                ("point_belongs_to", c_int), # PointBelongsToT
                ("corner_point", c_int),
                ("filler", c_int)
                ]
    def format_field(self, field):
        val = getattr(self, field)
        if field == "type":
            return PolygonIntersectionTypeT[getattr(val, 'value') if hasattr(val, 'value') else val]
        elif field == "point_belongs_to":
            return PointBelongsToT[getattr(val, 'value') if hasattr(val, 'value') else val]
        return val
