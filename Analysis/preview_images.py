import json,re
from pathlib import Path
import UnityPy
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Analysis'/'images'
OUT.mkdir(exist_ok=True)
textures=json.loads((ROOT/'Analysis'/'textures.json').read_text('utf-8'))
selected=[t for t in textures if re.search(r'menu|title|note|letter|control|backbutton',t['name'],re.I) and t['width']>40]
envs={}
tiles=[]
for t in selected:
    file=t['file']
    if file not in envs: envs[file]=UnityPy.load(str(ROOT/'Game'/'Lakeview Cabin Collection_Data'/file))
    o=next(o for o in envs[file].objects if o.path_id==t['path_id'] and Path(o.assets_file.name).name==file)
    im=o.read().image
    im.save(OUT/(file+'_'+str(t['path_id'])+'.png'))
    tile=Image.new('RGB',(350,335),(65,65,65))
    im.thumbnail((340,290))
    tile.paste(im,((350-im.width)//2,30),im if im.mode=='RGBA' else None)
    ImageDraw.Draw(tile).text((5,5),t['name']+' / '+file+' #'+str(t['path_id']),fill='white')
    tiles.append(tile)
for start in range(0,len(tiles),12):
    batch=tiles[start:start+12]
    sheet=Image.new('RGB',(350*3,335*((len(batch)+2)//3)))
    for i,tile in enumerate(batch): sheet.paste(tile,((i%3)*350,(i//3)*335))
    sheet.save(OUT/f'contact_{start//12+1}.png')
print('images',len(tiles))
