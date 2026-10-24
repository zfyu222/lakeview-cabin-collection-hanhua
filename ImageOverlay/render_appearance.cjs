// Render local HTML comparisons only, without opening or controlling the game.
const {chromium}=require('C:/Users/zfyu2/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1650,height:1000},deviceScaleFactor:1});
  await page.goto(pathToFileURL(path.join(__dirname,'audit_preview.html')).href);
  await page.evaluate(()=>{
   const source=document.querySelector('section[data-name="InfoNewspaper|InfoNewspaper"]');
   const old=source.cloneNode(true),fresh=source.cloneNode(true);
   old.querySelector('h2').textContent='之前：88% 灰底';
   fresh.querySelector('h2').textContent='现在：25% 轻底＋中文细描边';
   old.querySelectorAll('.label').forEach(e=>{e.style.background='rgba(43,43,43,.88)';e.style.textShadow='none';});
   const main=document.querySelector('main');main.replaceChildren(old,fresh);
   main.style.flexWrap='nowrap';main.style.width='max-content';
  });
  await page.locator('main').screenshot({path:path.join(__dirname,'opacity_comparison.png')});
  console.log('Rendered opacity_comparison.png (static illustration, not gameplay)');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
