const { chromium } = require('playwright');
(async () => {
  const [,, html, pdf, pngdir] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 1.5 });
  const failed = [];
  p.on('requestfailed', r => failed.push(r.url()));
  await p.goto('file://' + html, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
    const inn = pg.querySelector('.inner'); if (!inn) return {i:i+1,over:0}; return { i: i + 1, over: inn.scrollHeight - inn.clientHeight };
  }).filter(x => x.over > 1));
  const broken = await p.evaluate(() => [...document.images].filter(im => !im.complete || im.naturalWidth === 0).map(im => im.src));
  console.log('overflow', JSON.stringify(over)); console.log('failed', JSON.stringify(failed)); console.log('broken', JSON.stringify(broken));
  const fonts = await p.evaluate(() => [...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family));
  console.log('fonts', JSON.stringify([...new Set(fonts)]));
  await p.pdf({ path: pdf, width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
  if (pngdir) {
    const els = await p.$$('.page');
    for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: `${pngdir}/p${String(i + 1).padStart(2, '0')}.png` });
  }
  await b.close();
})();
