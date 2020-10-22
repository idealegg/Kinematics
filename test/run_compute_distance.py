from func_if.polygon_util import *
import func_if
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point


if __name__ == "__main__":
    sc = offl_if.sys_centre.SysCentre('SH')
    fv = offl_if.fdp_vol.FdpVolume('SH')
    chp = offl_if.char_point.CharPoint('SH')
    init_earth(sc)
    init_centre(sc)
    #start_p=kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(20.01333, 110.1383))
    start_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(19.833439, 110.0510))
    #start_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(19.55722, 109.9164))
    #start_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['NYB']['Lat_Long'])))
    end_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(19.37889, 109.8302))
    #end_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['P395']['Lat_Long'])))
    m_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(19.53019, 109.9034))
    height1 = AltitudeT(30183.72)
    #height1 = AltitudeT(24360.91)
    height2 = AltitudeT(20360.91)
    height3 = AltitudeT((24360.91+20360.91)/2)
    height4 = AltitudeT(0)
    dis, ret = distance_on_the_great_circle(start_p, end_p, height1)
    dis2, ret2 = distance_on_the_great_circle(start_p, m_p, height1)
    print('dis: %s, dis2: %s' %(dis, dis2))
    print('com_fl: %s' % (height1.value-(height1.value-height2.value)*dis2.value/dis.value,))
    dis, ret = distance_on_the_great_circle(start_p, end_p, height2)
    dis2, ret2 = distance_on_the_great_circle(start_p, m_p, height2)
    print('dis: %s, dis2: %s' % (dis, dis2))
    print('com_fl: %s' % (height1.value - (height1.value - height2.value) * dis2.value / dis.value,))
    dis, ret = distance_on_the_great_circle(start_p, end_p, height3)
    dis2, ret2 = distance_on_the_great_circle(start_p, m_p, height3)
    print('dis: %s, dis2: %s' % (dis, dis2))
    print('com_fl: %s' % (height1.value - (height1.value - height2.value) * dis2.value / dis.value,))
    dis, ret = distance_on_the_great_circle(start_p, end_p, height4)
    dis2, ret2 = distance_on_the_great_circle(start_p, m_p, height4)
    print('dis: %s, dis2: %s' % (dis, dis2))
    print('com_fl: %s' % (height1.value - (height1.value - height2.value) * dis2.value / dis.value,))



