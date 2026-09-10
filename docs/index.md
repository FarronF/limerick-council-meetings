<header style="margin-bottom: 1.5rem;">
  <h1 style="margin-bottom: 0.5rem; font-size: 2rem;">Limerick Council Meetings Archive</h1>
  <p style="font-size: 1.05rem; line-height: 1.5; opacity: 0.9; margin: 0;">
    Search text and records from all publicly available Limerick City and County Council agendas, minutes, and documents across multiple years.
  </p>
</header>

<style>
  .pf-container {
    display: flex;
    gap: 1.5rem;
    margin-top: 1.5rem;
  }
  
  .pf-sidebar {
    width: 280px;
    flex-shrink: 0;
    font-size: 0.88rem;
  }

  /* Material Details / Accordion Base Styling */
  .pf-sidebar details {
    border: 1px solid var(--md-default-fg-color--lightest, #e0e0e0);
    border-radius: 4px;
    margin-bottom: 0.75rem;
    background: var(--md-default-bg-color, #fff);
    overflow: hidden;
  }

  .pf-sidebar summary {
    font-weight: 600;
    padding: 0.75rem 1rem;
    cursor: pointer;
    user-select: none;
    background: var(--md-code-bg-color, rgba(0,0,0,0.02));
    color: var(--md-default-fg-color, #333);
    transition: background 0.2s, color 0.2s;
  }

  .pf-sidebar summary:hover {
    background: var(--md-accent-fg-color--transparent, rgba(0,0,0,0.05));
  }

  .pf-sidebar details[open] > summary {
    border-bottom: 1px solid var(--md-default-fg-color--lightest, #eee);
  }

  /* Main Filter Shell Accordion Toggle - Hidden on Desktop */
  .pf-main-filter-wrapper > summary {
    display: none;
  }

  .pf-filter-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0.2rem 0.75rem 0.2rem;
  }

  .pf-filter-list {
    max-height: 220px;
    overflow-y: auto;
    padding: 0.5rem 0.85rem;
  }

  .pf-option {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
    margin: 0.4rem 0;
    cursor: pointer;
    line-height: 1.3;
  }

  .pf-count {
    opacity: 0.65;
    font-size: 0.8em;
    margin-left: auto;
  }

  .pf-main {
    flex-grow: 1;
    min-width: 0;
  }

  .pf-search-box {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border: 1px solid var(--md-default-fg-color--lightest, #ccc);
    border-radius: 4px;
    margin-bottom: 1rem;
    background: var(--md-default-bg-color, #fff);
    color: var(--md-default-fg-color, #000);
    box-shadow: var(--md-shadow-z1, 0 1px 3px rgba(0,0,0,0.12));
  }

  .pf-meta-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    font-size: 0.9rem;
  }

  .pf-clear-btn {
    background: none;
    border: none;
    color: var(--md-typeset-a-color, #0056b3);
    cursor: pointer;
    text-decoration: underline;
    padding: 0;
    font-size: 0.85rem;
  }

  .pf-result-card {
    padding: 1.2rem;
    border: 1px solid var(--md-default-fg-color--lightest, #e0e0e0);
    border-radius: 4px;
    margin-bottom: 1rem;
    background: var(--md-default-bg-color, #fff);
    box-shadow: var(--md-shadow-z1, 0 1px 2px rgba(0,0,0,0.05));
  }

  .pf-result-card h3 {
    margin: 0 0 0.4rem 0;
    font-size: 1.1rem;
  }

  .pf-result-card mark {
    background-color: var(--md-accent-fg-color--transparent, rgba(255, 235, 59, 0.4));
    font-weight: bold;
    padding: 0 2px;
  }

  .pf-load-more {
    display: block;
    width: 100%;
    padding: 0.75rem;
    margin-top: 1rem;
    background: var(--md-primary-fg-color, #205493);
    color: var(--md-primary-bg-color, #fff);
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-align: center;
    font-weight: 600;
  }

  /* --- MOBILE RESPONSIVE BEHAVIOR (<= 768px) --- */
  @media screen and (max-width: 768px) {
    .pf-container {
      flex-direction: column;
    }
    .pf-sidebar {
      width: 100%;
    }
    
    /* Reveal the primary mobile accordion summary */
    .pf-main-filter-wrapper > summary {
      display: block;
      font-size: 1rem;
      border-radius: 4px;
    }

    .pf-main-filter-wrapper {
      margin-bottom: 1rem;
    }

    .pf-main-filter-inner {
      padding: 0.75rem 0.5rem 0.25rem 0.5rem;
    }
  }
</style>

<input type="text" id="pf-input" class="pf-search-box" placeholder="Search council meetings by keyword, topic, or motion...">

<div class="pf-container">
  <div class="pf-sidebar">
    <!-- Primary Shell Accordion for Mobile -->
    <details class="pf-main-filter-wrapper" id="pf-mobile-wrapper" open>
      <summary>Filters</summary>
      <div class="pf-main-filter-inner">
        <div class="pf-filter-header-bar">
          <button id="pf-clear-all" class="pf-clear-btn" style="display:none;">Clear all filters</button>
        </div>
        <div id="pf-filters-container">Loading filters...</div>
      </div>
    </details>
  </div>

  <div class="pf-main">
    <div class="pf-meta-bar">
      <span id="pf-stats">Initializing index...</span>
    </div>
    <div id="pf-results"></div>
    <button id="pf-load-more-btn" class="pf-load-more" style="display:none;">Load More Results</button>
  </div>
</div>

<hr style="margin: 3rem 0 2rem 0; opacity: 0.2;">

<footer style="font-size: 0.9rem; line-height: 1.6; opacity: 0.85; margin-bottom: 2rem;">
</footer>

<script type="module">
  let pagefind;
  let allResults = [];
  let currentRenderCount = 20;
  let debounceTimer = null;

  const FILTER_CONFIG = [
    { key: "Category", title: "Category" },
    { key: "Council Body", title: "Council Body" },
    { key: "Year", title: "Year" },
    { key: "Year-Month", title: "Year & Month" },
    { key: "File Type", title: "File Type" },
    { key: "Meeting Type", title: "Meeting Type" }
  ];

  async function init() {
    try {
      pagefind = await import(new URL('pagefind/pagefind.js', document.baseURI).href);
      await pagefind.init();

      const availableFilters = await pagefind.filters();
      renderFilterSidebar(availableFilters);

      document.getElementById('pf-input').addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => runSearch(), 250);
      });

      document.getElementById('pf-filters-container').addEventListener('change', () => runSearch(true));
      document.getElementById('pf-clear-all').addEventListener('click', clearAllFilters);
      document.getElementById('pf-load-more-btn').addEventListener('click', loadMoreResults);

      // Media query listener to ensure desktop view remains open when resizing
      const mediaQuery = window.matchMedia('(max-width: 768px)');
      const handleViewportChange = (e) => {
        const mobileWrapper = document.getElementById('pf-mobile-wrapper');
        if (!e.matches) {
          mobileWrapper.open = true; // Auto-expand when returning to desktop
        }
      };
      mediaQuery.addEventListener('change', handleViewportChange);

      await runSearch();
    } catch (err) {
      document.getElementById('pf-stats').innerText = "Failed to load Pagefind search index.";
      console.error(err);
    }
  }

  function renderFilterSidebar(filters) {
    const container = document.getElementById('pf-filters-container');
    container.innerHTML = '';

    FILTER_CONFIG.forEach(cfg => {
      const catKey = cfg.key;
      if (!filters[catKey]) return;

      const details = document.createElement('details');
      details.className = 'pf-filter-group';
      details.open = true; // Individual filter categories accordion open by default

      const summary = document.createElement('summary');
      summary.innerText = cfg.title;
      details.appendChild(summary);

      const listDiv = document.createElement('div');
      listDiv.className = 'pf-filter-list';

      const entries = Object.entries(filters[catKey]);

      if (catKey === "Council Body") {
        const fullCouncilItems = [];
        const municipalItems = [];
        const committeeItems = [];

        entries.forEach(([val, count]) => {
          if (val === "Limerick City and County Council") {
            fullCouncilItems.push([val, count]);
          } else if (
            val.includes("District") || 
            ["Adare-Rathkeale", "Newcastle West", "Cappamore-Kilmallock"].includes(val)
          ) {
            municipalItems.push([val, count]);
          } else {
            committeeItems.push([val, count]);
          }
        });

        fullCouncilItems.sort((a, b) => a[0].localeCompare(b[0]));
        municipalItems.sort((a, b) => a[0].localeCompare(b[0]));
        committeeItems.sort((a, b) => a[0].localeCompare(b[0]));

        const appendSection = (title, items) => {
          if (items.length === 0) return;
          const header = document.createElement('div');
          header.style.cssText = "font-size: 0.75rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.6; margin: 0.6rem 0 0.2rem 0;";
          header.innerText = title;
          listDiv.appendChild(header);

          items.forEach(([val, count]) => {
            listDiv.appendChild(createCheckboxLabel(catKey, val, count));
          });
        };

        appendSection("Full Council", fullCouncilItems);
        appendSection("Municipal Districts", municipalItems);
        appendSection("Committees", committeeItems);

      } else {
        entries.sort((a, b) => a[0].localeCompare(b[0]));
        entries.forEach(([val, count]) => {
          listDiv.appendChild(createCheckboxLabel(catKey, val, count));
        });
      }

      details.appendChild(listDiv);
      container.appendChild(details);
    });
  }

  function createCheckboxLabel(catKey, val, count) {
    const label = document.createElement('label');
    label.className = 'pf-option';
    label.dataset.cat = catKey;
    label.dataset.val = val;
    label.innerHTML = `
      <input type="checkbox" name="${catKey}" value="${val.replace(/"/g, '&quot;')}">
      <span>${val}</span>
      <span class="pf-count">(${count})</span>
    `;
    return label;
  }

  let searchSequence = 0;

  async function runSearch(isFilterChange = false) {
    const currentSequence = ++searchSequence;

    document.getElementById('pf-stats').innerText = "Searching...";
    document.getElementById('pf-results').innerHTML = '<p style="padding: 1rem; opacity: 0.7;">Searching...</p>';
    document.getElementById('pf-load-more-btn').style.display = 'none';

    const query = document.getElementById('pf-input').value.trim();
    const rawFilters = {};
    let totalActiveFilters = 0;

    document.querySelectorAll('#pf-filters-container input[type="checkbox"]:checked').forEach(cb => {
      const cat = cb.name;
      if (!rawFilters[cat]) {
        rawFilters[cat] = [];
      }
      rawFilters[cat].push(cb.value);
      totalActiveFilters++;
    });

    document.getElementById('pf-clear-all').style.display = totalActiveFilters > 0 ? 'inline' : 'none';

    const formatFiltersObj = (filtersMap) => {
      const formatted = {};
      for (const [cat, values] of Object.entries(filtersMap)) {
        if (values.length > 0) {
          formatted[cat] = values.length > 1 ? { any: values } : values[0];
        }
      }
      return formatted;
    };

    const mainFormattedFilters = formatFiltersObj(rawFilters);

    try {
      const response = await pagefind.search(query || null, { 
        filters: mainFormattedFilters
      });

      if (currentSequence !== searchSequence) return;

      allResults = response.results;
      currentRenderCount = 20;

      document.getElementById('pf-stats').innerText = `${allResults.length} meeting${allResults.length === 1 ? '' : 's'} found`;
      renderResultsSlice();

      const facetedFilters = {};
      for (const cfg of FILTER_CONFIG) {
        const catKey = cfg.key;
        const siblingFilters = { ...rawFilters };
        delete siblingFilters[catKey];
        
        const facetQueryResponse = await pagefind.search(query || null, {
          filters: formatFiltersObj(siblingFilters)
        });

        if (currentSequence !== searchSequence) return;
        if (facetQueryResponse.filters && facetQueryResponse.filters[catKey]) {
          facetedFilters[catKey] = facetQueryResponse.filters[catKey];
        }
      }

      updateFilterCounts(facetedFilters, rawFilters);

    } catch (err) {
      console.error(err);
      document.getElementById('pf-stats').innerText = "Error executing search.";
      document.getElementById('pf-results').innerHTML = '<p style="padding: 1rem; color: red;">Failed to fetch results.</p>';
    }
  }

  function updateFilterCounts(dynamicFilters, activeRawFilters) {
    if (!dynamicFilters) return;

    FILTER_CONFIG.forEach(cfg => {
      const catKey = cfg.key;
      const categoryCounts = dynamicFilters[catKey] || {};

      document.querySelectorAll(`.pf-option[data-cat="${catKey}"]`).forEach(label => {
        const val = label.dataset.val;
        const count = categoryCounts[val] || 0;
        const countSpan = label.querySelector('.pf-count');
        const checkbox = label.querySelector('input');

        if (countSpan) {
          countSpan.innerText = `(${count})`;
        }

        if (count === 0 && !checkbox.checked) {
          label.style.opacity = '0.35';
        } else {
          label.style.opacity = '1';
        }
      });
    });
  }

  async function renderResultsSlice() {
    const container = document.getElementById('pf-results');
    const loadMoreBtn = document.getElementById('pf-load-more-btn');

    if (currentRenderCount <= 20) {
      container.innerHTML = '';
    }

    if (allResults.length === 0) {
      container.innerHTML = '<p style="padding: 1rem; opacity: 0.7;">No matching council meetings found.</p>';
      loadMoreBtn.style.display = 'none';
      return;
    }

    const batch = allResults.slice(currentRenderCount - 20, currentRenderCount);
    const loadedData = await Promise.all(batch.map(item => item.data()));

    loadedData.forEach(item => {
      const card = document.createElement('div');
      card.className = 'pf-result-card';
      
      const title = item.meta?.title || item.url.split('/').pop().replace('.html', '');
      const fullDate = item.meta?.date || '';

      card.innerHTML = `
        <h3 style="margin-bottom: 0.2rem;"><a href="${item.url}">${title}</a></h3>
        ${fullDate ? `<div style="font-size: 0.82rem; opacity: 0.75; margin-bottom: 0.6rem;">Uploaded: <strong>${fullDate}</strong></div>` : ''}
        <p style="margin:0; font-size: 0.9em; line-height: 1.4;">${item.excerpt}</p>
      `;
      container.appendChild(card);
    });

    loadMoreBtn.style.display = allResults.length > currentRenderCount ? 'block' : 'none';
  }

  function loadMoreResults() {
    currentRenderCount += 20;
    renderResultsSlice();
  }

  function clearAllFilters() {
    document.querySelectorAll('#pf-filters-container input[type="checkbox"]').forEach(cb => cb.checked = false);
    runSearch();
  }

  init();
</script>
