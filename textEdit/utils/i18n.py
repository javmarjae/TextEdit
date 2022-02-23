from os.path import normpath, expanduser, join

import yaml
from PyQt5.QtCore import QSettings

CACHED_TRANS = None
CONFIG_FOLDER = normpath(expanduser('textEdit/resources/config/'))


def get_trans_dict(lang: str) -> dict:
    global CACHED_TRANS
    if CACHED_TRANS is None:
        try:
            with open(join(CONFIG_FOLDER, "i18n", lang) + ".yaml") as file:
                CACHED_TRANS = yaml.load(file, Loader=yaml.FullLoader)
        except (Exception,):
            CACHED_TRANS = {}

    return CACHED_TRANS


def trans(key: str) -> str:
    settings = QSettings("TextEdit", "SettingsDesktop")
    language = 'es'  
    settings.value("language", "es_ES")
    return get_trans_dict(language).get(key, key)