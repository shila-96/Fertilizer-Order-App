# Fertilizer Order App

A simple app for farmers to browse, order, and track fertilizer deliveries.

## Features
- User registration & login
- Browse fertilizer catalog
- Place & track orders
- Admin panel for inventory & order management
- Responsive design (mobile + web)

## Tech Stack
- Frontend: React / React Native
- Backend: Node.js + Express
- Database: MongoDB
- Authentication: JWT

## Quick Start

```bash
git clone https://github.com/shila-96/Fertilizer-Order-App.git
cd Fertilizer-Order-App

# Backend
cd backend
npm install
cp .env.example .env   # add your MongoDB URI & JWT secret
npm run dev

# Frontend
cd ../frontend
npm install
npm start
```

## Main API Routes
- `POST /api/auth/register` – Register
- `POST /api/auth/login` – Login
- `GET /api/products` – List fertilizers
- `POST /api/orders` – Create order
- `GET /api/orders` – User’s orders

## Contributing
1. Fork → Create branch → Commit → Push → Open PR  
2. Follow existing code style

## License
MIT