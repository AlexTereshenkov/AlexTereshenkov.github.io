import subprocess


def call_cmd(cmd: str):
    res = subprocess.run(cmd)
    return res.check_returncode()
