import sys

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as EvernoteTypes
from evernote.api.client import EvernoteClient

import settings

# todo: put try around everything that accesses the network

class FSAEvernote:
    """
    evernote specific routines
    """

    def __init__(self, verbose = False, mute = False):
        self.verbose = verbose
        self.mute = mute # for testing but stay offline
        if not self.mute:
            app_settings = settings.SettingsDialog()
            auth_token = app_settings.get('auth_token')
            self.client = EvernoteClient(token=auth_token, sandbox=True)

    def checks(self):
        if self.mute:
            return
        version_ok = self.user_store.checkVersion(
            "Evernote EDAMTest (Python)",
            UserStoreConstants.EDAM_VERSION_MAJOR,
            UserStoreConstants.EDAM_VERSION_MINOR
        )

        #print "Is my Evernote API version up to date? ", get_enml_str(version_ok)
        #print ""
        if not version_ok:
            print("bad version")
            sys.exit(1)

    def init_stores(self):
        if self.mute:
            return
        try:
            self.user_store = self.client.get_user_store()
            self.note_store = self.client.get_note_store()
            self.network_ok = True
            if self.verbose:
                print("network OK")
        except:
            self.network_ok = False

    def create_note(self, title, systeminfo):
        if self.mute:
            return
        # create a new note
        self.note = EvernoteTypes.Note()
        self.note.title = title
        self.create_note_enml(self.note, systeminfo)
        created_note = self.note_store.createNote(self.note)
        if self.verbose:
            print("created note", created_note.guid)
        return created_note.guid

    def update_note(self, config_guid, systeminfo):
        if self.mute:
            return
        self.note = self.client.get_note_store().getNote(config_guid, True, True, False, False)
        self.create_note_enml(self.note, systeminfo)
        self.note_store.updateNote(self.note)
        if self.verbose:
            print("updated note", config_guid)

    # create the note string in ENML
    def create_note_enml(self, note, systeminfo):
        enml_str = self.dict_to_enml(systeminfo)
        print(enml_str)
        # The content of an Evernote note is represented using Evernote Markup Language
        # (ENML). The full ENML specification can be found in the Evernote API Overview
        # at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
        note.content = '<?xml version="1.0" encoding="UTF-8"?>'
        note.content += '<!DOCTYPE en-note SYSTEM ' \
            '"http://xml.evernote.com/pub/enml2.dtd">'
        # note.content += '<en-note>Here is the Evernote logo:<br/>'
        note.content += '<en-note>' + enml_str + '<br/>'
        note.content += '</en-note>'

    def dict_to_enml(self, pdict):
        # put the system info into an ENML compatible string
        s = ''
        for e in pdict:
            s += e + " : " + pdict[e] + '<br/>\n'
        return s