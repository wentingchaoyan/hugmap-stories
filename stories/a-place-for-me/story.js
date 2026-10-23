const initialHash = location.hash;
let ready = false;
const panels = [...document.querySelectorAll('[data-step]')];
const storyPages = panels.filter(panel => panel.id !== 'cover' && panel.id !== 'afterword').length;
const fill = document.querySelector('#progressFill');
const count = document.querySelector('#progressCount');
const label = document.querySelector('#progressLabel');
let scheduled = false;
function updateProgress() {
  scheduled = false;
  if (!ready) return;
  const marker = Math.min(innerHeight * .45, 360);
  let current = panels[0];
  for (const panel of panels) if (panel.getBoundingClientRect().top <= marker) current = panel;
  const step = Number(current.dataset.step);
  fill.style.width = `${Math.min(step, storyPages) / storyPages * 100}%`;
  count.textContent = step > storyPages ? 'おわり' : `${step} / ${storyPages}`;
  label.textContent = step === 0 ? 'はじまり' : step > storyPages ? 'おはなしのあとに' : `${step}ページ`;

}
addEventListener('scroll', () => { if (!scheduled) {scheduled = true; requestAnimationFrame(updateProgress);} }, {passive:true});
addEventListener('resize', updateProgress);
addEventListener('load', () => {
  const target = document.getElementById(initialHash.slice(1));
  if (target && location.hash === initialHash) target.scrollIntoView({behavior:'instant'});
  ready = true;
  requestAnimationFrame(updateProgress);
});
document.querySelector('#textToggle').addEventListener('click', event => {
  const large = document.body.classList.toggle('large-text');
  event.currentTarget.setAttribute('aria-pressed', String(large));
  event.currentTarget.textContent = large ? '文字をもどす' : '文字を大きく';
});

// Hand-drawn frames remain independent from artwork and text.
const ns='http://www.w3.org/2000/svg';
function drawBubbles(){
 document.querySelectorAll('.bubble').forEach(el=>{
  const art=el.closest('.art'), img=art.querySelector('img');
  if(!img.complete||!img.naturalWidth)return;
  el.querySelector('svg')?.remove();
  const r=el.getBoundingClientRect(),ir=img.getBoundingClientRect();
  const w=r.width,h=r.height;
  const tx=ir.left+ir.width*Number(el.dataset.mouthX)/100-r.left;
  const ty=ir.top+ir.height*Number(el.dataset.mouthY)/100-r.top;
  const svg=document.createElementNS(ns,'svg');svg.setAttribute('aria-hidden','true');
  const start=Math.max(25,Math.min(w-25,tx));
  const dy=Math.max(1,ty-h), dx=tx-start;
  const scale=Math.min(1,28/Math.hypot(dx,dy));
  const endY=h+dy*scale,endX=start+dx*scale;
  const isThought=el.classList.contains('thought');
  const tail=isThought?'':` L ${endX} ${endY} L ${start-10} ${h-5}`;
  const path=document.createElementNS(ns,'path');
  path.setAttribute('d',`M ${w*.48} 3 C ${w*.76} 0 ${w-4} 7 ${w-3} ${h*.46} C ${w+1} ${h*.81} ${w*.83} ${h-2} ${start+10} ${h-5}${tail} C ${w*.30} ${h+1} 3 ${h-3} 3 ${h*.54} C 0 ${h*.17} ${w*.17} 1 ${w*.48} 3 Z`);
  path.setAttribute('fill','#fffdf9');path.setAttribute('stroke','#927660');path.setAttribute('stroke-width','1.7');path.setAttribute('stroke-linejoin','round');svg.append(path);
  if(isThought && !el.closest(".closeup")){for(let i=0;i<3;i++){let t=(i+1)/4;const c=document.createElementNS(ns,'circle');c.setAttribute('cx',start+(endX-start)*t);c.setAttribute('cy',h+7+(endY-h-7)*t);c.setAttribute('r',4-i);c.setAttribute('fill','#fffdf9');c.setAttribute('stroke','#927660');c.setAttribute('stroke-width','1');svg.append(c)}}
  el.prepend(svg);
 });
}
const bubbleResize=new ResizeObserver(drawBubbles);
document.querySelectorAll('.art').forEach(el=>{bubbleResize.observe(el);el.querySelector('img').addEventListener('load',drawBubbles)});
document.querySelector('#textToggle').addEventListener('click',()=>requestAnimationFrame(drawBubbles));
addEventListener('load',drawBubbles);
