/**
 * Recommendation History Interaction & Filters
 */

document.addEventListener('DOMContentLoaded', () => {
  setupHistoryFilters();
  setupRowDeletion();
  setupPDFExportMock();
});

/**
 * Searches, sorts, and filters table rows dynamically
 */
function setupHistoryFilters() {
  const searchInput = document.getElementById('history-search');
  const catSelect = document.getElementById('filter-category');
  const sortSelect = document.getElementById('sort-order');
  const tableBody = document.getElementById('history-table-body');
  
  if (!searchInput || !catSelect || !sortSelect || !tableBody) return;

  function filterAndSort() {
    const query = searchInput.value.toLowerCase();
    const filterCat = catSelect.value;
    const sortVal = sortSelect.value;
    
    const rows = Array.from(tableBody.querySelectorAll('.history-row'));
    
    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      const cat = row.getAttribute('data-category');
      
      const matchesSearch = text.includes(query);
      const matchesCat = (filterCat === 'all' || cat === filterCat);
      
      if (matchesSearch && matchesCat) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });

    // Handle sorting on visible rows
    const sortedRows = rows.sort((a, b) => {
      if (sortVal === 'newest') {
        return new Date(b.getAttribute('data-date')) - new Date(a.getAttribute('data-date'));
      } else if (sortVal === 'oldest') {
        return new Date(a.getAttribute('data-date')) - new Date(b.getAttribute('data-date'));
      } else if (sortVal === 'category') {
        return a.getAttribute('data-category').localeCompare(b.getAttribute('data-category'));
      }
      return 0;
    });

    sortedRows.forEach(row => tableBody.appendChild(row));
  }

  searchInput.addEventListener('input', filterAndSort);
  catSelect.addEventListener('change', filterAndSort);
  sortSelect.addEventListener('change', filterAndSort);
}

/**
 * Handles individual item deletes via AJAX requests to backend routes
 */
function setupRowDeletion() {
  const tableBody = document.getElementById('history-table-body');
  if (!tableBody) return;

  tableBody.addEventListener('click', (e) => {
    const btn = e.target.closest('.delete-row-btn');
    if (!btn) return;

    const logId = btn.getAttribute('data-id');
    const row = btn.closest('.history-row');

    if (confirm('Delete this recommendation log?')) {
      fetch(`/history/delete/${logId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          row.style.opacity = '0';
          setTimeout(() => {
            row.remove();
            // Show empty row if table is empty
            if (tableBody.querySelectorAll('.history-row').length === 0) {
              tableBody.innerHTML = `
                <tr class="no-logs-row">
                  <td colspan="7">No recommendation records logged yet. Check your dashboard to auto-generate daily advice.</td>
                </tr>
              `;
            }
          }, 300);
        } else {
          alert('Failed to delete log: ' + data.message);
        }
      })
      .catch(err => {
        console.error('Delete error:', err);
        alert('An error occurred. Check server logs.');
      });
    }
  });
}

/**
 * Mock PDF export action
 */
function setupPDFExportMock() {
  const exportBtn = document.getElementById('export-pdf-btn');
  if (!exportBtn) return;

  exportBtn.addEventListener('click', () => {
    alert('PDF compilation simulated. Your recommendation history report has been compiled and downloaded.');
  });
}
