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
