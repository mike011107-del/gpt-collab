// 把 fig_vattenfall_scales_v3.html 轉 PNG。視窗高設小，fullPage 截圖就只截內容高度（不補白到 800px）。
// 用法：NODE_PATH=$(npm root -g) node render_scales_v3.cjs 輸入.html 輸出.png [寬=900] [DPR=1]
const { chromium } = require('playwright');
const path = require('path');
const { pathToFileURL } = require('url');
(async () => {
  const [src, out, w = '900', dpr = '1'] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: 50 }, deviceScaleFactor: +dpr });
  const failed = [];
  page.on('requestfailed', r => failed.push(r.url()));
  await page.goto(pathToFileURL(path.resolve(src)).href, { waitUntil: 'load', timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.screenshot({ path: out, fullPage: true, timeout: 30000 });
  const info = await page.evaluate(() => ({
    size: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
    fonts: [...new Set([...document.querySelectorAll('h4,.s')].map(e => getComputedStyle(e).fontSize))],
    overflow: [...document.querySelectorAll('.s,h4')].filter(e => e.scrollWidth > e.clientWidth || e.scrollHeight > e.clientHeight).map(e => e.textContent),
  }));
  await browser.close();
  console.log(JSON.stringify({ out, ...info, failed }));
  process.exit(failed.length ? 3 : 0);
})().catch(e => { console.error(String(e)); process.exit(1); });
