const {chromium}=require('C:/Users/zfyu2/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');
const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1600,height:1100}});
 await page.goto(pathToFileURL(path.join(__dirname,'audit_preview.html')).href);
 const result=await page.locator('.label').evaluateAll(es=>({labels:es.length,overflow:es.filter(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1).map(e=>({text:e.innerText,card:e.closest('section').dataset.name}))}));
 await page.locator('section[data-name="InfoNewspaper|InfoNewspaper"]').screenshot({path:path.join(__dirname,'newspaper_preview.png')});
 await page.screenshot({path:path.join(__dirname,'audit_preview.png'),fullPage:false});
 require('node:fs').writeFileSync(path.join(__dirname,'audit_preview_validation.json'),JSON.stringify(result,null,2));
 console.log(JSON.stringify(result));await browser.close();
 if(result.overflow.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
