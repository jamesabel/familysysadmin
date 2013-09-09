
import evernote.edam.userstore.constants as UserStoreConstants

def checks(user_store):
    version_ok = user_store.checkVersion(
        "Evernote EDAMTest (Python)",
        UserStoreConstants.EDAM_VERSION_MAJOR,
        UserStoreConstants.EDAM_VERSION_MINOR
    )

    #print "Is my Evernote API version up to date? ", str(version_ok)
    #print ""
    if not version_ok:
        exit(1)

