---
hide:
  - toc
---

# Search Council Meetings

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
  
  .pf-filter-group {
    border: 1px solid var(--md-default-fg-color--lightest, #e0e0e0);
    border-radius: 6px;
    margin-bottom: 1rem;
    background: var(--md-default-bg-color, #fff);
    overflow: hidden;
  }

  .pf-filter-group details {
    width: 100%;
  }

  .pf-filter-group summary {
    font-weight: bold;
    padding: 0.85rem;
    cursor: pointer;
    user-select: none;
    background: var(--md-default-bg-color, #fff);
    border-bottom: 1px solid transparent;
    transition: background 0.2s;
  }

  .pf-filter-group details[open] summary {
    border-bottom: 1px solid var(--md-default-fg-color--lightest, #eee);
    background: var(--md-code-bg-color, rgba(0,0,0,0.02));
  }

  .pf-filter-list {
    max-height: 220px;
    overflow-y: auto;
    padding: 0.5rem 0.85rem 0.85rem 0.85rem;
  }

  .pf-option {
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
    margin: 0.35rem 0;
    cursor: pointer;
    line-height: 1.3;
    transition: opacity 0.2s;
  }

  .pf-option input {
    cursor: pointer;
  }

  .pf-count {
    opacity: 0.6;
    font-size: 0.8em;
    margin-left: auto;
  }

  .pf-main {
    flex-grow: 1;
  }

  .pf-search-box {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border: 1px solid var(--md-default-fg-color--lightest, #ccc);
    border-radius: 6px;
    margin-bottom: 1rem;
    background: var(--md-default-bg-color, #fff);
    color: var(--md-default-fg-color, #000);
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
    padding: 1rem;
    border: 1px solid var(--md-default-fg-color--lightest, #e0e0e0);
    border-radius: 6px;
    margin-bottom: 0.85rem;
    background: var(--md-default-bg-color, #fff);
  }

  .pf-result-card h3 {
    margin: 0 0 0.4rem 0;
    font-size: 1.1rem;
  }

  .pf-result-card mark {
    background-color: rgba(255, 235, 59, 0.4);
    font-weight: bold;
    padding: 0 2px;
  }

  .pf-load-more {
    display: block;
    width: 100%;
    padding: 0.6rem;
    margin-top: 1rem;
    background: var(--md-default-fg-color--lightest, #f0f0f0);
    border: 1px solid var(--md-default-fg-color--light, #ccc);
    border-radius: 4px;
    cursor: pointer;
    text-align: center;
  }
</style>

<input type="text" id="pf-input" class="pf-search-box" placeholder="Search council meetings by keyword, topic, or motion...">

<div class="pf-container">
  <div class="pf-sidebar">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
      <strong style="font-size:1rem;">Filters</strong>
      <button id="pf-clear-all" class="pf-clear-btn" style="display:none;">Clear all</button>
    </div>
    <div id="pf-filters-container">Loading filters...</div>
  </div>

  <div class="pf-main">
    <div class="pf-meta-bar">
      <span id="pf-stats">Initializing index...</span>
    </div>
    <div id="pf-results"></div>
    <button id="pf-load-more-btn" class="pf-load-more" style="display:none;">Load More Results</button>
  </div>
</div>

<script type="module">
  let pagefind;
  let allResults = [];
  let currentRenderCount = 20;

  const FILTER_CONFIG = [
    { key: "Year-Month", title: "Year & Month" },
    { key: "Category", title: "Category" },
    { key: "Council Body", title: "Council Body" },
    { key: "Meeting Type", title: "Meeting Type" }
  ];

  async function init() {
    try {
      // Import Pagefind core engine dynamically from compiled site outputs
      pagefind = await import("../pagefind/pagefind.js");
      await pagefind.init();

      const availableFilters = await pagefind.filters();
      renderFilterSidebar(availableFilters);

      document.getElementById('pf-input').addEventListener('input', () => runSearch());
      document.getElementById('pf-filters-container').addEventListener('change', () => runSearch());
      document.getElementById('pf-clear-all').addEventListener('click', clearAllFilters);
      document.getElementById('pf-load-more-btn').addEventListener('click', loadMoreResults);

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

      const groupDiv = document.createElement('div');
      groupDiv.className = 'pf-filter-group';

      const details = document.createElement('details');
      details.open = true;

      const summary = document.createElement('summary');
      summary.innerText = cfg.title;
      details.appendChild(summary);

      const listDiv = document.createElement('div');
      listDiv.className = 'pf-filter-list';

      const entries = Object.entries(filters[catKey]).sort((a, b) => a[0].localeCompare(b[0]));

      entries.forEach(([val, count]) => {
        const label = document.createElement('label');
        label.className = 'pf-option';
        label.dataset.cat = catKey;
        label.dataset.val = val;
        label.innerHTML = `
          <input type="checkbox" name="${catKey}" value="${val.replace(/"/g, '&quot;')}">
          <span>${val}</span>
          <span class="pf-count">(${count})</span>
        `;
        listDiv.appendChild(label);
      });

      details.appendChild(listDiv);
      groupDiv.appendChild(details);
      container.appendChild(groupDiv);
    });
  }

  function updateFilterCounts(dynamicFilters) {
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

        // Dim zero-count options while keeping selected ones visible
        if (count === 0 && !checkbox.checked) {
          label.style.opacity = '0.35';
        } else {
          label.style.opacity = '1';
        }
      });
    });
  }

  async function runSearch() {
    const query = document.getElementById('pf-input').value.trim();
    const selectedFilters = {};
    let totalActiveFilters = 0;

    // Collect checked values: arrays map to OR within a category, separate keys map to AND
    document.querySelectorAll('#pf-filters-container input[type="checkbox"]:checked').forEach(cb => {
      const cat = cb.name;
      if (!selectedFilters[cat]) {
        selectedFilters[cat] = [];
      }
      selectedFilters[cat].push(cb.value);
      totalActiveFilters++;
    });

    document.getElementById('pf-clear-all').style.display = totalActiveFilters > 0 ? 'inline' : 'none';

    const response = await pagefind.search(query || null, { filters: selectedFilters });
    allResults = response.results;
    currentRenderCount = 20;

    if (response.filters) {
      updateFilterCounts(response.filters);
    }

    document.getElementById('pf-stats').innerText = `${allResults.length} meeting${allResults.length === 1 ? '' : 's'} found`;

    renderResultsSlice();
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
      
      card.innerHTML = `
        <h3><a href="${item.url}">${title}</a></h3>
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

  window.addEventListener('DOMContentLoaded', init);
</script>
