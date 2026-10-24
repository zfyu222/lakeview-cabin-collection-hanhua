"""Build an additive runtime text layer and code-native previews. Original PNGs stay untouched."""
import base64,csv,hashlib,html,json,shutil,subprocess
from pathlib import Path
from appearance import CONFIG as APPEARANCE, css as appearance_css, csharp as appearance_csharp
ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
WORK=ROOT/'TranslateFiles/image-overlay'
DATA=(ROOT/'Game/Lakeview Cabin Collection_Data').resolve()
OUT=ROOT/'Patch/Lakeview Cabin Collection_Data/Managed'
BUILD=HERE/'build'
BUILD.mkdir(exist_ok=True)
OUT.mkdir(parents=True,exist_ok=True)
prior_manifest=json.loads((ROOT/'Patch/manifest.json').read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):subprocess.run([str(a) for a in args],check=True)
validation=json.loads((WORK/'TranslateFiles/reports/final_validation.json').read_text('utf-8'))
csvpath=WORK/'lakeview-cabin-collection-images_text_translated.csv'
assert validation['status']=='passed' and sha(csvpath)==validation['translation_sha256']
shutil.copy2(csvpath,ROOT/'lakeview-cabin-collection_images_text_translated.csv')
with csvpath.open(encoding='utf-8-sig',newline='') as f: text=[r[0] for r in csv.reader(f)]
def entry(row,box=(0,0,1,1),note=False,bright=False):return dict(row=row,box=box,note=note,bright=bright,text=text[row-1])
spec={
 'PauseMenu_0':[entry(1)],'PauseMenu_1':[entry(2)],'PauseMenu_2':[entry(3)],'PauseMenu_3':[entry(4)],
 'PauseMenuConfirm_0':[entry(5,(0,0,1,.5)),entry(6,(.08,.5,.42,.5),bright=True),entry(7,(.50,.5,.42,.5))],
 'PauseMenuConfirm_1':[entry(5,(0,0,1,.5)),entry(6,(.08,.5,.42,.5)),entry(7,(.50,.5,.42,.5),bright=True)],
 'Controller':[entry(8,(0,.86,1,.14))],
 'TitleVNewgame_0':[entry(9)],'TitleVNewgame_1':[entry(10)],'TitleVNewgame2_1':[entry(10)],
 'TitleVBonus_0':[entry(11)],'TitleVBonus_1':[entry(11)],
 'NoteNew':[entry(12,(.045,.025,.90,.66),True),entry(13,(.02,.83,.58,.13),True)],
 'Notes_0':[entry(14,(0,0,1,1),True)],
 'InfoLetter':[entry(15,(.28,.25,.34,.53),True)]
}
auditwork=ROOT/'TranslateFiles/image-audit'
auditcsv=auditwork/'lakeview-cabin-collection-image-audit_text_translated.csv'
auditvalidation=json.loads((auditwork/'TranslateFiles/reports/final_validation.json').read_text('utf-8'))
assert auditvalidation['status']=='passed' and sha(auditcsv)==auditvalidation['translation_sha256']
auditsource=ROOT/'lakeview-cabin-collection_image_audit_text.csv'
assert sha(auditsource)==auditvalidation['source_sha256']
with auditsource.open(encoding='utf-8-sig',newline='') as f:auditsourcetext=[r[0] for r in csv.reader(f)]
shutil.copy2(auditcsv,ROOT/'lakeview-cabin-collection_image_audit_text_translated.csv')
with auditcsv.open(encoding='utf-8-sig',newline='') as f:audittext=[r[0] for r in csv.reader(f)]
regions=json.loads((ROOT/'Analysis/image_audit/text_regions.json').read_text('utf-8'))
exclusions=[]
for p in regions:
 assert p['source']==auditsourcetext[p['row']-1], 'Image region source row changed'
 if p['image_index']==627:
  exclusions.append({'source':p['source'],'reason':'COMBO atlas label is outside all four exported multiplier sprite rects; do not cover their numbers'})
  continue
 for sprite in p['sprites']:
  key=sprite['texture']+'|'+sprite['name']
  spec.setdefault(key,[]).append(dict(row=p['row'],box=p['box'],note=p['note'],bright=False,text=audittext[p['row']-1],image_index=p['image_index']))
