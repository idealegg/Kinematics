from ctypes import *
from common.kinematics import *
from common.kine_polygon import *
import os


class Kinematics(object):
    def __init__(self):
        self.dll_dir = 'DLL'
        ##self.win32_dir = r'C:\Windows\System32'
        ##self.ntdll_path = os.path.join(self.win32_dir, 'ntdll.dll')
        ##self.kernel32_path = os.path.join(self.win32_dir, 'kernel32.dll')
        ##self.kernelbase_path = os.path.join(self.win32_dir, 'KernelBase.dll')
        ##self.app_help_path = os.path.join(self.win32_dir, 'apphelp.dll')
        ##self.msvcrt_path = os.path.join(self.win32_dir, 'msvcrt.dll')
        self.kineC_path = os.path.join(self.dll_dir, 'libC_kineC.dll')
        self.is_loaded = False
        self.is_earth_defined = False
        self.is_center_defined = False
        self.load_dll()

    def load_dll(self):
        if not self.is_loaded:
            #self.ntdll = WinDLL(self.ntdll_path)
            #self.kernel32 = WinDLL(self.kernel32_path)
            #self.kernelbase = WinDLL(self.kernelbase_path)
            #self.app_help = WinDLL(self.app_help_path)
            #self.msvcrt = WinDLL(self.msvcrt_path)
            self.kineC = WinDLL(self.kineC_path)
            self.is_loaded = True

    def earth_definition(self, great_axis, small_axis):
        # EXTERNFCT c_int EarthDefinition (Float64 great_axis, Float64 small_axis);
        func = self.kineC.EarthDefinition
        func.argtypes = (c_double, c_double)
        func.restype = c_int
        ret =  func(great_axis, small_axis)
        self.is_earth_defined = True
        return ret

    def center_definiton(self, geodesic_position):
        # EXTERNFCT c_int CenterDefinition (GeodesicPositionT *geodesic_position_p);
        func = self.kineC.CenterDefinition
        func.argtypes = (POINTER(GeodesicPositionT),)
        func.restype = c_int
        ret = func(pointer(geodesic_position))
        self.is_center_defined = True
        return ret

    def stereo_2_geo_coordinates(self, stereo, geo_p=None):
        # EXTERNFCT c_int StereoToGeoCoordinates (StereographicCoordinatesT *stereo_coordinate_p,
        # GeographicCoordinateT     *geographic_coordinate_p);
        func = self.kineC.StereoToGeoCoordinates
        func.argtypes = (POINTER(StereographicCoordinatesT), POINTER(GeographicCoordinateT))
        func.restype = c_int
        geo = GeographicCoordinateT()
        geo_p_not_defined = geo_p is None
        if geo_p_not_defined:
            geo_p = pointer(geo)
        ret = func(pointer(stereo), geo_p)
        if geo_p_not_defined:
            return geo
        return ret

    def geo_2_stereo_coordinates(self, geo, stereo_p=None):
        # EXTERNFCT c_int GeoToStereoCoordinates (GeographicCoordinateT     *geographic_coordinate_p,
        # StereographicCoordinatesT *stereo_coordinate_p);
        func = self.kineC.GeoToStereoCoordinates
        func.argtypes = (POINTER(GeographicCoordinateT),
                            POINTER(StereographicCoordinatesT))
        func.restype = c_int
        stereo = StereographicCoordinatesT()
        stereo_p_not_defined = stereo_p is None
        if stereo_p_not_defined:
            stereo_p = pointer(stereo)
        ret = func(pointer(geo), stereo_p)
        if stereo_p_not_defined:
            return stereo
        return ret

    def geodesic_2_stereo_coordinates(self, geodesic, stereo_p=None):
        # EXTERNFCT c_int GeodesicToStereoCoordinates (GeodesicPositionT           *geodesic_position_p,
        # StereographicCoordinatesT	*stereo_coordinate_p);
        func = self.kineC.GeodesicToStereoCoordinates
        func.argtypes = (POINTER(GeodesicPositionT),
                         POINTER(StereographicCoordinatesT))
        func.restype = c_int
        stereo = StereographicCoordinatesT()
        stereo_p_not_defined = stereo_p is None
        if stereo_p_not_defined:
            stereo_p = pointer(stereo)
        ret = func(pointer(geodesic), stereo_p)
        if stereo_p_not_defined:
            return stereo
        return ret

    def rational_altitude(self, value):
        # EXTERNFCT Float64 RationalAltitude(Float64 value);
        func = self.kineC.RationalAltitude
        func.argtypes = (c_double,)
        func.restype = c_double
        return func(value)

    def define_altitude_plane(self, plane_definition, plane_p=None):
        # EXTERNFCT c_int DefineAltitudePlane(PlaneDefinitionT * planeDefinition,
        #                        AltitudePlaneT   * plane);
        func = self.kineC.DefineAltitudePlane
        func.argtypes = (POINTER(PlaneDefinitionT),
                         POINTER(AltitudePlaneT))
        func.restype = c_int
        plane = AltitudePlaneT()
        plane_p_not_defined = plane_p is None
        if plane_p_not_defined:
            plane_p = pointer(plane)
        ret = func(pointer(plane_definition), plane_p)
        if plane_p_not_defined:
            #print ("define_altitude_plane: ret=[%s], plane: %s" % (ConvResultT[ret], plane))
            return plane
        return ret

    def create_polygon_set(self, number_of_polygons, max_number_of_points):
        func = self.kineC.CreatePolygonSet
        func.argtypes = (c_int, c_int, POINTER(PolygonHandleT), POINTER(c_void_p), POINTER(c_void_p))
        func.restype = c_int
        polygon_set_id = PolygonHandleT(-1)
        polygon_points = c_void_p()
        polygons = c_void_p()
        ret = func(number_of_polygons, max_number_of_points, pointer(polygon_set_id), pointer(polygon_points), pointer(polygons))
        return polygon_set_id, polygon_points, polygons, ret

    def address_of_polygon_points_lists(self, polygon_set_id):
        func = self.kineC.AddressOfPolygonPointsLists
        func.argtypes = (PolygonHandleT, POINTER(c_void_p))
        func.restype = c_int
        polygon_points = c_void_p()
        ret = func(polygon_set_id, pointer(polygon_points))
        return polygon_points, ret

    def address_of_polygons(self, polygon_setID):
        # EXTERNFCT c_int AddressOfPolygons(PolygonHandleT  polygon_setID,
        #                                void            **polygon);
        func = self.kineC.AddressOfPolygons
        func.argtypes = (PolygonHandleT,POINTER(c_void_p))
        func.restype = c_int
        polygon_p = c_void_p()
        ret = func(polygon_setID, pointer(polygon_p))
        return polygon_p, ret

    def address_of_single_points_list(self, polygon_set_id, polygon_index):
        func = self.kineC.AddressOfSinglePointsList
        func.argtypes = (PolygonHandleT, c_int, POINTER(c_void_p))
        func.restype = c_int
        single_polygon_points = c_void_p()
        ret = func(polygon_set_id, polygon_index, pointer(single_polygon_points))
        return single_polygon_points, ret

    def address_of_single_polygon(self, polygon_set_id, polygon_index):
        func = self.kineC.AddressOfSinglePolygon
        func.argtypes = (PolygonHandleT, c_int, POINTER(c_void_p))
        func.restype = c_int
        single_polygon = c_void_p()
        ret = func(polygon_set_id, polygon_index, pointer(single_polygon))
        return single_polygon, ret

    def fill_polygon_data(self, polygon_set_id, polygon_index, floor, ceiling):
        func = self.kineC.FillPolygonData
        func.argtypes = (PolygonHandleT, c_int, AltitudeT, AltitudeT)
        func.restype = c_int
        ret = func(polygon_set_id, polygon_index, floor, ceiling)
        return ret

    def add_point_2_list(self, polygon_set_id, polygon_index, latitude, longitude):
        func = self.kineC.AddPointToList
        func.argtypes = (PolygonHandleT, c_int, c_double, c_double)
        func.restype = c_int
        ret = func(polygon_set_id, polygon_index, latitude, longitude)
        return ret

    def get_num_of_polygons(self, ptr_polygons):
        func = self.kineC.GetNumberOfPolygons
        func.argtypes = (c_void_p,)
        func.restype = c_int
        test_num_polygons = func(ptr_polygons)
        return test_num_polygons

    def prepare_polygonic_volumes(self, offline, num_of_polygons, polygon_points, polygons):
        func = self.kineC.PreparePolygonicVolumes
        func.argtypes = (c_int,
                         c_int,
                         c_void_p,
                         c_void_p,
                         # POINTER(T_PolygonPreparationResults),
                         POINTER(c_int),
                         POINTER(c_int),
                         POINTER(c_int),
                         POINTER(c_int))
        func.restype = c_int
        validation_result = c_int()
        polygon_with_error = c_int()
        segment_with_error = c_int()
        segment_that_crosses = c_int()
        ret = func(offline, num_of_polygons, polygon_points, polygons,
                   pointer(validation_result),
                   pointer(polygon_with_error),
                   pointer(segment_with_error),
                   pointer(segment_that_crosses))
        return validation_result, polygon_with_error, segment_with_error, segment_that_crosses, ret

    def find_out_volume_containing_point(self,
                                         point_origin_p,
                                         altitude,
                                         polygons):
        func = self.kineC.FindOutVolumeContainingPoint
        func.argtypes = (POINTER(GeographicCoordinateT),
                         AltitudeT,
                         c_void_p,
                         POINTER(c_int),
                         POINTER(c_int))
        func.restype = c_int
        found = c_int()
        polygon_number = c_int()
        ret = func(point_origin_p, altitude, cast(polygons, c_void_p), pointer(found), pointer(polygon_number))
        return found, polygon_number, ret

    def find_all_volume_containing_point(self,
                                         point_origin_p,
                                         altitude,
                                         polygons):
        func = self.kineC.FindAllVolumesContainingPoint
        func.argtypes = (POINTER(GeographicCoordinateT),
                         AltitudeT,
                         c_void_p,
                         POINTER(c_int),
                         PolygonNumbers)
        func.restype = c_int
        num_found = c_int()
        polygon_numbers = PolygonNumbers()
        ret = func(point_origin_p, altitude, cast(polygons, c_void_p), pointer(num_found), polygon_numbers)
        return num_found, polygon_numbers, ret

    def compute_polygonic_volume_exit_point(self, trajectory, polygon):
        func = self.kineC.ComputePolygonicVolumeExitPoint
        func.argtypes = (POINTER(VolumicSegmentT),
                         c_void_p,
                         POINTER(PolygonIntersectionT))
        exit_intersection = PolygonIntersectionT()
        ret = func(trajectory, polygon, pointer(exit_intersection))
        return exit_intersection, ret

    def distance_on_the_great_circle(self, point_origin, point_dest, altitude):
        func = self.kineC.DistanceOnTheGreatCircleStereo
        func.argtypes = (POINTER(StereographicCoordinatesT),
                         POINTER(StereographicCoordinatesT),
                         POINTER(AltitudeT),
                         POINTER(DistanceT))
        dis = DistanceT()
        func.restype = c_int
        ret = func(pointer(point_origin), pointer(point_dest), pointer(altitude), pointer(dis))
        return dis, ret