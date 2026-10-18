const { chromium } = require('playwright');
(async () => {
  const [,, html, pdf, pngdir] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 560, height: 794 }, deviceScaleFactor: 2 });
  const failed = [];
  p.on('requestfailed', r => failed.push(r.url()));
  await p.goto('file://' + html, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
    const inn = pg.querySelector('.inner'); return { i: i + 1, over: inn.scrollHeight - inn.clientHeight };
  }).filter(x => x.over > 1));
  console.log('overflow', JSON.stringify(over));
  console.log('failed', JSON.stringify(failed));
  await p.pdf({ path: pdf, width: '148mm', height: '210mm', printBackground: true, preferCSSPageSize: true });
  if (pngdir) {
    const n = await p.evaluate(() => document.querySelectorAll('.page').length);
    for (let i = 0; i < n; i++) {
      const el = (await p.$$('.page'))[i];
      await el.screenshot({ path: `${pngdir}/p${String(i + 1).padStart(2, '0')}.png` });
    }
  }
  await b.close();
})();
