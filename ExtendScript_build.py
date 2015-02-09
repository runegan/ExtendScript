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


file_path = currentPath+'/'+currentFileName

if not os.path.exists(file_path):
    print 'The file must be saved first to be built'

else:
    with open(file_path, 'r') as file_handleFile:
        file_string = file_handleFile.read().decode("utf-8-sig")

        targetApp = settings['default_app']

        for line in file_string.splitlines():
            if re.match(r'.*#target', line):
                regex = r'.*#target [\"\']?([^\"\']*)[\"\']?;?'
                targetApp = re.sub(regex, r'\1', line)
                break

        if targetApp == "":
            print "Error: No target app"

        else:

            appAE = ['after effects', 'after-effects', 'aftereffects', 'ae']
            appPS = ['photoshop', 'ps']
            appAI = ['illustrator', 'ai']
            appID = ['indesign', 'id']

            targetApp = targetApp.lower()

            if targetApp in appAE:
                targetApp = 'After Effects'

            elif targetApp in appPS:
                targetApp = 'Photoshop'

            elif targetApp in appAI:
                targetApp = 'Illustrator'

            elif targetApp in appID:
                targetApp = 'InDesign'

            print "Target app is: " + targetApp

            # appleScript_path = packages+'/ExtendScript/run.scpt'

            # subprocess.call('arch -x86_64 '
            #   'osascript "'+appleScript_path+'" "'+file_path+'"',
            #   shell=True)

            print 'Done'
