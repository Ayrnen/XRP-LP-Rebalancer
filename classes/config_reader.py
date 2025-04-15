import configparser

class ConfigReader:
    def __init__(self):
        self.config_file = 'config.ini'
        self.config = configparser.ConfigParser()
        self._load_config()

    def _load_config(self):
        self.config.read(self.config_file)

    def get_section(self, section):
        return {key: value for key, value in self.config[section].items()}

    def get_section_keys(self, section):
        return list(self.config[section].keys())
    
    def get_value(self, section, key):
        return self.config[section][key]