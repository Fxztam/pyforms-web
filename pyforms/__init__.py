#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = 'GNU GPLv3'
__version__     = '4.0'
__maintainer__  = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__       = ["ricardojvr@gmail.com", "cajomferro@gmail.com"]
__status__      = "Production"


from confapp import conf

conf += 'pyforms.settings'


# add local settings
try:
    import local_settings
    conf += local_settings
except:
    pass


if conf.PYFORMS_MODE == 'GUI':

    from pyforms.gui.appmanager import start_app

elif conf.PYFORMS_MODE == 'TERMINAL':

    from pyforms_terminal.appmanager import start_app