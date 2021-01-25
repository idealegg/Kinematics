from func_if.polygon_util import *
import func_if
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point

def case1(ps):
    pts = []
    for p1 in ps:
        if type(p1) is list or type(p1) is tuple:
            start_p = GeographicCoordinateT(p1[0], p1[1])
        else:
            start_p = GeographicCoordinateT(*common.parse_tools.parse_lat_long(chp.char_point['DEFINITIONS'][p1]['Lat_Long']))
        pts.append(start_p)
    pro, ret = kine_dll.projection_to_the_great_circle_geo(*pts)
    print('ret: %s, pro: %s' % (ret, pro))
    pts.append(pro)
    for p in pts:
        p2 = kine_dll.geo_2_stereo_coordinates(p)
        print('pts: [%s] [%s]' %(p, p2))

def case2(p1, p2, h):
    pass

if __name__ == "__main__":
    sc = offl_if.sys_centre.SysCentre('BE')
    fv = offl_if.fdp_vol.FdpVolume('BE')
    chp = offl_if.char_point.CharPoint('BE')
    init_earth(sc)
    init_centre(sc)
    #case1()
    case1([ (37.30,115.04 ), 'KARVU', 'AVLIS'])





