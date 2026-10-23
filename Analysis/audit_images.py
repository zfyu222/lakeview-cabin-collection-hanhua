"""Inventory every texture, deduplicate decoded pixels, and produce review sheets."""
from pathlib import Path
import json,hashlib,collections
import UnityPy
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Analysis/image_audit'
(OUT/'images').mkdir(parents=True,exist_ok=True)
(OUT/'ocr').mkdir(exist_ok=True)
textures=json.loads((ROOT/'Analysis/textures.json').read_text('utf-8'))
byfile=collections.defaultdict(list)
for t in textures:byfile[t['file']].append(t)
unique={};rows=[];errors=[]
for file,items in byfile.items():
 env=UnityPy.load(str(ROOT/'Game/Lakeview Cabin Collection_Data'/file))
 objects={o.path_id:o for o in env.objects if Path(o.assets_file.name).name==file}
 for t in items:
  if t['width']<=0 or t['height']<=0:
   rows.append(dict(t,classification='runtime_empty_texture'));continue
  try:
   im=objects[t['path_id']].read().image.convert('RGBA')
   h=hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest()
   if h not in unique:
    index=len(unique)+1
    im.save(OUT/'images'/f'{index:04d}.png')
    # OCR preprocessing only; these enlarged inputs are never used as game assets.
    scale=min(6,max(2,1200//max(im.size)))
    bg=Image.new('RGBA',im.size,(180,180,180,255));bg.alpha_composite(im)
    bg.convert('RGB').resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST).save(OUT/'ocr'/f'{index:04d}.png')
    unique[h]=dict(index=index,file=file,path_id=t['path_id'],name=t['name'],width=im.width,height=im.height)
   rows.append(dict(t,index=unique[h]['index'],pixel_sha256=h,classification='pending_visual_review'))
  except Exception as ex:errors.append(dict(t,error=str(ex)))
 print(file,'unique',len(unique),flush=True)
ordered=sorted(unique.values(),key=lambda x:(-x['width']*x['height'],x['index']))
for start in range(0,len(ordered),64):
 batch=ordered[start:start+64]
 sheet=Image.new('RGB',(8*185,8*180),(37,39,43))
 draw=ImageDraw.Draw(sheet)
 for i,t in enumerate(batch):
  im=Image.open(OUT/'images'/f'{t["index"]:04d}.png')
  im.thumbnail((178,145),Image.Resampling.NEAREST)
  x=(i%8)*185;y=(i//8)*180
  sheet.paste(im,(x+(185-im.width)//2,y+28+(145-im.height)//2),im)
  draw.text((x+3,y+2),f'{t["index"]:04d} '+t['name'][:22],fill='white')
  draw.text((x+3,y+15),f'{t["width"]}x{t["height"]}',fill='#999999')
 sheet.save(OUT/f'sheet_{start//64+1:02d}.png')
(OUT/'inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'unique.json').write_text(json.dumps(ordered,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(texture_objects=len(textures),unique_images=len(unique),sheets=(len(unique)+63)//64,errors=len(errors))))
