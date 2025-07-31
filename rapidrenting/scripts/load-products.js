fetch('data/furniture.json')
  .then(res => res.json())
  .then(products => {
    const grid = document.getElementById('product-grid');

    products.forEach((product, index) => {
      const col = document.createElement('div');
      col.className = 'col-md-4 col-lg-4 d-flex align-items-stretch';

      const swiperId = `swiper-${index}`;

      const swiperSlides = product.images.map(img => `
        <div class="swiper-slide">
          <img src="${img}" class="card-img-top" alt="${product.name}">
        </div>
      `).join('');

      col.innerHTML = `
        <div class="product-card card shadow-sm w-100">
          <div class="swiper ${swiperId}">
            <div class="swiper-wrapper">
              ${swiperSlides}
            </div>
            <div class="swiper-pagination"></div>
            <div class="swiper-button-next"></div>
            <div class="swiper-button-prev"></div>
          </div>
          <div class="card-body">
            <h5 class="card-title">${product.name}</h5>
            <p class="card-text">${product.description}</p>
          </div>
        </div>
      `;

      grid.appendChild(col);

      // Initialize Swiper individually per card
      new Swiper(`.${swiperId}`, {
        loop: true,
        pagination: {
          el: `.${swiperId} .swiper-pagination`,
          clickable: true
        },
        navigation: {
          nextEl: `.${swiperId} .swiper-button-next`,
          prevEl: `.${swiperId} .swiper-button-prev`
        }
      });
    });
  })
  .catch(err => console.error('❌ Failed to load product data:', err));
