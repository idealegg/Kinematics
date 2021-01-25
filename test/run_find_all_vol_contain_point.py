from func_if.polygon_util import *
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point


if __name__ == "__main__":
    project='ZZ'
    sc = offl_if.sys_centre.SysCentre(project)
    fv = offl_if.fdp_vol.FdpVolume(project)
    chp = offl_if.char_point.CharPoint(project)
    init_earth(sc)
    init_centre(sc)
    ret = prepare_polygons(fv)
    if ret:
        print("prepare_polygons error: %s" % ret)
        exit(1)
    #find_all_volume_containing_point(chp.char_point['DEFINITIONS']['P270']['Lat_Long'], 15000.0)
    #find_all_volume_containing_point('230736N1140826E' ,15000.0)
    #find_all_volume_containing_point(chp.char_point['DEFINITIONS']['P154']['Lat_Long'],15000.0)
    #find_all_volume_containing_point(chp.char_point['DEFINITIONS']['SHL']['Lat_Long'],15000.0)
    #find_all_volume_containing_point(chp.char_point['DEFINITIONS']['POU']['Lat_Long'],15000.0)
    #find_all_volume_containing_point('231526N1151338E', 15000.0)
    #find_all_volume_containing_point('230730N1140734E', 15000.0)
    #find_all_volume_containing_point(chp.char_point['DEFINITIONS']['ENLAB']['Lat_Long'], 23622.04)
    #find_all_volume_containing_point(chp.char_point['DEFINITIONS']['ESMEB']['Lat_Long'], 23622.04)
    #find_all_volume_containing_point('322258N1143812E', 23622.04)
    #find_all_volume_containing_point('322300N1143812E', 23622.04)
    find_all_volume_containing_point(chp.char_point['DEFINITIONS']['P145']['Lat_Long'], 19972.94)


