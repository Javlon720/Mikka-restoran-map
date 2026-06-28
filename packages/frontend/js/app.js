// JDU RestoReviews Client Application

let currentUser = null;
let restaurants = [];
let selectedRestaurantId = null;
let activeStarRating = 0;

// Leaflet Map variables
let mainMap = null;
let mainMarkers = [];
let modalMap = null;
let modalMarker = null;

// Default map center (Tashkent)
const DEFAULT_CENTER = [41.311081, 69.279737];
const DEFAULT_ZOOM = 12;

document.addEventListener('DOMContentLoaded', () => {
  checkAuthState();
  initLanguage();
  initMainMap();
  loadRestaurants();
  setupEventListeners();
  initGoogleAuth();
  initAIChat();
});

// Toast System
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let icon = 'fa-info-circle';
  if (type === 'success') icon = 'fa-check-circle';
  if (type === 'danger') icon = 'fa-exclamation-circle';
  if (type === 'warning') icon = 'fa-exclamation-triangle';

  toast.innerHTML = `
    <i class="fa-solid ${icon} toast-icon"></i>
    <span>${message}</span>
  `;
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}

// Authentication Check
function checkAuthState() {
  const userStr = localStorage.getItem('jdu_user');
  
  const authControls = document.getElementById('auth-controls');
  const addRestTrigger = document.getElementById('btn-add-restaurant-trigger');
  
  if (userStr) {
    currentUser = JSON.parse(userStr);
    
    // Greeting display
    const welcomeText = window.i18n.get('welcomeUser', { username: currentUser.username });
    authControls.innerHTML = `
      <span class="user-greeting">${welcomeText}</span>
      <button class="btn btn-outline btn-sm" id="btn-logout" data-i18n="btnLogout">${window.i18n.get('btnLogout')}</button>
    `;
    
    document.getElementById('btn-logout').addEventListener('click', logout);

    // Show Add Restaurant button for admins
    if (currentUser.role === 'admin') {
      addRestTrigger.classList.remove('hidden');
    } else {
      addRestTrigger.classList.add('hidden');
    }
  } else {
    currentUser = null;
    authControls.innerHTML = `
      <button class="btn btn-outline btn-sm" id="btn-show-login" data-i18n="btnLogin">${window.i18n.get('btnLogin')}</button>
      <button class="btn btn-primary btn-sm" id="btn-show-register" data-i18n="btnRegister">${window.i18n.get('btnRegister')}</button>
    `;
    addRestTrigger.classList.add('hidden');
    
    document.getElementById('btn-show-login').addEventListener('click', () => openAuthModal('login'));
    document.getElementById('btn-show-register').addEventListener('click', () => openAuthModal('register'));
  }
}

async function logout() {
  try {
    await window.api.logout();
  } catch (error) {
    console.error('Backend logout failed:', error);
  }
  localStorage.removeItem('jdu_token');
  localStorage.removeItem('jdu_user');
  currentUser = null;
  checkAuthState();
  loadRestaurants(); // Reload to remove edit/delete actions
  showToast(window.i18n.get('alertSuccess'), 'success');
  if (typeof clearAIChatHistory === 'function') {
    clearAIChatHistory();
  }
}

// Language Driver
function initLanguage() {
  window.i18n.apply();
  document.getElementById('active-lang-text').textContent = window.i18n.current().toUpperCase();
}

function changeLanguage(lang) {
  window.i18n.set(lang);
  document.getElementById('active-lang-text').textContent = lang.toUpperCase();
  document.getElementById('lang-dropdown').classList.remove('show');
  
  // Re-translate dynamic pieces
  checkAuthState();
  loadRestaurants();
  if (selectedRestaurantId) {
    viewRestaurantDetails(selectedRestaurantId);
  }
  if (typeof updateAIChatLanguage === 'function') {
    updateAIChatLanguage();
  }
}

// Event Listeners Setup
function setupEventListeners() {
  // Lang dropdown toggler
  const langMenuBtn = document.getElementById('lang-menu-btn');
  const langDropdown = document.getElementById('lang-dropdown');
  langMenuBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    langDropdown.classList.toggle('show');
  });
  
  document.addEventListener('click', () => {
    langDropdown.classList.remove('show');
  });

  // Search
  document.getElementById('search-btn').addEventListener('click', searchRestaurants);
  document.getElementById('search-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchRestaurants();
  });

  // Modals closing
  document.getElementById('close-auth-modal').addEventListener('click', () => closeModal('modal-auth'));
  document.getElementById('close-rest-modal').addEventListener('click', () => closeModal('modal-restaurant'));
  document.getElementById('btn-cancel-restaurant').addEventListener('click', () => closeModal('modal-restaurant'));
  document.getElementById('close-details-modal').addEventListener('click', () => closeModal('modal-details'));

  // Auth toggle links
  document.getElementById('toggle-to-register').addEventListener('click', (e) => {
    e.preventDefault();
    switchAuthTab('register');
  });
  document.getElementById('toggle-to-login').addEventListener('click', (e) => {
    e.preventDefault();
    switchAuthTab('login');
  });

  // Forms submit
  document.getElementById('form-login').addEventListener('submit', handleLoginSubmit);
  document.getElementById('form-register').addEventListener('submit', handleRegisterSubmit);
  document.getElementById('form-restaurant').addEventListener('submit', handleRestaurantSubmit);
  document.getElementById('form-review').addEventListener('submit', handleReviewSubmit);

  // Trigger Add Restaurant
  document.getElementById('btn-add-restaurant-trigger').addEventListener('click', () => openRestaurantFormModal());

  // Logo branding clicks
  document.getElementById('logo-link').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('search-input').value = '';
    loadRestaurants();
  });

  // Star Ratings Input Logic
  const stars = document.querySelectorAll('.star-btn');
  stars.forEach(star => {
    star.addEventListener('click', () => {
      const rating = parseInt(star.getAttribute('data-value'), 10);
      setStarRating(rating);
    });
    star.addEventListener('mouseover', () => {
      const rating = parseInt(star.getAttribute('data-value'), 10);
      highlightStars(rating);
    });
    star.addEventListener('mouseout', () => {
      highlightStars(activeStarRating);
    });
  });

  document.getElementById('btn-cancel-review-edit').addEventListener('click', () => {
    resetReviewForm();
  });
}

