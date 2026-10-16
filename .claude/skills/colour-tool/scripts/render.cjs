// 把本機 HTML 或 SVG 算成 PNG，供 Read 工具實際看圖。
// 用法：NODE_PATH=$(npm root -g) node render.cjs 輸入.html|輸入.svg 輸出.png [寬px=1200] [裝置像素比=1]
// 限制：只開本機檔；頁面若要載入外部網址（字型、圖片），在擋網路的環境會失敗，結果要看 stderr 的失敗清單。
const { chromium } = require('playwright');
const path = require('path');
const { pathToFileURL } = require('url');
(async () => {
  const [src, out, w = '1200', dpr = '1'] = process.argv.slice(2);
  if (!src || !out) { console.error('用法：node render.cjs 輸入 輸出.png [寬] [DPR]'); process.exit(2); }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: 800 }, deviceScaleFactor: +dpr });
  const failed = [];
  page.on('requestfailed', r => failed.push(r.url()));
  const url = pathToFileURL(path.resolve(src)).href;
  const isSvg = src.toLowerCase().endsWith('.svg');
  if (isSvg) {
    // SVG 直接當文件開，fullPage 截圖會卡住；把 SVG 內容嵌進頁面，只截 SVG 本身
    const svg = require('fs').readFileSync(src, 'utf8');
    await page.setContent(`<html><body style="margin:0">${svg}</body></html>`, { waitUntil: 'load', timeout: 30000 });
  } else {
    await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  }
  await page.waitForTimeout(300);
  if (isSvg) await page.locator('svg').first().screenshot({ path: out, timeout: 30000 });
  else await page.screenshot({ path: out, fullPage: true, timeout: 30000 });
  const size = await page.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.scrollHeight]);
  await browser.close();
  console.log(JSON.stringify({ 輸出: out, 頁面尺寸: size, 載入失敗: failed }));
  process.exit(failed.length ? 3 : 0);
})().catch(e => { console.error(String(e)); process.exit(1); });
