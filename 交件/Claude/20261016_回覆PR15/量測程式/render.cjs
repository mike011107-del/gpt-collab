const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:736,height:200},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/name.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
for(const em of [0,0.025,0.055,0.14]){await p.evaluate(e=>{document.getElementById('t').style.letterSpacing=e+'em'},em);
 const f=await p.evaluate(()=>document.getElementById('t').getBoundingClientRect().width+' | '+document.fonts.check("700 80px 'Noto Sans TC'",'崧淳'));
 await p.screenshot({path:`k_${em}.png`});console.log(em,f);}
await b.close();})();
