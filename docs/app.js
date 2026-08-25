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
  const status = document.getElementById('search-status');
  const filterButtons = document.querySelectorAll('.search-lang');

  // Theme toggle
  themeToggle?.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    localStorage.setItem('theme', next);
  });

  // Search
  let mini = null;
  let indexPromise = null;
  let searchLang = 'all';

  async function loadIndex() {
    if (mini) return mini;
    if (!indexPromise) {
      indexPromise = (async () => {
        const res = await fetch('search-index.json');
        if (!res.ok) throw new Error(`Search index request failed: ${res.status}`);
        const data = await res.json();
        if (!window.MiniSearch) throw new Error('Search library did not load');
        mini = window.MiniSearch.loadJSON(JSON.stringify(data), {
          fields: ['heading', 'body'],
          storeFields: ['heading', 'lang', 'url'],
        });
        return mini;
      })().catch(error => {
        indexPromise = null;
        throw error;
      });
    }
    return indexPromise;
  }

  function runSearch() {
    if (!mini || !input) return;
    const q = input.value.trim();
    if (!q) {
      results.innerHTML = '';
      status.textContent = '';
      return;
    }
    let hits = mini.search(q, { prefix: true, fuzzy: 0.2 });
    if (searchLang !== 'all') hits = hits.filter(h => h.lang === searchLang);
    hits = hits.slice(0, 20);
    results.innerHTML = hits.map(h =>
      `<li><a href="${h.url}"><span class="lang-tag">${h.lang}</span>${h.heading}</a></li>`
    ).join('') || '<li style="padding:8px 16px;color:var(--muted)">No results</li>';
    status.textContent = hits.length === 1 ? '1 result' : `${hits.length} results`;
  }

  searchToggle?.addEventListener('click', async () => {
    dialog.showModal();
    input.focus();
    status.textContent = 'Loading search…';
    try {
      await loadIndex();
      status.textContent = '';
      runSearch();
    } catch (error) {
      results.innerHTML = '';
      status.textContent = 'Search could not be loaded. Try again.';
      console.error('Search failed to load', error);
    }
  });
  dialog?.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });

  filterButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      searchLang = btn.dataset.lang;
      filterButtons.forEach(b => {
        const selected = b === btn;
        b.classList.toggle('active', selected);
        b.setAttribute('aria-pressed', String(selected));
      });
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

  // Heading anchors: copy the section URL on click. Hash navigation still
  // happens, so the address bar matches what was copied.
  document.addEventListener('click', (e) => {
    const anchor = e.target.closest?.('.heading-anchor');
    if (!anchor || !navigator.clipboard) return;
    // anchor.href is resolved against the page's <base href>
    navigator.clipboard.writeText(anchor.href).then(() => {
      anchor.classList.add('copied');
      setTimeout(() => anchor.classList.remove('copied'), 1200);
    }).catch(() => {});
  });
})();
