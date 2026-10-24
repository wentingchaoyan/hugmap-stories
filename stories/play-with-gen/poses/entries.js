const filters = [...document.querySelectorAll('[data-filter]')];
const activities = [...document.querySelectorAll('[data-entries]')];
filters.forEach(button => button.addEventListener('click', () => {
  const selected = button.dataset.filter;
  filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  let count = 0;
  activities.forEach(card => {
    const show = selected === 'all' || card.dataset.entries.split(' ').includes(selected);
    card.hidden = !show;
    if (show) count++;
    const alternatives = card.querySelector('details');
    if (alternatives) alternatives.open = show && selected !== 'all' && !card.querySelector('.picture-entry').textContent.includes(button.textContent);
  });
  document.querySelector('#result-count').textContent = `${count}の遊び${selected === 'all' ? '' : ' · ' + button.textContent + 'の入口があるもの'}`;
}));
