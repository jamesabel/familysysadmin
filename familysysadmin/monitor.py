
import threading
import platform
import sys
import os
import time
import psutil
import datetime
import uptime
import collections

import fsaevernote
import fsaconfig

class Monitor(threading.Thread):
    def run(self):
        self.test_mode = True
        self.verbose = True
        config = fsaconfig.FSAConfig(self.verbose)
        if self.test_mode:
            # use sandbox
            self.auth_token = config.get('auth_token')
            if self.auth_token is None:
                print("error:auth_token not initialized - please put it in the secret area")
                sys.exit()

        fsa_note = fsaevernote.FSAEvernote(verbose = True)
        # todo: loop this in a separate thread, that can be stopped on close of the GUI
        #while continue_control.is_set():
        if True:
            fsa_note.init_stores()
            if fsa_note.network_ok:
                fsa_note.checks()
                config_guid = config.get('guid') # get the guid associated with this note (None if 1st time run)
                if config_guid is None:
                    config_guid = fsa_note.create_note(platform.node())
                    config.set('guid', config_guid)
                else:
                    # update the existing note
                    fsa_note.update_note(config_guid, self.get_systeminfo())
            else:
                print("network down")

    def get_systeminfo(self):
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