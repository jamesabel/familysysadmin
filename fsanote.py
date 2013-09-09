
import systeminfo

# create the note string in ENML
def create_note_enml(note):
    sysinfo = systeminfo.systeminfo()
    print(sysinfo.get_enml_str())
    # The content of an Evernote note is represented using Evernote Markup Language
    # (ENML). The full ENML specification can be found in the Evernote API Overview
    # at http://dev.evernote.com/documentation/cloud/chapters/ENML.php
    note.content = '<?xml version="1.0" encoding="UTF-8"?>'
    note.content += '<!DOCTYPE en-note SYSTEM ' \
        '"http://xml.evernote.com/pub/enml2.dtd">'
    # note.content += '<en-note>Here is the Evernote logo:<br/>'
    note.content += '<en-note>' + sysinfo.get_enml_str() + '<br/>'
    note.content += '</en-note>'