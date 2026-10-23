"""Build a local test payload from the workflow's approved CSV; no deployment."""
import collections,csv,hashlib,json,sys
from io import BytesIO
from pathlib import Path
import UnityPy
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools import subset
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'Analysis'))
from managed_types import generator,fixed_nodes
DATA=(ROOT/'Game'/'Lakeview Cabin Collection_Data').resolve()
OUT=ROOT/'Patch'/'Lakeview Cabin Collection_Data'

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def build():
    src=ROOT/'lakeview-cabin-collection_text.csv'
    dst=ROOT/'lakeview-cabin-collection_text_translated.csv'
    report=ROOT/'TranslateFiles'/'reports'/'final_validation.json'
    # Do not generate an apparent translation if the official export does not exist.
    if not dst.exists(): raise SystemExit('Approved workflow CSV missing; finish API translation and export first.')
    validation=json.loads(report.read_text('utf-8-sig'))
    if validation.get('status')!='passed' or validation.get('translation_sha256')!=digest(dst) or validation.get('source_sha256')!=digest(src):
        raise ValueError('Current source/translation is not covered by the workflow final validation')
    with src.open(encoding='utf-8-sig',newline='') as f: original=[r[0] for r in csv.reader(f)]
    with dst.open(encoding='utf-8-sig',newline='') as f: translated=[r[0] for r in csv.reader(f)]
    if len(original)!=len(translated): raise ValueError('CSV record count mismatch')
    mapping=json.loads((ROOT/'Analysis'/'source_mapping.json').read_text('utf-8'))
    hashes=json.loads((ROOT/'Analysis'/'source_hashes.json').read_text('utf-8'))
    fonts=json.loads((ROOT/'Analysis'/'fonts.json').read_text('utf-8'))
    grouped=collections.defaultdict(list)
    for r in mapping: grouped[r['file']].append(r)
    for r in fonts: grouped[r['file']]
    # Instantiate a static TrueType font for Unity 5's old FreeType implementation.
    font=TTFont(ROOT.parents[1]/'Tools'/'Fonts'/'NotoSC'/'NotoSansSC-variable.ttf')
    font=instantiateVariableFont(font,{'wght':400},inplace=True)
    sub=subset.Subsetter()
    sub.populate(unicodes=set(range(32,127))|{ord(c) for s in original+translated for c in s})
    sub.subset(font)
    buffer=BytesIO()
    font.save(buffer)
    fontdata=buffer.getvalue()
    g=generator(DATA.parent)
    nodes={}
    payload=[]
    OUT.mkdir(parents=True,exist_ok=True)
    for file,entries in grouped.items():
        if digest(DATA/file)!=hashes[file]: raise ValueError('Unsupported/modified source: '+file)
        env=UnityPy.load(str(DATA/file))
        objs={o.path_id:o for o in env.objects if Path(o.assets_file.name).name==file}
        objects=collections.defaultdict(list)
        for r in entries: objects[r['path_id']].append(r)
        for path_id,rows in objects.items():
            obj=objs[path_id]
            node=None
            if obj.type.name=='MonoBehaviour':
                classname=rows[0]['script']
                if classname not in nodes:
                    nodes[classname]=fixed_nodes(g,'PlayMaker.dll' if classname=='PlayMakerFSM' else 'Assembly-CSharp.dll',classname)
                node=nodes[classname]
            tree=obj.read_typetree(nodes=node)
            for r in rows:
                trail=r['field'] if isinstance(r['field'],list) else [r['field']]
                parent=tree
                for key in trail[:-1]: parent=parent[key]
                if parent[trail[-1]]!=r['text']: raise ValueError('Original field mismatch')
                parent[trail[-1]]=translated[r['csv_row']-1]
            obj.save_typetree(tree,nodes=node)
        for r in fonts:
            if r['file']!=file: continue
            obj=objs[r['path_id']]
            tree=obj.read_typetree()
            tree['m_FontData']=list(fontdata)
            tree['m_FontNames']=['Noto Sans SC']
            obj.save_typetree(tree)
        target=OUT/file
        target.write_bytes(env.file.save())
        check=UnityPy.load(str(target))
        verified={o.path_id:o for o in check.objects if Path(o.assets_file.name).name==file}
        for path_id,rows in objects.items():
            obj=verified[path_id]
            node=nodes[rows[0]['script']] if obj.type.name=='MonoBehaviour' else None
            tree=obj.read_typetree(nodes=node)
            for r in rows:
                v=tree
                for key in r['field'] if isinstance(r['field'],list) else [r['field']]: v=v[key]
                if v!=translated[r['csv_row']-1]: raise ValueError('Output verification failed')
        payload.append(dict(path=str(target.relative_to(ROOT)),game_path='Lakeview Cabin Collection_Data/'+file,source_sha256=hashes[file],sha256=digest(target),fields=len(entries)))
    (ROOT/'Patch'/'manifest.json').write_text(json.dumps({'status':'local_test_pending','translation_sha256':digest(dst),'csv_records':len(translated),'mapped_fields':len(mapping),'font':'Noto Sans SC static 400, subset','payload_files':payload},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'files':len(payload),'fields':len(mapping),'status':'built; game testing pending'}))

if __name__=='__main__': build()