(HERE/'audit_exclusions.json').write_text(json.dumps(exclusions,ensure_ascii=False,indent=2),encoding='utf-8')
incremental=ROOT/'ImageText/overlay_bindings_v05.json'
mapping_corrections=[]
# Visual reinspection: the old broad robot balloon covered the separate ALL NEW label.
robot=spec['CorridorWhite2|CorridorWhite2'][-1]
assert robot['text']=='愚蠢的人类！让我来修好它！' and robot['box']==[.35,.51,.085,.13]
mapping_corrections.append(dict(key='CorridorWhite2|CorridorWhite2',before=robot['box'],reason='Tighten balloon to exclude separately visible ALL NEW caption'))
robot['box']=[346/948,130/256,61/948,21/256]
# The exact SignsNEW_4 rectangle visibly says EXIT, not QUARTERS.
if (ROOT/'ImageText/overlay_bindings_final.json').exists():
 old=spec['SignsNEW|SignsNEW_4']
 assert len(old)==1 and old[0]['text']=='宿舍' and old[0]['image_index']==666
 mapping_corrections.append(dict(key='SignsNEW|SignsNEW_4',before=old,reason='Visual source rectangle reads EXIT; replace with formally reviewed exit label'))
 del spec['SignsNEW|SignsNEW_4']
 old=spec['Signs|Signs_11']
 assert len(old)==1 and old[0]['text']=='医疗舱' and old[0]['image_index']==504
 mapping_corrections.append(dict(key='Signs|Signs_11',before=old,reason='Source sprite rectangle also reads EXIT; MEDBAY is elsewhere in the atlas without a matching exported slice'))
 del spec['Signs|Signs_11']
corrections=ROOT/'ImageText/overlay_bindings_corrections.json'
if corrections.exists():
 for key,expected_index in [('ForSaleSign|ForSaleSign_0',272),('RandomScares|RandomScares_2',1142),('RandomScares|RandomScares_4',1142),('TitleSpacePsycho|TitleSpacePsycho_0',586),('TitleSpacePsycho|TitleSpacePsycho_1',586),('ToiletScribble|ToiletScribble',1214)]:
  old=spec.get(key)
  if not old or len(old)!=1 or old[0].get('image_index')!=expected_index:raise ValueError('Unexpected legacy correction scope: '+key)
  # Exact prior strings are archived below; the original immutable CSVs remain.
  mapping_corrections.append(dict(key=key,before=old,reason='Actual legacy sprite crop visually rechecked: remove text from non-text art or replace incorrect/split source mapping'))
  del spec[key]
if incremental.exists():
 extra=json.loads(incremental.read_text('utf-8'))
 src=ROOT/'lakeview-cabin-collection_image_v05_text.csv'
 dst=src.with_name(src.stem+'_translated.csv')
 mapping=src.with_suffix('.mapping.json')
 imagepayload=ROOT/'ImagePatch/v05-overlay/IMAGE_PATCH_MANIFEST.json'
 report=json.loads((ROOT/'TranslateFiles/image-text/TranslateFiles/reports/final_validation.json').read_text('utf-8'))
 assert report['status']=='passed' and report['semantic_review']=='full'
 assert sha(src)==extra['source_sha256']==report['source_sha256']
 assert sha(dst)==extra['translation_sha256']==report['translation_sha256']
 assert sha(mapping)==extra['mapping_sha256'] and sha(imagepayload)==extra['payload_sha256']
 with dst.open(encoding='utf-8-sig',newline='') as f:incremental_text=[r[0] for r in csv.reader(f)]
 for key,labels in extra['spec'].items():
  for label in labels:
   assert label['text']==incremental_text[label['row']-1], 'Incremental label differs from formal export'
   x,y,w,h=label['box']
   for old in spec.get(key,[]):
    ox,oy,ow,oh=old['box']
    if min(x+w,ox+ow)>max(x,ox) and min(y+h,oy+oh)>max(y,oy):
     raise ValueError('Incremental label overlaps existing translation: '+key)
   spec.setdefault(key,[]).append(label)
