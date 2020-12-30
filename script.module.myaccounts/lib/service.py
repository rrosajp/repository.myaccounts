# -*- coding: utf-8 -*-

'''
	My Accounts
'''

from myaccounts.modules import control
from myaccounts.modules import log_utils
import _strptime
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


class PremAccntNotification:
	def run(self):
		from datetime import datetime
		from myaccounts.modules import alldebrid
		from myaccounts.modules import premiumize
		from myaccounts.modules import realdebrid
		xbmc.log('[ script.module.myaccounts ]  Debrid Account Expiry Notification Service Starting...', 2)
		self.duration = [(15, 10), (11, 7), (8, 4), (5, 2), (3, 0)]
		if control.setting('alldebrid.username') != '' and control.setting('alldebrid.expiry.notice') == 'true':
			account_info = alldebrid.AllDebrid().account_info()['user']
			if account_info:
				if not account_info['isSubscribed']:
					# log_utils.log('AD account_info = %s' % account_info, log_utils.LOGNOTICE)
					expires = datetime.fromtimestamp(account_info['premiumUntil'])
					days_remaining = (expires - datetime.today()).days # int
					if self.withinRangeCheck('alldebrid', days_remaining):
						control.notification(message='AllDebrid Account expires in %s days' % days_remaining, icon=control.joinPath(control.artPath(), 'alldebrid.png'))

		if control.setting('premiumize.username') != '' and control.setting('premiumize.expiry.notice') == 'true':
			account_info = premiumize.Premiumize().account_info()
			if account_info:
				# log_utils.log('PM account_info = %s' % account_info, log_utils.LOGNOTICE)
				expires = datetime.fromtimestamp(account_info['premium_until'])
				days_remaining = (expires - datetime.today()).days # int
				if self.withinRangeCheck('premiumize', days_remaining):
					control.notification(message='Premiumize.me Account expires in %s days' % days_remaining, icon=control.joinPath(control.artPath(), 'premiumize.png'))

		if control.setting('realdebrid.username') != '' and control.setting('realdebrid.expiry.notice') == 'true':
			account_info = realdebrid.RealDebrid().account_info()
			if account_info:
				import time
				# log_utils.log('RD account_info = %s' % account_info, log_utils.LOGNOTICE)
				FormatDateTime = "%Y-%m-%dT%H:%M:%S.%fZ"
				try: expires = datetime.strptime(account_info['expiration'], FormatDateTime)
				except: expires = datetime(*(time.strptime(account_info['expiration'], FormatDateTime)[0:6]))
				days_remaining = (expires - datetime.today()).days # int
				if self.withinRangeCheck('realdebrid', days_remaining):
					control.notification(message='Real-Debrid Account expires in %s days' % days_remaining, icon=control.joinPath(control.artPath(), 'realdebrid.png'))

	def withinRangeCheck(self, debrid_provider, days_remaining):
		if days_remaining < 15:
			try: current_notification_range = int(control.setting('%s.notification.range' % debrid_provider))
			except: current_notification_range = 5
			for index, day_range in enumerate(self.duration):
				if day_range[0] > days_remaining > day_range[1] and current_notification_range != index:
					control.setSetting('%s.notification.range' % debrid_provider, str(index))
					return True
			return False
		else:
			control.setSetting('%s.notification.range' % debrid_provider, '')
			return False


if control.setting('checkAddonUpdates') == 'true':
	AddonCheckUpdate().run()
	xbmc.log('[ script.module.myaccounts ]  Addon update check complete', xbmc.LOGNOTICE)

PremAccntNotification().run()

xbmc.log('[ script.module.myaccounts ]  service stopped', xbmc.LOGNOTICE)