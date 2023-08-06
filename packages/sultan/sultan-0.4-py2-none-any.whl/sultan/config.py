import copy
import os
from .core import Base

DEFAULT_SETTINGS = {
    "HALT_ON_ERROR": True,
    "LOG_FORMAT": '%(log_color)s[%(name)s]: %(message)s',
    "LOG_COLORS": {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
}

class Settings(Base):


    def __getattribute__(self, attr):

        sultan_settings_module_env = 'SULTAN_SETTINGS_MODULE'
        settings = copy.deepcopy(DEFAULT_SETTINGS)
        if sultan_settings_module_env in os.environ:

            settings = __import__(os.environ[sultan_settings_module_env])
            for k, v in settings.items():
                settings[k] = v

        if attr in settings:
            return settings[attr]
        else:
            ValueError("Invalid Setting '%s'." % (attr))

settings = Settings()