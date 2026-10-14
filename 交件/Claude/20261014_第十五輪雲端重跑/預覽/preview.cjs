// 用法：NODE_PATH=$(npm root -g) node 預覽/preview.cjs（需要 playwright 與 Chromium）
const { chromium } = require('playwright');
const { pathToFileURL } = require('url');
const path = require('path');
const here = __dirname;
(async () => {
const pages = [['原版', '../../20261014_全部成果同步/01_第十五輪配色/手機頁.html'], ['路徑修正版', '手機頁_路徑修正版.html']];
const browser = await chromium.launch({ executablePath: process.env.CHROME || undefined });
const out = {};
for (const [name, rel] of pages) {
  for (const w of [390, 1280]) {
    const p = await browser.newPage({ viewport: { width: w, height: 844 } });
    await p.goto(pathToFileURL(path.join(here, rel)).href, { waitUntil: 'load' });
    await p.evaluate(async () => { for (const i of document.images) { i.loading = 'eager'; } await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
    const r = await p.evaluate(() => ({
      組數: document.querySelectorAll('article.combo').length,
      圖片總數: document.images.length,
      載入失敗: [...document.images].filter(i => !i.naturalWidth).map(i => i.getAttribute('src')),
      水平捲動: document.documentElement.scrollWidth > window.innerWidth,
      頁寬: document.documentElement.scrollWidth,
    }));
    out[`${name}_${w}`] = r;
    if (w === 390) await p.screenshot({ path: path.join(here, `截圖_${name}_390.png`), fullPage: true });
    await p.close();
  }
}
await browser.close();
console.log(JSON.stringify(out, null, 1));
})().catch(e => { console.error(e); process.exit(1); });
