import yaml
import os
import subprocess, shlex
from subprocess import PIPE, STDOUT

with open(os.path.join(__file__, "../data_center_cameras.yaml"), 'r') as f:
    data = yaml.load(f)

NAMESPACE=data.pop('namespace')
shellFile = "create-secrets.sh"

def getCmd(keyName, user, password):
    return "{} {} {} {} {}".format(shellFile, keyName, user, password, NAMESPACE)    

for secretKeyName, secretValues in data.items():
    USERNAME=secretValues['user']
    PASSWORD=secretValues['pass']
    CMD = getCmd(secretKeyName, USERNAME, PASSWORD)
    try:
        subprocess.check_call(shlex.split(CMD), stderr=STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print(e)