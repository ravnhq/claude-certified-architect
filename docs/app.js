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
        // loadJSON takes the raw text: res.json() would parse the 531 KB index
        // only for it to be re-serialized and parsed a second time here.
        const raw = await res.text();
        if (!window.MiniSearch) throw new Error('Search library did not load');
        mini = window.MiniSearch.loadJSON(raw, {
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

  // Guide TOC: open by default when it floats beside the prose (wide
  // viewports), collapsed inline otherwise; highlight the section in view.
  const toc = document.querySelector('.guide-toc');
  if (toc) {
    const wide = matchMedia('(min-width: 1160px)');
    const syncOpen = () => { toc.open = wide.matches; };
    syncOpen();
    wide.addEventListener('change', syncOpen);

    const links = new Map();
    toc.querySelectorAll('a[href*="#"]').forEach(a => {
      const id = decodeURIComponent(a.hash.slice(1));
      if (id) links.set(id, a);
    });
    const headings = [...links.keys()].map(id => document.getElementById(id)).filter(Boolean);
    let active = null;
    const setActive = id => {
      if (id === active) return;
      links.get(active)?.classList.remove('active');
      active = id;
      const link = links.get(id);
      link?.classList.add('active');
      if (link && toc.open) link.scrollIntoView({ block: 'nearest' });
    };
    // Measuring 267 headings on every scroll tick forced a full synchronous
    // layout each time. The heading offsets only move when the page reflows, so
    // they are cached and the hot path does a binary search over them — one
    // cheap scrollY read per frame and no layout at all.
    //
    // An IntersectionObserver was the other candidate and is wrong here: a
    // heading that crosses the line between two frames (an anchor jump, a
    // restored scroll position, a fast fling) is non-intersecting before and
    // after, so no entry is ever delivered for it and the TOC sticks.
    if (headings.length) {
      let offsets = [];
      let line = 80;
      const measure = () => {
        line = (parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 80) + 8;
        const top = scrollY;
        offsets = headings.map(h => h.getBoundingClientRect().top + top);
      };
      const update = () => {
        // The last heading at or above the line; index 0 before any has passed.
        const y = scrollY + line;
        let lo = 0;
        let hi = offsets.length - 1;
        let found = 0;
        while (lo <= hi) {
          const mid = (lo + hi) >> 1;
          if (offsets[mid] <= y) { found = mid; lo = mid + 1; } else hi = mid - 1;
        }
        setActive(headings[found].id);
      };
      let queued = false;
      const onScroll = () => {
        if (queued) return;
        queued = true;
        requestAnimationFrame(() => { queued = false; update(); });
      };
      measure();
      update();
      addEventListener('scroll', onScroll, { passive: true });
      // Anything that reflows the prose moves the offsets: a resize, the web
      // fonts swapping in, a <details> in the guide opening. The observer fires
      // after layout, so re-measuring there costs nothing extra.
      if ('ResizeObserver' in window) {
        const body = document.querySelector('.guide-body') || document.body;
        let first = true;
        new ResizeObserver(() => {
          if (first) { first = false; return; }
          measure();
          update();
        }).observe(body);
      } else {
        addEventListener('resize', () => { measure(); update(); });
      }
    }
  }

  // Warm an exam's question bank before the click. The landing page and the
  // score report each link into three different exams, so a static prefetch
  // would pull megabytes for two banks the visitor will not open; hovering or
  // tab-focusing one link names which bank to fetch. The guide pages, which
  // have exactly one matching exam, carry a plain <link rel=prefetch> instead.
  const bankMap = (() => {
    try { return JSON.parse(document.getElementById('bank-map')?.textContent || '{}'); }
    catch { return {}; }
  })();
  const warmed = new Set();
  const warmBank = e => {
    const a = e.target.closest?.('a[href]');
    if (!a) return;
    // Match on the shell's own key space (base-relative "practical/en.html"),
    // which is how the map is written.
    const href = a.getAttribute('href')?.split(/[?#]/)[0];
    const bank = href && bankMap[href];
    if (!bank || warmed.has(bank)) return;
    warmed.add(bank);
    const link = document.createElement('link');
    link.rel = 'prefetch';
    link.as = 'fetch';
    // No crossorigin: the engine's fetch() is same-origin with credentials, and
    // an anonymous prefetch would sit under a different cache key and be redone.
    link.href = bank;
    document.head.appendChild(link);
  };
  if (Object.keys(bankMap).length) {
    document.addEventListener('pointerenter', warmBank, { capture: true, passive: true });
    document.addEventListener('focusin', warmBank, { passive: true });
  }

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
