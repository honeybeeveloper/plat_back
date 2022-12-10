import logging
import json
import os

from config import CustomObject


class Config(CustomObject):
    LOGGING_LEVEL_MAP = {
        'error': logging.ERROR,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG,
    }

    def __init__(self, config_file):
        super(Config, self).__init__()
        if 'OZZ_HOME' not in os.environ:
            raise RuntimeError('OZZ_HOME not set')
        if 'OZZ_ENV' not in os.environ:
            raise RuntimeError('OZZ_ENV not set')
        self.home = os.environ['OZZ_HOME']
        self.env = os.environ['OZZ_ENV']
        self.config_file = f'{self.home}/{config_file}'
        self.__load_config()

    def __load_config(self):
        with open(self.config_file, encoding='utf-8') as config_file:
            loaded_config = json.load(config_file)
        default_config = loaded_config['production']

        # apply testing config
        self.is_testing = not self.env.startswith('prod')
        if self.is_testing and 'testing' in loaded_config:
            self.__copy_config(default_config, loaded_config['testing'], overwrite=True)

        default_config['logging']['level'] = self.LOGGING_LEVEL_MAP[default_config['logging']['level']]
        default_config['logging']['path'] = f"{self.home}/{default_config['logging']['dir']}"
        self.__set_attrs(self, default_config)

    def __copy_config(self, dest_config, src_config, overwrite=False):
        for key, value in src_config.items():
            if not overwrite:
                continue
            if type(value) == dict:
                if key not in dest_config:
                    dest_config[key] = {}
                self.__copy_config(dest_config[key], value, overwrite)
            else:
                dest_config[key] = value

    def __set_attrs(self, dest_cls, src_cls):
        for key, value in src_cls.items():
            if type(value) == dict:
                attr_cls = CustomObject()
                self.__set_attrs(attr_cls, src_cls[key])
                setattr(dest_cls, key, attr_cls)
            else:
                setattr(dest_cls, key, value)
