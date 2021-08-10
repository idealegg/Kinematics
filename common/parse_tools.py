import re
#from common.kinematics import *


colors = (
    ('b', 'blue'),
    ('g', 'green'),
    ('r', 'red'),
    ('c', 'cyan'),
    ('m', 'magenta'),
    ('y', 'yellow'),
    ('k', 'black'),
    ('w', 'white'))



def parse_lat_long(lat, long=''):
    '''350000N1240000E'''
    t_long = long
    t_lat = lat
    p1 = re.compile("(\d{2,3})(\d{2})((\d{2})?)([NSEW])")
    for s in [long, lat]:
        ress = re.findall(p1, s)
        if len(ress) in [1, 2]:
            for res in ress:
                tmp = int(res[0], 10) + int(res[1], 10) / 60.0 + int(res[3] or "0", 10) / 3600.0
                if res[4] == 'N':
                    t_lat = tmp
                elif res[4] == 'S':
                    t_lat = -tmp
                elif res[4] == 'E':
                    t_long = tmp
                elif res[4] == 'W':
                    t_long = -tmp
    return t_lat, t_long



def parse_height(height):
  res = re.match("S(\d{4})", height)
  if res:
    return int(res.group(1), 10)*10.0
  res = re.match("F(\d{3})", height)
  if res:
    return int(res.group(1), 10)*30.48

def parse_distance(dis):
  res = re.match("([\d.]+)(KM|M|NM)", dis)
  if res:
    if res.group(2) == 'KM':
        return float(res.group(1)) * 1000.0
    elif res.group(2) == 'M':
        return float(res.group(1))
    elif res.group(2) == 'NM':
        return float(res.group(1)) * 1852.0

def get_level(layer, fdp_vol):
  layer1 = []
  res = re.match("(\d+)-(\d+)", layer)
  if res:
    layer1.append(res.group(1))
    layer1.append(res.group(2))
  else:
    layer1.append(layer)
    layer1.append(layer)
  #print "layer: %s\n" % layer
  return fdp_vol['LAYER'][layer1[0]]['min'], fdp_vol['LAYER'][layer1[1]]['max']