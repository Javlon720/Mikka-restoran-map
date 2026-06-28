-- Drop tables if they exist
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS restaurants CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user', -- 'user' or 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Restaurants table
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    cuisine VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    image_url VARCHAR(555),
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT NOT NULL,
    image_url VARCHAR(555),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed Initial Users (Passwords are hashed 'admin123' and 'user123' respectively using bcrypt)
INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@jdu.uz', '$2a$10$ZJ4Ghxphe2PYCPQYTZ6kxejMH8aa7oOfTn3UVNaP48qkcnDcgTt5i', 'admin'),
('javlon', 'javlon@jdu.uz', '$2a$10$GdYI7I4sEojeC2GZP.EOtOmzrAimezp.jEqqN.Yd1a8aX79MqZWEa', 'user');

-- Seed Restaurants
INSERT INTO restaurants (name, description, cuisine, address, image_url, lat, lng, created_by) VALUES
('Rayhon National Foods', 'Best national Uzbek foods, pilaf, shashlik, lagman, and somsa.', 'Uzbek', 'Lutfiy Street, Tashkent', '/uploads/rayhon.jpg', 41.2956, 69.2145, 1),
('Tanuki Sushi', 'Premium Japanese restaurant with a cozy atmosphere and authentic sushi.', 'Japanese', 'Taras Shevchenko Street, Tashkent', '/uploads/tanuki.jpg', 41.3005, 69.2789, 1),
('La Cantine', 'Cozy French and Italian cafe, famous for croissants and fresh pasta.', 'European', 'Amir Temur Avenue, Tashkent', '/uploads/lacantine.jpg', 41.3114, 69.2801, 1);

-- Seed Reviews
INSERT INTO reviews (restaurant_id, user_id, rating, comment, image_url) VALUES
(1, 2, 5, 'Pilaf is absolutely amazing! Authentic taste and great service.', NULL),
(2, 2, 4, 'Very fresh sushi, but the price is a bit high. Highly recommended.', NULL),
(1, 1, 4, 'Good national dishes, fast service, nice decorations.', NULL);
