import re
import common.parse_tools
import os


class FdpVolume(object):
    def __init__(self, project):
        self.f_name = 'FDP_VOLUMES_DEFINITION'
        self.pro = project
        self.src_name = "".join([self.f_name, '.ASF'])
        self.bin_name = "".join([self.f_name, '.AIF'])
        self.src_path = os.path.join('offline', project, self.src_name)
        self.bin_path = os.path.join('offline', project, self.bin_name)
        self.fdp_vol = {'POINTS': {}, 'ARCS': {}, 'LAYER': {}, 'VOLUME': {}, 'SECTOR': {},
                 'MIL_AREA': {}, 'EUROCAT_T_AREA': {}, 'NON_SURVEILLANCE_TOWER': {}, 'FIR': {}}
        self.inited = False
        self.map_vol = {}
        self.parse_src()
        self.map_volume()
        #print ("fdp_vol: %s" % self.fdp_vol['VOLUME'])
        #print("map_vol: %s" % self.map_vol)

    def parse_src(self):
      fd = open(self.src_path)
      cur_title = ""
      cur_vol = ""
      cur_sec = ""
      cur_fir = ""
      last_layer = 0
      for line in fd:
        line = line.strip()
        comment = line.find("--")
        if comment != -1:
          line = line[:comment]
        if line:
          res = re.match("/(\w+)/", line)
          if res:
            cur_title = res.group(1)
          elif cur_title == "POINTS":
            res = re.search("^(\w+)\s*\|\s*(\w+)", line)
            if res:
              self.fdp_vol['POINTS'][res.group(1)] =  res.group(2)
          elif cur_title == "ARCS":
            res = re.search("^(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)", line)
            if res:
              self.fdp_vol['ARCS'][res.group(1)] = {}
              self.fdp_vol['ARCS'][res.group(1)]['start'] = res.group(2)
              self.fdp_vol['ARCS'][res.group(1)]['end'] = res.group(3)
              self.fdp_vol['ARCS'][res.group(1)]['centre'] = res.group(4)
              self.fdp_vol['ARCS'][res.group(1)]['precision'] = res.group(5)
          elif cur_title == "LAYER":
            res = re.search("^(\w+)\s*\|\s*(\w+)", line)
            if res:
              self.fdp_vol['LAYER'][res.group(1)] = {}
              self.fdp_vol['LAYER'][res.group(1)]['layer'] = res.group(2)
              self.fdp_vol['LAYER'][res.group(1)]['max'] = common.parse_tools.parse_height(res.group(2))
              self.fdp_vol['LAYER'][res.group(1)]['min'] = last_layer
              last_layer = self.fdp_vol['LAYER'][res.group(1)]['max']
          elif cur_title == "VOLUME":
            res = re.search("^(\w+)\s*\|\s*([\w-]+)\s*\|\s*([\w\s]+)", line)
            if res:
              cur_vol = res.group(1)
              self.fdp_vol['VOLUME'][cur_vol] = {}
              self.fdp_vol['VOLUME'][cur_vol]['layer'] = res.group(2).lstrip('0')
              self.fdp_vol['VOLUME'][cur_vol]['floor'], self.fdp_vol['VOLUME'][cur_vol]['ceiling'] = common.parse_tools.get_level(
                  self.fdp_vol['VOLUME'][cur_vol]['layer'],
                  self.fdp_vol
              )
              self.fdp_vol['VOLUME'][cur_vol]['points'] = res.group(3)
              self.fdp_vol['VOLUME'][cur_vol]['point_list'] = re.findall("\w+", self.fdp_vol['VOLUME'][cur_vol]['points'])
            else:
              res = re.search("^\s*\|\s*\|\s*([\w\s]+)", line)
              if res:
                self.fdp_vol['VOLUME'][cur_vol]['points'] = ' '.join([self.fdp_vol['VOLUME'][cur_vol]['points'], res.group(1)])
                self.fdp_vol['VOLUME'][cur_vol]['point_list'] = re.findall("\w+", self.fdp_vol['VOLUME'][cur_vol]['points'])
          elif cur_title == "SECTOR":
            line = line.replace("+", ' ')
            res = re.search("^(\w+)\s*\|\s*(\w+)\s*\|\s*([\w\s]+)", line)
            if res:
              cur_sec = res.group(1)
              self.fdp_vol['SECTOR'][cur_sec] = {}
              self.fdp_vol['SECTOR'][cur_sec]['precision'] = res.group(2)
              self.fdp_vol['SECTOR'][cur_sec]['vols'] = res.group(3)
              self.fdp_vol['SECTOR'][cur_sec]['vol_list'] = re.findall("\w+", self.fdp_vol['SECTOR'][cur_sec]['vols'])
            else:
              res = re.search("^\s*\|\s*\|\s*([\w\s]+)", line)
              self.fdp_vol['SECTOR'][cur_sec]['vols'] = ' '.join([self.fdp_vol['SECTOR'][cur_sec]['vols'], res.group(1)])
              self.fdp_vol['SECTOR'][cur_sec]['vol_list'] = re.findall("\w+", self.fdp_vol['SECTOR'][cur_sec]['vols'])
          elif cur_title in ('MIL_AREA', 'EUROCAT_T_AREA', 'NON_SURVEILLANCE_TOWER', 'FIR'):
            line = line.replace("+", ' ')
            res = re.search("^(\w+)\s*\|\s*([\w\s]+)", line)
            if res:
              cur_fir = res.group(1)
              self.fdp_vol[cur_title][cur_fir] = {}
              self.fdp_vol[cur_title][cur_fir]['vols'] = res.group(2)
              self.fdp_vol[cur_title][cur_fir]['vol_list'] = re.findall("\w+", self.fdp_vol[cur_title][cur_fir]['vols'])
            else:
              res = re.search("^\s*\|\s*([\w\s]+)", line)
              self.fdp_vol[cur_title][cur_fir]['vols'] = ' '.join([self.fdp_vol[cur_title][cur_fir]['vols'], res.group(1)])
              self.fdp_vol[cur_title][cur_fir]['vol_list'] = re.findall("\w+", self.fdp_vol[cur_title][cur_fir]['vols'])
      fd.close()
      self.inited = True

    def map_volume(self):
        i = 0
        self.map_vol = {}
        for vol in self.fdp_vol['VOLUME']:
            self.map_vol[i] = vol
            i+=1

