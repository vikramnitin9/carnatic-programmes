---
layout: default
title: Search
---

<div id="search-app">
  <div class="search-tabs">
    <button class="tab active" data-tab="artist">Artist Search</button>
    <button class="tab" data-tab="song">Song · Raga · Tala · Composer</button>
  </div>

  <div id="artist-panel" class="search-panel active">
    <input type="text" id="artist-input" class="search-input"
           placeholder="Search for an artist name…" autocomplete="off">
    <div id="artist-results" class="results"></div>
  </div>

  <div id="song-panel" class="search-panel">
    <div class="search-row">
      <input type="text" id="song-input" class="search-input"
             placeholder="Search across song, raga, tala, composer…" autocomplete="off">
      <select id="song-field" class="field-select">
        <option value="all">All fields</option>
        <option value="song">Song</option>
        <option value="raga">Raga</option>
        <option value="tala">Tala</option>
        <option value="composer">Composer</option>
      </select>
    </div>
    <div id="song-results" class="results"></div>
  </div>
</div>

<style>
  /* Tabs */
  .search-tabs {
    display: flex;
    gap: 0;
    border-bottom: 2px solid var(--border);
    margin-bottom: 1.5rem;
  }
  .tab {
    background: none;
    border: none;
    padding: 0.75rem 1.25rem;
    font-family: inherit;
    font-size: 0.95rem;
    color: #888;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
  }
  .tab:hover { color: var(--accent); }
  .tab.active {
    color: var(--accent);
    border-bottom-color: var(--accent);
    font-weight: 600;
  }

  /* Panels */
  .search-panel { display: none; }
  .search-panel.active { display: block; }

  /* Inputs */
  .search-input {
    width: 100%;
    padding: 0.75rem 1rem;
    font-family: inherit;
    font-size: 1rem;
    border: 2px solid var(--border);
    border-radius: 6px;
    background: var(--card-bg);
    color: var(--text);
    outline: none;
    transition: border-color 0.2s;
  }
  .search-input:focus { border-color: var(--accent); }
  .search-input::placeholder { color: #aaa; }

  .search-row {
    display: flex;
    gap: 0.75rem;
  }
  .search-row .search-input { flex: 1; }

  .field-select {
    padding: 0.75rem 0.75rem;
    font-family: inherit;
    font-size: 0.9rem;
    border: 2px solid var(--border);
    border-radius: 6px;
    background: var(--card-bg);
    color: var(--text);
    cursor: pointer;
    min-width: 120px;
  }

  .results { margin-top: 1.5rem; }
  .results-count {
    font-size: 0.9rem;
    color: #888;
    margin-bottom: 1rem;
    font-style: italic;
  }
  .no-results {
    text-align: center;
    color: #999;
    padding: 2rem;
    font-style: italic;
  }
  .hint {
    text-align: center;
    color: #aaa;
    padding: 3rem 1rem;
    font-style: italic;
    font-size: 0.95rem;
  }

  /* Artist results */
  .artist-accordion {
    border: 1px solid var(--border);
    border-radius: 6px;
    margin-bottom: 0.75rem;
    overflow: hidden;
  }
  .artist-accordion > summary {
    padding: 0.85rem 1rem;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--card-bg);
    list-style: none;
    transition: background 0.15s;
  }
  .artist-accordion > summary::-webkit-details-marker { display: none; }
  .artist-accordion > summary::before {
    content: '▸';
    margin-right: 0.6rem;
    color: var(--accent);
    transition: transform 0.15s;
    display: inline-block;
  }
  .artist-accordion[open] > summary::before {
    transform: rotate(90deg);
  }
  .artist-accordion > summary:hover { background: rgba(139,69,19,0.05); }
  .artist-name { font-weight: 600; color: var(--accent); }
  .result-count {
    font-size: 0.82rem;
    color: #999;
    background: rgba(139,69,19,0.08);
    padding: 0.15rem 0.55rem;
    border-radius: 10px;
  }

  .artist-sessions { padding: 0 1rem 0.75rem; }

  .session-accordion {
    border-left: 3px solid var(--border);
    margin: 0.5rem 0;
    padding-left: 0;
  }
  .session-accordion > summary {
    padding: 0.5rem 0.75rem;
    cursor: pointer;
    font-size: 0.92rem;
    list-style: none;
    color: var(--text);
    transition: color 0.15s;
  }
  .session-accordion > summary::-webkit-details-marker { display: none; }
  .session-accordion > summary::before {
    content: '▸';
    margin-right: 0.4rem;
    color: var(--accent-light);
    display: inline-block;
    transition: transform 0.15s;
  }
  .session-accordion[open] > summary::before {
    transform: rotate(90deg);
  }
  .session-accordion[open] {
    border-left-color: var(--accent);
  }
  .session-accordion > summary:hover { color: var(--accent); }

  .session-content {
    padding: 0.5rem 0.75rem 0.75rem;
  }
  .session-performers p {
    margin: 0.2rem 0;
    font-size: 0.9rem;
  }
  .session-content table {
    margin-top: 0.75rem;
    font-size: 0.85rem;
  }
  .view-link {
    display: inline-block;
    margin-top: 0.75rem;
    font-size: 0.85rem;
  }

  .session-year {
    font-weight: 700;
    color: var(--accent);
  }

  /* Song results table */
  .table-scroll { overflow-x: auto; }
  .song-results-table td,
  .song-results-table th {
    white-space: nowrap;
  }
  .song-results-table td:first-child {
    white-space: normal;
    min-width: 150px;
  }

  @media (max-width: 600px) {
    .search-row { flex-direction: column; }
    .field-select { min-width: auto; }
    .tab { padding: 0.6rem 0.75rem; font-size: 0.85rem; }
    .search-input { font-size: 0.95rem; }
  }
