"""Test player installer against a disposable original-file fixture, never start the game."""
import json,shutil,subprocess,tempfile
from pathlib import Path
from build_patchkit import ROOT,HERE,KIT,sha

def main():
    build=json.loads((HERE/'patchkit_build.json').read_text(encoding='utf-8'))
    outputs=build['installed_outputs'];tests=[]
    with tempfile.TemporaryDirectory(prefix='lakeview-installer-') as temp:
        root=Path(temp)
        # A filename marker satisfies directory validation; this empty file is never executed.
        (root/'Lakeview Cabin Collection.exe').write_bytes(b'')
        for item in outputs:
            if item['source_sha256']:
                original=ROOT/'Backups/original'/item['game_path']
                assert sha(original)==item['source_sha256']
                dest=root/item['game_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,dest)
        for item in build['files']:
            source=ROOT/item['path'];assert sha(source)==item['sha256']
            dest=root/item['game_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        for action,localized in [('--install',True),('--install',True),('--uninstall',False),('--install',True)]:
            run=subprocess.run([str(root/'安装汉化.exe'),action,'--game-root',str(root)],capture_output=True,encoding='utf-8',errors='replace')
            assert run.returncode==0,run.stdout+run.stderr
            for item in outputs:
                dest=root/item['game_path'];expected=item['sha256'] if localized else item['source_sha256']
                assert (sha(dest)==expected) if expected else not dest.exists(),item['game_path']
            tests.append({'action':action,'verified_outputs':len(outputs),'status':'passed'})
        # Reject unrelated modifications before changing any file.
        first=root/outputs[0]['game_path'];first.write_bytes(first.read_bytes()+b'UNSUPPORTED')
        before={x['game_path']:sha(root/x['game_path']) for x in outputs}
        run=subprocess.run([str(root/'安装汉化.exe'),'--install','--game-root',str(root)],capture_output=True,encoding='utf-8',errors='replace')
        assert run.returncode!=0
        assert all(sha(root/key)==value for key,value in before.items())
        tests.append({'action':'reject_unknown_modified_game','status':'passed','no_installed_file_changed':True})
    result={'status':'passed','scope':'Disposable original-file fixture; installer only, no gameplay or UI automation',
            'kit_files':build['files'],'installed_outputs':outputs,'tests':tests}
    (HERE/'installer_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'passed','tests':tests},ensure_ascii=False))

if __name__=='__main__':main()
