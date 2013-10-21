
import threading
import platform
import os
import time
import psutil
import datetime
import uptime
import collections
import wx
import win32api

import fsaevernote

class Monitor(threading.Thread):
    def run(self):
        self.continue_control = threading.Event()
        self.timeout = threading.Event()
        self.verbose = True
        app_settings = wx.Config()
        fsa_note = fsaevernote.FSAEvernote(verbose = True)
        while not self.continue_control.is_set():
            fsa_note.init_stores()
            if fsa_note.network_ok:
                fsa_note.checks()
                config_guid = app_settings.Read('guid') # get the guid associated with this note (None if 1st time run)
                if len(config_guid) > 0 :
                    # delete the existing note
                    fsa_note.delete_note(config_guid)
                config_guid = fsa_note.create_note(platform.node(), self.get_systeminfo())
                app_settings.Write('guid', config_guid)
            else:
                print("problem accessing evernote servers")
            self.timeout.clear()
            self.timeout.wait(60*60) # todo: make this a configuration option

    def update_monitor(self):
        print("update")
        self.timeout.set()

    def stop_monitor(self):
        print("stopping")
        self.continue_control.set()
        self.timeout.set()

    def get_systeminfo(self):
        gb = pow(1024.0,3)
        self.states = collections.OrderedDict()
        self.states['computername'] = platform.node()
        self.states['user'] = win32api.GetUserName()
        self.disks = psutil.disk_partitions(all=True)
        for disk in self.disks:
            disk_path = disk[0]
            try:
                total, used, free, percent = psutil.disk_usage(disk_path)
                volume_name, serial_number, max_len, flags, fs_name = win32api.GetVolumeInformation(disk_path)
                total = total/gb # convert to gb
                used = used/gb
                self.states[disk_path] = str(percent) + '% (' + str(used) + ' / ' + str(total) + ' gb) (' + volume_name + ')'
            except:
                print("warning: can not access", disk_path)
        self.states['usertime'] = str(os.times()[0])
        self.states['systemtime'] = str(os.times()[1])
        self.states['uptime'] = str(datetime.timedelta(seconds = uptime.uptime()))
        self.states['timestamp'] = time.strftime('%c')
        return self.states