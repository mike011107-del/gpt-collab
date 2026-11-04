const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({deviceScaleFactor:1});
const dir=process.argv[2];
for(const f of fs.readdirSync(dir).filter(x=>x.endsWith('.svg'))){
 const s=parseInt(f.match(/_(\d+)\.svg/)[1]);
 await p.setViewportSize({width:s,height:s});
 await p.setContent('<html><body style="margin:0">'+fs.readFileSync(path.join(dir,f),'utf8')+'</body></html>');
 await p.screenshot({path:path.join(dir,f.replace('.svg','.png'))});}
await b.close();})();
