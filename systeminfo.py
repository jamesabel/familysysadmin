
import os
import platform
import datetime
import psutil
import time
import uptime

# gather up the system info

class systeminfo :
    def __init__(self):
        self.computername = None
        self.disks = None
        self.info = {}

    def get(self):
        self.computername = platform.node()
        self.disks = psutil.disk_partitions(all=True)
        return self.info

    # put the system info into an ENML compatible string
    def get_enml_str(self):
        self.get()
        sep = '<br/>\n'
        s = "computername : " + self.computername + sep
        s += "disks :" + sep
        for disk in self.disks:
            disk_path = disk[0]
            disk_usage = str(psutil.disk_usage(disk_path)[3])
            s += disk_path + ' ' + disk_usage + '%' + sep
        s += "usertime : " + str(os.times()[0]) + sep
        s += "systemtime : " + str(os.times()[1]) + sep
        s += "uptime : " + str(datetime.timedelta(seconds = uptime.uptime())) + sep
        s += "timestamp : " + time.strftime('%c') + sep
        return s

