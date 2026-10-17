// Render SVG files into a sprite grid PNG via headless Chromium canvas.
// usage: node sprite.cjs listfile out.png cell
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [list, out, cellS='128'] = process.argv.slice(2);
  const files = fs.readFileSync(list,'utf8').trim().split('\n');
  const cell = +cellS, cols = Math.ceil(Math.sqrt(files.length));
  const svgs = files.map(f => fs.readFileSync(f,'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent('<html><body></body></html>');
  const data = await page.evaluate(async ({svgs, cell, cols}) => {
    const rows = Math.ceil(svgs.length/cols);
    const c = document.createElement('canvas'); c.width = cols*cell; c.height = rows*cell;
    const g = c.getContext('2d'); g.fillStyle='#fff'; g.fillRect(0,0,c.width,c.height);
    for (let i=0;i<svgs.length;i++){
      let s = svgs[i];
      if (!/width=/.test(s.slice(0,300))) s = s.replace('<svg', `<svg width="${cell}" height="${cell}"`);
      const img = new Image();
      img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(s)));
      try { await img.decode(); } catch(e) { continue; }
      // fit into cell preserving aspect
      const w = img.naturalWidth||cell, h = img.naturalHeight||cell, k = Math.min(cell/w, cell/h);
      const dw=w*k, dh=h*k;
      g.drawImage(img, (i%cols)*cell+(cell-dw)/2, Math.floor(i/cols)*cell+(cell-dh)/2, dw, dh);
    }
    return c.toDataURL('image/png');
  }, {svgs, cell, cols});
  fs.writeFileSync(out, Buffer.from(data.split(',')[1], 'base64'));
  await browser.close();
  console.log(JSON.stringify({n: files.length, cols}));
})().catch(e=>{console.error(e);process.exit(1)});
