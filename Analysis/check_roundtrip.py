import json,collections,hashlib
from pathlib import Path
import UnityPy
from managed_types import generator,fixed_nodes
ROOT=Path(__file__).resolve().parents[1]
DATA=(ROOT/'Game'/'Lakeview Cabin Collection_Data').resolve()
mapping=json.loads((ROOT/'Analysis'/'source_mapping.json').read_text('utf-8'))
g=generator(DATA.parent)
nodes={}
files=collections.defaultdict(set)
for r in mapping: files[r['file']].add(r['path_id'])
result=[]
for file,ids in files.items():
    env=UnityPy.load(str(DATA/file))
    for o in env.objects:
        if Path(o.assets_file.name).name!=file or o.path_id not in ids: continue
        original=o.get_raw_data()
        n=None
        if o.type.name=='MonoBehaviour':
            classname=next(r['script'] for r in mapping if r['file']==file and r['path_id']==o.path_id)
            if classname not in nodes: nodes[classname]=fixed_nodes(g,'PlayMaker.dll' if classname=='PlayMakerFSM' else 'Assembly-CSharp.dll',classname)
            n=nodes[classname]
        tree=o.read_typetree(nodes=n)
        o.save_typetree(tree,nodes=n)
        rebuilt=o.get_raw_data()
        result.append(dict(file=file,path_id=o.path_id,bytes=len(original),roundtrip_identical=original==rebuilt))
(ROOT/'Analysis'/'roundtrip_report.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('checked',len(result),'identical',sum(r['roundtrip_identical'] for r in result))
assert all(r['roundtrip_identical'] for r in result)
