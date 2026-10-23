"""Human transcriptions after reviewing every contact sheet; do not trust OCR as source."""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'Analysis/image_audit'
catalog=json.loads((ROOT/'Analysis/sprite_catalog.json').read_text('utf-8'))
unique=json.loads((AUDIT/'unique.json').read_text('utf-8'))
byid={x['index']:x for x in unique}
parts=[]
def add(index,text,box=(0,0,1,1),note=False,names=None,reason='Visually verified readable image text'):
 t=byid[index]
 sprites=[s for s in catalog if s['texture_file']==t['file'] and s['texture_id']==t['path_id'] and (names is None or s['name'] in names)]
 if names is not None:assert len(sprites)==len(names),(index,names)
 parts.append(dict(image_index=index,texture=t['name'],file=t['file'],texture_id=t['path_id'],source=text,box=box,note=note,sprites=sprites,reason=reason))

# Screenshot report: only the masthead and readable headlines, not decorative noise below.
add(1078,'The Lakeview Post',(.15,.17,.70,.105))
add(1078,'INFANT KIDNAPPINGS CONTINUE!',(.12,.28,.76,.32))
add(1078,'POLICE ARE BAFFLED',(.12,.64,.76,.10))
add(143,'"SMILING KILLER" CAUGHT IN COITUS WITH HIS SISTER!',(.07,.23,.84,.175))
add(143,'The childkiller terrorizing the town was caught at his home yesterday afternoon. The detectives at scene said they found the suspe...',(.08,.41,.42,.37),True,reason='Bottom is physically torn off; preserve the truncation and do not reconstruct missing words')
add(279,"Mr. K\nWe've recently discovered the long lost will of your great-grandfather.\nAccording to the document, you are to receive the following items:\n-One locked box (contents unknown)\n-A portrait of the deceased\nThank you.",(.09,.07,.81,.78),True)
add(323,'My parents leave at 8pm.\nThe key is in the mailbox...',(.15,.34,.72,.33),True)
add(319,'"HAPPY DAD" mask',(.20,.31,.48,.15))
add(201,'LACUS CABINA\nGAME CARTRIDGE\nMANUAL INCLUDED',(.20,.19,.57,.63),True)
for i in [130,220,312,353]:add(i,'ERROR!\nCAN YOU ZOOM OUT?\nERROR!',(.20,.19,.59,.53),True)
add(1227,"May 20th\nBack at the camp. I really need to fix the holes in the new building before someone gets hurt.\n\nJune 3th\nSome kids say they heard a baby screaming last night. Probably just to scare the younger ones...\n\nJune 10th\nNew owner. Seemed to have a bit of a temper. Better to just stay out of the way and focus on my work.\n\nJune 27th\nI think there's something in the water... Feeling kinda uneasy...\n\nJuly 2nd\nA kid went missing last night. The sheriff is shutting the camp down until further notice. Should probably look for a new job.",(.035,.025,.93,.95),True)
add(1575,"As I sit here at my final resting place, contemplating my last words, only one thing comes to mind.\nFuck all of you...\nI'm burning down the factory and cursing the lake you sought to protect.\nMay you never find peace when my blood still flows.",(.04,.03,.92,.80),True)
add(1398,"The game you're about to play is an account of the tragedy that befell a group of four youths. Names have been changed to respect what was left of the survivors.",(.08,.13,.84,.70),True)
add(1395,'PARADOX\nA problem has been detected and Windows has been shut down to prevent damage to your computer.\nPRESS ANY KEY TO FORMAT HARD DRIVE',(.02,.14,.96,.60),True,reason='Fictional in-game blue-screen joke. Translate as story text; never execute it')
add(1397,'****REMOVING ALL DATA FROM HARDDRIVE****',(.15,.70,.70,.17),False,reason='Fictional in-game blue-screen joke, not an instruction')

messages={135:'SAVE FILE DELETED',167:'EVERYONE ELSE IS BETTER THAN YOU',280:"HE'S TRYING TO DISTRACT YOU",335:'VIDEO GAMES ARE ROTTING YOUR BRAIN',351:'WHICH DOOR WAS IT?',369:"YOU WON'T SOLVE THIS",513:'MANKIND IS DOOMED.',753:'YOU AND YOUR FRIENDS ARE DEAD.',800:'YOU, YOUR DOG AND YOUR FRIENDS ARE DEAD.',1090:'YOUR BABY IS DEAD AND YOU ARE A COWARD.',1095:'YOUR BABY IS GONE AND YOU ARE DEAD.',1115:'YOUR BABY IS GONE AND YOU ARE A COWARD.',1124:'YOU AND YOUR BABY ARE DEAD.',1538:'THE BAND IS DEAD.'}
for index,message in messages.items():
 add(index,message,(.05,.28,.90,.25))
 add(index,'GAME OVER',(.07,.55,.86,.20))
