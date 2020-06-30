from ctypes import *
from common.kinematics import *
from common.kine_polygon import *
import common.parse_tools
import dll_if.kinematics
import pprint


polygonData = PolygonDataArrayT()
polygonPoints = GeographicCoordinateArrayTT()

pointDefinition = PolygonPointDefinitionT()
preparedPolygons = PolygonicVolumeDefinitionT()

polygonSetID = PolygonHandleT(-1)

kine_dll = dll_if.kinematics.Kinematics()
ppd_buffer = None
gc_buffer = None
segt_buffer = None
segt_pro_buffer = None

fv = None


def convert_feet_2_metres(feet):
    return kine_dll.rational_altitude(feet * FEET_TO_METER.value)

def convert_metres_2_feet(metre):
    return kine_dll.rational_altitude(metre * METER_TO_FEET.value)

def get_plane_definition(h):  # meter
    h = convert_feet_2_metres(h)
    return PlaneDefinitionT(GeodesicPositionT(0.0, 0.0, h),
                           GeodesicPositionT(0.0, 0.0, h),
                           GeodesicPositionT(0.0, 0.0, h))

def init_earth(sys_centre):
    ret = kine_dll.earth_definition(c_double(float(sys_centre.sys_ctr['RDF_HALF_GREAT_AXIS'])),
                              c_double(float(sys_centre.sys_ctr['RDF_HALF_SMALL_AXIS'])))
    print("init_earth: ret=%s" % ret)

def init_centre(sys_centre):
    center = GeodesicPositionT(*common.parse_tools.parse_lat_long(sys_centre.sys_ctr['SYSTEM_CENTRE']), 0.0)
    ret = kine_dll.center_definiton(center)
    print("init_centre: ret=%s" % ret)

