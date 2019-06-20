from PyQt5.QtCore import QSettings


# SETTINGS_NAME = 'asoconta'
# SETTINGS_NAME = 'asoconta_localhost'
SETTINGS_NAME = 'sqlite'


def get_settings():
    global settings
    settings = QSettings(SETTINGS_NAME, SETTINGS_NAME)
    return settings


def save_settings():
    global settings
    # this forces system to store settings in local storage
    del settings
    return get_settings()


settings = get_settings()

