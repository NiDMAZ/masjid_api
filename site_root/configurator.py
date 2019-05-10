import yaml
import json


class PropertyDict(dict):
    """
    A custom dictionary object that overloads the getattr, setattr, delattr
    to allow you to access the 1st level keys as properties
    """

    def __getattr__(self, name, default=None):
        if name in self:
            return self[name]
        else:
            return default

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: " + name)


class ConfigParser(PropertyDict):
    def __init__(self, file_name):
        super(ConfigParser, self).__init__()
        self._file_name = file_name
        self._config = None
        self._load_config()
        self._update_dict()

    def _update_dict(self):
        for key in self._config:
            self.update({key: self._config[key]})

    def _load_config(self):
        raise NotImplementedError("{}".format(self.__class__.__name__))

    @property
    def _parsed_config(self):
        return self._config


class JsonConfigParser(ConfigParser):
    def __init__(self, file_name):
        super(JsonConfigParser, self).__init__(file_name)

    def _load_config(self):
        with open(self._file_name, 'r') as f:
            self._config = json.load(f)


class YAMLConfigParser(ConfigParser):
    def __init__(self, file_name):
        super(YAMLConfigParser, self).__init__(file_name)

    def _load_config(self):
        with open(self._file_name, "r") as f:
            self._config = yaml.load(f, Loader=yaml.FullLoader)