def prepare_polygons_old(fdp_vol):
    global polygonData
    global polygonPoints
    global pointDefinition
    global preparedPolygons
    global ppd_buffer
    global gc_buffer
    global segt_buffer
    global segt_pro_buffer
    ps = fdp_vol.fdp_vol['POINTS']
    number_of_polygons = len(fdp_vol.map_vol)
    max_number_of_points = 0
    for i in range(number_of_polygons):
        vol = fdp_vol.fdp_vol['VOLUME'][fdp_vol.map_vol[i]]
        pprint.pprint(vol)
        polygonData[i].floor = convert_metres_2_feet(vol['floor'])
        polygonData[i].ceiling = convert_metres_2_feet(vol['ceiling'])
        polygonData[i].polygon_number = i
        polygonData[i].number_of_points = len(vol['point_list'])
        polygonData[i].floor_plane = kine_dll.define_altitude_plane(get_plane_definition(polygonData[i].floor.value))
        polygonData[i].ceiling_plane = kine_dll.define_altitude_plane(get_plane_definition(polygonData[i].ceiling.value))
        for p_cnt in range(polygonData[i].number_of_points):
            polygonPoints[i][p_cnt] = GeographicCoordinateT(*common.parse_tools.parse_lat_long(ps[vol['point_list'][p_cnt]]))
        if max_number_of_points < polygonData[i].number_of_points:
            max_number_of_points = polygonData[i].number_of_points
    pointDefinition.max_polygon_number = MAX_NB_OF_VOLUMIC_POLYGONS - 1
    pointDefinition.max_point_number = MAX_NB_OF_POINTS_IN_VOLUMIC_POLYGON - 1
    pointDefinition.offset_to_data = PolygonAddressOffsetT(addressof(polygonData) - addressof(pointDefinition))
    pointDefinition.offset_to_points = PolygonAddressOffsetT(addressof(polygonPoints) - addressof(pointDefinition))
    # Polygon numbers start from 0 so the maximum polygon number is the number of polygons - 1
    preparedPolygons.max_polygon_number = number_of_polygons - 1
    preparedPolygons.max_point_number = max_number_of_points - 1
    tmp_buffer = create_string_buffer(sizeof(PreparedPolygonDataT) * number_of_polygons)
    ppd_buffer_address = addressof(tmp_buffer)
    ppd_buffer = POINTER(PreparedPolygonDataT)(tmp_buffer)
    tmp_buffer = create_string_buffer(sizeof(GeographicCoordinateT) * max_number_of_points)
    gc_buffer_address = addressof(tmp_buffer)
    gc_buffer = POINTER(GeographicCoordinateT)(tmp_buffer)
    tmp_buffer = create_string_buffer(sizeof(c_int) * number_of_polygons * max_number_of_points)
    segt_buffer_address = addressof(tmp_buffer)
    segt_buffer = POINTER(c_int)(tmp_buffer)
    tmp_buffer = create_string_buffer(sizeof(c_int) * number_of_polygons * max_number_of_points)
    segt_pro_buffer_address = addressof(tmp_buffer)
    segt_pro_buffer = POINTER(c_int)(tmp_buffer)
    preparedPolygons.offset_to_data = PolygonAddressOffsetT(ppd_buffer_address - addressof(preparedPolygons))
    preparedPolygons.offset_to_points = PolygonAddressOffsetT(gc_buffer_address - addressof(preparedPolygons))
    preparedPolygons.offset_to_segments = PolygonAddressOffsetT(segt_buffer_address - addressof(preparedPolygons))
    preparedPolygons.offset_to_segments_processed = PolygonAddressOffsetT(segt_pro_buffer_address - addressof(preparedPolygons))
    validation_result, polygon_with_error, segment_with_error, segment_that_crosses, ret = kine_dll.prepare_polygonic_volumes(
                                       c_int(1),
                                       c_int(number_of_polygons),
                                       pointer(pointDefinition),
                                       pointer(preparedPolygons)
                                       )
    print("ppd_buffer: %x, gc_buffer: %x, segt_buffer: %x, segt_pro_buffer: %x" % (
        addressof(ppd_buffer), addressof(gc_buffer), addressof(segt_buffer), addressof(segt_pro_buffer)))
    print(pointDefinition)
    print(preparedPolygons)
    print(polygonData)
    print(pointDefinition)
    print("prepare_polygons:")
    print("validation_result=%s, polygon_with_error=%s, segment_with_error=%s, segment_that_crosses=%s, ret=%s" % (
        T_PolygonPreparationResults[validation_result], polygon_with_error, segment_with_error, segment_that_crosses, ConvResultT[ret]
    ))

