// scripts/render-products.js

fetch('data/furniture.json')
  .then(res => res.json())
  .then(products => {
    const grid     = document.getElementById('product-grid');
    const category = grid.dataset.category;             // e.g. "Electronics"
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
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">${product.name}</h5>
            <p class="card-text">${product.description}</p>
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
    });
  })
  .catch(err => console.error('❌ Failed to load product data:', err));