</style>

<script>
(function() {
  const BASE = document.querySelector('header a').getAttribute('href').replace(/\/$/, '');
  let DATA = null;
  let artistIndex = {};
  let songIndex = [];

  function esc(s) {
    const d = document.createElement('div');
    d.textContent = s || '';
    return d.innerHTML;
  }

  // --- Data loading & indexing ---

  fetch(BASE + '/search_data.json')
    .then(r => r.json())
    .then(data => {
      DATA = data;
      buildIndices();
      document.getElementById('artist-input').disabled = false;
      document.getElementById('song-input').disabled = false;
    });

  function buildIndices() {
    artistIndex = {};
    songIndex = [];

    DATA.forEach(prog => {
      prog.sessions.forEach(session => {
        // Artist index
        session.performers.forEach(perf => {
          const key = perf.name;
          if (!artistIndex[key]) artistIndex[key] = [];
          artistIndex[key].push({
            year: prog.year,
            conference: prog.conference,
            file: prog.file,
            date: session.date,
            performers: session.performers,
            songs: session.songs
          });
        });

        // Song index
        const mainPerformer = session.performers.length > 0
          ? session.performers[0].name : 'Unknown';
        session.songs.forEach(song => {
          songIndex.push({
            song: song.song || '',
            raga: song.raga || '',
            tala: song.tala || '',
            composer: song.composer || '',
            performer: mainPerformer,
            allPerformers: session.performers,
            year: prog.year,
            file: prog.file,
            date: session.date
          });
        });
      });
    });
  }

  // --- Tabs ---

  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.search-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById(tab.dataset.tab + '-panel').classList.add('active');
    });
  });

  // --- Artist search ---

  const artistInput = document.getElementById('artist-input');
  const artistResults = document.getElementById('artist-results');
  artistInput.disabled = true;
  artistResults.innerHTML = '<p class="hint">Loading data…</p>';

  let artistTimer;
  artistInput.addEventListener('input', () => {
    clearTimeout(artistTimer);
    artistTimer = setTimeout(() => searchArtists(artistInput.value), 150);
  });

  function searchArtists(query) {
    const q = query.trim().toLowerCase();
    if (q.length < 2) {
      artistResults.innerHTML = '<p class="hint">Type at least 2 characters to search</p>';
      return;
    }

    const matches = Object.entries(artistIndex)
      .filter(([name]) => name.toLowerCase().includes(q))
      .sort((a, b) => {
        // Exact prefix matches first
        const aStarts = a[0].toLowerCase().indexOf(q) === 0 ? 0 : 1;
        const bStarts = b[0].toLowerCase().indexOf(q) === 0 ? 0 : 1;
        if (aStarts !== bStarts) return aStarts - bStarts;
        return a[0].localeCompare(b[0]);
      });

    if (matches.length === 0) {
      artistResults.innerHTML = '<p class="no-results">No artists found</p>';
      return;
    }

    const countText = `<p class="results-count">${matches.length} artist${matches.length !== 1 ? 's' : ''} found</p>`;

    const html = matches.slice(0, 100).map(([name, sessions]) => {
      const sessionsHtml = sessions
        .sort((a, b) => a.year - b.year)
        .map(s => {
          const perfHtml = s.performers.map(p =>
            `<p><strong>${esc(p.name)}</strong>${p.role ? ' — ' + esc(p.role) : ''}</p>`
          ).join('');

          let tableHtml = '';
          if (s.songs.length > 0) {
            const rows = s.songs.map(song =>
              `<tr><td>${esc(song.song)}</td><td>${esc(song.raga)}</td><td>${esc(song.tala)}</td><td>${esc(song.composer)}</td></tr>`
            ).join('');
            tableHtml = `<table><thead><tr><th>Song</th><th>Raga</th><th>Tala</th><th>Composer</th></tr></thead><tbody>${rows}</tbody></table>`;
          }

          return `
            <details class="session-accordion">
              <summary><span class="session-year">${s.year}</span> · ${esc(s.date)}</summary>
              <div class="session-content">
                <div class="session-performers">${perfHtml}</div>
                ${tableHtml}
                <a href="${BASE}/programmes/${s.file}" class="view-link">View full programme →</a>
              </div>
            </details>`;
        }).join('');

      const count = sessions.length;
      return `
        <details class="artist-accordion">
          <summary>
            <span><span class="artist-name">${esc(name)}</span></span>
            <span class="result-count">${count} programme${count !== 1 ? 's' : ''}</span>
          </summary>
          <div class="artist-sessions">${sessionsHtml}</div>
        </details>`;
    }).join('');

    artistResults.innerHTML = countText + html;
  }

  // --- Song search ---

  const songInput = document.getElementById('song-input');
  const songField = document.getElementById('song-field');
  const songResults = document.getElementById('song-results');
  songInput.disabled = true;
  songResults.innerHTML = '<p class="hint">Loading data…</p>';

  let songTimer;
  songInput.addEventListener('input', () => {
    clearTimeout(songTimer);
    songTimer = setTimeout(() => searchSongs(songInput.value), 150);
  });
  songField.addEventListener('change', () => searchSongs(songInput.value));

  function searchSongs(query) {
    const q = query.trim().toLowerCase();
    if (q.length < 2) {
      songResults.innerHTML = '<p class="hint">Type at least 2 characters to search</p>';
      return;
    }

    const field = songField.value;
    const matches = songIndex.filter(s => {
      if (field === 'all') {
        return s.song.toLowerCase().includes(q) ||
               s.raga.toLowerCase().includes(q) ||
               s.tala.toLowerCase().includes(q) ||
               s.composer.toLowerCase().includes(q);
      }
      return (s[field] || '').toLowerCase().includes(q);
    });

    if (matches.length === 0) {
      songResults.innerHTML = '<p class="no-results">No songs found</p>';
      return;
    }

    const countText = `<p class="results-count">${matches.length} result${matches.length !== 1 ? 's' : ''} found</p>`;

    const rows = matches.slice(0, 200).map(s => `
      <tr>
        <td>${esc(s.song)}</td>
        <td>${esc(s.raga)}</td>
        <td>${esc(s.tala)}</td>
        <td>${esc(s.composer)}</td>
        <td>${esc(s.performer)}</td>
        <td><a href="${BASE}/programmes/${s.file}">${s.year}</a></td>
      </tr>
    `).join('');

    songResults.innerHTML = countText + `
      <div class="table-scroll">
        <table class="song-results-table">
          <thead><tr><th>Song</th><th>Raga</th><th>Tala</th><th>Composer</th><th>Artist</th><th>Year</th></tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>`;
  }
})();
</script>
