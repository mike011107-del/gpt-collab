// 用 Playwright 畫車門貼紙（透明底），字體 LXGW WenKai TC 由 Google Fonts 載入
const { chromium } = require('playwright');
const OUT=process.argv[2];
const H=`<link href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@700&display=block" rel="stylesheet">
<style>html,body{margin:0;background:transparent}.k{font-family:'LXGW WenKai TC';font-weight:700;line-height:1}
.box{display:inline-flex;align-items:center;justify-content:center;width:240px;height:240px}
.g{position:relative;display:inline-block;font-size:200px}.g .a{position:absolute;left:0;top:0;clip-path:inset(47% 0 0 47%)}</style>`;
const D={
 d1a:`<div class="box" style="background:#395848"><span class="g k" style="color:#fff">崧<span class="a" style="color:#FACA30">崧</span></span></div>`,
 d1b:`<div class="box" style="background:#B8283A;border-radius:10px;box-shadow:inset 0 0 0 10px #B8283A,inset 0 0 0 16px #F6F1E6"><div class="k" style="color:#F6F1E6;font-size:96px;display:flex;flex-direction:column;align-items:center;gap:4px"><span>崧</span><span>淳</span></div></div>`,
};
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:260,height:260},deviceScaleFactor:1});
for (const [k,v] of Object.entries(D)){
 await p.setContent(H+v,{waitUntil:'networkidle'}); await p.evaluate(()=>document.fonts.ready);
 const el=await p.$('.box'); await el.screenshot({path:`${OUT}/${k}_decal.png`,omitBackground:true}); console.log(k);
}
await b.close();})();
