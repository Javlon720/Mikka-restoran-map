const BASE_URL = '/api';

function getHeaders() {
  const token = localStorage.getItem('jdu_token');
  const headers = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

async function request(url, options = {}) {
  const headers = getHeaders();
  
  if (options.body && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(options.body);
  }

  const response = await fetch(`${BASE_URL}${url}`, {
    credentials: 'same-origin',
    ...options,
    headers: {
      ...headers,
      ...options.headers
    }
  });

  const text = await response.text();
  let data = {};
  if (text) {
    try {
      data = JSON.parse(text);
    } catch (e) {
      console.error('Failed to parse JSON response:', e, 'Raw text:', text);
      throw new Error('Invalid server response');
    }
  }

  if (!response.ok || data.success === false) {
    throw new Error(data.error || 'Something went wrong');
  }

  return data;
}

window.api = {
  // Authentication
  login: (emailOrUsername, password) => 
    request('/auth/login', { method: 'POST', body: { emailOrUsername, password } }),
  
  register: (username, email, password) => 
    request('/auth/register', { method: 'POST', body: { username, email, password } }),

  googleLogin: (idToken) => 
    request('/auth/google', { method: 'POST', body: { idToken } }),

  logout: () =>
    request('/auth/logout', { method: 'POST' }),

  getConfig: () => 
    request('/config'),

  // Restaurants
  getRestaurants: (search) => 
    request(`/restaurants${search ? `?search=${encodeURIComponent(search)}` : ''}`),
  
  getRestaurant: (id) => 
    request(`/restaurants/${id}`),
  
  createRestaurant: (formData) => 
    request('/restaurants', { method: 'POST', body: formData }),
  
  updateRestaurant: (id, formData) => 
    request(`/restaurants/${id}`, { method: 'PUT', body: formData }),
  
  deleteRestaurant: (id) => 
    request(`/restaurants/${id}`, { method: 'DELETE' }),

  // Reviews
  getReviews: (restaurantId) => 
    request(`/restaurants/${restaurantId}/reviews`),
  
  createReview: (formData) => 
    request('/reviews', { method: 'POST', body: formData }),
  
  updateReview: (id, formData) => 
    request(`/reviews/${id}`, { method: 'PUT', body: formData }),
  
  deleteReview: (id) => 
    request(`/reviews/${id}`, { method: 'DELETE' }),

  chat: (message, history) => 
    request('/chat', { method: 'POST', body: { message, history } })
};
