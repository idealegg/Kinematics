# -*- coding: utf-8 -*-
import sys
import os
import matplotlib.pyplot as plt
import pprint
import numpy as np
from func_if.polygon_util import *
import offl_if.fdp_vol
import offl_if.sys_centre
import offl_if.char_point
import numpy as np
import cv2


volume_dir = "volumes_dir"
colors = (
    ('b'  ,       'blue'   ) ,
    ('g'  ,       'green'  ) ,
    ('r'  ,       'red'    ) ,
    ('c'  ,       'cyan'   ),
    ('m'  ,       'magenta') ,
    ('y'  ,       'yellow' ) ,
    ('k'  ,       'black'  ) ,
    ('w'  ,       'white'  ) )
lines = (
    ('-'   ,      'solid line style'),
    ('--'  ,      'dashed line style'),
    ('-.'  ,      'dash-dot line style'),
#    (':'   ,      'dotted line style'),
#    ('.'   ,      'point marker'),
#    (','   ,      'pixel marker'),
#    ('o'   ,      'circle marker'),
#    ('v'   ,      'triangle_down marker'),
#    ('^'   ,      'triangle_up marker'),
#    ('<'   ,      'triangle_left marker'),
#    ('>'   ,      'triangle_right marker'),
#    ('1'   ,      'tri_down marker'),
#    ('2'   ,      'tri_up marker'),
#    ('3'   ,      'tri_left marker'),
#    ('4'   ,      'tri_right marker'),
#    ('s'   ,      'square marker'),
#    ('p'   ,      'pentagon marker'),
#    ('*'   ,      'star marker'),
#    ('h'   ,      'hexagon1 marker'),
#    ('H'   ,      'hexagon2 marker'),
#    ('+'   ,      'plus marker'),
#    ('x'   ,      'x marker'),
#    ('D'   ,      'diamond marker'),
#    ('d'   ,      'thin_diamond marker'),
#    ('|'   ,      'vline marker'),
    ('_'   ,      'hline marker'))


def readPoly(fileName):
  polyx = []
  polyy = []
  fd =  open(fileName)
  for line in fd:
    fields = line.split()
    polyx.append(float(fields[1]))
    polyy.append(float(fields[2]))
  fd.close()
  return polyx, polyy

def Daw1Poly(name, polyx, polyy, pnames=None):
  plt.figure(1)
  plt.title(name)
  plt.xlabel('x')
  plt.ylabel('y')
  plt.axis([min(polyx), max(polyx), min(polyy), max(polyy)])
  plt.grid(True)
  plt.plot(polyx, polyy, 'g-', label=name)
  if pnames:
    for i, pn in enumerate(pnames):
        plt.annotate(pn, xytext=(polyx[i], polyy[i]), xy=(polyx[i], polyy[i]))
  plt.show()

def mymin(listl):
  tmin = 1000000.0
  for i in listl:
    tmin = min(min(i), tmin)
  print( "mymin: %d\n" % tmin)
  return tmin

def mymax(listl):
  tmax = -1000000.0
  for i in listl:
    tmax = max(max(i), tmax)
  print( "mymax: %d\n" % tmax)
  return tmax

def DawPolys(names, polyxs, polyys):
  cl = map(lambda x:
               map(lambda y:x+y,
                   map(lambda x :x[0], list(lines))),
           map(lambda x:x[0], list(colors)))
  cl = np.array(cl).flatten().tolist()
  plt.figure(1)
  plt.title("Polys")
  plt.xlabel('x')
  plt.ylabel('y')
  xx = np.linspace(-51, -52, 100)
  yy = np.linspace(15, 16, 100)
  plt.axis([min(mymin(polyxs), min(xx)),
            max(mymax(polyxs),  max(xx)),
            min(mymin(polyys),  min(xx)),
            max(mymax(polyys), max(xx))])
  plt.grid(True)
  plt.plot(xx, yy, 'r-', label="zwhz")
  for i in range(1, len(names)):
    plt.plot(polyxs[i-1], polyys[i-1], cl[(i-1)%len(cl)], label=names[i])
  plt.legend()
  plt.show()


if __name__ == "__main__":
  polyxs = []
  polyys = []
  if 0:
      for i in range(1, len(sys.argv)):
        polyx, polyy = readPoly(os.path.sep.join([volume_dir, sys.argv[i]]))
        #pprint.pprint(polyx)
        #pprint.pprint(polyy)
        polyxs.append(polyx)
        polyys.append(polyy)
      #Daw1Poly(os.path.basename(sys.argv[1]), polyx, polyy)
      DawPolys(sys.argv, polyxs, polyys)
  else:
      project = 'NN'
      sc = offl_if.sys_centre.SysCentre(project)
      fv = offl_if.fdp_vol.FdpVolume(project)
      chp = offl_if.char_point.CharPoint(project)
      init_earth(sc)
      init_centre(sc)
      cur_vol = 'V1G'
      use_geo = False
      ptss = fv.fdp_vol['VOLUME'][cur_vol]['point_list']
      ptss2 = []
      for p in ptss:
          print("%s: %s" % (p, fv.fdp_vol['POINTS'][p]))
          if use_geo:
              x, y = common.parse_tools.parse_lat_long(fv.fdp_vol['POINTS'][p])
              polyxs.append(x)
              polyys.append(y)
          else:
              stg = kine_dll.geo_2_stereo_coordinates(
                  GeographicCoordinateT(*common.parse_tools.parse_lat_long(fv.fdp_vol['POINTS'][p])))
              polyxs.append(stg.x)
              polyys.append(stg.y)
      print(polyxs)
      print(polyys)
      Daw1Poly(cur_vol, polyxs, polyys, ptss)