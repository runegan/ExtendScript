import os
import re
import sys
import subprocess
import json

print 'Building ExtendScript...'

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

        targetApp = ""
        file_output = ""

        for line in file_string.splitlines():
            # Check if line includes target and
            # then extract the words after the
            # #target statment to variable targetApp
            if re.match(r'.*#target', line) and targetApp == "":
                regex = r'.*#target [\"\']?([^\"\';]*)[\"\']?;?'
                targetApp = re.sub(regex, r'\1', line)

        if targetApp == "":
            targetApp = settings['default_app']

        # Check target app
        apps = ['aftereffects', 'photoshop', 'illustrator', 'indesign']

        if targetApp in apps:
            # Do script
            appleScripts_path = packages+'/ExtendScript/Applescript'
            appleScriptFile = appleScripts_path+'/run_'+targetApp+'.scpt'

            subprocess.call(
                'arch -x86_64 '
                'osascript "'+appleScriptFile+'" "'+file_path+'"',
                shell=True)

            print 'Done'

        else:
            print 'Error: #Target: "'+targetApp+'" not recognised'
            print 'Target must be one of:'
            for app in apps:
                print app
