(() => {
  const langButtons = document.querySelectorAll('.lang-btn');
  const themeToggle = document.getElementById('theme-toggle');
  const searchToggle = document.getElementById('search-toggle');
  const dialog = document.getElementById('search-dialog');
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');

  // Lang switcher
  const stored = localStorage.getItem('lang');
  if (!stored) {
    const guess = (navigator.language || 'en').slice(0, 2);
    if (['en', 'es', 'pt'].includes(guess)) localStorage.setItem('lang', guess);
  }
  const currentLang = document.documentElement.lang || 'en';
  langButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.lang;
      localStorage.setItem('lang', target);
      const here = location.pathname;
      const map = [
        [/\/guides\/(en|es|pt)\.html/, `/guides/${target}.html`],
        [/\/practical\/(en|es|pt)\.html/, `/practical/${target}.html`],
      ];
      for (const [re, repl] of map) {
        if (re.test(here)) { location.href = here.replace(re, repl); return; }
      }
    });
  });

  // Theme toggle
  themeToggle?.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('theme', next);
  });

  // Search
  let mini = null;
  async function loadIndex() {
    if (mini) return mini;
    const res = await fetch('search-index.json');
    const data = await res.json();
    const ms = await import('https://cdn.jsdelivr.net/npm/minisearch@7/+esm');
    mini = ms.default.loadJSON(JSON.stringify(data), { fields: ['heading', 'body'], storeFields: ['heading', 'lang', 'url'] });
    return mini;
  }

  searchToggle?.addEventListener('click', async () => {
    dialog.showModal();
    input.focus();
    await loadIndex();
  });
  dialog?.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });

  let timer;
  input?.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (!mini) return;
      const lang = localStorage.getItem('lang') || currentLang;
      const hits = mini.search(input.value, { prefix: true, fuzzy: 0.2 })
        .filter(h => h.lang === lang).slice(0, 20);
      results.innerHTML = hits.map(h =>
        `<li><a href="${h.url}"><span class="lang-tag">${h.lang}</span>${h.heading}</a></li>`
      ).join('') || '<li style="padding:8px 16px;color:var(--muted)">No results</li>';
    }, 80);
  });

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); searchToggle?.click(); }
    if (e.key === 'Escape' && dialog?.open) dialog.close();
  });
})();
