// scripts/render-products.js

fetch('data/furniture.json')
  .then(res => res.json())
  .then(products => {
    const grid     = document.getElementById('product-grid');
    const category = grid.dataset.category;             // e.g. "Dining Room"
    const items    = products.filter(p => p.category === category);

    items.forEach((product, i) => {
      // 1) Column wrapper (Bootstrap row-cols handles 3-across)
      const col = document.createElement('div');
      col.className = 'col';

      // 2) Unique Swiper instance selector
      const swiperClass = `swiper-${category.toLowerCase().replace(/\s+/g,'-')}-${i}`;

      // 3) Build slides
      const slides = product.images.map(url => `
        <div class="swiper-slide">
          <img src="${url}" class="card-img-top" alt="${product.name}">
        </div>
      `).join('');

      // 4) Inject card + swiper markup
      col.innerHTML = `
        <div class="product-card card h-100">
          <div class="swiper ${swiperClass}">
            <div class="swiper-wrapper">
              ${slides}
            </div>
            <div class="swiper-pagination"></div>
            <div class="swiper-button-next"></div>
            <div class="swiper-button-prev"></div>
          </div>
          <div class="card-body d-flex flex-column" style="cursor: pointer;">
            <h5 class="card-title mb-2">${product.name}</h5>
            <p class="card-text flex-grow-1">${product.description}</p>
          </div>
        </div>
      `;
      grid.appendChild(col);

      // 5) Initialize this Swiper
      new Swiper(`.${swiperClass}`, {
        loop: true,
        pagination: {
          el: `.${swiperClass} .swiper-pagination`,
          clickable: true
        },
        navigation: {
          nextEl: `.${swiperClass} .swiper-button-next`,
          prevEl: `.${swiperClass} .swiper-button-prev`
        }
      });

      // 6) Modal click handler on text portion only
      const textEl = col.querySelector('.product-card .card-body');
      textEl.addEventListener('click', event => {
        event.stopPropagation();  // Prevent interfering with Swiper clicks
        document.getElementById('productModalLabel').textContent = product.name;
        document.getElementById('modal-description').textContent = product.description;
        document.getElementById('modal-sku').textContent = product.sku;
        document.getElementById('modal-brand').textContent = product.brand;
        document.getElementById('modal-category').textContent = product.category;
        const modal = new bootstrap.Modal(document.getElementById('productModal'));
        modal.show();
      });
    });
  })
  .catch(err => console.error('❌ Failed to load product data:', err));