last=ROOT/'ImageText/overlay_bindings_final.json'
if last.exists():
 more=json.loads(last.read_text('utf-8'))
 src=ROOT/'lakeview-cabin-collection_image_final_text.csv';dst=src.with_name(src.stem+'_translated.csv')
 report=json.loads((ROOT/'TranslateFiles/image-final/TranslateFiles/reports/final_validation.json').read_text('utf-8'))
 assert report['status']=='passed' and report['semantic_review']=='full'
 assert sha(src)==more['source_sha256']==report['source_sha256'] and sha(dst)==more['translation_sha256']==report['translation_sha256']
 assert sha(src.with_suffix('.mapping.json'))==more['mapping_sha256']
 assert sha(ROOT/'ImagePatch/final-overlay/IMAGE_PATCH_MANIFEST.json')==more['payload_sha256']
 with dst.open(encoding='utf-8-sig',newline='') as f:final_text=[r[0] for r in csv.reader(f)]
 for key,labels in more['spec'].items():
  for label in labels:
   assert label['text']==final_text[label['row']-1], 'Final label differs from formal export'
   x,y,w,h=label['box']
   for old in spec.get(key,[]):
    ox,oy,ow,oh=old['box']
    if min(x+w,ox+ow)>max(x,ox) and min(y+h,oy+oh)>max(y,oy):raise ValueError('Final label overlaps existing translation: '+key)
   spec.setdefault(key,[]).append(label)
if corrections.exists():
 fixed=json.loads(corrections.read_text('utf-8'))
 src=ROOT/'lakeview-cabin-collection_image_corrections_text.csv';dst=src.with_name(src.stem+'_translated.csv')
 report=json.loads((ROOT/'TranslateFiles/image-corrections/TranslateFiles/reports/final_validation.json').read_text('utf-8'))
 assert report['status']=='passed' and report['semantic_review']=='full'
 assert sha(src)==fixed['source_sha256']==report['source_sha256'] and sha(dst)==fixed['translation_sha256']==report['translation_sha256']
 assert sha(src.with_suffix('.mapping.json'))==fixed['mapping_sha256'] and sha(ROOT/'ImagePatch/corrections-overlay/IMAGE_PATCH_MANIFEST.json')==fixed['payload_sha256']
 with dst.open(encoding='utf-8-sig',newline='') as f:fixed_text=[r[0] for r in csv.reader(f)]
 for key,labels in fixed['spec'].items():
  assert key not in spec, 'Correction unexpectedly overwrites an unchecked label'
  for label in labels:assert label['text']==fixed_text[label['row']-1]
  spec[key]=labels
