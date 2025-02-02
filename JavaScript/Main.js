const ingredients = JSON.parse(localStorage.getItem('ingredients')) || [];

function saveIngredients() {
  localStorage.setItem('ingredients', JSON.stringify(ingredients));
}

function addIngredient(id, name, quantity, expiration) {
  const existingIngredient = ingredients.find(ingredient => ingredient.name === name);
  if (existingIngredient) {
    const currentQuantity = parseFloat(existingIngredient.quantity);
    const additionalQuantity = parseFloat(quantity);
    if (!isNaN(currentQuantity) && !isNaN(additionalQuantity)) {
      existingIngredient.quantity = `${currentQuantity + additionalQuantity} g`;
    }
  } else {
    ingredients.push({
      id: id,
      name: name,
      quantity: quantity,
      expiration: expiration,
      used: false
    });
  }
  saveIngredients();
  renderIngredients();
}

document.getElementById('addIngredientForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const name = document.getElementById('ingredientName').value;
  const quantity = document.getElementById('ingredientQuantity').value;
  const expiration = document.getElementById('ingredientExpiration').value;
  addIngredient(Date.now().toString(), name, quantity, expiration);
  alert('Ingredient added successfully!');
  document.getElementById('addIngredientForm').reset();
});

function useIngredient(name, usedQuantity) {
  const ingredient = ingredients.find(i => i.name === name);
  if (ingredient) {
    const currentQuantity = parseFloat(ingredient.quantity);
    const usedQty = parseFloat(usedQuantity);
    if (!isNaN(currentQuantity) && !isNaN(usedQty)) {
      ingredient.quantity = `${currentQuantity - usedQty} g`;
      ingredient.used = true;
    }
  }
  saveIngredients();
  renderIngredients();
}

function deleteIngredient(name) {
  const index = ingredients.findIndex(i => i.name === name);
  if (index !== -1) {
    ingredients.splice(index, 1);
  }
  saveIngredients();
  renderIngredients();
}

function deleteUsedIngredients() {
  for (let i = ingredients.length - 1; i >= 0; i--) {
    if (ingredients[i].used) {
      ingredients.splice(i, 1);
    }
  }
  saveIngredients();
  renderIngredients();
}

function renderIngredients() {
  const ingredientsTableBody = document.getElementById('ingredientsTable').querySelector('tbody');
  ingredientsTableBody.innerHTML = ''; // Clear the table body
  ingredients.forEach(ingredient => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${ingredient.name}</td>
      <td>${ingredient.quantity}</td>
      <td>${ingredient.expiration}</td>
      <td>${ingredient.used ? 'Yes' : 'No'}</td>
      <td>
        <input type="number" placeholder="Used quantity" id="usedQuantity-${ingredient.name}">
        <button onclick="useIngredient('${ingredient.name}', document.getElementById('usedQuantity-${ingredient.name}').value)">Use</button>
        <button onclick="deleteIngredient('${ingredient.name}')">Delete</button>
      </td>
    `;
    ingredientsTableBody.appendChild(row);
  });
}

// Initial render
renderIngredients();

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