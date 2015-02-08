import os
import sys
import subprocess
import json
from pprint import pprint

script, file_handle, packages = sys.argv

buildFolder = packages+'/ExtendScript'


# Get default settings
with open(buildFolder+'/ExtendScript.sublime-settings') as settingsFile:
	settings = json.load(settingsFile)

user_settings = ""
user_settingsFile = packages+'/User/ExtendScript.sublime-settings'

# Check if user settings file exists and is not empty
if os.path.exists(user_settingsFile):
	if os.stat(user_settingsFile).st_size != 0:
		with open(user_settingsFile) as settingsFile:
			user_settings = json.load(settingsFile)

		# Overwrite default settings with the user settings
		for setting in settings:
			if setting in user_settings:
				settings[setting] = user_settings[setting]


if not os.path.exists(file_handle):
	print 'The file must be saved first to be built'

else:
	with open(file_handle, 'r') as file_handle:
		file_string = file_handle.read().decode("utf-8-sig")
		file_handle.close()

		file_output = ""


		appleScriptFile = packages+'/ExtendScript/run.scpt'

		subprocess.call('arch -x86_64 '
			'osascript "'+appleScriptFile+'" "'+file_handle+'"',
			shell=True)


		print 'done'