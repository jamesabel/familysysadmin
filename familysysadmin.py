

import ConfigParser
import psutil
import platform

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as EvernoteTypes
from evernote.api.client import EvernoteClient

import fsaevernote
import fsanote
import fsaconfig

fsaevernote.check_secret_exists() # if we don't have the secret, print an error message at executable time
import secret

app_name = "familysysadmin"

client = EvernoteClient(token=secret.auth_token, sandbox=True)
user_store = client.get_user_store()
note_store = client.get_note_store()

fsaevernote.checks(user_store)

config = fsaconfig.FSAConfig(app_name)
config_guid = config.get_guid() # get the guid associated with this note (None if 1st time run)
if config_guid is None:
    # create a new note
    note = EvernoteTypes.Note()
    note.title = platform.node()
    fsanote.create_note_enml(note)
    created_note = note_store.createNote(note)
    config.set_guid(created_note.guid)
    print("created note", created_note.guid)
else:
    # update the existing note
    note = client.get_note_store().getNote(config_guid, True, True, False, False)
    fsanote.create_note_enml(note)
    note_store.updateNote(note)
    print("updated note", note.guid)




