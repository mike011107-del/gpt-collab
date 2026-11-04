const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+process.argv[2],{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
await p.pdf({path:process.argv[3],format:'A5',printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="width:100%;text-align:center;font-size:7px;color:#888"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',margin:{top:'13mm',bottom:'15mm',left:'12mm',right:'12mm'}});
await b.close();})();
