
import os
import ConfigParser

# config management (stores persistent data)

class FSAConfig:
    def __init__(self, app_name):
        self.app_name = app_name
        self.section = 'evernote'
        self.config = ConfigParser.SafeConfigParser()
        self.config_file_path = app_name + '.ini'

    def exists(self):
        return os.path.exists(self.config_file_path)

    def set_guid(self, guid):
        if not self.config.has_section(self.section):
            self.config.add_section(self.section)
        self.config.set(self.section, 'appname', self.app_name)
        self.config.set(self.section, 'guid', guid)
        self.write()

    def get_guid(self):
        guid = None
        if self.exists():
            self.config.read(self.config_file_path)
            if self.config.has_section(self.section):
                guid = self.config.get(self.section, 'guid')
        return guid

    def write(self):
        with open(self.config_file_path, 'wb') as configfile:
            self.config.write(configfile)