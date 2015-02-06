import sys
import subprocess

script, scriptFile, packages = sys.argv

subprocess.call("arch -x86_64 osascript '%s/ExtendScript/run.scpt' '%s'" %(packages, scriptFile), shell=True)
subprocess.call("echo done", shell=True);