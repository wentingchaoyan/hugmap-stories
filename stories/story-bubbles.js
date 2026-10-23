/* Hand-drawn frames; tails follow the speaker even when the art is letterboxed. */
(() => {
  const mouths = {
    mimo: {'scene-5':[.75,.60], 'scene-7':[.46,.42], 'scene-8':[.52,.42]},
    luke: {'scene-hello':[.53,.45], 'scene-eat-myself':[.42,.40], 'scene-grip':[.39,.53], 'scene-observe':[.42,.40], 'scene-ideas':[.37,.47], 'scene-one-bite':[.37,.43], 'scene-too-many':[.35,.43], 'scene-comfort':[.36,.43]},
    gen: {'scene-hello':[.81,.56], 'scene-stairs':[.31,.60], 'scene-observe':[.31,.60], 'scene-support':[.74,.52], 'scene-rest':[.68,.55]}
  };
  const ns='http://www.w3.org/2000/svg';
  const frames=[...document.querySelectorAll('figure > .bubble, figure > .speech-bubble, figure > .thought-bubble, figure > .observation-thoughts')];
  function paint(el,index) {
    const fig=el.closest('figure'), img=fig.querySelector('img');
    const b=el.getBoundingClientRect(), ir=img.getBoundingClientRect();
    if (!b.width || !ir.width || !img.naturalWidth) return;
    const scale=Math.min(ir.width/img.naturalWidth,ir.height/img.naturalHeight);
    const iw=img.naturalWidth*scale, ih=img.naturalHeight*scale;
    const pt=mouths[document.body.dataset.buddy]?.[fig.closest('section').id] || [.5,.4];
    const tx=ir.left+(ir.width-iw)/2+iw*pt[0]-b.left;
    const ty=ir.top+(ir.height-ih)/2+ih*pt[1]-b.top;
    const w=b.width,h=b.height,cx=w/2,cy=h/2,rx=w/2-2,ry=h/2-2;
    const theta=Math.atan2((ty-cy)/ry,(tx-cx)/rx);
    const ex=cx+rx*Math.cos(theta),ey=cy+ry*Math.sin(theta);
    const dist=Math.hypot(tx-ex,ty-ey)||1,ux=(tx-ex)/dist,uy=(ty-ey)/dist;
    const thought=el.classList.contains('thought')||el.classList.contains('thought-bubble')||el.classList.contains('observation-thoughts');
    let svg=el.querySelector(':scope > svg.story-bubble-frame');
    if(!svg){svg=document.createElementNS(ns,'svg');svg.classList.add('story-bubble-frame');svg.setAttribute('aria-hidden','true');el.prepend(svg);}
    svg.setAttribute('viewBox',`-38 -38 ${w+76} ${h+76}`);
    const points=[];
    // Begin just after the tail, traveling around the entire soft oval.
    const gap=thought?0:Math.min(.19,10/rx);
    for(let i=0;i<=72;i++){
      const a=theta+gap+(Math.PI*2-2*gap)*i/72;
      const wobble=1+.023*Math.sin(3*a+index)+.011*Math.cos(5*a+.7);
      points.push([cx+rx*Math.sign(Math.cos(a))*Math.abs(Math.cos(a))**.92*wobble,cy+ry*Math.sign(Math.sin(a))*Math.abs(Math.sin(a))**.92*wobble]);
    }
    if(!thought)points.push([ex+ux*Math.min(26,dist*.55),ey+uy*Math.min(26,dist*.55)]);
    const d=points.map((p,i)=>`${i?'L':'M'}${p[0].toFixed(2)},${p[1].toFixed(2)}`).join(' ')+' Z';
    const id='pencil-'+index;
    // Filled ribbon: a gently changing pen width, rather than a uniform SVG stroke.
    const edge=(side)=>points.map((p,i)=>{
      const prev=points[(i+points.length-1)%points.length], next=points[(i+1)%points.length];
      const dx=next[0]-prev[0],dy=next[1]-prev[1],len=Math.hypot(dx,dy)||1;
      const pen=1.15+.35*Math.sin(i*.21+index)+.16*Math.cos(i*.73);
      return [p[0]-dy/len*pen*side,p[1]+dx/len*pen*side];
    });
    const pathOf=ps=>ps.map((p,i)=>`${i?'L':'M'}${p[0].toFixed(2)},${p[1].toFixed(2)}`).join(' ')+' Z';
    const ribbon=pathOf(edge(1))+' '+pathOf(edge(-1).reverse());
    svg.innerHTML=`<defs><filter id="${id}" x="-15%" y="-25%" width="130%" height="150%"><feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="3" seed="${index+3}" result="grain"/><feDisplacementMap in="SourceGraphic" in2="grain" scale=".85" xChannelSelector="R" yChannelSelector="G"/></filter></defs><path d="${d}" fill="#fffdf9"/><path d="${ribbon}" fill="#705d51" fill-rule="evenodd" filter="url(#${id})"/>`;
    if(thought)for(const [offset,r] of [[10,4],[23,2.4]]){
      const dot=document.createElementNS(ns,'ellipse');dot.setAttribute('cx',ex+ux*offset);dot.setAttribute('cy',ey+uy*offset);dot.setAttribute('rx',r);dot.setAttribute('ry',r*.85);dot.setAttribute('fill','#fffdf9');dot.setAttribute('stroke','#705d51');dot.setAttribute('stroke-width','1.25');svg.append(dot);
    }
    el.dataset.tailTarget=`${tx.toFixed(1)},${ty.toFixed(1)}`;
  }
  const draw=()=>frames.forEach(paint);
  let pending=false;
  const schedule=()=>{if(!pending){pending=true;requestAnimationFrame(()=>{pending=false;draw();});}};
  const observer=new ResizeObserver(schedule);
  frames.forEach(el=>{observer.observe(el);observer.observe(el.closest('figure'));el.closest('figure').querySelector('img').addEventListener('load',schedule);});
  window.storyBubbleElements=frames;
  window.refreshStoryBubbles=draw;
  addEventListener('resize',schedule);addEventListener('load',schedule);document.fonts.ready.then(schedule);schedule();
})();
