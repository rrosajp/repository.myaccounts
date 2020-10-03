# -*- coding: utf-8 -*-

"""
	My Accounts
"""

import os.path
import xbmc
import xbmcaddon
import xbmcgui


def get(file):
	addonInfo = xbmcaddon.Addon().getAddonInfo
	addonPath = xbmc.translatePath(addonInfo('path'))
	helpFile = os.path.join(addonPath, 'lib', 'myaccounts', 'help', file + '.txt')
	r = open(helpFile)
	text = r.read()
	r.close()
	xbmcgui.Dialog().textviewer('[COLOR red]My Accounts[/COLOR] -  v%s - %s' % (xbmcaddon.Addon().getAddonInfo('version'), file), text)