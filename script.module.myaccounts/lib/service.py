# -*- coding: utf-8 -*-

'''
	My Accounts
'''

from myaccounts.modules import control
import xbmc


class AddonCheckUpdate:
	def run(self):
		xbmc.log('[ script.module.myaccounts ]  Addon checking available updates', xbmc.LOGNOTICE)
		try:
			import re
			import requests
			repo_xml = requests.get('https://raw.githubusercontent.com/a4k-openproject/repository.myaccounts/master/zips/addons.xml')
			if repo_xml.status_code != 200:
				xbmc.log('[ script.module.myaccounts ]  Could not connect to remote repo XML: status code = %s' % repo_xml.status_code, xbmc.LOGNOTICE)
				return
			repo_version = re.findall(r'<addon id=\"script.module.myaccounts\".*version=\"(\d*.\d*.\d*.\d*)\"', repo_xml.text)[0]
			local_version = control.addonVersion()
			if control.check_version_numbers(local_version, repo_version):
				while control.condVisibility('Library.IsScanningVideo'):
					control.sleep(10000)
				xbmc.log('[ script.module.myaccounts ]  A newer version is available. Installed Version: v%s, Repo Version: v%s' % (local_version, repo_version), xbmc.LOGNOTICE)
				control.notification(title = 'default', message = 'A new verison of My Accounts is available from the repository. Please consider updating to v%s' % repo_version, icon='default', time=5000, sound=False)
		except:
			import traceback
			traceback.print_exc()
			pass

if control.setting('checkAddonUpdates') == 'true':
	AddonCheckUpdate().run()
	xbmc.log('[ script.module.myaccounts ]  Addon update check complete', xbmc.LOGNOTICE)

xbmc.log('[ script.module.myaccounts ]  service stopped', xbmc.LOGNOTICE)