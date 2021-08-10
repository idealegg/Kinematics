from func_if.polygon_util import *
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point
import numpy as np
import cv2


if __name__ == "__main__":
    project='NN'
    sc = offl_if.sys_centre.SysCentre(project)
    fv = offl_if.fdp_vol.FdpVolume(project)
    chp = offl_if.char_point.CharPoint(project)
    init_earth(sc)
    init_centre(sc)
    img = np.zeros((512, 512, 3), np.uint8)
    cur_vol='V1G'
    ptss=fv.fdp_vol['VOLUME'][cur_vol]['point_list'][:-1]
    ptss2 = []
    for p in ptss:
        print("%s: %s" % (p, fv.fdp_vol['POINTS'][p]))
        stg = kine_dll.geo_2_stereo_coordinates(GeographicCoordinateT(*common.parse_tools.parse_lat_long(fv.fdp_vol['POINTS'][p])))
        ptss2.append([stg.x+10, stg.y+40])
    print(ptss2)
    pts = np.array(ptss2, np.int32)
    #pts = pts.reshape((-1, 1, 2))
    cv2.polylines(img, [pts], True, (00, 255, 255))
    cv2.imshow('line', img)
    cv2.waitKey()