document.addEventListener('DOMContentLoaded', () => {
  initProductTabs();
  hydrateMockContent();
});

function initProductTabs() {
  const tabs = document.querySelectorAll('[data-product-tab]');
  const panels = document.querySelectorAll('[data-product-panel]');

  if (!tabs.length) return;

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-product-tab');

      tabs.forEach((t) => t.classList.remove('active'));
      tab.classList.add('active');

      panels.forEach((panel) => {
        panel.classList.toggle('hidden', panel.getAttribute('data-product-panel') !== target);
      });
    });
  });
}

async function hydrateMockContent() {
  try {
    const response = await fetch('data/mock-data.json', { cache: 'no-store' });
    if (!response.ok) return;

    const data = await response.json();
    if (data.heroDeals) {
      injectHeroDeals(data.heroDeals);
    }
    if (data.destinations) {
      injectDestinations(data.destinations);
    }
    if (data.recommendations) {
      injectRecommendations(data.recommendations);
    }
  } catch (error) {
    console.warn('Unable to hydrate mock data', error);
  }
}

function injectHeroDeals(deals) {
  const host = document.querySelector('[data-inject="hero-deals"]');
  if (!host) return;
  host.classList.add('injected');

  deals.forEach((deal) => {
    const article = document.createElement('article');
    article.className = 'coupon-card border-2 border-dashed border-yellow-300';
    article.innerHTML = `
      <div class="tag">${deal.tag ?? ''}</div>
      <h3 class="text-lg font-semibold">${deal.title ?? ''}</h3>
      <button class="ghost-btn">${deal.cta ?? 'View'}</button>
    `;
    host.appendChild(article);
  });
}

function injectDestinations(items) {
  const host = document.querySelector('[data-inject="destination-grid"]');
  if (!host) return;
  host.classList.add('injected');

  items.forEach((item) => {
    const article = document.createElement('article');
    article.className = 'destination-card ring-2 ring-yellow-200';
    article.innerHTML = `
      <img src="${item.image}" alt="${item.title}">
      <div>
        <h3>${item.title}</h3>
        <p>${item.subtitle ?? ''}</p>
      </div>
    `;
    host.appendChild(article);
  });
}

function injectRecommendations(items) {
  const host = document.querySelector('[data-inject="recommendation-grid"]');
  if (!host) return;
  host.classList.add('injected');

  items.forEach((item) => {
    const card = document.createElement('article');
    card.className = 'recommend-card ring-2 ring-yellow-200';
    card.innerHTML = `
      ${item.badge ? `<div class="badge">${item.badge}</div>` : ''}
      <img src="${item.image}" alt="${item.title}">
      <div class="card-body">
        <p class="eyebrow">${item.title}</p>
        <p class="caption">${item.meta ?? ''}</p>
      </div>
    `;
    host.appendChild(card);
  });
}