def prepare_polygons(fdp_vol):
    global polygonData
    global polygonPoints
    global polygonSetID
    global fv
    fv = fdp_vol
    ps = fdp_vol.fdp_vol['POINTS']
    number_of_polygons = len(fdp_vol.map_vol)
    max_number_of_points = 0
    for i in range(number_of_polygons):
        vol = fdp_vol.fdp_vol['VOLUME'][fdp_vol.map_vol[i]]
        polygonData[i].floor = convert_metres_2_feet(vol['floor'])
        polygonData[i].ceiling = convert_metres_2_feet(vol['ceiling'])
        polygonData[i].polygon_number = i
        polygonData[i].number_of_points = len(vol['point_list']) - 1
        polygonData[i].floor_plane = kine_dll.define_altitude_plane(get_plane_definition(polygonData[i].floor.value))
        polygonData[i].ceiling_plane = kine_dll.define_altitude_plane(get_plane_definition(polygonData[i].ceiling.value))
        #polygonData[i].floor_plane = kine_dll.define_altitude_plane(get_plane_definition(-99999.9))
        #polygonData[i].ceiling_plane = kine_dll.define_altitude_plane(get_plane_definition(-99999.9))
        for p_cnt in range(polygonData[i].number_of_points):
            polygonPoints[i][p_cnt] = GeographicCoordinateT(*common.parse_tools.parse_lat_long(ps[vol['point_list'][p_cnt]]))
        if max_number_of_points < polygonData[i].number_of_points:
            max_number_of_points = polygonData[i].number_of_points
        #pprint.pprint(vol)
        #print("[%d]: num_of_pts=%s, max_num_of_pts=%s" % (i, polygonData[i].number_of_points, max_number_of_points))
    print("\nnumber_of_polygons=%s, max_num_of_pts=%s\n" % (number_of_polygons, max_number_of_points))
    polygonSetID, polygon_points, polygons, ret= kine_dll.create_polygon_set(number_of_polygons, max_number_of_points)
    print("create_polygon_set: ")
    print("polygonSetID=%s, polygon_points=%s, polygons=%s, ret=[%s]\n" % (polygonSetID, polygon_points, polygons, ConvResultT[ret]))
    if ret or not polygon_points or not polygons:
        return "%s: %s" % ('create_polygon_set', ConvResultT[ret])
    test_polygon_points, ret = kine_dll.address_of_polygon_points_lists(polygonSetID)
    print("address_of_polygon_points_lists: ")
    print("test_polygon_points=%s, polygon_points=%s, ret=[%s]\n" % (
        test_polygon_points, polygon_points, ConvResultT[ret]))
    if ret or test_polygon_points.value != polygon_points.value:
        return "%s: %s" % ('address_of_polygon_points_lists', ConvResultT[ret])
    test_polygons, ret = kine_dll.address_of_polygons(polygonSetID)
    print("address_of_polygons: ")
    print("test_polygons=%s, polygons=%s, ret=[%s]\n" % (
        test_polygons, polygons, ConvResultT[ret]))
    if ret or test_polygons.value != polygons.value:
        return "%s: %s" % ('address_of_polygons', ConvResultT[ret])
    points_list = cast(test_polygon_points, POINTER(PolygonPointDefinitionT))
    #print("point_list: %s, addr: %x, offset: %s"%(points_list, addressof(points_list), points_list.contents.offset_to_data.value))
    multiPolygonData = cast(addressof(points_list.contents) + points_list.contents.offset_to_data.value, POINTER(PolygonDataT))
    test_polygon_points, ret = kine_dll.address_of_single_points_list(polygonSetID, c_int(0))
    #print("address_of_single_points_list: ")
    #print("test_polygon_points=%s, ret=[%s]" % (test_polygon_points, ConvResultT[ret]))
    points_list = cast(test_polygon_points, POINTER(PolygonPointDefinitionT))
    #print("point_list: %s, addr: %x, offset: %s" % (
    #points_list, addressof(points_list), points_list.contents.offset_to_data.value))
    singlePolygonData = cast(addressof(points_list.contents) + points_list.contents.offset_to_data.value, POINTER(PolygonDataT))
    print("multiPolygonData=%s\nsinglePolygonData=%s\n" % (multiPolygonData, singlePolygonData))
    if ret:
        return "%s: %s" % ('address_of_single_points_list', ConvResultT[ret])
    for polygonIndex in range(number_of_polygons):
        ret = kine_dll.fill_polygon_data(polygonSetID, polygonIndex, polygonData[polygonIndex].floor, polygonData[polygonIndex].ceiling)
        #print("fill_polygon_data:")
        #print("polygonIndex=%s, ret=[%s]" % (polygonIndex, ConvResultT[ret]))
        if ret:
            return "%s: %s" % ('fill_polygon_data', ConvResultT[ret])
        for pointIndex in range(polygonData[polygonIndex].number_of_points):
            ret = kine_dll.add_point_2_list(polygonSetID, polygonIndex,
                                            polygonPoints[polygonIndex][pointIndex].latitude,
                                            polygonPoints[polygonIndex][pointIndex].longitude)
            #print("add_point_2_list:")
            #print("polygonIndex=%s, pointIndex=%s, ret=[%s]" % (polygonIndex, pointIndex, ConvResultT[ret]))
            if ret:
                return "%s: %s" % ('add_point_2_list', ConvResultT[ret])
    test_num_polygons = kine_dll.get_num_of_polygons(polygons)
    print("get_num_of_polygons:")
    print("test_num_polygons=%s, numberOfPolygons=%s\n" % (test_num_polygons, number_of_polygons))
    if test_num_polygons != number_of_polygons:
        return "%s: %s" % ('get_num_of_polygons', ConvResultT[0])
    validation_result, polygon_with_error, segment_with_error, segment_that_crosses, ret = kine_dll.prepare_polygonic_volumes(
                                       c_int(1),
                                       c_int(number_of_polygons),
                                       polygon_points,
                                       polygons
                                           )
    print("prepare_polygons:")
    print("validation_result=%s, polygon_with_error=%s, segment_with_error=%s, segment_that_crosses=%s, ret=%s\n\n" % (
        T_PolygonPreparationResults[validation_result.value], polygon_with_error, segment_with_error, segment_that_crosses, ConvResultT[ret]
    ))
    if validation_result or ret:
        return "%s: valid: %s, ret: %s" % ('prepare_polygonic_volumes', T_PolygonPreparationResults[validation_result.value], ConvResultT[ret])
    return ""

