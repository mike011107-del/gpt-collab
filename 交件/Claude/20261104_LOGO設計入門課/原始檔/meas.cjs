const {chromium}=require('playwright');
const F=process.argv[2]; const out=process.argv[3];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:600,height:600}});
for(const ch of ['上','國','小','口','一']){
 await p.setContent(`<html><head><link rel="stylesheet" href="file://${F}/700.css"></head><body style="margin:0;background:#fff"><div style="font-family:'Noto Sans TC';font-weight:700;font-size:500px;line-height:600px;width:600px;height:600px;text-align:center;color:#000">${ch}</div></body></html>`);
 await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(300);
 await p.screenshot({path:`${out}/${ch.codePointAt(0).toString(16)}.png`});}
await b.close();})();
