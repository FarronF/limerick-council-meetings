<script type="module">
  let pagefind;
  let allResults = [];
  let currentRenderCount = 20;
  let debounceTimer = null;
  let currentAbortController = null;

  const FILTER_CONFIG = [
    { key: "Category", title: "Category" },
    { key: "Council Body", title: "Council Body" },
    { key: "Meeting Type", title: "Meeting Type" }
    { key: "Year-Month", title: "Year & Month" },
  ];

  async function init() {
    try {
      pagefind = await import("../pagefind/pagefind.js");
      await pagefind.init();

      const availableFilters = await pagefind.filters();
      renderFilterSidebar(availableFilters);

      // Debounced input listener
      document.getElementById('pf-input').addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => runSearch(), 250);
      });

      // Immediate trigger for filters/checkboxes
      document.getElementById('pf-filters-container').addEventListener('change', () => runSearch(true));
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

        if (count === 0 && !checkbox.checked) {
          label.style.opacity = '0.35';
        } else {
          label.style.opacity = '1';
        }
      });
    });
  }

  async function runSearch(isFilterChange = false) {
    // Cancel any pending search operation
    if (currentAbortController) {
      currentAbortController.abort();
    }
    currentAbortController = new AbortController();
    const signal = currentAbortController.signal;

    const query = document.getElementById('pf-input').value.trim();
    const selectedFilters = {};
    let totalActiveFilters = 0;

    document.querySelectorAll('#pf-filters-container input[type="checkbox"]:checked').forEach(cb => {
      const cat = cb.name;
      if (!selectedFilters[cat]) {
        selectedFilters[cat] = [];
      }
      selectedFilters[cat].push(cb.value);
      totalActiveFilters++;
    });

    document.getElementById('pf-clear-all').style.display = totalActiveFilters > 0 ? 'inline' : 'none';

    try {
      // Pass the abort signal into pagefind search options
      const response = await pagefind.search(query || null, { 
        filters: selectedFilters,
        signal: signal 
      });

      // If aborted, exit early silently
      if (signal.aborted) return;

      allResults = response.results;
      currentRenderCount = 20;

      if (response.filters) {
        updateFilterCounts(response.filters);
      }

      document.getElementById('pf-stats').innerText = `${allResults.length} meeting${allResults.length === 1 ? '' : 's'} found`;

      renderResultsSlice();
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error(err);
      }
    }
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
