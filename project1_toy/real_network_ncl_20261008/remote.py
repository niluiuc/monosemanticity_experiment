"""Run commands and transfer bytes through the user's existing SSH proxy."""
import argparse, shlex, subprocess
from pathlib import Path
BASH = 'C:/Program Files/Git/bin/bash.exe'
def remote(command, data=None):
    result=subprocess.run([BASH,'-lc','ssh -o BatchMode=yes -O proxy ncsa '+shlex.quote(command)],
                          input=data, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace')+'\n'+result.stdout.decode(errors='replace'))
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--command'); p.add_argument('--command-file'); p.add_argument('--stdin-file'); p.add_argument('--output-file'); a=p.parse_args()
    command=Path(a.command_file).read_text() if a.command_file else a.command
    r=remote(command,Path(a.stdin_file).read_bytes() if a.stdin_file else None)
    if a.output_file: Path(a.output_file).write_bytes(r.stdout)
    else: print(r.stdout.decode(errors='replace'),end='')
    if r.stderr: print(r.stderr.decode(errors='replace'),end='')
