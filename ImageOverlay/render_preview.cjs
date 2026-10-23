const { chromium } = require('C:/Users/zfyu2/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
(async()=>{
  const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
  const page=await browser.newPage({viewport:{width:1400,height:1050},deviceScaleFactor:1});
  await page.goto(pathToFileURL(path.join(__dirname,'preview.html')).href);
  await page.screenshot({path:path.join(__dirname,'preview.png'),fullPage:true});
  const overflow=await page.locator('.label').evaluateAll(items=>items.filter(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1).length);
  console.log(JSON.stringify({preview:'preview.png',overflowing_labels:overflow}));
  await browser.close();
  if(overflow) process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
