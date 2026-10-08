"""Watch the submitted jobs; no submission, authentication or scientific changes."""
import datetime
import time
from pathlib import Path
from remote import remote

root='/scratch/idas3/ncl_native_20261008_v1'
log=Path(__file__).with_name('watch_log.txt')
for step in range(480):
    command=("squeue -h -j 11212169,11211781 -o '%i %T %R'; "
             f"du -h {root}/data 2>/dev/null; "
             f"if test -f {root}/logs/clean-11212169.out; then tail -c 200 {root}/logs/clean-11212169.out | tr '\\r' '\\n' | tail -4; fi; "
             f"if test -f {root}/logs/conditional-11211781.out; then tail -4 {root}/logs/conditional-11211781.out; fi")
    try:
        result=remote(command).stdout.decode(errors='replace')
    except Exception as error:
        print(f'WATCH STOPPED: {error}',flush=True)
        raise SystemExit(1)
    entry=datetime.datetime.now(datetime.timezone.utc).isoformat()+'\n'+result
    with log.open('a',encoding='utf-8') as file: file.write(entry+'\n')
    print(entry,flush=True)
    if 'PENDING' not in result and 'RUNNING' not in result and 'COMPLETING' not in result:
        print('Jobs left queue; inspect accounting and saved outputs.',flush=True)
        break
    time.sleep(30)
