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

        def makeReplacements(line):
            output = line

            if settings['compile_includes']:
                if re.match(r'.*#include', line):
                    output = replaceIncludes(line)

            if settings['set_debug_false']:
                if re.match(r'.*debug = .*', line):
                    output = replaceDebug(line)

            return output

        def replaceIncludes(line):
            path = re.sub(r'.*#include \"(.*)\";?', r'\1', line)
            path = currentPath + "/" + path
            with open(os.path.abspath(path)) as f:
                fileContent = f.read()

            return fileContent

        def replaceDebug(line):
            return re.sub(r'debug = true', r'debug = false', line)

        targetApp = ""
        file_output = ""

        for line in file_string.splitlines():
            # Check if line includes target and
            # then extract the words after the
            # #target statment to variable targetApp
            if re.match(r'.*#target', line) and targetApp == "":
                regex = r'.*#target [\"\']?([^\"\';]*)[\"\']?;?'
                targetApp = re.sub(regex, r'\1', line)

            file_output = file_output + makeReplacements(line) + '\n'

        if targetApp == "":
            targetApp = settings['default_app']

        # Find target app if written in other ways
        appAE = ['after effects', 'after-effects', 'aftereffects', 'ae']
        appPS = ['photoshop', 'ps']
        appAI = ['illustrator', 'ai']
        appID = ['indesign', 'id']

        targetApp = targetApp.lower()

        if targetApp in appAE:
            targetApp = 'AE'

        elif targetApp in appPS:
            targetApp = 'PS'

        elif targetApp in appAI:
            targetApp = 'AI'

        elif targetApp in appID:
            targetApp = 'ID'

        # Do script
        appleScripts_path = packages+'/ExtendScript/Applescript'
        appleScriptFile = appleScripts_path+'/Run'+targetApp+'.scpt'

        subprocess.call(
            'arch -x86_64 '
            'osascript "'+appleScriptFile+'" "'+file_path+'"',
            shell=True)

        print 'Done'