add(379,'GAME OVER')
add(62,'PRESS START/SPACE')
add(64,'PRESS CTRL TO TURN LIGHTING EFFECTS ON',(.01,.33,.98,.34))
add(66,'PRESS CTRL TO TURN LIGHTING EFFECTS OFF',(.01,.33,.98,.34))
add(245,'PRESS SELECT TO VIEW INFO')
add(342,'PRESS I TO VIEW INFO')
add(896,'HOLD TO PEEK')
add(124,'NOT ALL DOORS ARE EQUAL',names=['ZoomHints_0'])
add(124,'READ THE MANUAL',names=['ZoomHints_1'])
add(359,'POINT OF VIEW MATTERS')
add(742,'COMING SOON')
add(1131,'COME PLAY')
add(272,'FOR SALE',(.08,.28,.32,.36))
add(557,'THREAT DETECTED!\nEVACUATE!',(.10,.015,.80,.35))
add(592,'UNKNOWN THREAT DISCOVERED!\nGET OUT!',(.05,.03,.90,.90))
add(476,'ENTRY: not found',(.09,.22,.48,.12))
add(626,'BOOTING...',(.28,.31,.42,.18))
add(428,'NAVMAP V1.5b\nWELCOME',(.28,.31,.43,.28))
add(659,'INTERNAL COMM SYSTEM V.1.4.7',(.29,.15,.42,.04))
for i in [78,253]:add(i,'OPERATING DIFFICULTIES HAVE CAUSED AN INTERRUPTION IN PROGRAMMING.\nCHANNEL 1',(.20,.24,.60,.43),True)
for i in [131,368]:add(i,'TECHNICAL DIFFICULTIES',(.15,.26,.70,.20))
add(427,'POINTS',names=['PsychoWords_0'])
add(427,'AWESOME',names=['PsychoWords_1'])
add(427,'RADICAL',names=['PsychoWords_2'])
add(427,'EXTREME',names=['PsychoWords_3'])
add(427,'GNARLY',names=['PsychoWords_4'])
add(627,'COMBO',(.09,.77,.84,.18))
add(571,'CHOOSE',names=['RockPaperScissors_5'])
add(571,'YOU WIN',names=['RockPaperScissors_6'])
add(571,'YOU LOSE',names=['RockPaperScissors_7'])
add(571,'RPS WIZARD',names=['RockPaperScissors_13'])
add(496,'DRAW')
for num,word in enumerate(['TOILET','OFFICERS','SCIENTISTS','SANITATION']):add(578,word,names=['SignsNEW2_'+str(num)])
add(666,'QUARTERS',names=['SignsNEW_4'])
add(504,'MEDBAY',names=['Signs_11'])
add(637,'MAINTENANCE',(.435,.46,.10,.07))
add(637,'BAR TRIPLE TREY',(.25,.47,.095,.055))
add(637,'BAR TRIPLE TREY',(.69,.47,.095,.055))
add(637,'STUPID HUMAN! LET ME FIX IT!',(.35,.51,.085,.13),True)
add(820,'INTERGALACTIC REFUGEE CENTER',(.39,.38,.22,.11))
add(911,'KILLER VIDEOS\nVHS RENTAL',(.20,.36,.59,.20))
add(751,'OPEN')
add(169,'NOT YOU',(.10,.77,.55,.17))
add(72,'1 JOHN 3:14',(.14,.77,.55,.17))
add(750,'THE SEWERS SCREAM AT ME',(.37,.18,.49,.36),True)
add(1214,"RED\nRED\nRED",(.48,.31,.26,.36),True)
add(1142,'DOOMED',(.33,.02,.55,.25))
add(1625,'GAS',(.34,.29,.18,.13))

# Preserve original title artwork and add a caption strip below it.
for i in [95,126,183,234]:add(i,'LACUS CABINA',(.21,.89,.58,.11))
for i,source in [(1211,'LAKEVIEW CABIN III'),(1613,"LAKEVIEW CABIN IV\nCURSE OF THE LAKE\nDIRECTOR'S CUT"),(375,'LAKEVIEW CABIN V\nHOMECOMING'),(587,'CABIN 6'),(586,'SPACE PSYCHOS'),(878,'LAKEVIEW CABIN 7\nMANHATTAN MASSACRE'),(815,'TREASURE OF THE VAMPIRE REDNECKS'),(913,'LAKE OF THE DEAD'),(1076,'MERRY CHRISTMAS'),(1105,'LAST CHRISTMAS'),(539,'RPS WIZARD')]:
 if i==375:add(i,source,(0,.84,1,.16),names=['Title5_0'])
 else:add(i,source,(0,.84,1,.16))
for j,roman in enumerate(['III','IV','V','VI'],1):add(813,'LAKEVIEW CABIN '+roman,names=['MovieBoards_'+str(j)])

sources=list(dict.fromkeys(p['source'] for p in parts))
for p in parts:p['row']=sources.index(p['source'])+1
with (ROOT/'lakeview-cabin-collection_image_audit_text.csv').open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f).writerows([s] for s in sources)
(AUDIT/'text_regions.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2),encoding='utf-8')
print('unique source texts',len(sources),'regions',len(parts),'unmapped',[(p['image_index'],p['source']) for p in parts if not p['sprites']])
