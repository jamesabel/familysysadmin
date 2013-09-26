import os
import evernote.edam.userstore.constants as UserStoreConstants

# evernote specific routines
import systeminfo

def checks(user_store):
    version_ok = user_store.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )

    #print "Is my Evernote API version up to date? ", get_enml_str(version_ok)
    #print ""
    if not version_ok:
        exit(1)

# For testing, the developer must provide secret.py and it must have:
# auth_token = "your developer token"
#def check_secret_exists():
#    if not os.path.exists('secret.py'):
#        print("For testing, the developer must provide secret.py and it must look like:")
#        print('auth_token = "your developer token"')

# create the note string in ENML
def create_note_enml(note):
    sysinfo = systeminfo.systeminfo()
    enml_str = dict_to_enml(sysinfo.update())
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

def dict_to_enml(pdict):
    # put the system info into an ENML compatible string
    s = ''
    for e in pdict:
        s += e + " : " + pdict[e] + '<br/>\n'
    return s