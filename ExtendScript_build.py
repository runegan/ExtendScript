import os
import re
import sys
import subprocess
import json

script, currentPath, currentFileName, packages = sys.argv

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


file_path = currentPath+'/'+currentFileName


if not os.path.exists(file_path):
	print 'The file must be saved first to be built'

else:	
	with open(file_path, 'r') as file_handleFile:
		file_string = file_handleFile.read().decode("utf-8-sig")
		file_handleFile.close()

		
		file_output = ""

		for line in file_string.splitlines():
			if re.match(r'.*#target', line):
				targetApp = re.sub(r'.*#target \"(.*)\";?', r'\1', line)
				print "Target app is: " + targetApp
				break

		# appleScript_path = packages+'/ExtendScript/run.scpt'

		# subprocess.call('arch -x86_64 '
		# 	'osascript "'+appleScript_path+'" "'+file_path+'"',
		# 	shell=True)


		print 'Done'