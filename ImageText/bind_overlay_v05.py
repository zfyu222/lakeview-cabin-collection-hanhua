"""Bind the confirmed incremental overlay regions to this game's exact sprite rectangles."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parents[1]/'Tools/image_text'))
from core import read_json,write_json,digest
from translation_bridge import validate

def bind(dataset='v05'):
    source=ROOT/f'lakeview-cabin-collection_image_{dataset}_text.csv'
    translated=source.with_name(source.stem+'_translated.csv')
    workspace='image-text' if dataset=='v05' else 'image-final'
    validation=ROOT/f'TranslateFiles/{workspace}/TranslateFiles/reports/final_validation.json'
    validate(source,translated,validation)
    patch=ROOT/f'ImagePatch/{dataset}-overlay/IMAGE_PATCH_MANIFEST.json'
    payload=read_json(patch)
    if payload['mode']!='overlay' or payload['translation_sha256']!=digest(translated.read_bytes()):
        raise ValueError('Unexpected image overlay payload')
    catalog=read_json(ROOT/'Analysis/sprite_catalog.json')
    spec={};unbound=[];bindings=[]
    for item in payload['entries']:
        matches=[]
        for src in item['sources']:
            prov=src['provenance']
            for sp in catalog:
                if (sp['texture_file'],sp['texture_id'])!=(prov['asset_file'],prov['texture_path_id']):continue
                r=sp['rect'];left=r['x'];top=sp['texture_height']-r['y']-r['h']
                x1,y1,x2,y2=item['box']
                if x1<left or y1<top or x2>left+r['w'] or y2>top+r['h']:continue
                key=sp['texture']+'|'+sp['name']
                local=[(x1-left)/r['w'],(y1-top)/r['h'],(x2-x1)/r['w'],(y2-y1)/r['h']]
                label=dict(text=item['text'],box=local,note=False,bright=False,row=item['csv_row'],image_index=prov['legacy_index'])
                if label not in spec.setdefault(key,[]):spec[key].append(label)
                matches.append(dict(key=key,sprite_file=sp['file'],sprite_path_id=sp['path_id'],sprite_rect=r,texture_top_left=[left,top]))
        if not matches:unbound.append(item)
        bindings.append(dict(image_id=item['image_id'],csv_row=item['csv_row'],source_box=item['box'],matches=matches))
    result=dict(status='bound_subset_pending_user_test',installed=False,source_sha256=digest(source.read_bytes()),translation_sha256=digest(translated.read_bytes()),
                mapping_sha256=digest(source.with_suffix('.mapping.json').read_bytes()),payload_sha256=digest(patch.read_bytes()),
                labels=sum(map(len,spec.values())),sprite_keys=len(spec),spec=spec,bindings=bindings,unbound=unbound)
    write_json(ROOT/f'ImageText/overlay_bindings_{dataset}.json',result)
    print(dict(labels=result['labels'],keys=result['sprite_keys'],unbound=len(unbound)))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--dataset',choices=['v05','final'],default='v05')
    bind(parser.parse_args().dataset)
