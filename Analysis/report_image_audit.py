"""Record full contact-sheet review and distinguish translated regions from exclusions."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'Analysis/image_audit'
inventory=json.loads((HERE/'inventory.json').read_text('utf-8'))
unique=json.loads((HERE/'unique.json').read_text('utf-8'))
regions=json.loads((HERE/'text_regions.json').read_text('utf-8'))
indices={p['image_index'] for p in regions}
for item in inventory:
 if 'index' not in item:continue
 item['classification']='new_readable_text_transcribed' if item['index'] in indices else 'contact_sheet_reviewed_no_additional_transcription'
(HERE/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
report={
 'method':'all decoded textures deduplicated by pixels; all 27 contact sheets manually reviewed, with full-size reading for candidate images; Windows OCR used only to find candidates',
 'texture_objects':len(inventory),'unique_pixel_images':len(unique),'sprite_objects':len(json.loads((ROOT/'Analysis/sprite_catalog.json').read_text('utf-8'))),
 'contact_sheets_reviewed':list(range(1,28)),'decode_errors':json.loads((HERE/'errors.json').read_text('utf-8')),
 'new_source_records':93,'transcribed_image_regions':len(regions),'new_overlay_labels':123,'total_overlay_labels':143,'total_lookup_keys':118,
 'limits':[
  'Static asset review cannot prove every reachable game state is translated; user gameplay checks pending.',
  'No extra words invented for torn newspaper body, unreadable pixel noise or tiny illegible decorative text.',
  'Latin signature, creator handles, product brands, numbers, keys, alphabet puzzle pieces and Bible reference intentionally preserved.',
  'COMBO text in PsychoCombo atlas is outside the exported multiplier sprite rectangles; not overlaid on their numbers.',
  'SECURITY/ARMORY/RESEARCH/STORAGE/GENERATORS/EXIT labels in the older Signs atlas have no corresponding exported text sprite rectangles; MEDBAY is mapped. Revisit if these labels appear during gameplay.',
  'Notes1 torn KILL letter fragments are retained as puzzle artwork; their assembled appearance needs gameplay review.',
  'World pickups below 90 screen pixels keep original note icons; reading view is the intended Chinese display.',
 ],'game_test':'pending_user','computer_control_used':False
}
(HERE/'coverage_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:report[k] for k in ['texture_objects','unique_pixel_images','sprite_objects','new_source_records','total_overlay_labels']}))
