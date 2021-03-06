# -*- coding: utf-8 -*-
"""
	My Accounts
"""

import os.path
import xbmc
import xbmcaddon
import xbmcgui


def get():
	addonInfo = xbmcaddon.Addon().getAddonInfo
	addonPath = xbmc.translatePath(addonInfo('path'))
	helpFile = os.path.join(addonPath, 'changelog.txt')
	r = open(helpFile)
	text = r.read()
	r.close()
	xbmcgui.Dialog().textviewer('[COLOR red]My Accounts[/COLOR] -  v%s - ChangeLog' % (xbmcaddon.Addon().getAddonInfo('version')), text)