def find_out_volume_containing_point(coordinate, feet=0.0): # xxxNxxxE, feet
    p = GeographicCoordinateT(*common.parse_tools.parse_lat_long(coordinate))
    print("coordinate: %s, feet: %s, p: (%s, %s)\n" % (coordinate, feet, p.latitude, p.longitude ))
    alt = AltitudeT(feet)
    polygons, ret = kine_dll.address_of_polygons(polygonSetID)
    print("address_of_polygons: ")
    print("polygons=%s, ret=[%s]\n" % (polygons, ConvResultT[ret]))
    if ret:
        return "%s: %s" % ('address_of_polygons', ConvResultT[ret])
    found, polygon_number, ret = kine_dll.find_out_volume_containing_point(pointer(p), alt, polygons)
    print("find_out_volume_containing_point")
    if ret or not found:
        print("found=%s, ret=%s" % (found, ConvResultT[ret]))
        return "%s: %s" % ('find_out_volume_containing_point', ConvResultT[ret])
    print("found=%s, polygon_number=%s, name=%s, ret=%s\n\n" % (found, polygon_number, fv.map_vol[polygon_number.value], ConvResultT[ret]))
    return ''

def find_all_volume_containing_point(coordinate, feet=0.0): # xxxNxxxE, feet
    p = GeographicCoordinateT(*common.parse_tools.parse_lat_long(coordinate))
    print("coordinate: %s, feet: %s, p: (%s, %s)\n" % (coordinate, feet, p.latitude, p.longitude ))
    alt = AltitudeT(feet)
    polygons, ret = kine_dll.address_of_polygons(polygonSetID)
    print("address_of_polygons: ")
    print("polygons=%s, ret=[%s]\n" % (polygons, ConvResultT[ret]))
    if ret:
        return "%s: %s" % ('address_of_polygons', ConvResultT[ret])
    num_found, polygon_numbers, ret = kine_dll.find_all_volume_containing_point(pointer(p), alt, polygons)
    print("find_all_volume_containing_point")
    print("num_found=%s, ret=%s" % (num_found, ConvResultT[ret]))
    if ret or not num_found:
        return "%s: %s" % ('find_all_volume_containing_point', ConvResultT[ret])
    for num in range(num_found.value):
        print("num[%s]: polygon_num [%s], name [%s]\n\n" % (num, polygon_numbers[num], fv.map_vol[polygon_numbers[num]]))
    return ''

def compute_polygonic_volume_exit_point(trajectory, polygon_num=0):
    single_polygon, ret = kine_dll.address_of_single_polygon(polygonSetID, polygon_num)
    print("address_of_single_points_list: ")
    print("single_polygons=%s, ret=[%s]\n" % (single_polygon, ConvResultT[ret]))
    if ret:
        return "%s: %s" % ('address_of_single_points_list', ConvResultT[ret])
    exit_intersection, ret = kine_dll.compute_polygonic_volume_exit_point(trajectory, single_polygon)
    print("compute_polygonic_volume_exit_point")
    print("ret=%s" % (ConvResultT[ret]))
    if ret:
        return "%s: %s" % ('compute_polygonic_volume_exit_point', ConvResultT[ret])
    print(exit_intersection)
    return ''