// Headless rendering of local HTML only; never starts or controls the game.
const {chromium}=require('C:/Users/zfyu2/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');
const path=require('node:path'),fs=require('node:fs');
(async()=>{
 const folder=path.join(__dirname,'incremental-preview');fs.mkdirSync(folder,{recursive:true});
 const keys=new Set(['CorridorWhite2|CorridorWhite2']);
 for(const name of ['v05','final','corrections']){
  const data=JSON.parse(fs.readFileSync(path.join(__dirname,'../ImageText/overlay_bindings_'+name+'.json'),'utf8'));
  Object.keys(data.spec).forEach(k=>keys.add(k));
 }
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:2100,height:1200}});
  await page.goto(pathToFileURL(path.join(__dirname,'audit_preview.html')).href);
  const results=[];
  for(const key of keys){
   const card=page.locator('section').filter({has:page.locator('h2',{hasText:key})});
   // Match exactly: a prefix can otherwise capture multiple animation frames.
   const exact=page.locator('section[data-name='+JSON.stringify(key)+']');
   const file=key.replace(/[^a-zA-Z0-9_-]/g,'_')+'.png';
   await exact.screenshot({path:path.join(folder,file)});
   results.push({key,file});
  }
  fs.writeFileSync(path.join(folder,'manifest.json'),JSON.stringify({scope:'Static preview only; not in-game evidence',cards:results},null,2));
  console.log(JSON.stringify({cards:results.length,folder}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
