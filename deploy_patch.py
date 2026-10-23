"""Deploy or restore this project's local test payload, with strict hash guards."""
import argparse,hashlib,json,shutil,subprocess,csv,io
from pathlib import Path
ROOT=Path(__file__).resolve().parent
GAME=(ROOT/'Game').resolve()
BACKUP=ROOT/'Backups'/'original'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--restore',action='store_true')
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    listing=subprocess.run(['tasklist','/FI','IMAGENAME eq Lakeview Cabin Collection.exe','/FO','CSV','/NH'],capture_output=True,text=True).stdout
    if any(row and row[0].lower()=='lakeview cabin collection.exe' for row in csv.reader(io.StringIO(listing))):
        raise SystemExit('Game is running. Please close it yourself before deploying or restoring.')
    manifest=json.loads((ROOT/'Patch'/'manifest.json').read_text('utf-8'))
    # Validate every file before making the first change.
    for item in manifest['payload_files']:
        relative=Path(item['game_path'])
        target=GAME/relative
        if not target.resolve().is_relative_to(GAME): raise ValueError('Path escapes game directory')
        backup=BACKUP/relative
        payload=ROOT/item['path']
        if sha(payload)!=item['sha256']: raise ValueError('Payload changed: '+str(payload))
        current=sha(target) if target.exists() else None
        if current not in (item['source_sha256'],item['sha256']): raise ValueError('Unexpected current game file: '+str(target))
        if args.restore and item['source_sha256'] is not None and (not backup.exists() or sha(backup)!=item['source_sha256']): raise ValueError('Valid backup missing')
        if backup.exists() and sha(backup)!=item['source_sha256']: raise ValueError('Existing backup changed')
        if not args.restore and item['source_sha256'] is not None and not backup.exists() and current!=item['source_sha256']: raise ValueError('Cannot back up modified file')
    if args.dry_run:
        print('Validated',len(manifest['payload_files']),'files; no changes made.')
        return
    for item in manifest['payload_files']:
        relative=Path(item['game_path'])
        target=GAME/relative
        backup=BACKUP/relative
        if args.restore:
            if item['source_sha256'] is None:
                if target.exists(): target.unlink()
            else:
                shutil.copy2(backup,target)
                assert sha(target)==item['source_sha256']
        else:
            if item['source_sha256'] is not None and not backup.exists():
                backup.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(target,backup)
            shutil.copy2(ROOT/item['path'],target)
            assert sha(target)==item['sha256']
    print(('Restored' if args.restore else 'Deployed'),len(manifest['payload_files']),'files; backups:',BACKUP)
if __name__=='__main__': main()
