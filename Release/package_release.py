"""Package the exact installer kit after the recorded release gate passes."""
import argparse,json,subprocess,sys
from pathlib import Path
from build_patchkit import ROOT,HERE,sha

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--dry-run',action='store_true');args=parser.parse_args()
    kit=json.loads((HERE/'patchkit_build.json').read_text(encoding='utf-8'))
    verified=json.loads((HERE/'installer_validation.json').read_text(encoding='utf-8'))
    assert verified['status']=='passed' and verified['kit_files']==kit['files']
    assert verified['installed_outputs']==kit['installed_outputs']
    for item in kit['files']:assert sha(ROOT/item['path'])==item['sha256']
    metadata=json.loads((HERE/'release_metadata.json').read_text(encoding='utf-8'))
    command=[sys.executable,str(ROOT.parents[1]/'.agents/skills/game-release-patch/scripts/create_release_patch.py'),'--project',str(ROOT)]
    for key,value in metadata.items():command+=['--'+key.replace('_','-'),value]
    for item in kit['files']:command+=['--include',str(ROOT/item['path'])+'='+item['game_path']]
    if args.dry_run:command+=['--dry-run']
    subprocess.run(command,check=True)

if __name__=='__main__':main()
