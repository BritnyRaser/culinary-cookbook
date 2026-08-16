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

  .grocery-section h2 {
    margin: 0 0 0.9rem;
    color: #0e5870;
    font-size: 1.3rem;
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

  .grocery-thumb {
    width: 56px;
    height: 56px;
    object-fit: cover;
    border-radius: 14px;
    flex-shrink: 0;
    border: 1px solid rgba(18, 53, 74, 0.08);
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
  .cancel-toggle {
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
  .undo-toggle {
    background: #edf8fb;
    border: 1px solid #d1eaf0;
    color: #0f5a70;
    border-radius: 999px;
    padding: 0.36rem 0.6rem;
    font-size: 0.7rem;
    font-weight: 700;
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

  .grocery-item input[type="text"] {
    width: 90px;
    border: 1px solid #cfe8ee;
    border-radius: 10px;
    background: #ffffff;
    color: #173d52;
    padding: 0.35rem 0.45rem;
    font: inherit;
    font-size: 0.8rem;
  }

  .save-toggle {
    background: #0f766e;
    border-color: #0f766e;
    color: #ffffff;
  }

  .cancel-toggle {
    background: #ffffff;
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
    <section class="grocery-section">
      <h2>Produce</h2>
      <div class="grocery-grid">
        <article class="grocery-item" data-name="Apples">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?auto=format&fit=crop&w=220&q=80" alt="Apples">
          <div class="item-content">
            <span class="item-name">Apples</span>
            <span class="item-amount">6</span>
            <div class="edit-controls">
              <input type="text" value="6" aria-label="Edit Apples amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Apples">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>

        <article class="grocery-item" data-name="Avocados">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1519162808019-7de1683fa2ad?auto=format&fit=crop&w=220&q=80" alt="Avocados">
          <div class="item-content">
            <span class="item-name">Avocados</span>
            <span class="item-amount">2</span>
            <div class="edit-controls">
              <input type="text" value="2" aria-label="Edit Avocados amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Avocados">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>

        <article class="grocery-item" data-name="Bell Peppers">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?auto=format&fit=crop&w=220&q=80" alt="Bell Peppers">
          <div class="item-content">
            <span class="item-name">Bell Peppers</span>
            <span class="item-amount">3</span>
            <div class="edit-controls">
              <input type="text" value="3" aria-label="Edit Bell Peppers amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Bell Peppers">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>

        <article class="grocery-item" data-name="Carrots">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1447175008436-5d4f2a3c8fdd?auto=format&fit=crop&w=220&q=80" alt="Carrots">
          <div class="item-content">
            <span class="item-name">Carrots</span>
            <span class="item-amount">1 lb</span>
            <div class="edit-controls">
              <input type="text" value="1 lb" aria-label="Edit Carrots amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Carrots">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>
      </div>
    </section>

    <section class="grocery-section">
      <h2>Dairy</h2>
      <div class="grocery-grid">
        <article class="grocery-item" data-name="Cheddar Cheese">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?auto=format&fit=crop&w=220&q=80" alt="Cheddar Cheese">
          <div class="item-content">
            <span class="item-name">Cheddar Cheese</span>
            <span class="item-amount">8 oz</span>
            <div class="edit-controls">
              <input type="text" value="8 oz" aria-label="Edit Cheddar Cheese amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Cheddar Cheese">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>

        <article class="grocery-item" data-name="Greek Yogurt">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=220&q=80" alt="Greek Yogurt">
          <div class="item-content">
            <span class="item-name">Greek Yogurt</span>
            <span class="item-amount">32 oz</span>
            <div class="edit-controls">
              <input type="text" value="32 oz" aria-label="Edit Greek Yogurt amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Greek Yogurt">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>

        <article class="grocery-item" data-name="Milk">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1550583724-b2692b85b150?auto=format&fit=crop&w=220&q=80" alt="Milk">
          <div class="item-content">
            <span class="item-name">Milk</span>
            <span class="item-amount">1 gal</span>
            <div class="edit-controls">
              <input type="text" value="1 gal" aria-label="Edit Milk amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Milk">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>
      </div>
    </section>

    <section class="grocery-section">
      <h2>Pantry</h2>
      <div class="grocery-grid">
        <article class="grocery-item" data-name="Basil">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?auto=format&fit=crop&w=220&q=80" alt="Basil">
          <div class="item-content">
            <span class="item-name">Basil</span>
            <span class="item-amount">1 bunch</span>
            <div class="edit-controls">
              <input type="text" value="1 bunch" aria-label="Edit Basil amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Basil">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>

        <article class="grocery-item" data-name="Brown Rice">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1586201375761-83865001e31f?auto=format&fit=crop&w=220&q=80" alt="Brown Rice">
          <div class="item-content">
            <span class="item-name">Brown Rice</span>
            <span class="item-amount">2 bags</span>
            <div class="edit-controls">
              <input type="text" value="2 bags" aria-label="Edit Brown Rice amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Brown Rice">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>

        <article class="grocery-item" data-name="Olive Oil">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1470337458703-46ad1756a187?auto=format&fit=crop&w=220&q=80" alt="Olive Oil">
          <div class="item-content">
            <span class="item-name">Olive Oil</span>
            <span class="item-amount">1 bottle</span>
            <div class="edit-controls">
              <input type="text" value="1 bottle" aria-label="Edit Olive Oil amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Olive Oil">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>
      </div>
    </section>

    <section class="grocery-section">
      <h2>Meat</h2>
      <div class="grocery-grid">
        <article class="grocery-item" data-name="Chicken Breast">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?auto=format&fit=crop&w=220&q=80" alt="Chicken Breast">
          <div class="item-content">
            <span class="item-name">Chicken Breast</span>
            <span class="item-amount">1.5 lb</span>
            <div class="edit-controls">
              <input type="text" value="1.5 lb" aria-label="Edit Chicken Breast amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Chicken Breast">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>

        <article class="grocery-item" data-name="Ground Turkey">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1615937691194-97dbd3f3dc29?auto=format&fit=crop&w=220&q=80" alt="Ground Turkey">
          <div class="item-content">
            <span class="item-name">Ground Turkey</span>
            <span class="item-amount">1 lb</span>
            <div class="edit-controls">
              <input type="text" value="1 lb" aria-label="Edit Ground Turkey amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Ground Turkey">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>
      </div>
    </section>

    <section class="grocery-section">
      <h2>Bakery</h2>
      <div class="grocery-grid">
        <article class="grocery-item" data-name="Bread">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=220&q=80" alt="Bread">
          <div class="item-content">
            <span class="item-name">Bread</span>
            <span class="item-amount">1 loaf</span>
            <div class="edit-controls">
              <input type="text" value="1 loaf" aria-label="Edit Bread amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Bread">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>

        <article class="grocery-item" data-name="Buns">
          <img class="grocery-thumb" src="https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=220&q=80" alt="Buns">
          <div class="item-content">
            <span class="item-name">Buns</span>
            <span class="item-amount">8</span>
            <div class="edit-controls">
              <input type="text" value="8" aria-label="Edit Buns amount">
              <button class="save-toggle" type="button">Save</button>
              <button class="cancel-toggle" type="button">Cancel</button>
            </div>
          </div>
          <div class="item-actions">
            <button class="edit-toggle" type="button">Edit</button>
            <button class="check-toggle" type="button" aria-label="Check Buns">✓</button>
            <button class="undo-toggle" type="button">Undo</button>
          </div>
        </article>
      </div>
    </section>
  </div>
</section>

<script>
  document.querySelectorAll('.grocery-item').forEach((item) => {
    const checkToggle = item.querySelector('.check-toggle');
    const undoToggle = item.querySelector('.undo-toggle');
    const editToggle = item.querySelector('.edit-toggle');
    const cancelToggle = item.querySelector('.cancel-toggle');
    const saveToggle = item.querySelector('.save-toggle');
    const amountText = item.querySelector('.item-amount');
    const amountInput = item.querySelector('input[type="text"]');

    const setCheckedState = (checked) => {
      item.classList.toggle('is-checked', checked);
      item.classList.toggle('is-editing', false);
    };

    checkToggle.addEventListener('click', () => {
      const checked = !item.classList.contains('is-checked');
      setCheckedState(checked);
    });

    undoToggle.addEventListener('click', () => {
      setCheckedState(false);
    });

    editToggle.addEventListener('click', () => {
      item.classList.add('is-editing');
      amountInput.focus();
      amountInput.select();
    });

    cancelToggle.addEventListener('click', () => {
      item.classList.remove('is-editing');
      amountInput.value = amountText.textContent.trim();
    });

    saveToggle.addEventListener('click', () => {
      const nextValue = (amountInput.value || '').trim();
      if (nextValue) {
        amountText.textContent = nextValue;
      }
      item.classList.remove('is-editing');
    });
  });
</script>
