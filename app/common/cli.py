import sys
import subprocess


def exec_cmd(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = res.stdout.decode('utf8').strip() if res.stdout else ''
    stderr = res.stderr.decode('utf8').strip() if res.stderr else ''
    return (stdout, stderr)

