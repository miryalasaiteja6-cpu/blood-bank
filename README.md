# Blood Bank Management System

A full-stack Blood Bank Management System built for a college IMS project. The app demonstrates a modern healthcare dashboard, donor management, donation records, inventory control, request management, and database integration layers for PostgreSQL, MongoDB, Neo4j, and Redis.

## Features

- Role-based authentication with JWT
- Admin and staff dashboards
- Donor, donation, inventory, and hospital management
- Blood request workflow with inventory validation
- Chart-driven analytics and reports
- Demo data support with optional external DB integration
- API-ready backend using Express
- React frontend with responsive UI

## Tech stack

- Frontend: React + Vite + Chart.js
- Backend: Node.js + Express
- Relational DB: PostgreSQL integration layer
- NoSQL: MongoDB integration layer
- Graph DB: Neo4j integration layer
- Cache: Redis integration layer
- Security: bcrypt, JWT, helmet, CORS, rate limiting

## Quick start

1. Install dependencies:
   npm install
2. Copy environment variables:
   copy .env.example .env
3. Start backend and frontend:
   npm run dev
4. Open the frontend at http://localhost:5173
5. Backend API runs at http://localhost:5000/api

## Demo credentials

- Admin: admin@bbms.local / Admin@123
- Staff: staff@bbms.local / Staff@123
- Donor: donor@bbms.local / Donor@123

## Project structure

- backend/src : Express API, controllers, middleware, services
- frontend/src : React app and pages
- database/postgresql : PostgreSQL schema and seed scripts
- database/mongodb : MongoDB schema notes
- database/neo4j : Neo4j queries and graph model
- docs : architecture and deployment docs

## Database notes

The project includes integration-ready configuration for PostgreSQL, MongoDB, Neo4j, and Redis. If external services are not running, the app falls back to a demo in-memory data layer so the project remains usable and presentable.

## Deployment

See the docs folder for architecture and Azure deployment guidance.
