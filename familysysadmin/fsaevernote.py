import sys
import wx

import evernote
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as EvernoteTypes
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.api.client import EvernoteClient

# todo: fix the bug where we go back and forth from sandbox to developer and the logic with the existence
# of the GUID is broken.  If in one mode we create a note, we think the note exists but in reality
# it doesn't exist for the other mode (sandbox/developer).  Simple fix would be to have sandbox, developer and
# normal GUIDs.

class FSAEvernote:
    """
    evernote specific routines
    """

    def __init__(self, verbose = False, mute = False):
        self.verbose = verbose
        self.mute = mute # for testing but stay offline

    def get_client(self):
        self.client = None
        app_settings = wx.Config()

        # http://dev.evernote.com/doc/articles/authentication.php
        if app_settings.ReadBool('auth_mode_sandbox'):
            # https://sandbox.evernote.com/api/DeveloperToken.action
            sandbox_token = app_settings.Read('sandbox_token')
            if self.verbose:
                print("sandbox_token", sandbox_token)
            # I'm not sure what the default to EvernoteClient(sandbox) is, so provide it each time.
            # (if I don't I get an auth error)
            self.client = EvernoteClient(token=sandbox_token, sandbox=True)
        elif app_settings.ReadBool('auth_mode_dev'):
            # https://www.evernote.com/api/DeveloperToken.action
            dev_token = app_settings.Read('dev_token')
            if self.verbose:
                print("dev_token", dev_token)
            self.client = EvernoteClient(token=dev_token, sandbox=False)
        elif app_settings.ReadBool('auth_mode_normal'):
            print("auth_mode_normal not yet implemented")
        else:
            print("unknown auth mode")
        return self.client

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
        #try:
        self.get_client()
        self.user_store = self.client.get_user_store()
        print("user_store", self.user_store.checkVersion("Evernote EDAMTest (Python)",
            UserStoreConstants.EDAM_VERSION_MAJOR,
            UserStoreConstants.EDAM_VERSION_MINOR))
        #if self.verbose:
        #    print("user", self.user_store.getUser())
        self.note_store = self.client.get_note_store()
        self.network_ok = True
        if self.verbose:
            print("evernote server access OK")
        #except:
        #    self.network_ok = False

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

    #def update_note(self, config_guid, systeminfo):
    #    if self.mute:
    #        return
    #    note_store = self.get_client().get_note_store()
    #    self.note = note_store.getNote(config_guid, True, True, False, False)
    #    self.create_note_enml(self.note, systeminfo)
    #    self.note_store.updateNote(self.note)
    #    if self.verbose:
    #        print("updated note", config_guid)

    def delete_note(self, config_guid):
        note_store = self.get_client().get_note_store()
        try:
            note_store.expungeNote(config_guid)
        except evernote.edam.error.ttypes.EDAMNotFoundException:
            pass

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