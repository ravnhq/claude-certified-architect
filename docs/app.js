(() => {
  const topbar = document.querySelector('.topbar');
  if (topbar && 'ResizeObserver' in window) {
    const setH = () => document.documentElement.style.setProperty('--topbar-h', `${topbar.offsetHeight}px`);
    setH();
    new ResizeObserver(setH).observe(topbar);
  }

  const themeToggle = document.getElementById('theme-toggle');
  const searchToggle = document.getElementById('search-toggle');
  const dialog = document.getElementById('search-dialog');
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  const filterButtons = document.querySelectorAll('.search-lang');

  // Theme toggle
  themeToggle?.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('theme', next);
  });

  // Search
  let mini = null;
  let searchLang = 'all';

  async function loadIndex() {
    if (mini) return mini;
    const res = await fetch('search-index.json');
    const data = await res.json();
    const ms = await import('https://cdn.jsdelivr.net/npm/minisearch@7/+esm');
    mini = ms.default.loadJSON(JSON.stringify(data), { fields: ['heading', 'body'], storeFields: ['heading', 'lang', 'url'] });
    return mini;
  }

  function runSearch() {
    if (!mini || !input) return;
    const q = input.value.trim();
    if (!q) { results.innerHTML = ''; return; }
    let hits = mini.search(q, { prefix: true, fuzzy: 0.2 });
    if (searchLang !== 'all') hits = hits.filter(h => h.lang === searchLang);
    hits = hits.slice(0, 20);
    results.innerHTML = hits.map(h =>
      `<li><a href="${h.url}"><span class="lang-tag">${h.lang}</span>${h.heading}</a></li>`
    ).join('') || '<li style="padding:8px 16px;color:var(--muted)">No results</li>';
  }

  searchToggle?.addEventListener('click', async () => {
    dialog.showModal();
    input.focus();
    await loadIndex();
  });
  dialog?.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });

  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      searchLang = btn.dataset.lang;
      filterButtons.forEach(b => b.classList.toggle('active', b === btn));
      runSearch();
    });
  });

  let timer;
  input?.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(runSearch, 80);
  });

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); searchToggle?.click(); }
    if (e.key === 'Escape' && dialog?.open) dialog.close();
  });
})();
