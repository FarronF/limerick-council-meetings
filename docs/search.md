<script type="module">
  let pagefind;
  let allResults = [];
  let currentRenderCount = 20;
  let debounceTimer = null;

  const FILTER_CONFIG = [
    { key: "Category", title: "Category" },
    { key: "Council Body", title: "Council Body" },
    { key: "Meeting Type", title: "Meeting Type" },
    { key: "Year", title: "Year" },
    { key: "Year-Month", title: "Year & Month" }
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

      const entries = Object.entries(filters[catKey]);

      if (catKey === "Council Body") {
        // Define exact categories and order groups
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

        // Sort sub-lists alphabetically
        fullCouncilItems.sort((a, b) => a[0].localeCompare(b[0]));
        municipalItems.sort((a, b) => a[0].localeCompare(b[0]));
        committeeItems.sort((a, b) => a[0].localeCompare(b[0]));

        // Helper to append section header and items
        const appendSection = (title, items) => {
          if (items.length === 0) return;
          const header = document.createElement('div');
          header.style.cssText = "font-size: 0.75rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.5; margin: 0.6rem 0 0.2rem 0;";
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
        // Standard alphabetical sorting for all other facets
        entries.sort((a, b) => a[0].localeCompare(b[0]));
        entries.forEach(([val, count]) => {
          listDiv.appendChild(createCheckboxLabel(catKey, val, count));
        });
      }

      details.appendChild(listDiv);
      groupDiv.appendChild(details);
      container.appendChild(groupDiv);
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
      if (currentRenderCount <= 20) {
        currentRenderCount = 20;
      }

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

  init();
</script>
