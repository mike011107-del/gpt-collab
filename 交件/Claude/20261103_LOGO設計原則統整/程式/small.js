const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:400},deviceScaleFactor:1});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(300);
const ids=await p.$$eval('div[id]',els=>els.map(e=>e.id));
for(const id of ids){const el=await p.$('#'+id);await el.screenshot({path:process.argv[3]+'/'+id+'.png'});}
await b.close();})();
