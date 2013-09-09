

import ConfigParser
import psutil
import platform

import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient

import checks
import fsanote
import fsaconfig

# For testing, the developer must provide secret.py and it must have:
# auth_token = "your developer token"
import secret

app_name = "familysysadmin"

client = EvernoteClient(token=secret.auth_token, sandbox=True)
user_store = client.get_user_store()
note_store = client.get_note_store()

checks.checks(user_store)

config = fsaconfig.FSAConfig(app_name)
config_guid = config.get_guid()

if config_guid is None:
    note = Types.Note()
    note.title = platform.node()
    fsanote.fill_note(note)
    created_note = note_store.createNote(note)
    config.set_guid(created_note.guid)
    print("created note", created_note.guid)
else:
    note = client.get_note_store().getNote(config_guid, True, True, False, False)
    fsanote.fill_note(note)
    note_store.updateNote(note)
    print("updated note", note.guid)




