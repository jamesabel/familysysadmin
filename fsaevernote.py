import os
import evernote.edam.userstore.constants as UserStoreConstants

# evernote specific routines

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
def check_secret_exists():
    if not os.path.exists('secret.py'):
        print("For testing, the developer must provide secret.py and it must look like:")
        print('auth_token = "your developer token"')

