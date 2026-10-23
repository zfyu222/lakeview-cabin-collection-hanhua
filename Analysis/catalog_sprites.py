from pathlib import Path
import UnityPy,json
ROOT=Path(__file__).resolve().parents[1]
rows=[]
for file in (ROOT/'Game/Lakeview Cabin Collection_Data').glob('*.assets'):
 env=UnityPy.load(str(file))
 for o in env.objects:
  if o.type.name!='Sprite' or Path(o.assets_file.name).name!=file.name:continue
  s=o.read();r=s.m_Rect
  tex=s.m_RD.texture.deref()
  t=tex.read()
  rows.append({'file':file.name,'path_id':o.path_id,'name':s.m_Name,'texture':t.m_Name,'texture_file':Path(tex.assets_file.name).name,'texture_id':tex.path_id,'texture_width':t.m_Width,'texture_height':t.m_Height,'rect':{'x':r.x,'y':r.y,'w':r.width,'h':r.height}})
(ROOT/'Analysis/sprite_catalog.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('sprite catalog',len(rows))
