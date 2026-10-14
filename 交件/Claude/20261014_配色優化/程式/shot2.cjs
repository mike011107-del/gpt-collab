const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1000,height:800},deviceScaleFactor:2});
for(const g of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/out/'+g+'_sheet.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.screenshot({path:'out/'+g+'_sheet.png',fullPage:true});console.log(g);}
await b.close();})();
