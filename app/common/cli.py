import sys
import subprocess
from pprint import pprint


def exec_cmd(cmd, is_output_cmd=False, msg='', is_shell_option=False, is_debug=False):
    if type(cmd) is str:
        cmd = cmd.split(' ')

    if is_output_cmd:
        print(' '.join(cmd))

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=is_shell_option)

    if is_debug:
        pprint(res)

    stdout = res.stdout.decode('utf8').strip() if res.stdout else ''
    stderr = res.stderr.decode('utf8').strip() if res.stderr else ''

    if stderr:
        print(stderr)
    elif msg:
        print(msg)

    return (stdout, stderr)

