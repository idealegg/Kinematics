import re
import os
import common.parse_tools


class SysCentre(object):
    pattern = re.compile('^\s*(\w+)\s*\|\s*([\w.]+)')
    def __init__(self, project):
        self.f_name = 'SYSTEM_CENTRE'
        self.pro = project
        self.src_name = "".join([self.f_name, '.ASF'])
        self.bin_name = "".join([self.f_name, '.AIF'])
        self.src_path = os.path.join('offline', project, self.src_name)
        self.bin_path = os.path.join('offline', project, self.bin_name)
        self.sys_ctr = {}
        self.inited = False
        self.parse_src()

    def parse_src(self):
        self.sys_ctr = {}
        fd = open(self.src_path)
        for line in fd:
            ret = re.search(SysCentre.pattern, line)
            if ret:
                self.sys_ctr[ret.group(1)] = ret.group(2)
        fd.close()
        assert('SYSTEM_CENTRE' in self.sys_ctr)
        assert ('RDF_HALF_GREAT_AXIS' in self.sys_ctr)
        assert ('RDF_HALF_SMALL_AXIS' in self.sys_ctr)
        self.sys_ctr['RDF_HALF_GREAT_AXIS'] = common.parse_tools.parse_distance(self.sys_ctr['RDF_HALF_GREAT_AXIS'])
        self.sys_ctr['RDF_HALF_SMALL_AXIS'] = common.parse_tools.parse_distance(self.sys_ctr['RDF_HALF_SMALL_AXIS'])
        print("SYSTEM_CENTRE: %s" % self.sys_ctr['SYSTEM_CENTRE'])
        print("RDF_HALF_GREAT_AXIS: %s" % self.sys_ctr['RDF_HALF_GREAT_AXIS'])
        print("RDF_HALF_SMALL_AXIS: %s" % self.sys_ctr['RDF_HALF_SMALL_AXIS'])

