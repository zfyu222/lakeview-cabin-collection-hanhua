"""Build a VCDIFF installer kit, excluding complete original game resources."""
import hashlib,json,shutil,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
KIT=HERE/'Build/PatchKit'
XDELTA=ROOT.parents[1]/'Tools/xdelta3/v3.2.2/xdelta3-3.2.2-windows-x86_64/xdelta3.exe'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    payload=json.loads((ROOT/'Patch/manifest.json').read_text(encoding='utf-8'))
    folder=KIT/'ChinesePatch'
    for name in ['deltas','files','tools','Licenses']:(folder/name).mkdir(parents=True,exist_ok=True)
    decoder=folder/'tools/xdelta3.exe'
    shutil.copy2(XDELTA,decoder)
    manifest={'game_version':'Steam Build 2415026','platform':'Steam（Windows）',
              'translation_sha256':payload['translation_sha256'],'decoder_path':'ChinesePatch/tools/xdelta3.exe',
              'decoder_sha256':sha(decoder),'files':[]}
    for index,item in enumerate(payload['payload_files']):
        source=ROOT/item['path'];assert sha(source)==item['sha256']
        added=item['source_sha256'] is None
        record={k:item[k] for k in ['game_path','source_sha256','sha256']}
        record['added']=added
        if added:
            output=folder/'files'/Path(item['game_path']).name
            shutil.copy2(source,output)
        else:
            baseline=ROOT/'Backups/original'/item['game_path']
            assert sha(baseline)==item['source_sha256'],str(baseline)
            output=folder/'deltas'/('%02d.vcdiff'%index)
            subprocess.run([str(XDELTA),'-f','-e','-9','-A','-s',str(baseline),str(source),str(output)],check=True)
        record.update(patch_path=output.relative_to(KIT).as_posix(),patch_sha256=sha(output))
        manifest['files'].append(record)
        print(output.name,output.stat().st_size,flush=True)
    for license in (HERE/'Licenses').glob('*.txt'):shutil.copy2(license,folder/'Licenses'/license.name)
    (folder/'Licenses/NOTICE.txt').write_text('xdelta 3.2.2: https://github.com/jmacd/xdelta\nNoto Sans SC: https://github.com/notofonts/noto-cjk\nFont data is subsetted and carried in binary differences. Full original game resources are not distributed.\n',encoding='utf-8')
    (folder/'patch_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    subprocess.run(['C:/Windows/Microsoft.NET/Framework/v4.0.30319/csc.exe','/noconfig','/nologo','/utf8output','/target:exe',
        '/reference:System.dll','/reference:System.Core.dll','/reference:System.Web.Extensions.dll','/out:'+str(KIT/'安装汉化.exe'),str(HERE/'PatchInstaller.cs')],check=True)
    files=[{'path':p.relative_to(ROOT).as_posix(),'game_path':p.relative_to(KIT).as_posix(),'sha256':sha(p),'size':p.stat().st_size}
           for p in sorted(KIT.rglob('*')) if p.is_file()]
    report={'status':'built_pending_game_release_gate','patch_format':'VCDIFF / xdelta 3.2.2','files':files,
            'total_bytes':sum(x['size'] for x in files),'installed_outputs':payload['payload_files']}
    (HERE/'patchkit_build.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Kit files:',len(files),'bytes:',report['total_bytes'])

if __name__=='__main__':main()
