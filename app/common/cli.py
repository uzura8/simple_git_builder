import sys
import subprocess


def exec_cmd(cmd, is_output_cmd=False, msg=''):
    if type(cmd) is str:
        cmd = cmd.split(' ')

    if is_output_cmd:
        print(' '.join(cmd))

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = res.stdout.decode('utf8').strip() if res.stdout else ''
    stderr = res.stderr.decode('utf8').strip() if res.stderr else ''

    if stderr:
        print(stderr)
    elif msg:
        print(msg)

    return (stdout, stderr)

