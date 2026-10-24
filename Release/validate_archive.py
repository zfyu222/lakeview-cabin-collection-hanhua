"""Validate ZIP contents and exercise its extracted installer on original-file fixtures."""
import hashlib,json,shutil,subprocess,tempfile,zipfile
from pathlib import Path,PurePosixPath
from build_patchkit import ROOT,HERE,sha

def main():
    archive=ROOT/'Dispatch/Lakeview Cabin Collection_子非鱼汉化1.0.zip'
    kit=json.loads((HERE/'patchkit_build.json').read_text(encoding='utf-8'))
    tests=[]
    with tempfile.TemporaryDirectory(prefix='lakeview-release-') as temp:
        game=Path(temp)/'Extracted';game.mkdir()
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            expected={x['game_path'] for x in kit['files']}|{'补丁说明.txt','PATCH_MANIFEST.json','SHA256SUMS.txt'}
            assert set(z.namelist())==expected and len(z.namelist())==len(expected)
            guide=z.read('补丁说明.txt');assert guide.startswith(b'\xef\xbb\xbf')
            text=guide.decode('utf-8-sig');assert '待填入' not in text and '10分钟' in text and 'F7' in text and 'F8' in text
            manifest=json.loads(z.read('PATCH_MANIFEST.json'))
            sums={line.split('  ',1)[1]:line.split('  ',1)[0] for line in z.read('SHA256SUMS.txt').decode().splitlines()}
            assert {x['path'] for x in manifest['files']}=={x['game_path'] for x in kit['files']}==set(sums)
            for item in kit['files']:
                data=z.read(item['game_path']);actual=hashlib.sha256(data).hexdigest()
                assert actual==item['sha256']==sums[item['game_path']]
                assert actual==sha(ROOT/'Dispatch/Files'/item['game_path'])
                receipt=next(x for x in manifest['files'] if x['path']==item['game_path'])
                assert receipt['sha256']==actual and receipt['size']==len(data)
            for name in z.namelist():
                path=PurePosixPath(name);assert not path.is_absolute() and '..' not in path.parts
            z.extractall(game)
        (game/'Lakeview Cabin Collection.exe').write_bytes(b'') # Never executed.
        for item in kit['installed_outputs']:
            if item['source_sha256']:
                baseline=ROOT/'Backups/original'/item['game_path'];assert sha(baseline)==item['source_sha256']
                dest=game/item['game_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(baseline,dest)
        for action,localized in [('--install',True),('--uninstall',False),('--install',True)]:
            run=subprocess.run([str(game/'安装汉化.exe'),action,'--game-root',str(game)],capture_output=True,encoding='utf-8',errors='replace')
            assert run.returncode==0,run.stdout+run.stderr
            for item in kit['installed_outputs']:
                dest=game/item['game_path'];expected=item['sha256'] if localized else item['source_sha256']
                assert (sha(dest)==expected) if expected else not dest.exists(),item['game_path']
            tests.append({'action':action,'output_hashes_checked':18,'status':'passed'})
    result={'status':'passed','archive':archive.relative_to(ROOT).as_posix(),'sha256':sha(archive),'bytes':archive.stat().st_size,
            'payload_files':len(kit['files']),'archive_entries':len(kit['files'])+3,'utf8_bom_guide':True,'all_payload_checksums':'passed',
            'extracted_installer_tests':tests,'gameplay_test':'User: opening approximately 10 minutes, no obvious errors; no full playthrough'}
    (HERE/'archive_validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
