/* Match paper to the scene; optional watercolor mode removes only neutral
   paper connected to the outside. Enclosed figures and coloured scenery remain. */
(() => {
  const cache = new Map();
  for (const img of document.querySelectorAll('img[data-paper-edge]')) {
    const prepare = () => {
      if (img.dataset.paperEdgeReady) return;
      img.dataset.paperEdgeReady = 'true';
      try {
        let parent = img.parentElement;
        let background = 'rgb(255, 253, 249)';
        while (parent) {
          const color = getComputedStyle(parent).backgroundColor;
          if (color !== 'transparent' && color !== 'rgba(0, 0, 0, 0)') {background = color; break;}
          parent = parent.parentElement;
        }
        const rgb = background.match(/[\d.]+/g).slice(0, 3).map(Number);
        const width = Math.min(.16, Number(img.dataset.paperEdge) || .05);
        const key = `${img.currentSrc}|${background}|${width}|${img.hasAttribute('data-paper-clean')}|${img.hasAttribute('data-paper-wash')}`;
        if (cache.has(key)) {img.src = cache.get(key); return;}
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        const ctx = canvas.getContext('2d', {willReadFrequently:true});
        ctx.drawImage(img,0,0);
        const frame = ctx.getImageData(0,0,canvas.width,canvas.height);
        const pixels = frame.data, w = canvas.width, h = canvas.height;
        // Remove the connected neutral paper texture, not enclosed white figures.
        // Warm floor/grass and coloured outlines are excluded from this region.
        if (img.hasAttribute('data-paper-clean')) {
          const seen = new Uint8Array(w*h), queue = new Int32Array(w*h);
          let head=0, tail=0;
          const visit = (p) => {
            if (seen[p]) return;
            seen[p]=1;
            const i=p*4, lo=Math.min(pixels[i],pixels[i+1],pixels[i+2]);
            const hi=Math.max(pixels[i],pixels[i+1],pixels[i+2]);
            if (lo<225 || hi-lo>15) return;
            queue[tail++]=p;
          };
          for(let x=0;x<w;x++){visit(x);visit((h-1)*w+x);}
          for(let y=0;y<h;y++){visit(y*w);visit(y*w+w-1);}
          while(head<tail){
            const p=queue[head++], x=p%w, y=Math.floor(p/w);
            if(x>0)visit(p-1);if(x<w-1)visit(p+1);
            if(y>0)visit(p-w);if(y<h-1)visit(p+w);
          }
          for(let q=0;q<tail;q++){
            const i=queue[q]*4;
            const lo=Math.min(pixels[i],pixels[i+1],pixels[i+2]);
            const hi=Math.max(pixels[i],pixels[i+1],pixels[i+2]);
            const t=Math.max(0,Math.min(1,(lo-225)/18));
            const neutral=1-Math.max(0,hi-lo-6)/9;
            const amount=t*t*(3-2*t)*neutral;
            if (img.hasAttribute('data-paper-wash')) {
              pixels[i+3]=Math.round(pixels[i+3]*(1-amount));
            } else {
              for(let c=0;c<3;c++) pixels[i+c]=Math.round(pixels[i+c]*(1-amount)+rgb[c]*amount);
            }
          }
        }
        for (let y=0;y<h;y++) {
          for (let x=0;x<w;x++) {
            const distance = Math.min(x/(w-1),1-x/(w-1),y/(h-1),1-y/(h-1));
            if (distance >= width) continue;
            const t = distance/width;
            const keep = t*t*(3-2*t);
            const i = (y*w+x)*4;
            for (let c=0;c<3;c++) pixels[i+c] = Math.round(rgb[c]*(1-keep)+pixels[i+c]*keep);
            // The edge pass preserves alpha; only connected paper was removed above.
          }
        }
        ctx.putImageData(frame,0,0);
        const result = canvas.toDataURL('image/png');
        cache.set(key,result);
        img.src = result;
      } catch (error) {
        // Keep the original artwork if canvas processing is unavailable.
        console.warn('Paper edge blending skipped:',error);
      }
    };
    if (img.complete && img.naturalWidth) prepare();
    else img.addEventListener('load',prepare,{once:true});
  }
})();
