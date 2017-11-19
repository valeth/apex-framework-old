import os
from itertools import zip_longest
import yaml


class ConfigurationError(Exception):
    pass


class InvalidConfiguration(ConfigurationError):
    pass


class MissingConfiguration(ConfigurationError):
    def __init__(self, file):
        message = f"Missing configuration file: {file}"
        super().__init__(message)


class Config(object):
    def __init__(self, config, *, defaults={}):
        if not isinstance(config, dict):
            raise InvalidConfiguration

        self._defaults = dict(defaults)
        self._config = dict(defaults)
        self._config.update(config)
        self._config_store = {}

        self.__populate()

    def __getattribute__(self, name):
        try:
            return super(Config, self).__getattribute__(name)
        except AttributeError:
            return self.__set(name, None)

    def __repr__(self):
        return str(self._config_store)

    def __populate(self):
        for key, value in self._config.items():
            if isinstance(value, dict):
                self.__populate_dict(key, value)
            elif isinstance(value, list):
                self.__populate_list(key, value)
            else:
                self.__set(key, value)

    def __populate_dict(self, key, dic):
        default = self._defaults.get(key, {})
        self.__set(key, Config(dic, defaults=default))

    def __populate_list(self, key, lst):
        items = zip_longest(lst, self._defaults.get(key, []), fillvalue=None)
        tmp = []
        for elem, default in items:
            if isinstance(elem, dict):
                tmp.append(Config(elem, defaults=(default or {})))
            else:
                tmp.append(elem)
        self.__set(key, tmp)

    def __set(self, key, value):
        self._config_store[key] = value
        return self.__setattr__(key, value)

    @classmethod
    def new(cls, config, *, defaults={}):
        if isinstance(config, list):
            return [cls(conf, defaults=defaults) for conf in config]

        return cls(config, defaults=defaults)

    @classmethod
    def from_file(cls, filename, *, defaults={}, required=True):
        if os.path.exists(filename):
            with open(filename, encoding='utf-8') as config_file:
                config = yaml.safe_load(config_file)
                return cls.new(config, defaults=defaults)
        elif required:
            cls.log.error(f"Missing configuration file: {filename}")
            raise MissingConfiguration(filename)

        return cls.new(defaults)
