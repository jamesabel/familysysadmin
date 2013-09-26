import platform
import threading
import sys

import ConfigParser
import psutil
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as EvernoteTypes
from evernote.api.client import EvernoteClient

import fsaevernote
import fsaconfig
import exitcontrol

class FamilySysAdmin:

    def __init__(self, test_mode = False, verbose = False):
        self.verbose = verbose
        self.test_mode = test_mode
        self.app_name = "familysysadmin"

        if self.test_mode:
            # use sandbox
            config = fsaconfig.FSAConfig(self.app_name, self.verbose)
            self.auth_token = config.get_auth_token()
            if self.auth_token is None:
                print("error:auth_token not initialized - please put it in the secret area")
                sys.exit()

    def run(self):
        continue_control_timeout = 3 # fast for testing, slow for regular use

        continue_control = threading.Event()

        exit_control = exitcontrol.KBHit()
        exit_control.setup(events=[continue_control,], exit_criteria='q')
        exit_control.start()

        client = EvernoteClient(token=self.auth_token, sandbox=True)

        while not exit_control.get_exit_control_flag():

            try:
                user_store = client.get_user_store()
                note_store = client.get_note_store()
                network_ok = True
            except:
                network_ok = False

            # todo: put try around everything that accesses the network
            if network_ok:
                fsaevernote.checks(user_store)

                config = fsaconfig.FSAConfig(self.app_name, self.verbose)
                config_guid = config.get_guid() # get the guid associated with this note (None if 1st time run)
                if config_guid is None:
                    # create a new note
                    note = EvernoteTypes.Note()
                    note.title = platform.node()
                    fsaevernote.create_note_enml(note)
                    created_note = note_store.createNote(note)
                    config.set_guid(created_note.guid)
                    if self.verbose:
                        print("created note", created_note.guid)
                else:
                    # update the existing note
                    note = client.get_note_store().getNote(config_guid, True, True, False, False)
                    fsaevernote.create_note_enml(note)
                    note_store.updateNote(note)
                    if self.verbose:
                        print("updated note", note.guid)
            else:
                print("network down")

            continue_control.wait(continue_control_timeout)




