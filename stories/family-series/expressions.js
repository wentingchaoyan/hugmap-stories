// Place the frame in reserved space; its tail points toward the speaker in the image.
(() => {
 const ns='http://www.w3.org/2000/svg';
 function draw(el){
  const img=el.closest('figure').querySelector('img');
  if(!img.complete||!img.naturalWidth)return;
  const r=el.getBoundingClientRect(),ir=img.getBoundingClientRect(),w=r.width,h=r.height;
  if(!w||!h)return;
  el.querySelector('svg')?.remove();
  const svg=document.createElementNS(ns,'svg');svg.setAttribute('viewBox',`0 0 ${w} ${h}`);svg.setAttribute('aria-hidden','true');
  const tx=ir.left+ir.width*Number(el.dataset.x)/100-r.left;
  const ty=ir.top+ir.height*Number(el.dataset.y)/100-r.top;
  const start=Math.max(30,Math.min(w-30,w*.55));
  const dx=tx-start,dy=ty-(h-5),scale=Math.min(1,30/Math.hypot(dx,dy));
  const ex=start+dx*scale,ey=h-5+dy*scale;
  const thought=el.classList.contains('thought');
  const noTail=el.dataset.tail==='none';
  const tail=(thought||noTail)?'':` L ${ex} ${ey} L ${start-9} ${h-6}`;
  const path=document.createElementNS(ns,'path');
  path.setAttribute('d',`M ${w*.45} 4 C ${w*.72} 1 ${w-6} 9 ${w-4} ${h*.46} C ${w+1} ${h*.77} ${w*.85} ${h-2} ${start+9} ${h-6}${tail} C ${w*.28} ${h+1} 5 ${h-4} 4 ${h*.55} C 0 ${h*.22} ${w*.15} 1 ${w*.45} 4 Z`);
  svg.append(path);
  if(thought&&!noTail){for(let i=1;i<=3;i++){const t=i/3,c=document.createElementNS(ns,'circle');c.setAttribute('cx',start+(ex-start)*t);c.setAttribute('cy',h+3+(ey-h+6)*t);c.setAttribute('r',4.2-i*.8);svg.append(c);}}
  el.prepend(svg);
 }
 const all=[...document.querySelectorAll('.expression')];
 const refresh=()=>all.forEach(draw);
 const observer=new ResizeObserver(refresh);
 all.forEach(el=>{observer.observe(el);const img=el.closest('figure').querySelector('img');observer.observe(img);img.addEventListener('load',refresh);});
 document.fonts?.ready.then(refresh);addEventListener('load',refresh);refresh();
})();
