/* Optional authoring UI. Geometry uses percentages of the figure width. */
(() => {
  const frames=window.storyBubbleElements||[];
  if(!frames.length)return;
  const buddy=document.body.dataset.buddy,language=document.documentElement.lang;
  const key=`hugmap-bubbles:${buddy}:${language}:1`;
  const mode=()=>matchMedia('(max-width:600px)').matches?'mobile':'desktop';
  const fixedNode=document.getElementById('bubble-layout-defaults');
  const defaults=fixedNode?JSON.parse(fixedNode.textContent):{mobile:{},desktop:{}};
  const editing=new URLSearchParams(location.search).get('editBubbles')==='1';
  let saved=JSON.parse(JSON.stringify(defaults)),selected=null,active=false,panel;
  const ids=new Map(frames.map(el=>[el,`${el.closest('section').id}:${frames.filter(x=>x.closest('section')===el.closest('section')).indexOf(el)}`]));
  const announce=msg=>{if(panel)panel.querySelector('[role=status]').textContent=msg;};
  function persist(){try{localStorage.setItem(key,JSON.stringify(saved));announce('このブラウザに保存しました。');}catch{announce('保存できません。設定を書き出して保管してください。');}}
  try{const v=JSON.parse(localStorage.getItem(key));if((editing||!fixedNode)&&v?.mobile&&v?.desktop)saved={mobile:{...defaults.mobile,...v.mobile},desktop:{...defaults.desktop,...v.desktop}};}catch{}
  const originals=new Map(frames.map(el=>[el,el.getAttribute('style')]));
  function apply(el){
    const old=originals.get(el);if(old===null)el.removeAttribute('style');else el.setAttribute('style',old);
    const data=saved[mode()][ids.get(el)];if(!data)return;
    const fw=el.closest('figure').getBoundingClientRect().width;
    for(const [name,value] of Object.entries(data)){
      if(!Number.isFinite(value))continue;
      if(name==='w') {el.style.setProperty('width',fw*value/100+'px','important');el.style.setProperty('max-width','none','important');}
      if(name==='h') el.style.setProperty('height',fw*value/100+'px','important');
    }
    el.style.setProperty('translate',`${fw*(data.x||0)/100}px ${fw*(data.y||0)/100}px`,'important');
    el.style.setProperty('box-sizing','border-box','important');
    el.style.setProperty('align-content','center');
  }
  function redraw(){frames.forEach(apply);window.refreshStoryBubbles?.();if(selected&&panel)showValues();}
  const values=el=>{
    const fw=el.closest('figure').getBoundingClientRect().width,r=el.getBoundingClientRect();
    return {x:0,y:0,w:r.width/fw*100,h:r.height/fw*100,...saved[mode()][ids.get(el)]};
  };
  function showValues(){
    panel.querySelector('.be-selection').textContent=selected?selected.closest('section').querySelector('h2')?.textContent||ids.get(selected):'吹き出しを選んでください';
    const v=selected?values(selected):{};
    for(const n of ['x','y','w','h']){const input=panel.querySelector(`[name=${n}]`);input.disabled=!selected;if(document.activeElement!==input)input.value=selected?Math.round(v[n]*10)/10:'';}
    panel.querySelector('.be-mode').textContent=mode()==='mobile'?'スマートフォン用の配置':'PC用の配置';
  }
  function select(el){selected=el;frames.forEach(f=>f.classList.toggle('be-selected',f===el));showValues();}
  function change(data){saved[mode()][ids.get(selected)]={...saved[mode()][ids.get(selected)],...data};apply(selected);window.refreshStoryBubbles?.();showValues();}
  function toggle(on){active=on;document.body.classList.toggle('bubble-editing',on);panel.hidden=!on;document.querySelector('.be-open').hidden=on;if(!on)frames.forEach(f=>f.classList.remove('be-selected'));else if(selected)select(selected);}
  redraw();
  let scheduled=false;
  addEventListener('resize',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(()=>{scheduled=false;redraw();});}});
  if(new URLSearchParams(location.search).get('editBubbles')!=='1')return;
  const style=document.createElement('style');style.textContent=`
  .be-panel,.be-open{position:fixed;z-index:10000;background:#fffdf9;color:#584a41;border:1px solid #c6b8aa;box-shadow:0 5px 25px #38271a24;font:13px/1.5 system-ui,sans-serif;border-radius:14px}
  .be-panel{right:12px;bottom:12px;width:280px;padding:16px;max-height:48vh;overflow:auto}.be-panel[hidden],.be-open[hidden]{display:none}
  .be-panel h2{font:600 16px/1.4 system-ui;margin:0 0 6px}.be-panel p{margin:5px 0}.be-panel button,.be-open{font:inherit;cursor:pointer;padding:7px 10px;border:1px solid #c6b8aa;border-radius:8px;background:#fff;color:#584a41}.be-panel button:focus-visible,.be-panel input:focus-visible{outline:2px solid #a34d30;outline-offset:2px}
  .be-panel .be-inputs{display:grid;grid-template-columns:1fr 1fr;gap:6px}.be-panel label{display:flex;align-items:center;justify-content:space-between;gap:4px}.be-panel input[type=number]{width:68px;padding:5px;border:1px solid #c6b8aa;border-radius:5px;font:inherit}.be-panel .be-actions{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.be-panel.be-compact>:not(h2):not(.be-collapse){display:none!important}.be-panel .be-collapse{font-size:11px;padding:4px 8px;margin-bottom:6px}.be-panel small{display:block;color:#776659;font-size:11px}.be-selection{font-weight:600}.be-open{right:12px;bottom:12px}
  .bubble-editing figure>.bubble,.bubble-editing figure>.speech-bubble,.bubble-editing figure>.thought-bubble,.bubble-editing figure>.observation-thoughts{cursor:move;touch-action:none;user-select:none;outline:1px dashed #bc9d82;outline-offset:7px}
  .bubble-editing .be-selected{outline:2px dashed #a34d30!important;z-index:15!important}
  .be-resize{display:none!important}.bubble-editing .be-selected>.be-resize{display:block!important;position:absolute;right:-9px;bottom:-9px;width:18px;height:18px;border:2px solid white;border-radius:4px;background:#a34d30;cursor:nwse-resize;padding:0;touch-action:none;z-index:5}
  `;document.head.append(style);
  panel=document.createElement('aside');panel.className='be-panel';panel.setAttribute('aria-label','吹き出しの編集');panel.innerHTML=`<h2>吹き出しを調整</h2><button data-action="collapse" class="be-collapse">操作欄をたたむ</button><small class="be-mode"></small><p class="be-selection"></p><p>本体をドラッグで移動。右下の取っ手でサイズ変更。</p><div class="be-inputs"><label>横位置 <input name="x" type="number" step="1" min="-150" max="150"></label><label>縦位置 <input name="y" type="number" step="1" min="-150" max="150"></label><label>横幅 <input name="w" type="number" step="1" min="15" max="150"></label><label>縦幅 <input name="h" type="number" step="1" min="8" max="120"></label></div><small>数値は絵の横幅に対する％。位置は元の配置からの移動量です。</small><div class="be-actions"><button data-action="reset">選択を元に戻す</button><button data-action="export">設定を書き出す</button><button data-action="import">設定を読み込む</button><button data-action="preview">編集枠を隠す</button></div><input type="file" accept="application/json,.json" hidden><p role="status" aria-live="polite"></p><small>保存先はこのブラウザのみ。公開サイトへは未反映です。言語別・PC／スマートフォン別に保存します。</small>`;document.body.append(panel);
  const opener=document.createElement('button');opener.className='be-open';opener.textContent='吹き出しを編集';opener.onclick=()=>toggle(true);document.body.append(opener);
  for(const el of frames){
    const handle=document.createElement('button');handle.className='be-resize';handle.setAttribute('aria-label','吹き出しの大きさを変更');el.append(handle);
    el.addEventListener('pointerdown',e=>{
      if(!active||e.button>0)return;select(el);e.preventDefault();
      const resize=e.target===handle, start=values(el),fw=el.closest('figure').getBoundingClientRect().width,sx=e.clientX,sy=e.clientY;
      el.setPointerCapture(e.pointerId);
      const move=ev=>{const dx=(ev.clientX-sx)/fw*100,dy=(ev.clientY-sy)/fw*100;change(resize?{w:Math.max(15,Math.min(150,start.w+dx)),h:Math.max(8,Math.min(120,start.h+dy))}:{x:Math.max(-150,Math.min(150,start.x+dx)),y:Math.max(-150,Math.min(150,start.y+dy))});};
      const up=()=>{el.removeEventListener('pointermove',move);el.removeEventListener('pointerup',up);el.removeEventListener('pointercancel',up);persist();};
      el.addEventListener('pointermove',move);el.addEventListener('pointerup',up);el.addEventListener('pointercancel',up);
    });
  }
  panel.querySelectorAll('input[type=number]').forEach(input=>input.addEventListener('input',()=>{if(!selected||input.value==='')return;const n=Number(input.value);if(Number.isFinite(n)&&n>=Number(input.min)&&n<=Number(input.max)){change({[input.name]:n});persist();}}));
  panel.addEventListener('click',e=>{const action=e.target.dataset.action;if(action==='collapse'){const compact=panel.classList.toggle('be-compact');e.target.textContent=compact?'操作欄を開く':'操作欄をたたむ';}if(action==='reset'&&selected){const id=ids.get(selected),base=defaults[mode()][id];if(base)saved[mode()][id]={...base};else delete saved[mode()][id];redraw();persist();}if(action==='preview')toggle(false);if(action==='import')panel.querySelector('input[type=file]').click();if(action==='export'){
    const blob=new Blob([JSON.stringify({version:1,buddy,language,layouts:saved},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`${buddy}-${language}-bubble-layout.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);announce('設定を書き出しました。このファイルで配置を共有できます。');
  }});
  panel.querySelector('input[type=file]').addEventListener('change',async e=>{try{
    const file=e.target.files[0];if(!file)return;const data=JSON.parse(await file.text());
    if(data.version!==1||data.buddy!==buddy||data.language!==language)throw Error('違う絵本・言語の設定です。');
    const clean={mobile:{},desktop:{}};
    for(const m of ['mobile','desktop'])for(const [id,v] of Object.entries(data.layouts[m]||{})){
      if(![...ids.values()].includes(id))continue;clean[m][id]={};
      for(const n of ['x','y','w','h'])if(n in v){const value=v[n],min=n==='w'?15:n==='h'?8:-150,max=n==='h'?120:150;if(!Number.isFinite(value)||value<min||value>max)throw Error('設定の数値を確認してください。');clean[m][id][n]=value;}
    }
    saved=clean;redraw();persist();
  }catch(err){announce('読み込めませんでした。'+err.message);}e.target.value='';});
  toggle(true);showValues();
})();
