"""CSS-only previews of actual sprite crops, using the runtime coverage map."""
from pathlib import Path
import base64,html,json
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
spec=json.loads((HERE/'overlay_map.json').read_text('utf-8'))
catalog=json.loads((ROOT/'Analysis/sprite_catalog.json').read_text('utf-8'))
cards=[]
for key,labels in spec.items():
 if '|' not in key:continue
 texture,name=key.split('|',1)
 s=next(s for s in catalog if s['texture']==texture and s['name']==name)
 img=ROOT/'Analysis/image_audit/images'/('%04d.png'%labels[0]['image_index'])
 w,h=Image.open(img).size
 r=s['rect'];sw,sh=r['w'],r['h'];sx,sy=r['x'],h-r['y']-sh
 scale=min(4,740/sw,900/sh)
 url='data:image/png;base64,'+base64.b64encode(img.read_bytes()).decode()
 layers=''
 for e in labels:
  x,y,bw,bh=e['box']
  size=max(9,min(64,sw*bw/12 if e['note'] else sh*bh*.72))*scale
  padding=max(4,sw*bw*scale*.035) if e['note'] else max(1,sh*bh*scale*.05)
  layers+=f'<div class="label {"note" if e["note"] else ""}" style="left:{x*100}%;top:{y*100}%;width:{bw*100}%;height:{bh*100}%;font-size:{size}px;padding:{padding}px">{html.escape(e["text"])}</div>'
 cards.append((key,f'<section data-name="{html.escape(key)}"><h2>{html.escape(key)}</h2><div class="sprite" style="width:{sw*scale}px;height:{sh*scale}px;background-image:url({url});background-size:{w*scale}px {h*scale}px;background-position:-{sx*scale}px -{sy*scale}px">{layers}</div></section>'))
# Put the reported newspaper and two long reading pages first for review.
priority=['InfoNewspaper|InfoNewspaper','LongDiaryNew|LongDiaryNew','LongDiaryMan2|LongDiaryMan2']
cards.sort(key=lambda c:priority.index(c[0]) if c[0] in priority else 99)
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>图片漏译补查预览</title><style>
body{margin:24px;background:#17191d;color:#eee;font:16px "Microsoft YaHei",sans-serif}h1{font-size:25px}h2{font-size:13px;color:#a5acb7}p{color:#bbb}main{display:flex;flex-wrap:wrap;gap:22px;align-items:flex-start}section{padding:14px;background:#24272c;border-radius:7px}.sprite{position:relative;image-rendering:pixelated;background-repeat:no-repeat}.label{position:absolute;box-sizing:border-box;background:rgba(43,43,43,.88);display:flex;align-items:center;justify-content:center;text-align:center;font-weight:bold;line-height:1.2;white-space:pre-line;padding:2px;overflow:hidden}.note{display:block;text-align:left;font-weight:normal;padding:3.5%;line-height:1.25}body.original .label{visibility:hidden}button{font:inherit;padding:8px;margin-bottom:20px}
</style><h1>图片漏译补查：灰色蒙版＋中文</h1><p>静态排版示意，非实机截图。原图保留；游戏内按 F8 可切换覆盖层。下列为新增区域。</p><button onclick="document.body.classList.toggle('original')">原文 / 中文覆盖</button><main>'''+''.join(c[1] for c in cards)+'''</main><script>for(const el of document.querySelectorAll('.label')){while((el.scrollHeight>el.clientHeight+1||el.scrollWidth>el.clientWidth+1)&&parseFloat(getComputedStyle(el).fontSize)>8){el.style.fontSize=(parseFloat(getComputedStyle(el).fontSize)-.5)+'px';}}</script></html>'''
(HERE/'audit_preview.html').write_text(page,encoding='utf-8')
print(json.dumps({'sprite_cards':len(cards)}))
