from func_if.polygon_util import *
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point
import common.parse_tools


if __name__ == "__main__":
    project = 'GUTM'
    sc = offl_if.sys_centre.SysCentre(project)
    fv = offl_if.fdp_vol.FdpVolume(project)
    chp = offl_if.char_point.CharPoint(project)
    init_earth(sc)
    init_centre(sc)
    ret = prepare_polygons(fv)
    if ret:
        print("prepare_polygons error: %s" % ret)
        exit(1)
    trajectory = VolumicSegmentT(
        #GeographicCoordinateT(23.12677    ,114.1405),
        #GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['P154']['Lat_Long'])),
        GeographicCoordinateT(23.25727    ,115.2272),
        AltitudeT(15000.0),
        #GeographicCoordinateT(*common.parse_tools.parse_lat_long('900000N1140832E')),
        GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['P270']['Lat_Long'])),
        AltitudeT(15000.0))
    print(trajectory)
    #for num in range(12):
    for num in (5, 11):
        compute_polygonic_volume_exit_point(trajectory, num)
    trajectory = VolumicSegmentT(
        #GeographicCoordinateT(23.12677, 114.1405),
        GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['P270']['Lat_Long'])),
        AltitudeT(15000.0),
        GeographicCoordinateT(23.12500    ,114.1260),
        #GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['SHL']['Lat_Long'])),
        AltitudeT(15000.0))
    print(trajectory)
    #for num in range(12):
    for num in (5, 11):
        compute_polygonic_volume_exit_point(trajectory, num)



