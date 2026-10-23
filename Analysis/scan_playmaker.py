import json
from pathlib import Path
import UnityPy
from managed_types import generator, fixed_nodes

ROOT=Path(__file__).resolve().parents[1]
DATA=(ROOT/'Game'/'Lakeview Cabin Collection_Data').resolve()
g=generator(DATA.parent)
scripts_env=UnityPy.load(str(DATA/'globalgamemanagers.assets'))
scripts={o.path_id:o.read_typetree() for o in scripts_env.objects if o.type.name=='MonoScript'}
nodes={}
values=[]
errors=[]
parsed=0
for path in sorted(DATA.iterdir()):
    if not (path.suffix=='.assets' or (path.name.startswith('level') and path.name[5:].isdigit())): continue
    env=UnityPy.load(str(path))
    for o in env.objects:
        if o.type.name!='MonoBehaviour' or Path(o.assets_file.name).name!=path.name: continue
        base=o.read_typetree(check_read=False)
        ref=base['m_Script']
        if not ref['m_FileID']: continue
        external=o.assets_file.externals[ref['m_FileID']-1]
        if 'globalgamemanagers.assets' not in str(external): continue
        script=scripts.get(ref['m_PathID'],{})
        classname=script.get('m_ClassName')
        if classname not in ('PlayMakerFSM','PlayMakerArrayListProxy','PlayMakerHashTableProxy'): continue
        try:
            if classname not in nodes:
                ns=script.get('m_Namespace','')
                nodes[classname]=fixed_nodes(g,script['m_AssemblyName'],ns+'.'+classname if ns else classname)
            tree=o.read_typetree(nodes=nodes[classname])
            parsed+=1
            def walk(v,trail):
                if isinstance(v,dict):
                    for k,x in v.items(): walk(x,trail+[k])
                elif isinstance(v,list):
                    for i,x in enumerate(v): walk(x,trail+[i])
                elif isinstance(v,str) and v.strip():
                    if (trail[-1]=='value' and ('fsmStringParams' in trail or 'stringVariables' in trail)) or 'preFillStringList' in trail or 'fsmPropertyParams' in trail:
                        values.append(dict(file=path.name,path_id=o.path_id,script=classname,field=trail,text=v,fsm=tree.get('fsm',{}).get('name')))
            walk(tree,[])
        except Exception as ex:
            errors.append(dict(file=path.name,path_id=o.path_id,script=classname,error=str(ex)))
    print(path.name,'parsed',parsed,flush=True)
(ROOT/'Analysis'/'playmaker_values.json').write_text(json.dumps(values,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'Analysis'/'playmaker_errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf-8')
print('parsed',parsed,'values',len(values),'unique',len(set(x['text'] for x in values)),'errors',len(errors))
