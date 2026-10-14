const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:930},deviceScaleFactor:2});
for(const g of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/out/'+g+'_docs.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
await p.screenshot({path:'out/'+g+'_docs.png'});console.log(g);}
await b.close();})();