// Stars display helper
function setStarRating(rating) {
  activeStarRating = rating;
  document.getElementById('review-rating').value = rating;
  highlightStars(rating);
}

function highlightStars(rating) {
  const stars = document.querySelectorAll('.star-btn');
  stars.forEach(star => {
    const val = parseInt(star.getAttribute('data-value'), 10);
    if (val <= rating) {
      star.classList.remove('fa-regular');
      star.classList.add('fa-solid');
    } else {
      star.classList.remove('fa-solid');
      star.classList.add('fa-regular');
    }
  });
}

// Maps Initializer
function initMainMap() {
  mainMap = L.map('main-map').setView(DEFAULT_CENTER, DEFAULT_ZOOM);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; CartoDB',
    subdomains: 'abcd',
    maxZoom: 20
  }).addTo(mainMap);
}

// Main map loading markers
function updateMainMapMarkers() {
  // Clear previous markers
  mainMarkers.forEach(m => mainMap.removeLayer(m));
  mainMarkers = [];

  restaurants.forEach(rest => {
    if (rest.lat && rest.lng) {
      const marker = L.marker([rest.lat, rest.lng]).addTo(mainMap);
      
      const popupHtml = `
        <div style="color: #1f2937; font-family: sans-serif; min-width: 150px;">
          <h4 style="margin: 0 0 4px 0; font-size: 0.95rem;">${rest.name}</h4>
          <p style="margin: 0 0 6px 0; font-size: 0.75rem; color: #6b7280;">${rest.cuisine}</p>
          <button onclick="viewRestaurantDetails(${rest.id})" style="background: #6366f1; border: none; color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; cursor: pointer; width: 100%;">
            View details
          </button>
        </div>
      `;
      
      marker.bindPopup(popupHtml);
      mainMarkers.push(marker);
    }
  });
}