(HERE/'mapping_corrections.json').write_text(json.dumps(mapping_corrections,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'overlay_map.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['using System.Collections.Generic;','namespace LakeviewChinese { public static class OverlayData { public static Dictionary<string,Entry[]> Create() { return new Dictionary<string,Entry[]> {']
for name,labels in spec.items():
 vals=[]
 for e in labels:
  args=[json.dumps(e['text'],ensure_ascii=False)]+[str(float(x))+'f' for x in e['box']]+[str(e['note']).lower(),str(e['bright']).lower()]
  vals.append('new Entry('+','.join(args)+')')
 lines.append('{'+json.dumps(name)+',new Entry[]{'+','.join(vals)+'}},')
lines.append('}; } } }')
(BUILD/'OverlayData.cs').write_text('\n'.join(lines),encoding='utf-8-sig')
(BUILD/'Appearance.cs').write_text(appearance_csharp(),encoding='utf-8-sig')
csc=Path('C:/Windows/Microsoft.NET/Framework/v3.5/csc.exe')
run([csc,'/nologo','/target:library','/nostdlib','/out:'+str(OUT/'LakeviewChineseOverlay.dll'),'/reference:'+str(DATA/'Managed/mscorlib.dll'),'/reference:'+str(DATA/'Managed/System.dll'),'/reference:'+str(DATA/'Managed/UnityEngine.dll'),HERE/'ChineseOverlay.cs',BUILD/'OverlayData.cs',BUILD/'Appearance.cs'])
cecil=ROOT.parents[1]/'Tools/XUnity.AutoTranslator/libs/Mono.Cecil.dll'
run(['C:/Windows/Microsoft.NET/Framework/v4.0.30319/csc.exe','/nologo','/out:'+str(BUILD/'PatchBootstrap.exe'),'/reference:'+str(cecil),HERE/'PatchBootstrap.cs'])
shutil.copy2(cecil,BUILD/'Mono.Cecil.dll')
original=ROOT/'Backups/original/Lakeview Cabin Collection_Data/Managed/Assembly-CSharp.dll'
if not original.exists(): original=DATA/'Managed/Assembly-CSharp.dll'
if sha(original)!='24614b17719774fbd412985502fe431f0d800f66d03f970eb10e62b8a086293d':
 raise ValueError('Unsupported Assembly-CSharp.dll source; do not patch another version')
run([BUILD/'PatchBootstrap.exe',original,OUT/'LakeviewChineseOverlay.dll',OUT/'Assembly-CSharp.dll',DATA/'Managed'])
manifest={'status':'built_not_game_tested','method':'runtime IMGUI gray panel and Chinese label; original textures unchanged','toggle':'F8','source_assembly_sha256':sha(original),'translation_sha256':sha(csvpath),'audit_translation_sha256':sha(auditcsv),'sprite_names':len(spec),'labels':sum(len(x) for x in spec.values()),'payload_files':[]}
if incremental.exists():
 manifest['incremental_translation_sha256']=extra['translation_sha256']
 manifest['incremental_labels']=extra['labels']
 manifest['incremental_unbound_regions']=len(extra['unbound'])
if last.exists():
 manifest['final_translation_sha256']=more['translation_sha256'];manifest['final_labels']=more['labels'];manifest['final_unbound_regions']=len(more['unbound'])
manifest['mapping_corrections']=mapping_corrections
manifest['appearance']=APPEARANCE
if corrections.exists():
 manifest['corrections_translation_sha256']=fixed['translation_sha256'];manifest['corrections_labels']=fixed['labels']
for file in ('Assembly-CSharp.dll','LakeviewChineseOverlay.dll'):
 f=OUT/file
 manifest['payload_files'].append({'path':str(f.relative_to(ROOT)),'game_path':'Lakeview Cabin Collection_Data/Managed/'+file,'sha256':sha(f),'source_sha256':sha(original) if file=='Assembly-CSharp.dll' else None})
for item in manifest['payload_files']:
 previous=next((x for x in prior_manifest['payload_files'] if x['game_path']==item['game_path']),None)
 if previous:
  item['previous_sha256']=sorted(set(previous.get('previous_sha256',[])+[previous['sha256']])-{item['sha256']})
(HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
root_manifest_path=ROOT/'Patch/manifest.json'
root_manifest=json.loads(root_manifest_path.read_text('utf-8'))
overlay_paths={x['game_path'] for x in manifest['payload_files']}
root_manifest['payload_files']=[x for x in root_manifest['payload_files'] if x['game_path'] not in overlay_paths]+manifest['payload_files']
root_manifest['status']='image_overlay_pending_user_test'
root_manifest['image_overlay_translation_sha256']=manifest['translation_sha256']
root_manifest_path.write_text(json.dumps(root_manifest,ensure_ascii=False,indent=2),encoding='utf-8')

# Preview uses HTML/CSS layers over the untouched exported PNG. It does not raster-edit any game image.
sprites=json.loads((ROOT/'Analysis/overlay_sprites.json').read_text('utf-8'))
previews=[('PauseMenu_0','sharedassets2.assets_153.png'),('PauseMenu_1','sharedassets2.assets_153.png'),('PauseMenu_2','sharedassets2.assets_153.png'),('PauseMenu_3','sharedassets2.assets_153.png'),('PauseMenuConfirm_0','sharedassets2.assets_227.png'),('NoteNew','sharedassets3.assets_97.png'),('Notes_0','sharedassets3.assets_118.png'),('InfoLetter','sharedassets24.assets_39.png')]
from PIL import Image
cards=[]
for name,imgfile in previews:
 original_image=ROOT/'Analysis/images'/imgfile
 w,h=Image.open(original_image).size
 sprite=next(x for x in sprites if x['name']==name)
 r=sprite['rect']; sx=r['x'];sy=h-r['y']-r['h'];sw=r['w'];sh=r['h']
 # A CSS background crop selects an existing Unity sprite without touching its image bytes.
 scale=3 if sw<200 else 2
 url='data:image/png;base64,'+base64.b64encode(original_image.read_bytes()).decode()
 layers=''
 for e in spec[name]:
  x,y,bw,bh=e['box'];font= max(9,min(26,sw*bw/12 if e['note'] else sh*bh*.70))*scale
  if e['note']: font=min(font,16*scale)
  dim='color:#777;' if name.startswith('PauseMenuConfirm_') and y>=.49 and not e['bright'] else ''
  layers+=f'<div class="label {"note" if e["note"] else ""}" style="{dim}left:{x*100}%;top:{y*100}%;width:{bw*100}%;height:{bh*100}%;font-size:{font}px">{html.escape(e["text"])}</div>'
 cards.append(f'<section><h2>{html.escape(name)}</h2><div class="sprite" style="width:{sw*scale}px;height:{sh*scale}px;background-image:url({url});background-size:{w*scale}px {h*scale}px;background-position:-{sx*scale}px -{sy*scale}px">{layers}</div></section>')
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>图片文字覆盖预览</title><style>
body{background:#17191d;color:#eee;font:16px "Microsoft YaHei",sans-serif;margin:32px}h1{font-size:26px}h2{font-size:14px;color:#a5acb7}main{display:flex;flex-wrap:wrap;gap:26px;align-items:flex-start}section{background:#22252b;padding:18px;border-radius:8px}.sprite{position:relative;background-repeat:no-repeat;image-rendering:pixelated}.label{position:absolute;box-sizing:border-box;background:rgba(43,43,43,.88);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:bold;line-height:1.2;padding:2px;overflow:hidden;white-space:pre-line}.label.note{display:block;text-align:left;font-weight:normal;padding:12px;line-height:1.35}body.original .label{visibility:hidden}button{font:inherit;padding:8px 14px;margin-bottom:22px}p{color:#a5acb7;max-width:850px}
</style><h1>灰色半透明蒙版＋中文</h1><p>静态排版预览，非游戏截图。保留原贴图，覆盖层可独立关闭。实际游戏字号随精灵在屏幕上的尺寸适配；以下展示暂停菜单、确认框及便条样式。</p><button onclick="document.body.classList.toggle('original')">对照：原文 / 中文覆盖</button><main>'''+''.join(cards)+'''</main><script>for(const el of document.querySelectorAll('.label')){while((el.scrollHeight>el.clientHeight||el.scrollWidth>el.clientWidth)&&parseFloat(getComputedStyle(el).fontSize)>9){el.style.fontSize=(parseFloat(getComputedStyle(el).fontSize)-1)+'px';}}</script></html>'''
(HERE/'preview.html').write_text(page.replace('</style>',appearance_css()+'</style>'),encoding='utf-8')
print(json.dumps({'status':'built_not_game_tested','sprite_names':len(spec),'labels':manifest['labels'],'preview':str(HERE/'preview.html')}))
