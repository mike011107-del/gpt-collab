const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:1600}});
for(const n of process.argv.slice(3)){let s=fs.readFileSync(process.argv[2]+'/'+n+'.svg','utf8').replace(/<title>.*?<\/title>/,'').replace('<svg ','<svg style="width:1600px;height:1600px" fill="#000" ');
await p.setContent('<html><body style="margin:0;background:#fff">'+s+'</body></html>');await p.screenshot({path:'meas/'+n+'.png'});}
await b.close();})();
