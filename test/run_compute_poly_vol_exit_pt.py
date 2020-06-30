from func_if.polygon_util import *
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point
import common.parse_tools


if __name__ == "__main__":
    sc = offl_if.sys_centre.SysCentre('BE')
    fv = offl_if.fdp_vol.FdpVolume('BE')
    chp = offl_if.char_point.CharPoint('BE')
    init_earth(sc)
    init_centre(sc)
    ret = prepare_polygons(fv)
    if ret:
        print("prepare_polygons error: %s" % ret)
        exit(1)
    trajectory = VolumicSegmentT(
        GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['ZBAA']['Lat_Long'])),
        AltitudeT(10000.0),
        GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['ZSSS']['Lat_Long'])),
        AltitudeT(10000.0))
    print(trajectory)
    for num in range(30, 50):
        compute_polygonic_volume_exit_point(trajectory, num)



