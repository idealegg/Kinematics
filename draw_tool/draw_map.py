def getlevel(layer, fdp_vol):
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


def getXYZ(fdp_vol, vol_list):
  X = []
  Y = []
  Z = []
  X1 = []
  Y1 = []
  Z1 = []
  for vol in vol_list:
    for point in fdp_vol['VOLUME'][vol]['point_list']:
      level = getlevel(fdp_vol['VOLUME'][vol]['layer'], fdp_vol)
      p = Point(fdp_vol['POINTS'][point], "", True, level[0])
      X.append(p.x)
      Y.append(p.y)
      Z.append(p.z)
      p = Point(fdp_vol['POINTS'][point], "", True, level[1])
      X1.append(p.x)
      Y1.append(p.y)
      Z1.append(p.z)
  return X, Y, Z, X1, Y1, Z1


def draw_vol(fdp_vol, vol, color, ax1):
  X, Y, Z, X1, Y1, Z1 = getXYZ(fdp_vol, [vol])
  ax1.plot_trisurf(X, Y, Z, linewidth=0.2, antialiased=True, color=color)
  ax1.plot_trisurf(X1, Y1, Z1, linewidth=0.2, antialiased=True, color=color)


def draw_sec(fdp_vol, secs, ax1):
  global colors
  i = 0
  for sec in secs:
    for vol in fdp_vol['SECTOR'][sec]['vol_list']:
      draw_vol(fdp_vol, vol, colors[i % len(colors)][0], ax1)
    i = i + 1


def draw_fir(fdp_vol, firs, ax1):
  global colors
  i = 0
  for fir in firs:
    for vol in fdp_vol['FIR'][fir]['vol_list']:
      draw_vol(fdp_vol, vol, colors[i % len(colors)][0], ax1)
    i = i + 1


def draw_route(char_point, route, ax1, level):
  X = []
  Y = []
  Z = []
  for point in route:
    if type(point) == type(()):
      if len(point) == 2:
        p = Point(point[1], point[0], False, level)
      else:
        p = Point(point[1], point[0], False, 0)
      name = "(%f, %f)"%(point[0], point[1])
    else:
      p = Point(char_point['DEFINITIONS'][point]['Lat_Long'], "", True, level)
      name = point
    X.append(p.x)
    Y.append(p.y)
    Z.append(p.z)
    ax1.text(p.x, p.y, p.z, name, color="b")
  #ax1.plot(X, Y, Z, linewidth=10)
  ax1.plot(X, Y, Z, 'ro')
