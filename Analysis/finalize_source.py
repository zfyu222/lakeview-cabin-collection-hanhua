"""Select evidenced display fields, exclude identifiers and placeholders."""
import csv,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Analysis'
display=json.loads((OUT/'display_text.json').read_text('utf-8'))
values=json.loads((OUT/'playmaker_values.json').read_text('utf-8'))
selected=[]
excluded=[]
for r in display:
    s=r['text'].strip()
    if not re.search('[A-Za-z]{2}',s) or s in ('000','C-3','A-1','B-4','LOG GOES HERE!'):
        excluded.append(dict(r,reason='placeholder or numeric/internal room code; preserve original'))
    else:
        selected.append(r)
for r in values:
    s=r['text']
    if (r['fsm'] in ('Blurps','Blurber') and ((s.upper()==s and ' ' in s and len(s)>6) or s in ('GET OUT OF HERabaaAARG','OH N-splooorghugg!','SAVE YOURSE-HUaargh'))) or 'preFillStringList' in r['field'] or ('StringParameter' in r['field'] and s=='Loading...'):
        selected.append(r)
texts=list(dict.fromkeys(r['text'] for r in selected))
for r in selected: r['csv_row']=texts.index(r['text'])+1
with (ROOT/'lakeview-cabin-collection_text.csv').open('w',encoding='utf-8-sig',newline='') as f:
    csv.writer(f).writerows([s] for s in texts)
(OUT/'source_mapping.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'excluded_text.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2),encoding='utf-8')
context={}
for i,s in enumerate(texts,1):
    sources=[r for r in selected if r['csv_row']==i]
    first=sources[0]
    is_fsm=first['type'] if 'type' in first else 'PlayMakerFSM'
    context[str(i)]={'group':'lakeview-cabin-collection','resource':'; '.join(dict.fromkeys(r['file']+'#'+str(r['path_id']) for r in sources)), 'text_type': 'social feed / NPC exclamation' if is_fsm=='PlayMakerFSM' else 'credits' if 'Directed by' in s else 'note / UI', 'note':'Text contains authored line breaks. Keep staff names unchanged; translate role labels and prose. Social hashtags are in-world jokes and may be translated; not program identifiers. Picture text is outside this attempt.'}
(OUT/'translation_context.json').write_text(json.dumps(context,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'unique_texts':len(texts),'occurrences':len(selected),'excluded_occurrences':len(excluded)},ensure_ascii=False))
for i,s in enumerate(texts,1): print(i,repr(s[:90]))
