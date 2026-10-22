/* Remove only white paper connected to the image boundary at display time.
   Enclosed white figures remain opaque; original artwork files are unchanged. */
for (const img of document.querySelectorAll('.panel figure img')) {
  const prepare = () => {
    if (img.dataset.paperCutout) return;
    img.dataset.paperCutout = 'true';
    const canvas = document.createElement('canvas');
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const ctx = canvas.getContext('2d', {willReadFrequently:true});
    ctx.drawImage(img, 0, 0);
    const frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const {data} = frame;
    const w = canvas.width, h = canvas.height;
    const croppedChild = img.src.includes('mimo-voice-pingpong');
    const childEdge = new Int32Array(h).fill(-1);
    if (croppedChild) {
      for(let y=Math.floor(h*.24);y<h;y++) {
        for(let x=0;x<Math.floor(w*.49);x++) {
          const i=(y*w+x)*4;
          if(data[i]>180 && data[i]-data[i+1]>45 && data[i+1]-data[i+2]>10) childEdge[y]=x;
        }
      }
    }
    const seen = new Uint8Array(w*h);
    const queue = new Int32Array(w*h);
    let head = 0, tail = 0;
    const visit = (p) => {
      if (seen[p] || (croppedChild && p%w<=childEdge[Math.floor(p/w)])) return;
      seen[p] = 1;
      const i = p*4;
      const lo = Math.min(data[i],data[i+1],data[i+2]);
      const hi = Math.max(data[i],data[i+1],data[i+2]);
      if (data[i+3] < 8 || (lo > 224 && hi-lo < 24)) queue[tail++] = p;
    };
    // The close-up child is cropped at the left and lower edges.
    // Those edges are inside the silhouette, not exterior paper.
    for (let x=0;x<w;x++) {visit(x);if (!croppedChild || x>w*.5) visit((h-1)*w+x);}
    for (let y=0;y<h;y++) {if (!croppedChild) visit(y*w);visit(y*w+w-1);}
    while (head < tail) {
      const p = queue[head++];
      data[p*4+3] = 0;
      const x = p%w;
      if (x) visit(p-1);
      if (x<w-1) visit(p+1);
      if (p>=w) visit(p-w);
      if (p<w*(h-1)) visit(p+w);
    }
    ctx.putImageData(frame,0,0);
    img.src = canvas.toDataURL('image/png');
  };
  if (img.complete && img.naturalWidth) prepare();
  else img.addEventListener('load',prepare,{once:true});
}
