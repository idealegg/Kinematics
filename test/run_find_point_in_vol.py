from func_if.polygon_util import *
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point


def case1():
    sc = offl_if.sys_centre.SysCentre('BE')
    fv = offl_if.fdp_vol.FdpVolume('BE')
    chp = offl_if.char_point.CharPoint('BE')
    init_earth(sc)
    init_centre(sc)
    ret = prepare_polygons(fv)
    if ret:
        print("prepare_polygons error: %s" % ret)
        exit(1)
    #find_out_volume_containing_point('400430N1163524E', 0)
    #find_out_volume_containing_point('311154N1212006E', 0)
    #find_out_volume_containing_point('392955N1163506E', 0)
    find_out_volume_containing_point(chp.char_point['DEFINITIONS']['ZBAA']['Lat_Long'])
    find_out_volume_containing_point(chp.char_point['DEFINITIONS']['ZSQD']['Lat_Long'])
    find_out_volume_containing_point(chp.char_point['DEFINITIONS']['ZGGG']['Lat_Long'])

def case2(site, plist):
    sc = offl_if.sys_centre.SysCentre(site)
    fv = offl_if.fdp_vol.FdpVolume(site)
    chp = offl_if.char_point.CharPoint(site)
    init_earth(sc)
    init_centre(sc)
    ret = prepare_polygons(fv)
    if ret:
        print("prepare_polygons error: %s" % ret)
        exit(1)
    #find_out_volume_containing_point('343109N1135026E', 12400.00)
    for p in plist:
        find_all_volume_containing_point(p[0], p[1] if len(p)>1 else 0.0)


if __name__ == "__main__":
    case2('ZZ', [((34.517662, 113.841034), 2088.5498),
                 ((34.517662, 113.841034), 3000.0),
                 ((34.7005272, 113.78241), 12400.0),
                 ])