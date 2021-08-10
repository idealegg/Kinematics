from func_if.polygon_util import *
import func_if
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point

def case1():
    # start_p=kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(20.01333, 110.1383))
    start_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(19.833439, 110.0510))
    # start_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(19.55722, 109.9164))
    # start_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['NYB']['Lat_Long'])))
    end_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(19.37889, 109.8302))
    # end_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['P395']['Lat_Long'])))
    m_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(19.53019, 109.9034))
    height1 = AltitudeT(30183.72)
    # height1 = AltitudeT(24360.91)
    height2 = AltitudeT(20360.91)
    height3 = AltitudeT((24360.91 + 20360.91) / 2)
    height4 = AltitudeT(0)
    dis, ret = distance_on_the_great_circle(start_p, end_p, height1)
    dis2, ret2 = distance_on_the_great_circle(start_p, m_p, height1)
    print('dis: %s, dis2: %s' % (dis, dis2))
    print('com_fl: %s' % (height1.value - (height1.value - height2.value) * dis2.value / dis.value,))
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

def case2(p1, p2, h=0.0):
    if type(p1) is list or type(p1) is tuple:
        start_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(p1[0], p1[1]))
    else:
        start_p = kine_dll.geo_2_stereo_coordinates(
            GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS'][p1]['Lat_Long'])))
    if type(p2) is list or type(p2) is tuple:
        end_p = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(p2[0], p2[1]))
    else:
        end_p = kine_dll.geo_2_stereo_coordinates(
            GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS'][p2]['Lat_Long'])))
    dis, ret = distance_on_the_great_circle(start_p, end_p, AltitudeT(h))
    print('ret: %s, dis: %s' % (ret, dis))
    return dis.value

if __name__ == "__main__":
    site = 'JN'
    sc = offl_if.sys_centre.SysCentre(site)
    fv = offl_if.fdp_vol.FdpVolume(site)
    chp = offl_if.char_point.CharPoint(site)
    init_earth(sc)
    init_centre(sc)
    #case1()
    #case2((35.02716    ,111.3598), (35.02833    ,111.3583), 20000.00)
    #case2((35.02716, 111.3598), (35.02833, 111.3583), 0)
    #case2('KARVU', 'AVLIS')
    #case2((37.30082815419277 ,115.03778946015574), 'AVLIS')
    h1 = 23800.0
    h2 = 26574.8
    #d1 = case2('FQG', (25.84427, 119.4215), 0.0)
    #d2 = case2('FQG', (25.88519, 119.4354), 0.0)
    #print(h1 + (h2-h1)*(d1/d2))
    #case2((25.84427    ,119.4215), (25.83997    ,119.4201), 25798.40)
    #dis, ret = distance_on_the_great_circle(
    #    #kine_dll.geo_2_stereo_coordinates(
    #    #    GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['PAVTU']['Lat_Long'])))
    #    kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(28.21115698127199 ,114.3460392688246))
    #    , kine_dll.geo_2_stereo_coordinates(
    #        GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS']['OVTAN']['Lat_Long'])))
    #    , AltitudeT(29199.47))
    dis, ret = distance_on_the_great_circle(
       kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(32.36431    ,118.6723))
       , kine_dll.geo_2_stereo_coordinates(
            GeographicCoordinateT(32.36430    ,118.6722))
       , AltitudeT(0.0))
    print('ret: %s, dis: %s' % (ret, dis))
    dis, ret = distance_on_the_great_circle(
        kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(32.36431, 118.6723))
        , kine_dll.geo_2_stereo_coordinates(
            GeographicCoordinateT(32.07269    ,118.7610))
        , AltitudeT(0.0))
    print('ret: %s, dis: %s' % (ret, dis))





