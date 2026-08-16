---
title: "Grocery List"
---

<style>
  .grocery-page {
    max-width: 1100px;
    margin: 0 auto;
    padding: 2rem 1rem 3rem;
  }

  .grocery-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
  }

  .grocery-header h1 {
    margin: 0;
    color: #12354a;
    font-size: clamp(2.2rem, 4vw, 3.2rem);
  }

  .grocery-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #edf9fb;
    color: #0f766e;
    border: 1px solid #d3ebee;
    border-radius: 999px;
    padding: 0.5rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }

  .grocery-sections {
    display: grid;
    gap: 1.5rem;
  }

  .grocery-section {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid #dfeef2;
    border-radius: 24px;
    padding: 1rem 1rem 0.9rem;
    box-shadow: 0 12px 28px rgba(15, 88, 105, 0.08);
  }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.9rem;
  }

  .section-header h2 {
    margin: 0;
    color: #0e5870;
    font-size: 1.3rem;
  }

  .add-item-button {
    border: none;
    background: #0f766e;
    color: #ffffff;
    border-radius: 999px;
    padding: 0.45rem 0.8rem;
    cursor: pointer;
    font-size: 0.75rem;
    font-weight: 700;
  }

  .grocery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.9rem;
  }

  .grocery-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    background: linear-gradient(180deg, #ffffff 0%, #f4fbff 100%);
    border: 1px solid #daeef1;
    border-radius: 18px;
    padding: 0.75rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
  }

  .grocery-item:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 18px rgba(13, 48, 83, 0.05);
  }

  .grocery-item.is-checked {
    opacity: 0.62;
  }

  .grocery-item.is-checked .item-name,
  .grocery-item.is-checked .item-amount {
    text-decoration: line-through;
  }

  .item-content {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
  }

  .item-name {
    color: #1d4558;
    font-weight: 700;
    font-size: 0.96rem;
    line-height: 1.3;
  }

  .item-amount {
    color: #5b7a88;
    font-size: 0.8rem;
    font-weight: 600;
    line-height: 1.2;
  }

  .item-actions {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    flex-shrink: 0;
  }

  .check-toggle,
  .undo-toggle,
  .edit-toggle,
  .save-toggle,
  .cancel-toggle,
  .remove-toggle,
  .add-submit,
  .add-cancel {
    border: none;
    cursor: pointer;
    font: inherit;
    transition: all 0.2s ease;
  }

  .check-toggle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #eaf7f7;
    border: 1px solid #b9dfdc;
    color: #0f766e;
    font-weight: 900;
    font-size: 0.82rem;
  }

  .grocery-item.is-checked .check-toggle {
    background: #0f766e;
    border-color: #0f766e;
    color: #ffffff;
  }

  .edit-toggle,
  .save-toggle,
  .cancel-toggle,
  .undo-toggle,
  .remove-toggle,
  .add-submit,
  .add-cancel {
    background: #edf8fb;
    border: 1px solid #d1eaf0;
    color: #0f5a70;
    border-radius: 999px;
    padding: 0.36rem 0.6rem;
    font-size: 0.7rem;
    font-weight: 700;
    min-width: 28px;
    min-height: 28px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .undo-toggle {
    display: none;
  }

  .grocery-item.is-checked .undo-toggle {
    display: inline-flex;
  }

  .edit-controls {
    display: none;
    align-items: center;
    gap: 0.4rem;
    margin-top: 0.35rem;
  }

  .grocery-item.is-editing .edit-controls {
    display: flex;
  }

  .grocery-item.is-editing .item-amount,
  .grocery-item.is-editing .edit-toggle {
    display: none;
  }

  .grocery-item input[type="text"],
  .add-form input[type="text"],
  .add-form select {
    border: 1px solid #cfe8ee;
    border-radius: 10px;
    background: #ffffff;
    color: #173d52;
    padding: 0.35rem 0.45rem;
    font: inherit;
    font-size: 0.8rem;
  }

  .grocery-item input[type="text"] {
    width: 90px;
  }

  .save-toggle,
  .add-submit {
    background: #0f766e;
    border-color: #0f766e;
    color: #ffffff;
  }

  .cancel-toggle,
  .add-cancel {
    background: #ffffff;
  }

  .empty-state {
    color: #66808a;
    font-size: 0.9rem;
    font-style: italic;
    padding: 0.5rem 0.1rem 0.2rem;
  }

  .add-form {
    display: none;
    margin-top: 0.8rem;
    padding: 0.8rem;
    background: #f4fbff;
    border: 1px solid #dfeef2;
    border-radius: 16px;
    gap: 0.55rem;
    align-items: end;
    flex-wrap: wrap;
  }

  .grocery-section.is-adding .add-form {
    display: flex;
  }

  .add-form label {
    display: flex;
    flex-direction: column;
    gap: 0.28rem;
    color: #365a6d;
    font-size: 0.74rem;
    font-weight: 700;
  }

  @media (max-width: 640px) {
    .grocery-page {
      padding: 1.25rem 0.75rem 2.5rem;
    }

    .grocery-grid {
      grid-template-columns: 1fr;
    }
  }
</style>

<section class="grocery-page">
  <header class="grocery-header">
    <h1>Grocery List</h1>
    <div class="grocery-badge">Checklist view</div>
  </header>

  <div class="grocery-sections">
    <section class="grocery-section" data-section="Produce">
      <div class="section-header">
        <h2>Produce</h2>
        <button class="add-item-button" type="button">Add</button>
      </div>
      <div class="grocery-grid" data-grid="Produce"></div>
      <form class="add-form" data-form="Produce">
        <label>
          Ingredient
          <input type="text" name="name" placeholder="e.g. Spinach" required>
        </label>
        <label>
          Amount
          <input type="text" name="amount" placeholder="2" required>
        </label>
        <label>
          Unit
          <select name="unit">
            <option value="each">each</option>
            <option value="oz">oz</option>
            <option value="lb">lb</option>
            <option value="bunch">bunch</option>
            <option value="bag">bag</option>
            <option value="bottle">bottle</option>
            <option value="loaf">loaf</option>
            <option value="gal">gal</option>
            <option value="box">box</option>
            <option value="pack">pack</option>
            <option value="can">can</option>
            <option value="jar">jar</option>
          </select>
        </label>
        <button class="add-submit" type="submit">Add Ingredient</button>
        <button class="add-cancel" type="button">Cancel</button>
      </form>
    </section>

    <section class="grocery-section" data-section="Bakery">
      <div class="section-header">
        <h2>Bakery</h2>
        <button class="add-item-button" type="button">Add</button>
      </div>
      <div class="grocery-grid" data-grid="Bakery"></div>
      <form class="add-form" data-form="Bakery">
        <label>
          Ingredient
          <input type="text" name="name" placeholder="e.g. Sourdough" required>
        </label>
        <label>
          Amount
          <input type="text" name="amount" placeholder="2" required>
        </label>
        <label>
          Unit
          <select name="unit">
            <option value="each">each</option>
            <option value="oz">oz</option>
            <option value="lb">lb</option>
            <option value="loaf">loaf</option>
            <option value="pack">pack</option>
          </select>
        </label>
        <button class="add-submit" type="submit">Add Ingredient</button>
        <button class="add-cancel" type="button">Cancel</button>
      </form>
    </section>

    <section class="grocery-section" data-section="Meat">
      <div class="section-header">
        <h2>Meat</h2>
        <button class="add-item-button" type="button">Add</button>
      </div>
      <div class="grocery-grid" data-grid="Meat"></div>
      <form class="add-form" data-form="Meat">
        <label>
          Ingredient
          <input type="text" name="name" placeholder="e.g. Chicken" required>
        </label>
        <label>
          Amount
          <input type="text" name="amount" placeholder="1.5" required>
        </label>
        <label>
          Unit
          <select name="unit">
            <option value="lb">lb</option>
            <option value="oz">oz</option>
            <option value="each">each</option>
          </select>
        </label>
        <button class="add-submit" type="submit">Add Ingredient</button>
        <button class="add-cancel" type="button">Cancel</button>
      </form>
    </section>

    <section class="grocery-section" data-section="Pantry">
      <div class="section-header">
        <h2>Pantry</h2>
        <button class="add-item-button" type="button">Add</button>
      </div>
      <div class="grocery-grid" data-grid="Pantry"></div>
      <form class="add-form" data-form="Pantry">
        <label>
          Ingredient
          <input type="text" name="name" placeholder="e.g. Rice" required>
        </label>
        <label>
          Amount
          <input type="text" name="amount" placeholder="2" required>
        </label>
        <label>
          Unit
          <select name="unit">
            <option value="bag">bag</option>
            <option value="can">can</option>
            <option value="jar">jar</option>
            <option value="bottle">bottle</option>
            <option value="each">each</option>
            <option value="oz">oz</option>
          </select>
        </label>
        <button class="add-submit" type="submit">Add Ingredient</button>
        <button class="add-cancel" type="button">Cancel</button>
      </form>
    </section>

    <section class="grocery-section" data-section="Dairy">
      <div class="section-header">
        <h2>Dairy</h2>
        <button class="add-item-button" type="button">Add</button>
      </div>
      <div class="grocery-grid" data-grid="Dairy"></div>
      <form class="add-form" data-form="Dairy">
        <label>
          Ingredient
          <input type="text" name="name" placeholder="e.g. Cheese" required>
        </label>
        <label>
          Amount
          <input type="text" name="amount" placeholder="8" required>
        </label>
        <label>
          Unit
          <select name="unit">
            <option value="oz">oz</option>
            <option value="gal">gal</option>
            <option value="each">each</option>
            <option value="pack">pack</option>
          </select>
        </label>
        <button class="add-submit" type="submit">Add Ingredient</button>
        <button class="add-cancel" type="button">Cancel</button>
      </form>
    </section>

    <section class="grocery-section" data-section="Frozen">
      <div class="section-header">
        <h2>Frozen</h2>
        <button class="add-item-button" type="button">Add</button>
      </div>
      <div class="grocery-grid" data-grid="Frozen"></div>
      <form class="add-form" data-form="Frozen">
        <label>
          Ingredient
          <input type="text" name="name" placeholder="e.g. Frozen Peas" required>
        </label>
        <label>
          Amount
          <input type="text" name="amount" placeholder="1" required>
        </label>
        <label>
          Unit
          <select name="unit">
            <option value="bag">bag</option>
            <option value="box">box</option>
            <option value="each">each</option>
            <option value="lb">lb</option>
          </select>
        </label>
        <button class="add-submit" type="submit">Add Ingredient</button>
        <button class="add-cancel" type="button">Cancel</button>
      </form>
    </section>

    <section class="grocery-section" data-section="Personal Care">
      <div class="section-header">
        <h2>Personal Care</h2>
        <button class="add-item-button" type="button">Add</button>
      </div>
      <div class="grocery-grid" data-grid="Personal Care"></div>
      <form class="add-form" data-form="Personal Care">
        <label>
          Ingredient
          <input type="text" name="name" placeholder="e.g. Shampoo" required>
        </label>
        <label>
          Amount
          <input type="text" name="amount" placeholder="1" required>
        </label>
        <label>
          Unit
          <select name="unit">
            <option value="each">each</option>
            <option value="bottle">bottle</option>
            <option value="pack">pack</option>
          </select>
        </label>
        <button class="add-submit" type="submit">Add Ingredient</button>
        <button class="add-cancel" type="button">Cancel</button>
      </form>
    </section>

    <section class="grocery-section" data-section="Home Supplies">
      <div class="section-header">
        <h2>Home Supplies</h2>
        <button class="add-item-button" type="button">Add</button>
      </div>
      <div class="grocery-grid" data-grid="Home Supplies"></div>
      <form class="add-form" data-form="Home Supplies">
        <label>
          Ingredient
          <input type="text" name="name" placeholder="e.g. Dish Soap" required>
        </label>
        <label>
          Amount
          <input type="text" name="amount" placeholder="1" required>
        </label>
        <label>
          Unit
          <select name="unit">
            <option value="each">each</option>
            <option value="bottle">bottle</option>
            <option value="pack">pack</option>
          </select>
        </label>
        <button class="add-submit" type="submit">Add Ingredient</button>
        <button class="add-cancel" type="button">Cancel</button>
      </form>
    </section>

    <section class="grocery-section" data-section="Miscellaneous">
      <div class="section-header">
        <h2>Miscellaneous</h2>
        <button class="add-item-button" type="button">Add</button>
      </div>
      <div class="grocery-grid" data-grid="Miscellaneous"></div>
      <form class="add-form" data-form="Miscellaneous">
        <label>
          Ingredient
          <input type="text" name="name" placeholder="e.g. Candle" required>
        </label>
        <label>
          Amount
          <input type="text" name="amount" placeholder="1" required>
        </label>
        <label>
          Unit
          <select name="unit">
            <option value="each">each</option>
            <option value="pack">pack</option>
            <option value="box">box</option>
            <option value="bottle">bottle</option>
          </select>
        </label>
        <button class="add-submit" type="submit">Add Ingredient</button>
        <button class="add-cancel" type="button">Cancel</button>
      </form>
    </section>
  </div>
</section>

<script>
  const groceryState = {
    Produce: [
      { name: 'Apples', amount: 6, unit: 'each' },
      { name: 'Avocados', amount: 2, unit: 'each' },
      { name: 'Bell Peppers', amount: 3, unit: 'each' }
    ],
    Bakery: [
      { name: 'Bread', amount: 1, unit: 'loaf' }
    ],
    Meat: [],
    Pantry: [],
    Dairy: [],
    Frozen: [],
    'Personal Care': [],
    'Home Supplies': [],
    'Miscellaneous': []
  };

  const sectionOrder = ['Produce', 'Bakery', 'Meat', 'Pantry', 'Dairy', 'Frozen', 'Personal Care', 'Home Supplies', 'Miscellaneous'];

  const formatAmount = (amount, unit) => {
    const normalizedAmount = amount == null || amount === '' ? '1' : String(amount).trim();
    const normalizedUnit = unit && unit !== 'each' ? unit : '';
    return normalizedUnit ? `${normalizedAmount} ${normalizedUnit}` : normalizedAmount;
  };

  function renderSection(sectionName) {
    const grid = document.querySelector('[data-grid="' + sectionName + '"]');
    const section = document.querySelector('.grocery-section[data-section="' + sectionName + '"]');
    if (!grid) return;

    grid.innerHTML = '';
    const items = groceryState[sectionName] || [];

    if (!items.length) {
      const empty = document.createElement('div');
      empty.className = 'empty-state';
      empty.textContent = 'No items yet';
      grid.appendChild(empty);
      return;
    }

    items.forEach((item, itemIndex) => {
      const article = document.createElement('article');
      article.className = 'grocery-item';
      article.innerHTML = `
        <div class="item-content">
          <span class="item-name">${item.name}</span>
          <span class="item-amount">${formatAmount(item.amount, item.unit)}</span>
          <div class="edit-controls">
            <input type="text" value="${item.amount}" aria-label="Edit ${item.name} amount">
            <select aria-label="Edit ${item.name} unit">
              <option value="each" ${item.unit === 'each' ? 'selected' : ''}>each</option>
              <option value="oz" ${item.unit === 'oz' ? 'selected' : ''}>oz</option>
              <option value="lb" ${item.unit === 'lb' ? 'selected' : ''}>lb</option>
              <option value="bunch" ${item.unit === 'bunch' ? 'selected' : ''}>bunch</option>
              <option value="bag" ${item.unit === 'bag' ? 'selected' : ''}>bag</option>
              <option value="bottle" ${item.unit === 'bottle' ? 'selected' : ''}>bottle</option>
              <option value="loaf" ${item.unit === 'loaf' ? 'selected' : ''}>loaf</option>
              <option value="gal" ${item.unit === 'gal' ? 'selected' : ''}>gal</option>
              <option value="box" ${item.unit === 'box' ? 'selected' : ''}>box</option>
              <option value="pack" ${item.unit === 'pack' ? 'selected' : ''}>pack</option>
              <option value="can" ${item.unit === 'can' ? 'selected' : ''}>can</option>
              <option value="jar" ${item.unit === 'jar' ? 'selected' : ''}>jar</option>
            </select>
            <button class="save-toggle" type="button" aria-label="Save ${item.name}">Save</button>
            <button class="cancel-toggle" type="button" aria-label="Cancel editing ${item.name}">Cancel</button>
          </div>
        </div>
        <div class="item-actions">
          <button class="edit-toggle" type="button" aria-label="Edit ${item.name}">✎</button>
          <button class="remove-toggle" type="button" aria-label="Remove ${item.name}">−</button>
          <button class="check-toggle" type="button" aria-label="Check ${item.name}">✓</button>
          <button class="undo-toggle" type="button" aria-label="Undo ${item.name}">↺</button>
        </div>
      `;

      const checkToggle = article.querySelector('.check-toggle');
      const undoToggle = article.querySelector('.undo-toggle');
      const editToggle = article.querySelector('.edit-toggle');
      const cancelToggle = article.querySelector('.cancel-toggle');
      const saveToggle = article.querySelector('.save-toggle');
      const removeToggle = article.querySelector('.remove-toggle');
      const amountText = article.querySelector('.item-amount');
      const amountInput = article.querySelector('input[type="text"]');
      const unitSelect = article.querySelector('select');

      checkToggle.addEventListener('click', () => {
        article.classList.toggle('is-checked');
      });

      undoToggle.addEventListener('click', () => {
        article.classList.remove('is-checked');
      });

      editToggle.addEventListener('click', () => {
        article.classList.add('is-editing');
        amountInput.focus();
        amountInput.select();
      });

      cancelToggle.addEventListener('click', () => {
        article.classList.remove('is-editing');
        amountInput.value = item.amount;
        unitSelect.value = item.unit;
      });

      saveToggle.addEventListener('click', () => {
        const nextAmount = (amountInput.value || '').trim();
        const nextUnit = unitSelect.value || 'each';
        if (nextAmount) {
          item.amount = nextAmount;
          item.unit = nextUnit;
          amountText.textContent = formatAmount(nextAmount, nextUnit);
        }
        article.classList.remove('is-editing');
      });

      removeToggle.addEventListener('click', () => {
        groceryState[sectionName].splice(itemIndex, 1);
        renderSection(sectionName);
      });

      grid.appendChild(article);
    });
  }

  function renderAllSections() {
    sectionOrder.forEach(renderSection);
  }

  document.querySelectorAll('.add-item-button').forEach((button) => {
    button.addEventListener('click', () => {
      const section = button.closest('.grocery-section');
      section.classList.add('is-adding');
      const input = section.querySelector('input[name="name"]');
      if (input) input.focus();
    });
  });

  document.querySelectorAll('.add-cancel').forEach((button) => {
    button.addEventListener('click', () => {
      const section = button.closest('.grocery-section');
      section.classList.remove('is-adding');
      section.querySelector('form').reset();
    });
  });

  document.querySelectorAll('.add-form').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const sectionName = form.dataset.form;
      const formData = new FormData(form);
      const name = (formData.get('name') || '').toString().trim();
      const amount = (formData.get('amount') || '').toString().trim();
      const unit = (formData.get('unit') || 'each').toString();

      if (!name || !amount) return;

      const list = groceryState[sectionName] || [];
      list.push({
        name,
        amount,
        unit
      });
      groceryState[sectionName] = list;
      form.reset();
      form.closest('.grocery-section').classList.remove('is-adding');
      renderSection(sectionName);
    });
  });

  renderAllSections();
</script>
