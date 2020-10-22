import re
import os


class CharPoint(object):
    def __init__(self, project):
        self.f_name = 'CHARACTERISTIC_POINTS'
        self.pro = project
        self.src_name = "".join([self.f_name, '.ASF'])
        self.bin_name = "".join([self.f_name, '.AIF'])
        self.src_path = os.path.join('offline', project, self.src_name)
        self.bin_path = os.path.join('offline', project, self.bin_name)
        self.char_point = {'DEFINITIONS': {}}
        self.inited = False
        self.parse_src()
        #print(self.char_point)

    def parse_src(self):
        fd = open(self.src_path)
        self.char_point = {'DEFINITIONS': {}}
        cur_title = ""
        for line in fd:
          line = line.strip()
          comment = line.find("--")
          if comment != -1:
            line = line[:comment]
          if line:
            res = re.match("/(\w+)/", line)
            if res:
              cur_title = res.group(1)
            elif cur_title == "DEFINITIONS":
              res = re.search(
"(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|\s*([\w\s]*)\s*\|\s*(\w+)\s*\|\s*(\w+)"
                , line)
              if res:
                self.char_point['DEFINITIONS'][res.group(1)] = {}
                self.char_point['DEFINITIONS'][res.group(1)]['Lat_Long'] = res.group(2)
                self.char_point['DEFINITIONS'][res.group(1)]['Type'] = res.group(3)
                self.char_point['DEFINITIONS'][res.group(1)]['Relevant_fix'] = res.group(4)
                self.char_point['DEFINITIONS'][res.group(1)]['Airport_Id'] = res.group(5)
                self.char_point['DEFINITIONS'][res.group(1)]['Pilot_display'] = res.group(6)
                self.char_point['DEFINITIONS'][res.group(1)]['DTI'] = res.group(7)
        fd.close()
        self.inited = True


