from func_if.polygon_util import *
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point
import common.parse_tools


if __name__ == "__main__":
    project = 'SH'
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
        #GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['PAVTU']['Lat_Long'])),
        #GeographicCoordinateT(23.25727    ,115.2272),
        GeographicCoordinateT(26.6166668    ,119.616669),
        AltitudeT(25405.7637),
        #GeographicCoordinateT(*common.parse_tools.parse_lat_long('900000N1140832E')),
        #GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['OVTAN']['Lat_Long'])),
        GeographicCoordinateT(26.6976547    ,119.616669),
        AltitudeT(26574.8027))
    print(trajectory)
    #for num in range(12):
    for num in range(0, 937):
        compute_polygonic_volume_exit_point(trajectory, num)




