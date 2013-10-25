
import os
import wx
import winpaths

import familysysadmin.familysysadmin

# todo:
# - figure out how to not have an error when starting up with nothing in the registry
# - make guid text boxes reasonable big even if there is nothing yet

if __name__ == "__main__":
    app_data_folder = os.path.join(winpaths.get_local_appdata(), familysysadmin.familysysadmin.APP_NAME)
    if not os.path.exists(app_data_folder):
        os.mkdir(app_data_folder)
    redirect_file = os.path.join(app_data_folder, 'log.txt')
    app = familysysadmin.familysysadmin.FamilySysAdminApp(redirect=True, filename=redirect_file)
    app.MainLoop()



