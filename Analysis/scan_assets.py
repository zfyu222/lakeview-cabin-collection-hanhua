"""Read-only Unity inventory and display-text extraction; never modifies Game/."""
import collections
import csv
import hashlib
import json
import re
from pathlib import Path
import UnityPy

ROOT = Path(__file__).resolve().parents[1]
DATA = (ROOT / 'Game' / 'Lakeview Cabin Collection_Data').resolve()
OUT = ROOT / 'Analysis'
records, candidates, fonts, textures, errors, inventory, hashes = [], [], [], [], [], {}, {}
for path in sorted(DATA.iterdir()):
    if not (path.suffix == '.assets' or re.fullmatch(r'level\d+', path.name)):
        continue
    hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    env = UnityPy.load(str(path))
    own = [o for o in env.objects if Path(o.assets_file.name).name == path.name]
    inventory[path.name] = dict(collections.Counter(o.type.name for o in own))
    for obj in own:
        kind = obj.type.name
        base = dict(file=path.name, path_id=obj.path_id, type=kind)
        if kind in ('TextMesh', 'GUIText', 'TextAsset', 'Font', 'Texture2D'):
            try:
                tree = obj.read_typetree()
                name = tree.get('m_Name', '')
                if kind in ('TextMesh', 'GUIText') and tree.get('m_Text', '').strip():
                    records.append(dict(base, field='m_Text', text=tree['m_Text'], font=tree.get('m_Font')))
                elif kind == 'TextAsset':
                    candidates.append(dict(base, name=name, text=tree.get('m_Script', ''), classification='text_asset_unreviewed'))
                elif kind == 'Font':
                    fonts.append(dict(base, name=name, font_names=tree.get('m_FontNames'), size=len(tree.get('m_FontData', [])), character_count=len(tree.get('m_CharacterRects', []))))
                elif kind == 'Texture2D':
                    textures.append(dict(base, name=name, width=tree.get('m_Width'), height=tree.get('m_Height')))
            except Exception as ex:
                errors.append(dict(base, error=str(ex)))
        elif kind == 'MonoBehaviour':
            raw = obj.get_raw_data()
            # Candidates only: mixed PlayMaker strings include internal keys. Never export these blindly.
            for match in re.finditer(rb'[\x20-\x7e]{4,}', raw):
                value = match.group().decode('ascii')
                if ' ' in value and re.search('[A-Za-z]{3}', value):
                    candidates.append(dict(base, object_relative_offset=match.start(), text=value, classification='monobehaviour_unreviewed'))
    print(path.name, len(own), 'display', len(records), flush=True)

for name, value in [('display_text', records), ('candidates', candidates), ('fonts', fonts), ('textures', textures), ('errors', errors), ('inventory', inventory), ('source_hashes', hashes)]:
    (OUT / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
unique = list(dict.fromkeys(r['text'] for r in records))
with (ROOT / 'lakeview-cabin-collection_text.csv').open('w', encoding='utf-8-sig', newline='') as f:
    csv.writer(f).writerows([text] for text in unique)
mapping = [dict(r, csv_row=unique.index(r['text']) + 1) for r in records]
(OUT / 'source_mapping.json').write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(dict(unique_display_texts=len(unique), display_occurrences=len(records), unreviewed_candidates=len(candidates), fonts=len(fonts), textures=len(textures), errors=len(errors))))
