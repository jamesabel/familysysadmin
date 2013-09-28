
import os
import ConfigParser

class FSAConfig:
    """
    Config management (stores persistent data).
    """
    def __init__(self, verbose=False):
        self.app_name = 'familysysadmin'
        self.verbose = verbose
        self.section = 'evernote'
        self.config = ConfigParser.SafeConfigParser()
        self.config_file_path = self.app_name + '.ini'
        if self.verbose:
            print("config_file:", self.config_file_path)

    def exists(self):
        return os.path.exists(self.config_file_path)

    def get(self, name):
        """
        Generic "get a value" from the configuration file.
        """
        val = None
        if self.exists():
            self.config.read(self.config_file_path)
            if self.config.has_option(self.section, name):
                val = self.config.get(self.section, name)
        return val

    def set(self, key, val):
        if not self.config.has_section(self.section):
            self.config.add_section(self.section)
            self.set('app_name', self.app_name) # new config file - put in the app name
        self.config.set(self.section, key, val)
        self.write()

    def write(self):
        with open(self.config_file_path, 'wb') as configfile:
            self.config.write(configfile)