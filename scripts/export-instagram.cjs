// Run with Playwright available in NODE_PATH. Exports only the Japanese carousel assets.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'assets/marketing/instagram');
const css = `
*{box-sizing:border-box}html,body{margin:0!important;padding:0!important;scroll-behavior:auto!important}body.webtoon{background:#fffdf9!important}
.story-header,.progress,.next,.cover-arrow,.end-links,.sources,.colophon,.webtoon .eyebrow{display:none!important}
.webtoon main{width:540px!important;max-width:none!important;overflow:hidden!important}
.webtoon main>section{display:none!important}
.webtoon main>section.export-slide{display:flex!important;position:relative!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;width:540px!important;height:675px!important;min-height:675px!important;padding:56px 38px 40px!important;gap:15px!important;overflow:hidden!important;transform:none!important;opacity:1!important}
.webtoon .copy,.webtoon .story-beat{width:100%!important;max-width:460px!important;padding:0!important;margin:0!important;flex-shrink:0!important}
.webtoon h1{font-size:38px!important;line-height:1.35!important;margin:0!important}.webtoon h2{font-size:25px!important;line-height:1.45!important;margin:0!important}
.webtoon .story-text{font-size:16px!important;line-height:1.8!important;margin:12px 0 0!important}.webtoon .story-beat .story-text{margin:0!important}
.webtoon .cover .buddy-role{font-size:15px!important;line-height:1.7!important;margin:14px 0 0!important}
.webtoon .panel figure{width:100%!important;max-width:420px!important;margin:0!important;flex:0 0 auto!important;min-height:0!important}
.webtoon .panel figure img{display:block!important;width:100%!important;height:260px!important;max-height:260px!important;object-fit:contain!important;margin:0 auto!important}
.webtoon .cover figure img{height:330px!important;max-height:330px!important}
.webtoon .panel figure.bubble-art{gap:17px 12px!important}
.webtoon .bubble-art .bubble,.webtoon .bubble-art .speech-bubble,.webtoon .bubble-art .thought-bubble{font-size:12px!important;line-height:1.5!important;padding:7px 12px!important;max-width:195px!important}
.webtoon .panel .bubble-art .observation-thoughts{padding:9px 12px!important;gap:5px!important;max-width:195px!important}
.webtoon .observation-thoughts .bubble{padding:0!important}
.webtoon .afterword h2{font-size:27px!important;line-height:1.7!important}.webtoon .afterword>p:not(.eyebrow){font-size:18px!important;line-height:2!important;margin:16px 0!important}
.webtoon[data-buddy="gen"] .panel figure.bubble-art{display:grid!important;grid-template-columns:1fr 1fr!important;gap:18px 10px!important}
.webtoon[data-buddy="gen"] .panel .bubble-art>.bubble,.webtoon[data-buddy="gen"] .panel .bubble-art .observation-thoughts{position:relative!important;inset:auto!important;transform:none!important;grid-row:1!important;width:100%!important;align-self:end!important}
.webtoon[data-buddy="gen"] .panel .bubble-art>img{grid-row:2!important;grid-column:1 / -1!important}
.export-header{position:absolute;top:23px;left:38px;right:38px;height:16px;display:flex;justify-content:space-between;align-items:center;font:10px/16px Arial,sans-serif;letter-spacing:.12em;color:#927d6f}
.export-number{font-variant-numeric:tabular-nums;letter-spacing:.08em}
`;
const closing = {
 mimo:['ことばになる前の「伝えたい」も、<br>いっしょに。','声も、視線も、しぐさも。<br>その子の気持ちに出会う入り口です。','今日の小さなやりとりを、<br>いっしょに楽しんでいこう。'],
 luke:['きみの「やってみたい」を、<br>いっしょに。','道具や環境を、少し工夫して。<br>その子に合う方法を探します。','「できた！」のうれしさを、<br>いっしょに分かち合おう。'],
 gen:['その子の「行きたい」を、<br>いっしょに。','支えを借りても、途中で休んでも。<br>その子に合う方法を探します。','「今日は、ここまで来られたね」。<br>そんな喜びを、いっしょに。']
};
(async()=>{
const server=http.createServer((req,res)=>{const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}try{res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.png':'image/png','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
let browser;try{
browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:540,height:675},deviceScaleFactor:2});
let count=0;
for(const buddy of ['mimo','luke','gen']){
 const dir=path.join(output,buddy);fs.mkdirSync(dir,{recursive:true});
 await page.goto(`http://127.0.0.1:${server.address().port}/stories/hello-${buddy}/index.html`,{waitUntil:'networkidle'});
 await page.evaluate(async()=>{for(const img of document.images){img.loading='eager';await img.decode().catch(()=>{});}await document.fonts.ready;});await page.waitForTimeout(2000);
 await page.addStyleTag({content:css});
 await page.evaluate(c=>{document.querySelector('.afterword').innerHTML=`<h2>${c[0]}</h2><p>${c[1]}</p><p>${c[2]}</p>`;},closing[buddy]);
 const ids=await page.locator('main>section').evaluateAll(es=>es.map(e=>e.id));
 for(let i=0;i<ids.length;i++){
  const result=await page.evaluate(({id,i,n,buddy})=>{
   document.querySelectorAll('.export-slide').forEach(e=>e.classList.remove('export-slide'));
   const e=document.getElementById(id);e.classList.add('export-slide');
   const header=document.createElement('div');header.className='export-header';header.innerHTML=`<span>HUGMAP STORIES · ${buddy.toUpperCase()}</span><span class="export-number">${String(i+1).padStart(2,'0')} / ${String(n).padStart(2,'0')}</span>`;e.append(header);
   const fig=e.querySelector('figure');if(fig){const img=fig.querySelector('img');const parts=[...e.children].filter(n=>!n.classList.contains('export-header')&&getComputedStyle(n).display!=='none');const total=parts.reduce((v,n)=>v+n.getBoundingClientRect().height,0)+(parts.length-1)*15+96;const reduction=Math.max(0,total-675);if(reduction){const h=Math.max(130,img.getBoundingClientRect().height-reduction-8);img.style.setProperty('height',h+'px','important');img.style.setProperty('max-height',h+'px','important');}}
   window.scrollTo(0,0);const number=header.querySelector('.export-number').getBoundingClientRect();
   const parts=[...e.children].filter(n=>n!==header&&getComputedStyle(n).display!=='none');
   return {numberTop:number.top,numberRight:number.right,overflow:e.scrollHeight>e.clientHeight,contentBottom:Math.max(...parts.map(n=>n.getBoundingClientRect().bottom))};
  },{id:ids[i],i,n:ids.length,buddy});
  if(result.numberTop!==23||result.numberRight!==502||result.overflow||result.contentBottom>650)throw new Error(JSON.stringify({buddy,id:ids[i],...result}));
  await page.screenshot({path:path.join(dir,`${String(i+1).padStart(2,'0')}-${ids[i]}.png`)});count++;
 }
 console.log(`${buddy}: ${ids.length} pages, fixed header positions verified`);
}
console.log(`Exported ${count} images at 1080x1350.`);
}finally{await browser?.close();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
