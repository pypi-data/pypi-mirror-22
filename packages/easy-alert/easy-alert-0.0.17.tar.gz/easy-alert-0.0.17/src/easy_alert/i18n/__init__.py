import os
import locale


def __get_locale():
    # environment LANG is the first priority
    lang = os.environ.get('LANG')
    if lang:
        return lang.lower()
    loc = locale.getdefaultlocale()[0]
    return loc.lower() if loc else "C"


__locale = __get_locale()

if __locale.startswith('ja_'):
    from messages_ja import *
else:
    from messages_en import *