// Load and Render Restaurants
async function loadRestaurants() {
  try {
    const searchVal = document.getElementById('search-input').value;
    const resData = await window.api.getRestaurants(searchVal);
    restaurants = resData.data;

    // Fetch review averages on the fly for each restaurant
    for (let r of restaurants) {
      const revData = await window.api.getReviews(r.id);
      r.reviews = revData.data;
      if (r.reviews.length > 0) {
        const sum = r.reviews.reduce((acc, item) => acc + item.rating, 0);
        r.avgRating = (sum / r.reviews.length).toFixed(1);
      } else {
        r.avgRating = null;
      }
    }

    renderRestaurantsList();
    updateMainMapMarkers();
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

function searchRestaurants() {
  loadRestaurants();
}

function renderRestaurantsList() {
  const container = document.getElementById('restaurants-grid');
  container.innerHTML = '';

  if (restaurants.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-muted);">
        <i class="fa-solid fa-store-slash" style="font-size: 3rem; margin-bottom: 12px; display: block;"></i>
        <p>No restaurants found.</p>
      </div>
    `;
    return;
  }

  restaurants.forEach(rest => {
    const card = document.createElement('div');
    card.className = 'restaurant-card';
    card.addEventListener('click', (e) => {
      // Don't open if clicked on edit/delete button
      if (e.target.closest('.btn-sm')) return;
      viewRestaurantDetails(rest.id);
    });

    const imgUrl = rest.imageUrl ? rest.imageUrl : 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&q=80&w=300';
    
    // Rating star generation
    let starsHtml = '<i class="fa-regular fa-star"></i>'.repeat(5);
    let ratingValText = 'N/A';
    if (rest.avgRating) {
      ratingValText = rest.avgRating;
      const fullStars = Math.floor(rest.avgRating);
      const halfStar = rest.avgRating - fullStars >= 0.5 ? 1 : 0;
      const emptyStars = 5 - fullStars - halfStar;
      starsHtml = '<i class="fa-solid fa-star"></i>'.repeat(fullStars) + 
                  (halfStar ? '<i class="fa-solid fa-star-half-stroke"></i>' : '') + 
                  '<i class="fa-regular fa-star"></i>'.repeat(emptyStars);
    }

    // Admin controls on card
    let adminControls = '';
    if (currentUser && currentUser.role === 'admin') {
      adminControls = `
        <div class="restaurant-card-actions">
          <button class="btn btn-outline btn-sm" onclick="openRestaurantFormModal(${rest.id})">
            <i class="fa-solid fa-pen"></i>
          </button>
          <button class="btn btn-danger btn-sm" onclick="deleteRestaurant(${rest.id})">
            <i class="fa-solid fa-trash"></i>
          </button>
        </div>
      `;
    }

    card.innerHTML = `
      <img src="${imgUrl}" class="restaurant-card-img" alt="${rest.name}">
      <div class="restaurant-card-body">
        <div>
          <div class="restaurant-card-header">
            <h3 class="restaurant-card-title">${rest.name}</h3>
            <span class="restaurant-card-cuisine">${rest.cuisine}</span>
          </div>
          <div class="restaurant-card-rating">
            <span class="rating-stars">${starsHtml}</span>
            <span class="rating-number">${ratingValText}</span>
            <span class="rating-count">(${window.i18n.get('reviewsCount', { count: rest.reviews.length })})</span>
          </div>
          <p class="restaurant-card-desc">${rest.description}</p>
        </div>
        <div class="restaurant-card-footer">
          <span class="restaurant-card-address"><i class="fa-solid fa-location-dot"></i>${rest.address}</span>
          ${adminControls}
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

// Modal handling helper
function openModal(id) {
  document.getElementById(id).classList.add('show');
  document.body.style.overflow = 'hidden';
}

function closeModal(id) {
  document.getElementById(id).classList.remove('show');
  document.body.style.overflow = '';
}

// Auth Tab switching
function openAuthModal(tab = 'login') {
  openModal('modal-auth');
  switchAuthTab(tab);
  if (googleAuthInitialized) {
    renderGoogleButton();
  }
}

function switchAuthTab(tab) {
  const tabLogin = document.getElementById('auth-tab-login');
  const tabRegister = document.getElementById('auth-tab-register');
  
  if (tab === 'login') {
    tabLogin.classList.remove('hidden');
    tabRegister.classList.add('hidden');
  } else {
    tabLogin.classList.add('hidden');
    tabRegister.classList.remove('hidden');
  }
}

// Auth Forms Actions
async function handleLoginSubmit(e) {
  e.preventDefault();
  const emailOrUsername = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  try {
    const res = await window.api.login(emailOrUsername, password);
    localStorage.setItem('jdu_user', JSON.stringify(res.user));
    
    closeModal('modal-auth');
    showToast(window.i18n.get('alertSuccess'), 'success');
    checkAuthState();
    loadRestaurants();
    if (typeof clearAIChatHistory === 'function') {
      clearAIChatHistory();
    }
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

async function handleRegisterSubmit(e) {
  e.preventDefault();
  const username = document.getElementById('register-username').value;
  const email = document.getElementById('register-email').value;
  const password = document.getElementById('register-password').value;

  try {
    await window.api.register(username, email, password);
    showToast('Registration successful! Please login.', 'success');
    switchAuthTab('login');
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

// Google Auth Actions
let googleAuthInitialized = false;
let googleButtonRendered = false;

async function initGoogleAuth() {
  if (typeof google === 'undefined' || !google.accounts || !google.accounts.id) {
    setTimeout(initGoogleAuth, 100);
    return;
  }
  
  try {
    const res = await window.api.getConfig();
    if (res.googleClientId && res.googleClientId.trim() !== '') {
      google.accounts.id.initialize({
        client_id: res.googleClientId,
        callback: handleGoogleLogin
      });
      googleAuthInitialized = true;
      
      // If modal is already open, render it immediately
      if (document.getElementById('modal-auth').classList.contains('show')) {
        renderGoogleButton();
      }
    } else {
      console.warn('Google client ID is placeholder or empty. Google login disabled.');
    }
  } catch (err) {
    console.error('Google auth init failed:', err);
  }
}

function renderGoogleButton() {
  if (!googleAuthInitialized || googleButtonRendered) return;
  const btnContainer = document.getElementById('google-signin-btn');
  if (btnContainer) {
    google.accounts.id.renderButton(
      btnContainer,
      { theme: 'outline', size: 'large', width: 300 }
    );
  }
  const signupBtnContainer = document.getElementById('google-signup-btn');
  if (signupBtnContainer) {
    google.accounts.id.renderButton(
      signupBtnContainer,
      { theme: 'outline', size: 'large', width: 300 }
    );
  }
  googleButtonRendered = true;
}

async function handleGoogleLogin(response) {
  try {
    const res = await window.api.googleLogin(response.credential);
    localStorage.setItem('jdu_user', JSON.stringify(res.user));
    
    closeModal('modal-auth');
    showToast(window.i18n.get('alertSuccess'), 'success');
    checkAuthState();
    loadRestaurants();
    if (typeof clearAIChatHistory === 'function') {
      clearAIChatHistory();
    }
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

// Restaurant CRUD Admin actions
async function openRestaurantFormModal(editId = null) {
  openModal('modal-restaurant');
  const title = document.getElementById('rest-modal-title');
  const form = document.getElementById('form-restaurant');
  form.reset();

  document.getElementById('coords-lat').textContent = '-';
  document.getElementById('coords-lng').textContent = '-';
  document.getElementById('rest-lat').value = '';
  document.getElementById('rest-lng').value = '';

  // Initialize modal map inside form
  setTimeout(() => {
    if (!modalMap) {
      modalMap = L.map('modal-map').setView(DEFAULT_CENTER, DEFAULT_ZOOM);
      L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; CartoDB',
        maxZoom: 20
      }).addTo(modalMap);

      modalMap.on('click', (e) => {
        const { lat, lng } = e.latlng;
        setFormCoordinates(lat, lng);
      });
    } else {
      modalMap.setView(DEFAULT_CENTER, DEFAULT_ZOOM);
      modalMap.invalidateSize();
      if (modalMarker) {
        modalMap.removeLayer(modalMarker);
        modalMarker = null;
      }
    }
  }, 300);

  if (editId) {
    title.textContent = window.i18n.get('btnEditRestaurant');
    try {
      const res = await window.api.getRestaurant(editId);
      const rest = res.data;
      
      document.getElementById('edit-rest-id').value = rest.id;
      document.getElementById('rest-name').value = rest.name;
      document.getElementById('rest-cuisine').value = rest.cuisine;
      document.getElementById('rest-address').value = rest.address;
      document.getElementById('rest-description').value = rest.description;
      
      if (rest.lat && rest.lng) {
        setTimeout(() => {
          setFormCoordinates(rest.lat, rest.lng);
          modalMap.setView([rest.lat, rest.lng], 14);
        }, 400);
      }
    } catch (error) {
      showToast(error.message, 'danger');
    }
  } else {
    title.textContent = window.i18n.get('btnAddRestaurant');
    document.getElementById('edit-rest-id').value = '';
  }
}

function setFormCoordinates(lat, lng) {
  document.getElementById('coords-lat').textContent = lat.toFixed(6);
  document.getElementById('coords-lng').textContent = lng.toFixed(6);
  document.getElementById('rest-lat').value = lat;
  document.getElementById('rest-lng').value = lng;

  if (modalMarker) {
    modalMarker.setLatLng([lat, lng]);
  } else {
    modalMarker = L.marker([lat, lng], { draggable: true }).addTo(modalMap);
    modalMarker.on('dragend', (e) => {
      const { lat, lng } = e.target.getLatLng();
      setFormCoordinates(lat, lng);
    });
  }
}

async function handleRestaurantSubmit(e) {
  e.preventDefault();
  
  const editId = document.getElementById('edit-rest-id').value;
  const name = document.getElementById('rest-name').value;
  const cuisine = document.getElementById('rest-cuisine').value;
  const address = document.getElementById('rest-address').value;
  const description = document.getElementById('rest-description').value;
  const fileInput = document.getElementById('rest-image');
  const lat = document.getElementById('rest-lat').value;
  const lng = document.getElementById('rest-lng').value;

  const formData = new FormData();
  formData.append('name', name);
  formData.append('cuisine', cuisine);
  formData.append('address', address);
  formData.append('description', description);
  if (fileInput.files[0]) {
    formData.append('image', fileInput.files[0]);
  }
  if (lat && lng) {
    formData.append('lat', lat);
    formData.append('lng', lng);
  }

  try {
    if (editId) {
      await window.api.updateRestaurant(editId, formData);
    } else {
      await window.api.createRestaurant(formData);
    }
    
    closeModal('modal-restaurant');
    showToast(window.i18n.get('alertSuccess'), 'success');
    loadRestaurants();
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

async function deleteRestaurant(id) {
  if (!confirm(window.i18n.get('alertDeleteConfirm'))) return;
  try {
    await window.api.deleteRestaurant(id);
    showToast(window.i18n.get('alertSuccess'), 'success');
    loadRestaurants();
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

// View Details & Reviews list
async function viewRestaurantDetails(id) {
  selectedRestaurantId = id;
  openModal('modal-details');
  resetReviewForm();

  document.getElementById('review-restaurant-id').value = id;

  try {
    const res = await window.api.getRestaurant(id);
    const rest = res.data;
    
    const detailsContainer = document.getElementById('details-view');
    const fallbackImage = 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&q=80&w=600';
    const imgUrl = rest.imageUrl ? rest.imageUrl : fallbackImage;

    detailsContainer.innerHTML = `
      <div class="details-header">
        <img src="${imgUrl}" class="details-image" alt="${rest.name}">
        <div class="details-meta">
          <h2 class="details-title">${rest.name}</h2>
          <span class="details-cuisine">${rest.cuisine}</span>
          <div class="details-info-row">
            <i class="fa-solid fa-location-dot"></i>
            <span><strong>${window.i18n.get('addressLabel')}:</strong> ${rest.address}</span>
          </div>
          ${rest.lat ? `
            <div class="details-info-row">
              <i class="fa-solid fa-map"></i>
              <span><strong>GPS:</strong> ${rest.lat.toFixed(5)}, ${rest.lng.toFixed(5)}</span>
            </div>
          ` : ''}
        </div>
      </div>
      <div class="details-desc-box">
        <h4>${window.i18n.get('detailsLabel')}</h4>
        <p>${rest.description}</p>
      </div>
    `;

    // Load reviews
    loadReviewsList();

  } catch (error) {
    showToast(error.message, 'danger');
    closeModal('modal-details');
  }
}

async function loadReviewsList() {
  const container = document.getElementById('reviews-list-container');
  container.innerHTML = `<div style="text-align:center; padding: 20px;"><i class="fa-solid fa-spinner fa-spin"></i></div>`;

  try {
    const res = await window.api.getReviews(selectedRestaurantId);
    const reviews = res.data;
    container.innerHTML = '';

    if (reviews.length === 0) {
      container.innerHTML = `<p style="color: var(--text-muted); font-size: 0.9rem;">${window.i18n.get('noReviews')}</p>`;
      return;
    }

    reviews.forEach(rev => {
      const div = document.createElement('div');
      div.className = 'review-item';
      
      const starsHtml = '<i class="fa-solid fa-star"></i>'.repeat(rev.rating) + 
                        '<i class="fa-regular fa-star"></i>'.repeat(5 - rev.rating);
      
      // Determine if active user can edit/delete this review
      let actionsHtml = '';
      if (currentUser && (currentUser.id === rev.userId || currentUser.role === 'admin')) {
        actionsHtml = `
          <div class="review-actions">
            <button type="button" class="btn btn-outline btn-sm" onclick="editReview(${rev.id}, ${rev.rating}, '${escapeHtml(rev.comment)}')">
              <i class="fa-solid fa-pen"></i>
            </button>
            <button type="button" class="btn btn-danger btn-sm" onclick="deleteReview(${rev.id})">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>
        `;
      }

      const imgHtml = rev.imageUrl ? `<img src="${rev.imageUrl}" class="review-image" onclick="window.open('${rev.imageUrl}', '_blank')">` : '';
      const dateText = new Date(rev.createdAt || Date.now()).toLocaleDateString();

      div.innerHTML = `
        <div class="review-item-header">
          <div>
            <span class="review-user">${rev.username}</span>
            <span class="review-date">${dateText}</span>
          </div>
          <span style="color: var(--warning); font-size: 0.8rem;">${starsHtml}</span>
        </div>
        <p class="review-comment">${rev.comment}</p>
        ${imgHtml}
        ${actionsHtml}
      `;
      container.appendChild(div);
    });
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

// Review write & edit actions
async function handleReviewSubmit(e) {
  e.preventDefault();
  
  if (!currentUser) {
    showToast(window.i18n.get('alertAuthRequired'), 'warning');
    openAuthModal('login');
    return;
  }

  const editId = document.getElementById('edit-review-id').value;
  const rating = document.getElementById('review-rating').value;
  const comment = document.getElementById('review-comment').value;
  const fileInput = document.getElementById('review-image');

  if (!rating) {
    showToast('Please select star rating!', 'warning');
    return;
  }

  const formData = new FormData();
  formData.append('restaurantId', selectedRestaurantId);
  formData.append('rating', rating);
  formData.append('comment', comment);
  if (fileInput.files[0]) {
    formData.append('image', fileInput.files[0]);
  }

  try {
    if (editId) {
      await window.api.updateReview(editId, formData);
    } else {
      await window.api.createReview(formData);
    }

    showToast(window.i18n.get('alertSuccess'), 'success');
    resetReviewForm();
    loadReviewsList();
    loadRestaurants(); // Update ratings count and avg stars on main view
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

function editReview(id, rating, comment) {
  document.getElementById('edit-review-id').value = id;
  document.getElementById('review-comment').value = comment;
  setStarRating(rating);
  document.getElementById('btn-cancel-review-edit').classList.remove('hidden');
  
  // Scroll form into view
  document.querySelector('.review-compose-section').scrollIntoView({ behavior: 'smooth' });
}

async function deleteReview(id) {
  if (!confirm(window.i18n.get('alertDeleteConfirm'))) return;
  try {
    await window.api.deleteReview(id);
    showToast(window.i18n.get('alertSuccess'), 'success');
    loadReviewsList();
    loadRestaurants();
  } catch (error) {
    showToast(error.message, 'danger');
  }
}

function resetReviewForm() {
  document.getElementById('form-review').reset();
  document.getElementById('edit-review-id').value = '';
  setStarRating(0);
  document.getElementById('btn-cancel-review-edit').classList.add('hidden');
}

// Helpers
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Expose functions globally for click handlers
window.changeLanguage = changeLanguage;
window.viewRestaurantDetails = viewRestaurantDetails;
window.openRestaurantFormModal = openRestaurantFormModal;
window.deleteRestaurant = deleteRestaurant;
window.editReview = editReview;
window.deleteReview = deleteReview;

// // AI Chat Widget Logic
let aiChatHistory = [];
let isAILoading = false;

const botResponses = {
  "uz": {
    "welcome": "Assalomu alaykum! Men Mikka AI yordamchisiman. Sizga platformadagi restoranlar, oshxonalar va sharhlar bo'yicha qanday yordam bera olaman?",
    "top": "Mikka platformasidagi eng yaxshi baholangan restoranlarni topish uchun qidiruv tizimidan foydalanishingiz yoki shunchaki \"Eng yaxshi restoranlar\" deb yozishingiz mumkin. Hozirda foydalanuvchilarimiz tomonidan eng yuqori baholangan joylar ro'yxatini ko'rsataman.",
    "uzbek": "Milliy taomlarimizni (palov, somsa, kabob va boshqalar) taklif qiladigan eng shinam restoranlarni topish uchun qidiruvga \"Uzbek\" yoki \"Milliy taomlar\" deb yozing. Sizga eng yaxshi milliy taomlar zallarini tavsiya qilaman.",
    "review": "Sharh yozish juda oson! Istalgan restoran sahifasiga kiring, \"Sharh yozish\" tugmasini bosing, yulduzchalarni tanlang va o'z fikringizni qoldiring. Bu boshqa foydalanuvchilarga to'g'ri tanlov qilishda yordam beradi.",
    "help": "Men sizga platformadagi restoranlar haqida ma'lumot berishim, oshxonalar bo'yicha tavsiyalar qilishim va sayt navigatsiyasi haqida gapirib berishim mumkin. Masalan, \"Yapon taomlari bormi?\" deb so'rang.",
    "pills": {
      "top": "Eng yaxshi baholanganlar ⭐",
      "uzbek": "Milliy taomlar 🇺🇿",
      "review": "Qanday sharh yoziladi? ✍️",
      "help": "Yordam 💡"
    }
  },
  "ru": {
    "welcome": "Здравствуйте! Я цифровой помощник Mikka AI. Чем я могу помочь вам в поиске ресторанов, кухонь и отзывов на платформе?",
    "top": "Чтобы найти лучшие рестораны на платформе Mikka, вы можете использовать поиск или просто написать \"Лучшие рестораны\". Я покажу вам заведения с самым высоким рейтингом.",
    "uzbek": "Чтобы найти уютные рестораны с национальной узбекской кухней (плов, сомса, шашлык), введите в поиске \"Uzbek\" или \"Национальная кухня\".",
    "review": "Написать отзыв очень просто! Перейдите на страницу любого ресторана, нажмите кнопку \"Написать отзыв\", выберите рейтинг и оставьте свой комментарий.",
    "help": "Я могу помочь вам найти информацию о ресторанах на платформе, дать рекомендации по кухням и объяснить навигацию по сайту. Например, спросите: \"Есть ли японская кухня?\"",
    "pills": {
      "top": "Лучшие рестораны ⭐",
      "uzbek": "Узбекская кухня 🇺🇿",
      "review": "Как написать отзыв? ✍️",
      "help": "Помощь 💡"
    }
  },
  "en": {
    "welcome": "Hello! I am Mikka AI digital assistant. How can I help you find restaurants, cuisines, and reviews on our platform?",
    "top": "To find the top-rated restaurants on the Mikka platform, you can use the search bar or just type \"Best restaurants\". I will show you the places with the highest ratings from our users.",
    "uzbek": "To find cozy restaurants serving traditional Uzbek cuisine (plov, somsa, kebab), search for \"Uzbek\" or \"National cuisine\".",
    "review": "Writing a review is very easy! Just visit any restaurant page, click the \"Write a Review\" button, choose a star rating, and write your comment.",
    "help": "I can help you find information about restaurants on the platform, recommend cuisines, and guide you through the site. For example, ask: \"Is there any Japanese restaurant?\"",
    "pills": {
      "top": "Top-rated restaurants ⭐",
      "uzbek": "Uzbek cuisines 🇺🇿",
      "review": "How to write a review? ✍️",
      "help": "Help 💡"
    }
  },
  "ja": {
    "welcome": "こんにちは！Mikka AIデジタルアシスタントです。当プラットフォーム上のレストラン、料理、口コミの検索についてどのようにお手伝いしましょうか？",
    "top": "Mikkaプラットフォームで最も評価の高いレストランを見つけるには、検索バーを使用するか、「最高のレストラン」と入力してください。ユーザーからの評価が最も高い場所を表示します。",
    "uzbek": "伝統的なウズベク料理（プロフ、サムサ、ケバブなど）を提供する居心地の良いレストランを見つけるには、「ウズベク」または「郷土料理」で検索してください。",
    "review": "口コミの書き方はとても簡単です！レストランのページにアクセスし、「口コミを書く」ボタンをクリックして、星評価を選んでコメントを記入してください。",
    "help": "プラットフォーム上のレストランに関する情報の検索、料理の推奨、およびサイトのナビゲーションについてお手伝いできます。例えば、「日本食レストランはありますか？」と聞いてみてください。",
    "pills": {
      "top": "最高評価の店 ⭐",
      "uzbek": "ウズベク料理店 🇺🇿",
      "review": "口コミの書き方は？ ✍️",
      "help": "ヘルプ 💡"
    }
  }
};

function initAIChat() {
  const chatbot = document.getElementById('chatbot-widget');
  if (!chatbot) return;

  const toggleBtn = document.getElementById('chat-toggle-btn');
  const closeBtn = document.getElementById('chat-close-btn');
  const windowEl = document.getElementById('chat-window');
  const bodyEl = document.getElementById('chat-window-body');
  const userInput = document.getElementById('chat-user-input');
  const sendBtn = document.getElementById('chat-send-btn');
  const badge = toggleBtn ? toggleBtn.querySelector('.chat-notification-badge') : null;
  const quickReplies = document.getElementById('chat-quick-replies');

  if (!toggleBtn || !windowEl || !bodyEl || !userInput || !sendBtn) return;



  function toggleChat() {
    const isActive = windowEl.classList.contains('active');
    if (isActive) {
      windowEl.classList.remove('active');
      toggleBtn.classList.remove('active');
    } else {
      windowEl.classList.add('active');
      toggleBtn.classList.add('active');
      if (badge) {
        badge.style.display = 'none';
      }
      updateAIChatLanguage();
      userInput.focus();
      scrollToBottom();
    }
  }

  toggleBtn.addEventListener('click', () => {
    toggleChat();
  });

  closeBtn.addEventListener('click', () => {
    if (windowEl.classList.contains('active')) {
      toggleChat();
    }
  });

  // Handle message sending
  async function handleSend() {
    if (isAILoading) return;
    const text = userInput.value.trim();
    if (text === '') return;

    userInput.value = '';
    await processChatMessage(text);
  }

  sendBtn.addEventListener('click', (e) => {
    e.preventDefault();
    handleSend();
  });

  userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSend();
    }
  });

  // Quick reply pills clicks
  if (quickReplies) {
    quickReplies.querySelectorAll('.quick-reply-pill').forEach(pill => {
      pill.addEventListener('click', async (e) => {
        e.preventDefault();
        if (isAILoading) return;
        const keyword = pill.getAttribute('data-keyword');
        const text = pill.textContent;
        await processChatMessage(text, keyword);
      });
    });
  }

  // Initial translation apply
  updateAIChatLanguage();
}

function clearAIChatHistory() {
  aiChatHistory = [];
  const currentLang = window.i18n.current() || 'en';
  const langKey = botResponses[currentLang] ? currentLang : 'en';
  const welcomeMessageText = botResponses[langKey].welcome;
  
  const pillsTranslation = botResponses[langKey].pills || {
    "top": "Eng yaxshi baholanganlar ⭐",
    "uzbek": "Milliy taomlar 🇺🇿",
    "review": "Qanday sharh yoziladi? ✍️",
    "help": "Yordam 💡"
  };

  const bodyEl = document.getElementById('chat-window-body');
  if (bodyEl) {
    // Retain only welcome bubble and quick replies
    bodyEl.innerHTML = `
      <!-- Welcome Message -->
      <div class="chat-bubble assistant-bubble animate-fade-in">
          <p id="chat-welcome-text">${welcomeMessageText}</p>
      </div>
      
      <!-- Quick replies pills -->
      <div class="chat-quick-replies" id="chat-quick-replies">
          <button class="quick-reply-pill" data-keyword="top">${pillsTranslation.top}</button>
          <button class="quick-reply-pill" data-keyword="uzbek">${pillsTranslation.uzbek}</button>
          <button class="quick-reply-pill" data-keyword="review">${pillsTranslation.review}</button>
          <button class="quick-reply-pill" data-keyword="help">${pillsTranslation.help}</button>
      </div>
    `;
    scrollToBottom();
    
    // Re-attach listeners to new quick replies
    const newQuickReplies = document.getElementById('chat-quick-replies');
    if (newQuickReplies) {
      newQuickReplies.querySelectorAll('.quick-reply-pill').forEach(pill => {
        pill.addEventListener('click', async (e) => {
          e.preventDefault();
          if (isAILoading) return;
          const keyword = pill.getAttribute('data-keyword');
          const text = pill.textContent;
          await processChatMessage(text, keyword);
        });
      });
    }
  }

  isAILoading = false;
  const userInput = document.getElementById('chat-user-input');
  const sendBtn = document.getElementById('chat-send-btn');
  if (userInput) {
    userInput.disabled = false;
    let placeholderText = "Xabaringizni yozing...";
    if (currentLang === 'ru') placeholderText = "Введите ваше сообщение...";
    if (currentLang === 'en') placeholderText = "Type your message...";
    if (currentLang === 'ja') placeholderText = "メッセージを入力してください...";
    userInput.setAttribute('placeholder', placeholderText);
  }
  if (sendBtn) sendBtn.disabled = false;

  // Close widget
  const windowEl = document.getElementById('chat-window');
  const toggleBtn = document.getElementById('chat-toggle-btn');
  if (windowEl) windowEl.classList.remove('active');
  if (toggleBtn) toggleBtn.classList.remove('active');
}

function updateAIChatLanguage() {
  const currentLang = window.i18n.current() || 'en';
  const langKey = botResponses[currentLang] ? currentLang : 'en';
  
  const welcomeText = document.getElementById('chat-welcome-text');
  if (welcomeText) {
    welcomeText.textContent = botResponses[langKey].welcome;
  }

  // Update quick reply pills translation
  const pills = document.querySelectorAll('.quick-reply-pill');
  pills.forEach(pill => {
    const keyword = pill.getAttribute('data-keyword');
    if (keyword && botResponses[langKey].pills && botResponses[langKey].pills[keyword]) {
      pill.textContent = botResponses[langKey].pills[keyword];
    }
  });

  // Also update footer input placeholder translation
  const userInput = document.getElementById('chat-user-input');
  if (userInput) {
    let placeholderText = "Xabaringizni yozing...";
    if (currentLang === 'ru') placeholderText = "Введите ваше сообщение...";
    if (currentLang === 'en') placeholderText = "Type your message...";
    if (currentLang === 'ja') placeholderText = "メッセージを入力してください...";
    userInput.setAttribute('placeholder', placeholderText);
  }
}

async function processChatMessage(text, forceKeyword = null) {
  if (isAILoading) return;
  
  appendAIChatMessage('user', text);
  scrollToBottom();

  const userInput = document.getElementById('chat-user-input');
  const sendBtn = document.getElementById('chat-send-btn');
  if (userInput) userInput.disabled = true;
  if (sendBtn) sendBtn.disabled = true;

  // Dim quick reply pills
  const pills = document.querySelectorAll('.quick-reply-pill');
  pills.forEach(p => p.classList.add('disabled'));

  // Show typing loader
  const loadingId = appendAILoadingIndicator();
  scrollToBottom();

  isAILoading = true;

  // Check if text or forceKeyword matches any of the local bot responses
  const currentLang = window.i18n.current() || 'en';
  const langKey = botResponses[currentLang] ? currentLang : 'en';
  const lowerText = text.toLowerCase();
  
  let localReply = null;
  const keyword = forceKeyword || (
    lowerText.includes('reyting') || lowerText.includes('yaxshi') || lowerText.includes('best') || lowerText.includes('top') ? 'top' :
    lowerText.includes('milliy') || lowerText.includes('uzbek') || lowerText.includes('o\'zbek') || lowerText.includes('taom') ? 'uzbek' :
    lowerText.includes('sharh') || lowerText.includes('otziv') || lowerText.includes('review') || lowerText.includes('yozish') ? 'review' :
    lowerText.includes('yordam') || lowerText.includes('help') || lowerText.includes('ai') || lowerText.includes('mikka') ? 'help' : null
  );

  if (keyword && botResponses[langKey][keyword]) {
    localReply = botResponses[langKey][keyword];
  }

  // Simulate delay for bot reply
  setTimeout(async () => {
    removeAILoadingIndicator(loadingId);
    
    if (localReply) {
      appendAIChatMessage('assistant', localReply);
      isAILoading = false;
      if (userInput) {
        userInput.disabled = false;
        userInput.focus();
      }
      if (sendBtn) sendBtn.disabled = false;
      pills.forEach(p => p.classList.remove('disabled'));
      scrollToBottom();
    } else {
      // Query Gemini
      try {
        const res = await window.api.chat(text, aiChatHistory);
        const replyText = res.reply || 'AI response is empty.';
        appendAIChatMessage('assistant', replyText);

        aiChatHistory.push({ role: 'user', content: text });
        aiChatHistory.push({ role: 'model', content: replyText });
        if (aiChatHistory.length > 20) {
          aiChatHistory = aiChatHistory.slice(-20);
        }
      } catch (err) {
        appendAIChatMessage('assistant', `Error: ${err.message}`);
      } finally {
        isAILoading = false;
        if (userInput) {
          userInput.disabled = false;
          userInput.focus();
        }
        if (sendBtn) sendBtn.disabled = false;
        pills.forEach(p => p.classList.remove('disabled'));
        scrollToBottom();
      }
    }
  }, 1000);
}

function appendAIChatMessage(role, content) {
  const bodyEl = document.getElementById('chat-window-body');
  const quickReplies = document.getElementById('chat-quick-replies');
  if (!bodyEl) return;

  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${role === 'user' ? 'user-bubble' : 'assistant-bubble'}`;
  
  // Basic markdown rendering
  let parsedContent = escapeHtml(content)
    .replace(/\n\n/g, '<br><br>')
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/•\s(.*?)(<br>|$)/g, '<li>$1</li>');

  bubble.innerHTML = parsedContent;

  // Append before quick replies container to keep them at the bottom
  if (quickReplies) {
    bodyEl.insertBefore(bubble, quickReplies);
  } else {
    bodyEl.appendChild(bubble);
  }
}

function appendAILoadingIndicator() {
  const bodyEl = document.getElementById('chat-window-body');
  const quickReplies = document.getElementById('chat-quick-replies');
  if (!bodyEl) return '';

  const id = 'typing-indicator';
  const indicator = document.createElement('div');
  indicator.className = 'typing-indicator';
  indicator.id = id;
  indicator.innerHTML = `
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
    <span class="typing-dot"></span>
  `;

  if (quickReplies) {
    bodyEl.insertBefore(indicator, quickReplies);
  } else {
    bodyEl.appendChild(indicator);
  }
  return id;
}

function removeAILoadingIndicator(id) {
  const indicator = document.getElementById(id);
  if (indicator) indicator.remove();
}

function scrollToBottom() {
  const bodyEl = document.getElementById('chat-window-body');
  if (bodyEl) {
    bodyEl.scrollTop = bodyEl.scrollHeight;
  }
}
