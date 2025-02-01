// Sort state
let currentSort = {
  column: null,
  direction: 'asc'
};

function openMenu() {
  document.getElementById("myMenu").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeMenu() {
  document.getElementById("myMenu").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}

// DOM Elements
const tableBody = document.getElementById('ingredientsTableBody');
const searchInput = document.querySelector('.searchInput');
const sortableHeaders = document.querySelectorAll('.sortable');

// Sort functionality
function sortIngredients(column) {
  const direction = currentSort.column === column && currentSort.direction === 'asc' ? 'desc' : 'asc';
  
  const sortedIngredients = [...ingredients].sort((a, b) => {
      if (a[column] === b[column]) return 0;
      if (a[column] === '') return 1;
      if (b[column] === '') return -1;
      
      return direction === 'asc' 
          ? a[column] < b[column] ? -1 : 1
          : a[column] > b[column] ? -1 : 1;
  });

  currentSort = { column, direction };
  renderTable(sortedIngredients);
  updateSortIcons();
}

// Update sort icons
function updateSortIcons() {
  sortableHeaders.forEach(header => {
      const column = header.dataset.sort;
      const icon = header.querySelector('.sort-icon');
      
      if (column === currentSort.column) {
          icon.textContent = currentSort.direction === 'asc' ? '↑' : '↓';
      } else {
          icon.textContent = '↕';
      }
  });
}



function renderTable(data) {
  tableBody.innerHTML = data.map(ingredient => `
      <tr>
          <td>${ingredient.name}</td>
          <td>${ingredient.quantity}</td>
          <td>${ingredient.expiration}</td>
          <td>
              <input 
                  type="checkbox" 
                  class="checkbox" 
                  ${ingredient.used ? 'checked' : ''}
                  data-id="${ingredient.id}"
              >
          </td>
      </tr>
  `).join('');

  // Add checkbox event listeners
  tableBody.querySelectorAll('.checkbox').forEach(checkbox => {
      checkbox.addEventListener('change', (e) => {
          const id = e.target.dataset.id;
          const ingredient = ingredients.find(i => i.id === id);
          if (ingredient) {
              ingredient.used = e.target.checked;
          }
      });
  });
}

// Search functionality
searchInput.addEventListener('input', (e) => {
  const searchTerm = e.target.value.toLowerCase();
  const filteredIngredients = ingredients.filter(ingredient => 
      ingredient.name.toLowerCase().includes(searchTerm) ||
      ingredient.quantity.toLowerCase().includes(searchTerm) ||
      ingredient.expiration.toLowerCase().includes(searchTerm)
  );
  renderTable(filteredIngredients);
});

// Add sort event listeners
sortableHeaders.forEach(header => {
  header.addEventListener('click', () => {
      const column = header.dataset.sort;
      sortIngredients(column);
  });
});

// Initial render
renderTable(ingredients);