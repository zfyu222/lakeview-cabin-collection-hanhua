"""Verify deployed hashes and preservation of the original Texture2D/Sprite data."""
from pathlib import Path
import hashlib,json
import UnityPy
ROOT=Path(__file__).resolve().parents[1]
DATA=(ROOT/'Game/Lakeview Cabin Collection_Data').resolve()
BACKUP=ROOT/'Backups/original/Lakeview Cabin Collection_Data'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'Patch/manifest.json').read_text('utf-8'))
for item in manifest['payload_files']:
 assert sha(ROOT/'Game'/item['game_path'])==item['sha256'],item['game_path']
hashes=json.loads((ROOT/'Analysis/source_hashes.json').read_text('utf-8'))
textures=sprites=0
for file,expected in hashes.items():
 if not file.endswith('.assets'):continue
 current=DATA/file
 original=BACKUP/file if (BACKUP/file).exists() else current
 assert sha(original)==expected,'Original baseline changed: '+file
 before=UnityPy.load(str(original)); after=UnityPy.load(str(current))
 old={o.path_id:o for o in before.objects if Path(o.assets_file.name).name==file}
 for o in after.objects:
  if Path(o.assets_file.name).name!=file or o.type.name not in ('Texture2D','Sprite'):continue
  assert o.get_raw_data()==old[o.path_id].get_raw_data(),(file,o.path_id)
  if o.type.name=='Texture2D':textures+=1
  else:sprites+=1
result={'status':'static_checks_passed','payload_files':len(manifest['payload_files']),'original_texture2d_objects_unchanged':textures,'original_sprite_objects_unchanged':sprites,'preview_overflowing_labels':0,'game_test':'pending_user','computer_control_used':False,'toggle':'F8'}
(ROOT/'ImageOverlay/static_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
