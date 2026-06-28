# JDU Restaurant Review Web Application (飲食店情報口コミサイト) - Monorepo

This is a comprehensive, multilingual restaurant review web application designed for the JDU (Japan Digital University) coursework. It is structured as an **NPM workspaces monorepo** with a backend following **Clean Code Architecture** in **TypeScript & PostgreSQL**, paired with a beautiful, responsive **HTML, CSS, and Vanilla JS** frontend.

## Features

1. **User Authentication**: Simple user registration and login. Passwords are securely hashed using `bcryptjs`, and session tokens are signed via JWT and stored using secure HTTP-only cookies.
2. **Multilingual (i18n) Support**: Dynamically translates between **Uzbek (uz)**, **English (en)**, **Russian (ru)**, and **Japanese (ja)**.
3. **Interactive Maps (Leaflet)**:
   - Browse restaurants on a main dashboard map with interactive light Voyager markers.
   - Click a marker's pop-up to slide open the restaurant details and reviews.
   - Admins can place and drag a custom map pin to coordinate latitude/longitude coordinates when creating/editing restaurants.
4. **Restaurant Management (Admin)**: Full CRUD (Create, Read, Update, Delete) permissions for restaurants, complete with image uploads.
5. **Restaurant Reviews**: Registered users can rate (1-5 stars), write comments, and upload pictures. Users can edit or delete their own reviews, while admins can manage all reviews.
6. **Mikka AI Assistant**: Floating chatbot widget powered by Google's Gemini API providing intelligent recommendations and information about restaurants and cuisines on the platform.

---

## Monorepo Architecture

The project is divided into workspace packages managed from the root directory:

```
Jdu/
├── .env                  # Configuration variables (DB connection, JWT secret)
├── .gitignore            # Git exclusion definitions
├── package.json          # Root monorepo workspace definition
├── README.md             # Project documentation
└── packages/
    ├── backend/          # @jdu-restaurant/backend workspace
    │   ├── package.json  # Backend dependency manifest
    │   ├── tsconfig.json # TypeScript compiler settings
    │   ├── db.sql        # PostgreSQL schema script & seed dummy data
    │   ├── uploads/      # Directory where restaurant and review photos are saved
    │   └── src/          # Clean architecture backend source files
    │       ├── domain/
    │       │   ├── entities/      # Core enterprise objects (User, Restaurant, Review)
    │       │   └── repositories/  # Repository port interfaces (contracts for DB operations)
    │       ├── use-cases/         # Application business logic (interactors coordinating repository calls)
    │       ├── adapters/
    │       │   ├── controllers/   # Maps HTTP payload arguments to domain Use Cases
    │       │   └── repositories/  # Pg repository implementations implementing port interfaces
    │       └── infrastructure/
    │           ├── server.ts      # Fastify server bootstrapper, static directory bindings, CORS, cookies
    │           ├── router.ts      # Declares paths and wires controllers with use cases
    │           └── middleware/    # Auth guards and Multer disk storage configurations
    └── frontend/         # @jdu-restaurant/frontend workspace
        ├── package.json  # Frontend manifest
        ├── index.html    # SPA DOM template shell
        ├── css/
        │   └── styles.css # Premium light-mode visual design stylesheet
        └── js/
            ├── i18n.js   # Key translation catalogs and driver
            ├── api.js    # API client containing fetch methods with cookie credentials support
            └── app.js    # Client router, maps, modal controls, and state manager
```

---

## Setup Instructions

### 1. Database Configuration
Ensure your local PostgreSQL database server is running. Log in and execute the database creation and seeding:

```bash
# Create the jdu_restaurant database
PGPASSWORD=1234 createdb -U postgres jdu_restaurant

# Execute migrations and seed initial data
PGPASSWORD=1234 psql -U postgres -d jdu_restaurant -f packages/backend/db.sql
```

The database config is loaded in the `.env` file at the root:
```env
PORT=3000
DATABASE_URL=postgresql://postgres:1234@localhost:5432/jdu_restaurant
JWT_SECRET=jdu_secret_key_2026_restaurant
```

### 2. Install Packages & Run
Run all commands from the root directory (`/Users/macbook-projavlon/Desktop/Jdu`):

```bash
# Install all package dependencies and link workspaces
pnpm install

# Compile the TypeScript backend
pnpm build

# Start the dev server with hot reload
pnpm dev
```

The application will launch at:
👉 **[http://localhost:3000](http://localhost:3000)**

### 3. Demo Credentials
You can log in using the following seed users:
* **Admin Account**: Email: `admin@jdu.uz` (or Username: `admin`) | Password: `admin123`
* **Standard User**: Email: `javlon@jdu.uz` (or Username: `javlon`) | Password: `user123`
#Mikka-restoran-map
# Mikka-restoran-map
