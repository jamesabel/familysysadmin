
import os
import platform
import datetime
import collections
import psutil
import time
import uptime

# gather up the system info

# todo: add a 'changed' semantic so we know if we need to update the note

class systeminfo :

    def update(self):
        self.states = collections.OrderedDict()
        self.states['computername'] = platform.node()
        self.disks = psutil.disk_partitions(all=True)
        for disk in self.disks:
            disk_path = disk[0]
            try:
                disk_usage = str(psutil.disk_usage(disk_path)[3])
                self.states[disk_path] = disk_usage + '%'
            except:
                print("warning: can not access", disk_path)
        self.states['usertime'] = str(os.times()[0])
        self.states['systemtime'] = str(os.times()[1])
        self.states['uptime'] = str(datetime.timedelta(seconds = uptime.uptime()))
        self.states['timestamp'] = time.strftime('%c')
        return self.states


