"""Recheck formal image exports and installed payload; never mark gameplay verified."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parents[1]/'Tools/image_text'))
from core import read_json,write_json,digest
from translation_bridge import validate

datasets=[]
for name,workspace in [('v05','image-text'),('final','image-final'),('corrections','image-corrections')]:
    source=ROOT/f'lakeview-cabin-collection_image_{name}_text.csv'
    translated=source.with_name(source.stem+'_translated.csv')
    original,target,report=validate(source,translated,ROOT/f'TranslateFiles/{workspace}/TranslateFiles/reports/final_validation.json')
    binding=read_json(ROOT/f'ImageText/overlay_bindings_{name}.json')
    datasets.append(dict(name=name,records=len(original),source_sha256=digest(source.read_bytes()),translation_sha256=digest(translated.read_bytes()),
                         bound_regions=binding['labels'],unbound=binding['unbound'],semantic_review=report['semantic_review']))
manifest=read_json(ROOT/'ImageOverlay/manifest.json');payload=read_json(ROOT/'Patch/manifest.json')
for item in payload['payload_files']:
    assert digest((ROOT/item['path']).read_bytes())==item['sha256']
    assert digest((ROOT/'Game'/item['game_path']).read_bytes())==item['sha256']
static=read_json(ROOT/'ImageOverlay/static_validation.json')
assert static['status']=='static_checks_passed'
assert static['payload_sha256']=={x['game_path']:x['sha256'] for x in payload['payload_files']}
spec=read_json(ROOT/'ImageOverlay/overlay_map.json');labels=sum(map(len,spec.values()))
assert labels==manifest['labels']
assert not read_json(ROOT/'ImageOverlay/audit_preview_validation.json')['overflow']
assert read_json(ROOT/'ImageOverlay/audit_preview_validation.json')['labels']==labels
for bad in ['ForSaleSign|ForSaleSign_0','RandomScares|RandomScares_2','RandomScares|RandomScares_4']:
    assert bad not in spec, 'Non-text sprite still incorrectly overlaid'
assert spec['SignsNEW|SignsNEW_4'][0]['text']=='出口' and spec['Signs|Signs_11'][0]['text']=='出口'
result=dict(status='installed_pending_user_verification',date='2026-10-24',image_datasets=datasets,overlay_labels=labels,sprite_keys=len(spec),
            payload_files=len(payload['payload_files']),original_texture2d_objects_unchanged=static['original_texture2d_objects_unchanged'],
            original_sprite_objects_unchanged=static['original_sprite_objects_unchanged'],mapping_corrections=manifest['mapping_corrections'],
            retained=['署名、品牌、数字、按键和解谜字母','故障残字和无法可靠辨认的雪花帧','没有对应精灵切片的图集区域；来源和已审译文保留，不能冒称已安装'],
            unresolved_scope=['No full game playthrough or hidden-state verification by the user yet','Atlas labels with no reliable display binding, including old MEDBAY/COMBO and source regions listed as unbound','Screen/camera alignment and small world-label readability require user tests, especially below 1920px'],
            computer_control_used=False,game_test='pending_user',fully_localized_verified=False,guide='ImageOverlay/TESTING.md')
write_json(ROOT/'ImageText/coverage_final.json',result)
print(dict(status=result['status'],labels=labels,sprite_keys=len(spec),image_records=sum(x['records'] for x in datasets),fully_verified=False))
