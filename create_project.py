from pathlib import Path

root = Path(r'C:\Users\Miriy\OneDrive\btech 1-2\IMS\Mission_blood')

files = {
    'README.md': '''# Blood Bank Management System

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
''',
    '.env.example': '''PORT=5000
JWT_SECRET=change-this-secret
POSTGRES_URL=postgresql://postgres:postgres@localhost:5432/bbms
MONGO_URI=mongodb://localhost:27017/bbms
REDIS_URL=redis://localhost:6379
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
CLIENT_URL=http://localhost:5173
''',
    'docker-compose.yml': '''version: "3.9"
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: bbms
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongodata:/data/db

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  neo4j:
    image: neo4j:5
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/password
    volumes:
      - neodata:/data

volumes:
  pgdata:
  mongodata:
  neodata:
''',
    'backend/src/config/database.js': '''import pg from 'pg';
import { MongoClient } from 'mongodb';
import { createClient } from 'redis';
import neo4j from 'neo4j-driver';

const { Pool } = pg;

export const pgPool = process.env.POSTGRES_URL ? new Pool({ connectionString: process.env.POSTGRES_URL }) : null;
export const mongoClient = process.env.MONGO_URI ? new MongoClient(process.env.MONGO_URI) : null;
export const redisClient = process.env.REDIS_URL ? createClient({ url: process.env.REDIS_URL }) : null;
export const neo4jDriver = process.env.NEO4J_URI
  ? neo4j.driver(
      process.env.NEO4J_URI,
      neo4j.auth.basic(process.env.NEO4J_USER || 'neo4j', process.env.NEO4J_PASSWORD || 'password')
    )
  : null;

export async function initExternalServices() {
  const status = {
    postgres: false,
    mongodb: false,
    redis: false,
    neo4j: false,
  };

  try {
    if (pgPool) {
      await pgPool.query('SELECT 1');
      status.postgres = true;
    }
  } catch (error) {
    console.warn('PostgreSQL unavailable, using demo data mode');
  }

  try {
    if (mongoClient) {
      await mongoClient.connect();
      status.mongodb = true;
    }
  } catch (error) {
    console.warn('MongoDB unavailable, using demo data mode');
  }

  try {
    if (redisClient) {
      await redisClient.connect();
      status.redis = true;
    }
  } catch (error) {
    console.warn('Redis unavailable, using demo data mode');
  }

  try {
    if (neo4jDriver) {
      const session = neo4jDriver.session();
      await session.run('RETURN 1');
      await session.close();
      status.neo4j = true;
    }
  } catch (error) {
    console.warn('Neo4j unavailable, using demo data mode');
  }

  return status;
}
''',
    'backend/src/config/demoData.js': '''import bcrypt from 'bcryptjs';

const hash = (value) => bcrypt.hashSync(value, 10);

export const state = {
  users: [
    {
      id: 'u-001',
      fullName: 'System Administrator',
      email: 'admin@bbms.local',
      mobile: '+91 9876543210',
      password: hash('Admin@123'),
      role: 'admin',
      bloodGroup: 'O+',
      dob: '1990-06-15',
      gender: 'Male',
      address: '12 Blood Care Avenue',
      city: 'Bengaluru',
      state: 'Karnataka',
      pinCode: '560001',
      createdAt: '2024-01-12T09:00:00.000Z'
    },
    {
      id: 'u-002',
      fullName: 'Priya Nair',
      email: 'staff@bbms.local',
      mobile: '+91 9988776655',
      password: hash('Staff@123'),
      role: 'staff',
      bloodGroup: 'A+',
      dob: '1988-06-22',
      gender: 'Female',
      address: '45 Red Cross Road',
      city: 'Mysuru',
      state: 'Karnataka',
      pinCode: '570001',
      createdAt: '2024-02-10T08:30:00.000Z'
    },
    {
      id: 'u-003',
      fullName: 'Rahul Menon',
      email: 'donor@bbms.local',
      mobile: '+91 9123456789',
      password: hash('Donor@123'),
      role: 'donor',
      bloodGroup: 'B+',
      dob: '1995-07-18',
      gender: 'Male',
      address: '88 Green Valley',
      city: 'Mysuru',
      state: 'Karnataka',
      pinCode: '570005',
      createdAt: '2024-03-05T11:45:00.000Z'
    }
  ],
  donors: [
    {
      id: 'D-1001',
      name: 'Rahul Menon',
      dob: '1995-07-18',
      gender: 'Male',
      bloodGroup: 'B+',
      phone: '+91 9123456789',
      email: 'rahul.menon@gmail.com',
      address: '88 Green Valley',
      city: 'Mysuru',
      district: 'Mysuru',
      pincode: '570005',
      weight: 72,
      lastDonationDate: '2024-10-02',
      status: 'Available',
      eligible: true,
      createdAt: '2024-03-05T11:45:00.000Z'
    },
    {
      id: 'D-1002',
      name: 'Ananya Rao',
      dob: '1992-02-14',
      gender: 'Female',
      bloodGroup: 'O+',
      phone: '+91 8765432101',
      email: 'ananya.r@gmail.com',
      address: '2 Lake View Road',
      city: 'Bengaluru',
      district: 'Bengaluru Urban',
      pincode: '560010',
      weight: 61,
      lastDonationDate: '2024-09-04',
      status: 'Available',
      eligible: true,
      createdAt: '2024-01-25T10:00:00.000Z'
    },
    {
      id: 'D-1003',
      name: 'Vikram Shah',
      dob: '1986-11-11',
      gender: 'Male',
      bloodGroup: 'A+',
      phone: '+91 9876112233',
      email: 'vikram.shah@gmail.com',
      address: '9 Cross Street',
      city: 'Hubballi',
      district: 'Dharwad',
      pincode: '580020',
      weight: 80,
      lastDonationDate: '2024-08-14',
      status: 'Unavailable',
      eligible: false,
      createdAt: '2024-02-18T14:15:00.000Z'
    }
  ],
  hospitals: [
    {
      id: 'H-2001',
      name: 'City Care Hospital',
      type: 'Private',
      city: 'Bengaluru',
      district: 'Bengaluru Urban',
      phone: '+91 9876543211',
      email: 'care@citycarehospitals.com',
      address: '14 MG Road',
      contactPerson: 'Dr. S. Nair',
      status: 'Active'
    },
    {
      id: 'H-2002',
      name: 'Namma Health Centre',
      type: 'Government',
      city: 'Mysuru',
      district: 'Mysuru',
      phone: '+91 9845632112',
      email: 'info@nammahealth.in',
      address: '31 Hospital Street',
      contactPerson: 'Dr. Kamath',
      status: 'Active'
    }
  ],
  donations: [
    {
      id: 'DN-3001',
      donorId: 'D-1001',
      donorName: 'Rahul Menon',
      bloodGroup: 'B+',
      quantityMl: 450,
      units: 1,
      donationDate: '2024-11-01',
      center: 'Mysuru Blood Center',
      screeningStatus: 'Approved',
      medicalStatus: 'Eligible',
      approved: true,
      createdAt: '2024-11-01T08:30:00.000Z'
    },
    {
      id: 'DN-3002',
      donorId: 'D-1002',
      donorName: 'Ananya Rao',
      bloodGroup: 'O+',
      quantityMl: 400,
      units: 1,
      donationDate: '2024-10-20',
      center: 'Bengaluru Red Cross',
      screeningStatus: 'Approved',
      medicalStatus: 'Eligible',
      approved: true,
      createdAt: '2024-10-20T09:10:00.000Z'
    }
  ],
  inventory: [
    { id: 'INV-4001', bloodGroup: 'A+', units: 12, reserved: 2, expiryDate: '2025-01-12', storageLocation: 'Cold Room A', component: 'Whole Blood', status: 'Healthy' },
    { id: 'INV-4002', bloodGroup: 'A-', units: 8, reserved: 1, expiryDate: '2024-12-20', storageLocation: 'Cold Room A', component: 'Packed RBC', status: 'Low' },
    { id: 'INV-4003', bloodGroup: 'B+', units: 15, reserved: 3, expiryDate: '2025-01-18', storageLocation: 'Cold Room B', component: 'Platelets', status: 'Healthy' },
    { id: 'INV-4004', bloodGroup: 'O+', units: 17, reserved: 4, expiryDate: '2025-02-14', storageLocation: 'Cold Room C', component: 'Plasma', status: 'Healthy' },
    { id: 'INV-4005', bloodGroup: 'AB+', units: 9, reserved: 1, expiryDate: '2024-12-28', storageLocation: 'Cold Room D', component: 'Whole Blood', status: 'Low' },
    { id: 'INV-4006', bloodGroup: 'O-', units: 6, reserved: 2, expiryDate: '2025-01-16', storageLocation: 'Emergency Vault', component: 'Whole Blood', status: 'Low' }
  ],
  requests: [
    {
      id: 'BR-5001',
      patientName: 'Suresh Kumar',
      age: 48,
      hospitalName: 'Namma Health Centre',
      hospitalContact: '+91 8899776600',
      bloodGroup: 'B+',
      component: 'Packed Red Blood Cells',
      units: 2,
      requiredDate: '2024-11-12',
      emergencyLevel: 'High',
      doctor: 'Dr. Shwetha',
      status: 'Approved',
      createdAt: '2024-11-05T08:00:00.000Z'
    },
    {
      id: 'BR-5002',
      patientName: 'Lalitha R',
      age: 29,
      hospitalName: 'City Care Hospital',
      hospitalContact: '+91 9009009009',
      bloodGroup: 'O+',
      component: 'Platelets',
      units: 1,
      requiredDate: '2024-11-14',
      emergencyLevel: 'Medium',
      doctor: 'Dr. Iyer',
      status: 'Pending',
      createdAt: '2024-11-08T10:00:00.000Z'
    }
  ],
  reservations: [],
  notifications: [
    { id: 'N-6001', title: 'Low stock alert', message: 'A- units are below minimum stock threshold.', createdAt: '2024-11-06T09:00:00.000Z', read: false },
    { id: 'N-6002', title: 'Donation approved', message: 'Donation DN-3001 has been approved and added to inventory.', createdAt: '2024-11-01T12:00:00.000Z', read: true }
  ],
  audit: []
};

export const demoStats = {
  totalDonors: state.donors.length,
  totalDonations: state.donations.length,
  totalBloodUnits: state.inventory.reduce((sum, item) => sum + item.units, 0),
  pendingRequests: state.requests.filter((request) => ['Pending', 'Under Review'].includes(request.status)).length,
  approvedRequests: state.requests.filter((request) => request.status === 'Approved').length,
  registeredHospitals: state.hospitals.length
};
''',
    'backend/src/middleware/auth.js': '''import jwt from 'jsonwebtoken';
import { state } from '../config/demoData.js';

export function authenticateToken(req, res, next) {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.startsWith('Bearer ') ? authHeader.split(' ')[1] : null;

  if (!token) {
    return res.status(401).json({ message: 'Authentication token is required.' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'bbms-demo-secret');
    req.user = decoded;
    const user = state.users.find((entry) => entry.id === decoded.id || entry.email === decoded.email);
    if (!user) {
      return res.status(401).json({ message: 'User not found.' });
    }
    req.user.role = user.role;
    next();
  } catch (error) {
    return res.status(403).json({ message: 'Invalid or expired token.' });
  }
}

export function authorizeRoles(...roles) {
  return (req, res, next) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ message: 'You do not have permission to access this resource.' });
    }
    next();
  };
}
''',
    'backend/src/services/dataService.js': '''import { state } from '../config/demoData.js';

export function getDashboardData() {
  const totalDonors = state.donors.length;
  const totalDonations = state.donations.length;
  const totalBloodUnits = state.inventory.reduce((total, item) => total + item.units, 0);
  const pendingRequests = state.requests.filter((request) => ['Pending', 'Under Review'].includes(request.status)).length;
  const approvedRequests = state.requests.filter((request) => request.status === 'Approved').length;
  const registeredHospitals = state.hospitals.length;

  const donationTrend = [
    { label: 'Jan', value: 12 },
    { label: 'Feb', value: 18 },
    { label: 'Mar', value: 14 },
    { label: 'Apr', value: 22 },
    { label: 'May', value: 20 },
    { label: 'Jun', value: 26 }
  ];

  const bloodGroupDistribution = state.inventory.map((item) => ({
    label: item.bloodGroup,
    value: item.units
  }));

  return {
    totalDonors,
    totalDonations,
    totalBloodUnits,
    pendingRequests,
    approvedRequests,
    registeredHospitals,
    donationTrend,
    bloodGroupDistribution,
    recentDonations: state.donations.slice(0, 5),
    recentRequests: state.requests.slice(0, 5),
    lowStockAlerts: state.inventory.filter((item) => item.status === 'Low'),
    notifications: state.notifications.slice(0, 5)
  };
}

export function getDonors() {
  return state.donors;
}

export function addDonor(payload) {
  const donor = {
    id: `D-${Date.now()}`,
    ...payload,
    createdAt: new Date().toISOString()
  };
  state.donors.push(donor);
  return donor;
}

export function updateDonor(id, payload) {
  const donorIndex = state.donors.findIndex((donor) => donor.id === id);
  if (donorIndex === -1) return null;
  state.donors[donorIndex] = { ...state.donors[donorIndex], ...payload };
  return state.donors[donorIndex];
}

export function deleteDonor(id) {
  const donorIndex = state.donors.findIndex((donor) => donor.id === id);
  if (donorIndex === -1) return false;
  state.donors.splice(donorIndex, 1);
  return true;
}

export function getInventory() {
  return state.inventory;
}

export function addInventoryRecord(payload) {
  const record = {
    id: `INV-${Date.now()}`,
    ...payload,
    createdAt: new Date().toISOString()
  };
  state.inventory.push(record);
  return record;
}

export function reserveInventory(itemId, quantity) {
  const item = state.inventory.find((entry) => entry.id === itemId);
  if (!item) return null;
  if (item.units < quantity) return null;
  item.units -= quantity;
  item.reserved += quantity;
  return item;
}

export function getRequests() {
  return state.requests;
}

export function addRequest(payload) {
  const item = {
    id: `BR-${Date.now()}`,
    ...payload,
    status: 'Pending',
    createdAt: new Date().toISOString()
  };
  state.requests.push(item);
  state.notifications.unshift({
    id: `N-${Date.now()}`,
    title: 'New blood request',
    message: `${payload.patientName} requested ${payload.bloodGroup} ${payload.component}.`,
    createdAt: new Date().toISOString(),
    read: false
  });
  return item;
}

export function updateRequestStatus(id, status) {
  const request = state.requests.find((item) => item.id === id);
  if (!request) return null;
  request.status = status;
  return request;
}

export function getHospitals() {
  return state.hospitals;
}

export function getNotifications() {
  return state.notifications;
}

export function searchDonors({ bloodGroup, city, availability, pincode }) {
  return state.donors.filter((donor) => {
    const bloodMatch = !bloodGroup || donor.bloodGroup === bloodGroup;
    const cityMatch = !city || donor.city.toLowerCase() === city.toLowerCase();
    const pincodeMatch = !pincode || donor.pincode === pincode;
    const availabilityMatch = !availability || donor.status === availability;
    return bloodMatch && cityMatch && pincodeMatch && availabilityMatch && donor.eligible;
  });
}

export function getReports() {
  return {
    daily: [
      { date: '2024-11-01', donations: 5, requests: 4 },
      { date: '2024-11-02', donations: 6, requests: 3 },
      { date: '2024-11-03', donations: 4, requests: 5 },
      { date: '2024-11-04', donations: 7, requests: 2 }
    ],
    monthly: [
      { month: 'Jan', value: 32 },
      { month: 'Feb', value: 38 },
      { month: 'Mar', value: 41 },
      { month: 'Apr', value: 36 },
      { month: 'May', value: 45 }
    ],
    inventorySummary: state.inventory.map((item) => ({
      bloodGroup: item.bloodGroup,
      available: item.units,
      reserved: item.reserved,
      status: item.status
    }))
  };
}
''',
    'backend/src/controllers/authController.js': '''import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { validationResult } from 'express-validator';
import { state } from '../config/demoData.js';

export const registerUser = async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ message: 'Validation failed', errors: errors.array() });
  }

  const { fullName, email, mobile, password, dateOfBirth, gender, bloodGroup, address, city, state, pinCode, role } = req.body;

  const existing = state.users.find((user) => user.email.toLowerCase() === email.toLowerCase());
  if (existing) {
    return res.status(409).json({ message: 'A user with this email already exists.' });
  }

  const newUser = {
    id: `u-${Date.now()}`,
    fullName,
    email,
    mobile,
    password: await bcrypt.hash(password, 10),
    dob: dateOfBirth,
    gender,
    bloodGroup,
    address,
    city,
    state,
    pinCode,
    role: role || 'donor',
    createdAt: new Date().toISOString()
  };

  state.users.push(newUser);

  const token = jwt.sign({ id: newUser.id, email: newUser.email, role: newUser.role }, process.env.JWT_SECRET || 'bbms-demo-secret', {
    expiresIn: '8h'
  });

  res.status(201).json({
    token,
    user: {
      id: newUser.id,
      fullName: newUser.fullName,
      email: newUser.email,
      role: newUser.role,
      bloodGroup: newUser.bloodGroup,
      city: newUser.city,
      state: newUser.state
    }
  });
};

export const loginUser = async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ message: 'Validation failed', errors: errors.array() });
  }

  const { email, password } = req.body;
  const user = state.users.find((entry) => entry.email.toLowerCase() === email.toLowerCase());

  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ message: 'Invalid email or password.' });
  }

  const token = jwt.sign({ id: user.id, email: user.email, role: user.role }, process.env.JWT_SECRET || 'bbms-demo-secret', {
    expiresIn: '8h'
  });

  return res.json({
    token,
    user: {
      id: user.id,
      fullName: user.fullName,
      email: user.email,
      role: user.role,
      bloodGroup: user.bloodGroup,
      city: user.city,
      state: user.state
    }
  });
};

export const getCurrentUser = (req, res) => {
  const user = state.users.find((entry) => entry.id === req.user.id || entry.email === req.user.email);
  if (!user) {
    return res.status(404).json({ message: 'User not found.' });
  }

  res.json({
    id: user.id,
    fullName: user.fullName,
    email: user.email,
    role: user.role,
    bloodGroup: user.bloodGroup,
    city: user.city,
    state: user.state
  });
};
''',
    'backend/src/controllers/dashboardController.js': '''import { getDashboardData } from '../services/dataService.js';

export const getDashboard = (req, res) => {
  const dashboard = getDashboardData();
  res.json(dashboard);
};
''',
    'backend/src/controllers/resourceController.js': '''import { getDonors, addDonor, updateDonor, deleteDonor, getInventory, addInventoryRecord, reserveInventory, getRequests, addRequest, updateRequestStatus, getHospitals, getNotifications, searchDonors, getReports } from '../services/dataService.js';

export const listDonors = (req, res) => res.json(getDonors());
export const createDonor = (req, res) => res.status(201).json(addDonor(req.body));
export const updateDonorById = (req, res) => {
  const result = updateDonor(req.params.id, req.body);
  if (!result) return res.status(404).json({ message: 'Donor not found.' });
  res.json(result);
};
export const deleteDonorById = (req, res) => {
  const deleted = deleteDonor(req.params.id);
  if (!deleted) return res.status(404).json({ message: 'Donor not found.' });
  res.json({ message: 'Donor removed successfully.' });
};

export const listInventory = (req, res) => res.json(getInventory());
export const createInventory = (req, res) => res.status(201).json(addInventoryRecord(req.body));
export const reserveInventoryById = (req, res) => {
  const result = reserveInventory(req.params.id, Number(req.body.quantity || 1));
  if (!result) return res.status(400).json({ message: 'Not enough stock available for reservation.' });
  res.json(result);
};

export const listRequests = (req, res) => res.json(getRequests());
export const createRequest = (req, res) => res.status(201).json(addRequest(req.body));
export const updateRequestStatusById = (req, res) => {
  const result = updateRequestStatus(req.params.id, req.body.status);
  if (!result) return res.status(404).json({ message: 'Request not found.' });
  res.json(result);
};

export const listHospitals = (req, res) => res.json(getHospitals());
export const listNotifications = (req, res) => res.json(getNotifications());

export const findDonors = (req, res) => {
  const matches = searchDonors(req.query);
  res.json(matches);
};

export const getReportData = (req, res) => res.json(getReports());
''',
    'backend/src/routes/api.js': '''import express from 'express';
import { body } from 'express-validator';
import { authenticateToken, authorizeRoles } from '../middleware/auth.js';
import { registerUser, loginUser, getCurrentUser } from '../controllers/authController.js';
import { getDashboard } from '../controllers/dashboardController.js';
import {
  listDonors,
  createDonor,
  updateDonorById,
  deleteDonorById,
  listInventory,
  createInventory,
  reserveInventoryById,
  listRequests,
  createRequest,
  updateRequestStatusById,
  listHospitals,
  listNotifications,
  findDonors,
  getReportData
} from '../controllers/resourceController.js';

const router = express.Router();

router.get('/health', (req, res) => {
  res.json({ status: 'ok', app: 'Blood Bank Management System' });
});

router.post(
  '/auth/register',
  [
    body('fullName').notEmpty().withMessage('Full name is required.'),
    body('email').isEmail().withMessage('Valid email is required.'),
    body('password').isLength({ min: 8 }).withMessage('Password must be at least 8 characters long.'),
    body('mobile').notEmpty().withMessage('Mobile number is required.')
  ],
  registerUser
);

router.post(
  '/auth/login',
  [
    body('email').isEmail().withMessage('Valid email is required.'),
    body('password').notEmpty().withMessage('Password is required.')
  ],
  loginUser
);

router.get('/auth/me', authenticateToken, getCurrentUser);

router.get('/dashboard', authenticateToken, getDashboard);
router.get('/donors', authenticateToken, listDonors);
router.post('/donors', authenticateToken, authorizeRoles('admin', 'staff'), createDonor);
router.put('/donors/:id', authenticateToken, authorizeRoles('admin', 'staff'), updateDonorById);
router.delete('/donors/:id', authenticateToken, authorizeRoles('admin'), deleteDonorById);

router.get('/inventory', authenticateToken, listInventory);
router.post('/inventory', authenticateToken, authorizeRoles('admin', 'staff'), createInventory);
router.patch('/inventory/:id/reserve', authenticateToken, authorizeRoles('admin', 'staff'), reserveInventoryById);

router.get('/requests', authenticateToken, listRequests);
router.post('/requests', authenticateToken, createRequest);
router.patch('/requests/:id/status', authenticateToken, authorizeRoles('admin', 'staff'), updateRequestStatusById);

router.get('/hospitals', authenticateToken, listHospitals);
router.get('/notifications', authenticateToken, listNotifications);
router.get('/search-donors', authenticateToken, findDonors);
router.get('/reports', authenticateToken, getReportData);

export default router;
''',
    'backend/src/server.js': '''import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import morgan from 'morgan';
import apiRoutes from './routes/api.js';
import { initExternalServices } from './config/database.js';

dotenv.config();

const app = express();
const port = Number(process.env.PORT || 5000);

app.use(
  cors({
    origin: process.env.CLIENT_URL || 'http://localhost:5173',
    credentials: true
  })
);
app.use(helmet());
app.use(
  rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 200,
    message: { message: 'Too many requests, please try again later.' }
  })
);
app.use(morgan('dev'));
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true }));

app.use('/api', apiRoutes);

app.use((req, res) => {
  res.status(404).json({ message: 'Route not found.' });
});

app.use((error, req, res, next) => {
  console.error('Unhandled server error:', error);
  res.status(500).json({ message: 'Internal Server Error' });
});

async function startServer() {
  await initExternalServices();
  app.listen(port, () => {
    console.log(`Blood Bank Management System backend running on http://localhost:${port}`);
  });
}

startServer();
''',
    'frontend/src/main.jsx': '''import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './styles.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
''',
    'frontend/src/context/AuthContext.jsx': '''import { createContext, useContext, useMemo, useState } from 'react';
import { apiFetch } from '../services/api';

const AuthContext = createContext(null);

const getStoredUser = () => {
  try {
    const raw = localStorage.getItem('bbms-user');
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};

const getStoredToken = () => localStorage.getItem('bbms-token') || '';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getStoredUser());
  const [token, setToken] = useState(getStoredToken());

  const login = async (payload) => {
    const result = await apiFetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload)
    });

    setToken(result.token);
    setUser(result.user);
    localStorage.setItem('bbms-token', result.token);
    localStorage.setItem('bbms-user', JSON.stringify(result.user));
    return result;
  };

  const register = async (payload) => {
    const result = await apiFetch('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload)
    });

    setToken(result.token);
    setUser(result.user);
    localStorage.setItem('bbms-token', result.token);
    localStorage.setItem('bbms-user', JSON.stringify(result.user));
    return result;
  };

  const logout = () => {
    setUser(null);
    setToken('');
    localStorage.removeItem('bbms-token');
    localStorage.removeItem('bbms-user');
  };

  const value = useMemo(() => ({ user, token, login, register, logout }), [user, token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
''',
    'frontend/src/services/api.js': '''const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export async function apiFetch(path, options = {}) {
  const token = localStorage.getItem('bbms-token');
  const headers = new Headers(options.headers || {});

  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers
  });

  const text = await response.text();
  const payload = text ? JSON.parse(text) : null;

  if (!response.ok) {
    throw new Error(payload?.message || 'Request failed');
  }

  return payload;
}
''',
    'frontend/src/App.jsx': '''import { Navigate, Route, Routes, Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth, AuthProvider } from './context/AuthContext';
import { apiFetch } from './services/api';
import { useEffect, useState } from 'react';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, ArcElement, Tooltip, Legend);

function App() {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  );
}

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navItems = [
    { path: '/', label: 'Home' },
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/donors', label: 'Donors' },
    { path: '/inventory', label: 'Inventory' },
    { path: '/requests', label: 'Requests' },
    { path: '/hospitals', label: 'Hospitals' },
    { path: '/reports', label: 'Reports' }
  ];

  return (
    <>
      <header className="topbar">
        <div className="brand-wrap">
          <div className="brand-mark">+</div>
          <div>
            <div className="brand-name">Blood Bank IMS</div>
            <small>LifeLink Healthcare</small>
          </div>
        </div>
        <nav className="nav">
          {navItems.map((item) => (
            <NavLink key={item.path} to={item.path} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="nav-actions">
          {!user ? (
            <>
              <Link to="/login" className="btn btn-secondary">Login</Link>
              <Link to="/register" className="btn btn-primary">Register</Link>
            </>
          ) : (
            <>
              <span className="user-badge">{user.role}</span>
              <button type="button" className="btn btn-primary" onClick={handleLogout}>Logout</button>
            </>
          )}
        </div>
      </header>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/donors" element={<ProtectedRoute><DonorsPage /></ProtectedRoute>} />
        <Route path="/inventory" element={<ProtectedRoute><InventoryPage /></ProtectedRoute>} />
        <Route path="/requests" element={<ProtectedRoute><RequestsPage /></ProtectedRoute>} />
        <Route path="/hospitals" element={<ProtectedRoute><HospitalsPage /></ProtectedRoute>} />
        <Route path="/reports" element={<ProtectedRoute><ReportsPage /></ProtectedRoute>} />
      </Routes>
    </>
  );
}

function HeroMetrics({ stats }) {
  const cards = [
    { label: 'Registered Donors', value: stats?.totalDonors ?? 0 },
    { label: 'Total Donations', value: stats?.totalDonations ?? 0 },
    { label: 'Available Blood Units', value: stats?.totalBloodUnits ?? 0 },
    { label: 'Partner Hospitals', value: stats?.registeredHospitals ?? 0 }
  ];

  return (
    <div className="hero-metrics">
      {cards.map((card) => (
        <div key={card.label} className="metric-card">
          <span>{card.label}</span>
          <strong>{card.value}</strong>
        </div>
      ))}
    </div>
  );
}

function HomePage() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    apiFetch('/dashboard')
      .then((data) => setStats(data))
      .catch(() => setStats(null));
  }, []);

  return (
    <main className="page home-page">
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">Reliable blood access</span>
          <h1>Donate Blood, Save Lives</h1>
          <p>Connecting blood donors, hospitals, and patients through a secure, transparent blood management platform.</p>
          <div className="cta-row">
            <Link to="/reports" className="btn btn-primary">Find Blood</Link>
            <Link to="/register" className="btn btn-secondary">Become a Donor</Link>
          </div>
          <HeroMetrics stats={stats} />
        </div>
        <div className="hero-panel">
          <div className="mini-card">
            <h3>Blood availability</h3>
            <ul>
              <li>A+: 12 units</li>
              <li>O+: 17 units</li>
              <li>AB+: 9 units</li>
              <li>O-: 6 units</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="info-grid">
        <div className="feature-block">
          <h3>About us</h3>
          <p>LifeLink Blood Bank is a secure community-led initiative to streamline donor engagement, blood inventory, and emergency support.</p>
        </div>
        <div className="feature-block">
          <h3>Available blood</h3>
          <p>Track inventory by blood group and blood component with expiry and low-stock monitoring built in.</p>
        </div>
        <div className="feature-block">
          <h3>Find donors</h3>
          <p>Search by blood group, city, district, pincode, and availability to match eligible donors quickly.</p>
        </div>
      </section>

      <section className="section-grid">
        <div className="panel">
          <h3>Blood donation process</h3>
          <ol className="timeline">
            <li>Register and complete medical screening</li>
            <li>Donate at an approved blood camp or center</li>
            <li>Approval and safe collection into inventory</li>
            <li>Emergency requests are matched by compatibility rules</li>
          </ol>
        </div>
        <div className="panel">
          <h3>Donation awareness</h3>
          <p>Each unit of blood can help multiple patients. Regular voluntary donation helps maintain healthy inventories and faster response times during emergencies.</p>
        </div>
      </section>
    </main>
  );
}

function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: 'admin@bbms.local', password: 'Admin@123' });
  const [error, setError] = useState('');

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await login(form);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <main className="auth-shell">
      <div className="auth-card">
        <h2>Login</h2>
        {error && <div className="alert error">{error}</div>}
        <form onSubmit={handleSubmit} className="stack-form">
          <label>
            Email
            <input name="email" value={form.email} onChange={handleChange} />
          </label>
          <label>
            Password
            <input type="password" name="password" value={form.password} onChange={handleChange} />
          </label>
          <button type="submit" className="btn btn-primary full-width">Sign In</button>
        </form>
      </div>
    </main>
  );
}

function RegisterPage() {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [form, setForm] = useState({
    fullName: 'New Donor',
    email: 'newdonor@example.com',
    mobile: '+91 9000000000',
    password: 'Password@123',
    dateOfBirth: '2001-02-03',
    gender: 'Female',
    bloodGroup: 'A+',
    address: '12 Test Lane',
    city: 'Bengaluru',
    state: 'Karnataka',
    pinCode: '560018',
    role: 'donor'
  });
  const [error, setError] = useState('');

  const handleChange = (event) => {
    setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await register(form);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <main className="auth-shell">
      <div className="auth-card wide">
        <h2>Create account</h2>
        {error && <div className="alert error">{error}</div>}
        <form onSubmit={handleSubmit} className="stack-form grid-two">
          <label>Full name<input name="fullName" value={form.fullName} onChange={handleChange} /></label>
          <label>Email<input name="email" value={form.email} onChange={handleChange} /></label>
          <label>Mobile<input name="mobile" value={form.mobile} onChange={handleChange} /></label>
          <label>Password<input type="password" name="password" value={form.password} onChange={handleChange} /></label>
          <label>Date of birth<input type="date" name="dateOfBirth" value={form.dateOfBirth} onChange={handleChange} /></label>
          <label>Gender<select name="gender" value={form.gender} onChange={handleChange}><option>Female</option><option>Male</option><option>Other</option></select></label>
          <label>Blood group<select name="bloodGroup" value={form.bloodGroup} onChange={handleChange}><option>A+</option><option>A-</option><option>B+</option><option>B-</option><option>AB+</option><option>AB-</option><option>O+</option><option>O-</option></select></label>
          <label>Role<select name="role" value={form.role} onChange={handleChange}><option value="donor">Donor</option><option value="staff">Blood Bank Staff</option><option value="admin">Admin</option><option value="hospital">Hospital Staff</option></select></label>
          <label className="span-two">Address<input name="address" value={form.address} onChange={handleChange} /></label>
          <label>City<input name="city" value={form.city} onChange={handleChange} /></label>
          <label>State<input name="state" value={form.state} onChange={handleChange} /></label>
          <label>PIN code<input name="pinCode" value={form.pinCode} onChange={handleChange} /></label>
          <button type="submit" className="btn btn-primary full-width span-two">Register</button>
        </form>
      </div>
    </main>
  );
}

function DashboardPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    apiFetch('/dashboard')
      .then((payload) => setData(payload))
      .catch((error) => console.error(error));
  }, []);

  if (!data) return <div className="page"><h2>Loading dashboard...</h2></div>;

  const chartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{ label: 'Monthly donations', data: data.donationTrend.map((item) => item.value), borderColor: '#c62828', backgroundColor: 'rgba(198,40,40,0.2)' }]
  };

  const inventoryChart = {
    labels: data.bloodGroupDistribution.map((item) => item.label),
    datasets: [{ label: 'Units', data: data.bloodGroupDistribution.map((item) => item.value), backgroundColor: ['#d32f2f', '#ef5350', '#f48fb1', '#ffab91', '#b39ddb', '#90caf9', '#80cbc4', '#aed581'] }]
  };

  return (
    <main className="page dashboard">
      <h1>Admin dashboard</h1>
      <div className="stats-grid">
        <StatCard label="Total Donors" value={data.totalDonors} />
        <StatCard label="Total Donations" value={data.totalDonations} />
        <StatCard label="Total Blood Units" value={data.totalBloodUnits} />
        <StatCard label="Pending Requests" value={data.pendingRequests} />
        <StatCard label="Approved Requests" value={data.approvedRequests} />
        <StatCard label="Registered Hospitals" value={data.registeredHospitals} />
      </div>

      <div className="chart-grid">
        <div className="panel chart-panel">
          <h3>Monthly donation trends</h3>
          <Line data={chartData} />
        </div>
        <div className="panel chart-panel">
          <h3>Blood inventory by group</h3>
          <Bar data={inventoryChart} />
        </div>
      </div>

      <div className="list-grid">
        <div className="panel">
          <h3>Recent donations</h3>
          <ul className="simple-list">
            {data.recentDonations.map((donation) => (
              <li key={donation.id}><span>{donation.donorName}</span><span>{donation.bloodGroup}</span></li>
            ))}
          </ul>
        </div>
        <div className="panel">
          <h3>Low stock alerts</h3>
          <ul className="simple-list">
            {data.lowStockAlerts.map((item) => (
              <li key={item.id}><span>{item.bloodGroup}</span><span>{item.units} units</span></li>
            ))}
          </ul>
        </div>
      </div>
    </main>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="stat-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function DonorsPage() {
  const [donors, setDonors] = useState([]);
  useEffect(() => {
    apiFetch('/donors')
      .then((payload) => setDonors(payload))
      .catch((error) => console.error(error));
  }, []);

  return (
    <main className="page">
      <div className="section-head">
        <h1>Donor management</h1>
        <button className="btn btn-primary" type="button">Add donor</button>
      </div>
      <div className="table-card">
        <table>
          <thead>
            <tr><th>ID</th><th>Name</th><th>Blood</th><th>City</th><th>Status</th><th>Eligibility</th></tr>
          </thead>
          <tbody>
            {donors.map((donor) => (
              <tr key={donor.id}>
                <td>{donor.id}</td>
                <td>{donor.name}</td>
                <td>{donor.bloodGroup}</td>
                <td>{donor.city}</td>
                <td>{donor.status}</td>
                <td>{donor.eligible ? 'Eligible' : 'Not eligible'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}

function InventoryPage() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    apiFetch('/inventory').then((payload) => setItems(payload)).catch(console.error);
  }, []);

  return (
    <main className="page">
      <h1>Blood inventory management</h1>
      <div className="table-card">
        <table>
          <thead>
            <tr><th>Blood group</th><th>Units</th><th>Reserved</th><th>Expiry</th><th>Component</th><th>Status</th></tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.bloodGroup}</td>
                <td>{item.units}</td>
                <td>{item.reserved}</td>
                <td>{item.expiryDate}</td>
                <td>{item.component}</td>
                <td>{item.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}

function RequestsPage() {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    apiFetch('/requests').then((payload) => setRequests(payload)).catch(console.error);
  }, []);

  return (
    <main className="page">
      <h1>Blood requests</h1>
      <div className="table-card">
        <table>
          <thead>
            <tr><th>Patient</th><th>Hospital</th><th>Blood group</th><th>Units</th><th>Status</th></tr>
          </thead>
          <tbody>
            {requests.map((request) => (
              <tr key={request.id}>
                <td>{request.patientName}</td>
                <td>{request.hospitalName}</td>
                <td>{request.bloodGroup}</td>
                <td>{request.units}</td>
                <td>{request.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}

function HospitalsPage() {
  const [hospitals, setHospitals] = useState([]);

  useEffect(() => {
    apiFetch('/hospitals').then((payload) => setHospitals(payload)).catch(console.error);
  }, []);

  return (
    <main className="page">
      <h1>Hospitals</h1>
      <div className="card-grid">
        {hospitals.map((hospital) => (
          <div key={hospital.id} className="info-card">
            <h3>{hospital.name}</h3>
            <p>{hospital.city}</p>
            <p>{hospital.contactPerson}</p>
            <p>{hospital.phone}</p>
          </div>
        ))}
      </div>
    </main>
  );
}

function ReportsPage() {
  const [reports, setReports] = useState(null);

  useEffect(() => {
    apiFetch('/reports').then((payload) => setReports(payload)).catch(console.error);
  }, []);

  if (!reports) return <main className="page"><h1>Loading reports...</h1></main>;

  const reportData = {
    labels: reports.daily.map((entry) => entry.date),
    datasets: [{ label: 'Daily donations', data: reports.daily.map((entry) => entry.donations), backgroundColor: '#d32f2f' }]
  };

  const donut = {
    labels: reports.inventorySummary.map((entry) => entry.bloodGroup),
    datasets: [{ data: reports.inventorySummary.map((entry) => entry.available), backgroundColor: ['#d32f2f', '#ef5350', '#f48fb1', '#ffab91', '#b39ddb', '#90caf9'] }]
  };

  return (
    <main className="page">
      <h1>Reports and analytics</h1>
      <div className="chart-grid">
        <div className="panel chart-panel">
          <h3>Daily donation reports</h3>
          <Bar data={reportData} />
        </div>
        <div className="panel chart-panel">
          <h3>Blood group availability</h3>
          <Doughnut data={donut} />
        </div>
      </div>
    </main>
  );
}

export default App;
''',
    'frontend/src/styles.css': '''* {
  box-sizing: border-box;
}

:root {
  --bg: #f5f1f1;
  --panel: #ffffff;
  --primary: #b71c1c;
  --primary-dark: #7f0000;
  --primary-soft: #fdeaea;
  --text: #1d1d1d;
  --muted: #5f5f5f;
  --border: #eadcdc;
  --shadow: 0 12px 30px rgba(137, 26, 26, 0.08);
}

body {
  margin: 0;
  font-family: 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
}

a {
  text-decoration: none;
}

button, input, select {
  font: inherit;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 28px;
  background: rgba(255, 255, 255, 0.95);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(12px);
}

.brand-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-mark {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  color: white;
  font-size: 1.5rem;
  background: linear-gradient(135deg, #c62828, #ef5350);
}

.brand-name {
  font-weight: 700;
}

.nav {
  display: flex;
  gap: 18px;
}

.nav-link {
  color: var(--muted);
  font-weight: 600;
}

.nav-link.active {
  color: var(--primary);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn {
  border: none;
  border-radius: 10px;
  padding: 10px 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
}

.btn-secondary {
  background: var(--primary-soft);
  color: var(--primary);
}

.user-badge {
  padding: 8px 12px;
  border-radius: 999px;
  background: #f4e1e1;
  color: var(--primary);
  text-transform: uppercase;
  font-size: 0.72rem;
  font-weight: 700;
}

.page,
.auth-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 18px 60px;
}

.hero {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 24px;
  padding: 40px 18px 0;
  align-items: center;
}

.hero-copy {
  background: linear-gradient(135deg, #fff, #fff8f8);
  border-radius: 28px;
  padding: 40px;
  box-shadow: var(--shadow);
}

.eyebrow {
  display: inline-block;
  background: var(--primary-soft);
  color: var(--primary);
  padding: 8px 12px;
  border-radius: 999px;
  font-weight: 700;
  margin-bottom: 16px;
}

.hero-copy h1 {
  margin: 0 0 14px;
  font-size: clamp(2.4rem, 5vw, 4.5rem);
  line-height: 1.1;
}

.hero-copy p {
  color: var(--muted);
  font-size: 1.04rem;
  max-width: 620px;
}

.cta-row {
  display: flex;
  gap: 12px;
  margin: 24px 0 28px;
}

.hero-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.metric-card,
.stat-card,
.panel,
.info-card,
.auth-card,
.table-card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 18px;
  box-shadow: var(--shadow);
}

.metric-card,
.stat-card {
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric-card span,
.stat-card span {
  color: var(--muted);
  font-size: 0.8rem;
}

.metric-card strong,
.stat-card strong {
  font-size: 1.8rem;
}

.hero-panel {
  display: flex;
  align-items: center;
  justify-content: center;
}

.mini-card {
  width: 100%;
  background: linear-gradient(180deg, #fff, #fff2f2);
  border-radius: 28px;
  padding: 28px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

.mini-card h3 {
  margin-top: 0;
}

.mini-card ul {
  padding-left: 20px;
  color: var(--muted);
  line-height: 2;
}

.info-grid,
.section-grid,
.chart-grid,
.list-grid,
.card-grid,
.stats-grid {
  display: grid;
  gap: 18px;
  margin-top: 26px;
}

.info-grid { grid-template-columns: repeat(3, 1fr); }
.section-grid { grid-template-columns: repeat(2, 1fr); }
.chart-grid { grid-template-columns: repeat(2, 1fr); }
.list-grid { grid-template-columns: repeat(2, 1fr); }
.card-grid { grid-template-columns: repeat(3, 1fr); }
.stats-grid { grid-template-columns: repeat(6, 1fr); }

.feature-block,
.panel,
.info-card {
  padding: 22px;
}

.timeline {
  margin: 0;
  padding-left: 20px;
  color: var(--muted);
  line-height: 2;
}

.auth-shell {
  display: grid;
  place-items: center;
  min-height: calc(100vh - 90px);
}

.auth-card {
  width: min(100%, 560px);
  padding: 28px;
}

.auth-card.wide {
  width: min(100%, 760px);
}

.stack-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.grid-two {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 8px;
  color: var(--muted);
  font-weight: 600;
}

input, select {
  width: 100%;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: #fff;
}

.full-width {
  width: 100%;
}

.span-two {
  grid-column: span 2;
}

.alert {
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 18px;
}

.alert.error {
  background: #ffebee;
  color: #b71c1c;
}

.table-card {
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--border);
  text-align: left;
}

th {
  background: #f9f3f3;
}

.chart-panel {
  min-height: 280px;
}

@media (max-width: 960px) {
  .hero,
  .stats-grid,
  .info-grid,
  .section-grid,
  .chart-grid,
  .list-grid,
  .card-grid,
  .grid-two {
    grid-template-columns: 1fr;
  }

  .topbar {
    flex-wrap: wrap;
    gap: 16px;
  }

  .nav {
    flex-wrap: wrap;
  }
}
''',
    'database/postgresql/schema.sql': '''CREATE TABLE roles (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL,
  description TEXT
);

CREATE TABLE users (
  id UUID PRIMARY KEY,
  full_name VARCHAR(150) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  mobile VARCHAR(20) NOT NULL,
  password_hash TEXT NOT NULL,
  dob DATE,
  gender VARCHAR(20),
  blood_group VARCHAR(5),
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(100),
  pin_code VARCHAR(20),
  role_id INTEGER REFERENCES roles(id),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE donors (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR(150) NOT NULL,
  dob DATE,
  gender VARCHAR(20),
  blood_group VARCHAR(5),
  phone VARCHAR(20),
  email VARCHAR(150),
  address TEXT,
  city VARCHAR(100),
  district VARCHAR(100),
  pincode VARCHAR(20),
  weight NUMERIC(5,2),
  last_donation_date DATE,
  eligibility_status BOOLEAN DEFAULT TRUE,
  availability_status VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE hospitals (
  id UUID PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  type VARCHAR(50),
  city VARCHAR(100),
  district VARCHAR(100),
  phone VARCHAR(20),
  email VARCHAR(150),
  address TEXT,
  contact_person VARCHAR(150),
  status VARCHAR(50) DEFAULT 'Active',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE blood_banks (
  id UUID PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  city VARCHAR(100),
  address TEXT,
  phone VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE donations (
  id UUID PRIMARY KEY,
  donor_id UUID REFERENCES donors(id),
  donation_date DATE NOT NULL,
  blood_group VARCHAR(5) NOT NULL,
  quantity_ml INTEGER NOT NULL CHECK (quantity_ml > 0),
  donation_center VARCHAR(150),
  screening_status VARCHAR(50),
  medical_eligibility VARCHAR(50),
  approved BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE blood_inventory (
  id UUID PRIMARY KEY,
  blood_group VARCHAR(5) NOT NULL,
  component VARCHAR(50) NOT NULL,
  available_units INTEGER NOT NULL DEFAULT 0 CHECK (available_units >= 0),
  reserved_units INTEGER NOT NULL DEFAULT 0 CHECK (reserved_units >= 0),
  expired_units INTEGER NOT NULL DEFAULT 0 CHECK (expired_units >= 0),
  min_stock INTEGER DEFAULT 5,
  expiry_date DATE,
  storage_location VARCHAR(100),
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE blood_requests (
  id UUID PRIMARY KEY,
  patient_name VARCHAR(150) NOT NULL,
  patient_age INTEGER NOT NULL,
  hospital_id UUID REFERENCES hospitals(id),
  hospital_contact VARCHAR(20),
  required_blood_group VARCHAR(5),
  blood_component VARCHAR(50),
  required_units INTEGER CHECK (required_units > 0),
  required_date DATE,
  emergency_level VARCHAR(30),
  doctor_info TEXT,
  status VARCHAR(50) DEFAULT 'Pending',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE blood_reservations (
  id UUID PRIMARY KEY,
  request_id UUID REFERENCES blood_requests(id),
  inventory_id UUID REFERENCES blood_inventory(id),
  reserved_units INTEGER NOT NULL CHECK (reserved_units > 0),
  reservation_status VARCHAR(30) DEFAULT 'Reserved',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE blood_issues (
  id UUID PRIMARY KEY,
  request_id UUID REFERENCES blood_requests(id),
  issued_by UUID REFERENCES users(id),
  issued_units INTEGER NOT NULL,
  issued_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE notifications (
  id UUID PRIMARY KEY,
  title VARCHAR(150),
  message TEXT,
  type VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW(),
  read_flag BOOLEAN DEFAULT FALSE
);

CREATE TABLE audit_records (
  id UUID PRIMARY KEY,
  entity_type VARCHAR(50),
  entity_id UUID,
  action VARCHAR(100),
  actor_id UUID REFERENCES users(id),
  details JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_donors_blood_group ON donors(blood_group);
CREATE INDEX idx_donors_city ON donors(city);
CREATE INDEX idx_inventory_group ON blood_inventory(blood_group);
CREATE INDEX idx_requests_status ON blood_requests(status);
''',
    'database/mongodb/schemas.md': '''# MongoDB schema design

## Collection: activity_logs
```
{
  _id: ObjectId,
  userId: "u-001",
  action: "login",
  ipAddress: "192.168.1.5",
  userAgent: "Mozilla/5.0",
  timestamp: ISODate("2024-11-10T12:00:00Z"),
  metadata: { page: "/dashboard", role: "admin" }
}
```

## Collection: donation_events
```
{
  _id: ObjectId,
  donationId: "DN-3001",
  donorId: "D-1001",
  action: "approved",
  screeningStatus: "Approved",
  timestamp: ISODate("2024-11-01T08:30:00Z")
}
```

## Collection: notifications
```
{
  _id: ObjectId,
  receiverId: "u-002",
  title: "Low stock alert",
  message: "A- units are below minimum threshold",
  status: "unread",
  createdAt: ISODate("2024-11-06T09:00:00Z")
}
```

## Collection: audit_events
```
{
  _id: ObjectId,
  entity: "blood_request",
  entityId: "BR-5001",
  event: "approved",
  actor: "admin@bbms.local",
  details: { approvedBy: "admin" },
  createdAt: ISODate("2024-11-07T10:00:00Z")
}
```

These flexible documents are stored in MongoDB because they are event-centric, semi-structured, and write-heavy, unlike transactional relational data that obeys structured schema constraints in PostgreSQL.
''',
    'database/neo4j/queries.cypher': '''CREATE (:BloodGroup {name: 'A+'}), (:BloodGroup {name: 'A-'}), (:BloodGroup {name: 'B+'}), (:BloodGroup {name: 'B-'}), (:BloodGroup {name: 'AB+'}), (:BloodGroup {name: 'AB-'}), (:BloodGroup {name: 'O+'}), (:BloodGroup {name: 'O-'});

CREATE (:Donor {id: 'D-1001', name: 'Rahul Menon', bloodGroup: 'B+', city: 'Mysuru', eligible: true})
CREATE (:Donor {id: 'D-1002', name: 'Ananya Rao', bloodGroup: 'O+', city: 'Bengaluru', eligible: true})
CREATE (:Hospital {id: 'H-2001', name: 'City Care Hospital', city: 'Bengaluru'})
CREATE (:BloodBank {id: 'BB-1', name: 'Mysuru Blood Center', city: 'Mysuru'})
CREATE (:BloodRequest {id: 'BR-5001', patientName: 'Suresh Kumar', requiredUnits: 2})

MATCH (d:Donor {id: 'D-1001'}), (bg:BloodGroup {name: 'B+'}) MERGE (d)-[:HAS_BLOOD_GROUP]->(bg);
MATCH (d:Donor {id: 'D-1001'}), (l:Location {city: 'Mysuru'}) MERGE (d)-[:LOCATED_IN]->(l);
MATCH (h:Hospital {id: 'H-2001'}), (r:BloodRequest {id: 'BR-5001'}) MERGE (h)-[:REQUESTS]->(r);
MATCH (bb:BloodBank {id: 'BB-1'}), (h:Hospital {id: 'H-2001'}) MERGE (bb)-[:SERVES]->(h);

// Eligible donor candidates
MATCH (d:Donor)-[:HAS_BLOOD_GROUP]->(bg:BloodGroup {name: 'O+'})
WHERE d.eligible = true
RETURN d.name, d.city;

// Nearby donor-hospital relationships
MATCH (d:Donor)-[:LOCATED_IN]->(:Location {city: 'Mysuru'})
MATCH (h:Hospital {city: 'Mysuru'})
RETURN d.name, h.name;

// Hospital demand pattern
MATCH (h:Hospital)-[:REQUESTS]->(r:BloodRequest)
RETURN h.name, count(r) AS requestCount;

// Blood bank distribution network
MATCH (bb:BloodBank)-[:SERVES]->(h:Hospital)
RETURN bb.name, h.name;
''',
    'database/seed/demo-data.sql': '''INSERT INTO roles (name, description) VALUES
('admin', 'System administrator'),
('staff', 'Blood bank staff'),
('donor', 'Blood donor'),
('hospital_staff', 'Hospital staff');

INSERT INTO users (id, full_name, email, mobile, password_hash, dob, gender, blood_group, address, city, state, pin_code, role_id)
VALUES
('11111111-1111-1111-1111-111111111111', 'System Administrator', 'admin@bbms.local', '+91 9876543210', '$2a$10$X1k0wWqz0GVtA1j6QBV9H.MQ6Z8WvO1V3Vd3isERfYq8srO7JX2rq', '1990-01-01', 'Male', 'O+', '12 Blood Care Ave', 'Bengaluru', 'Karnataka', '560001', 1);
''',
    'docs/architecture.md': '''# System Architecture

The blood bank system is designed around a modular three-layer architecture.

- Presentation Layer: React frontend dashboard and landing page
- Application Layer: Express.js REST API with role-based access
- Data Layer: PostgreSQL for transactional records, MongoDB for event logs, Neo4j for graph relationships, Redis for cached reads

## Workflow

1. A donor registers or logs in.
2. The system validates credentials and issues a JWT.
3. Donations and blood requests are created through authenticated endpoints.
4. Inventory changes are validated before stock calculation updates.
5. Dashboard analytics aggregate the transactional state and cached summaries.
6. MongoDB logs activity and notifications, while Neo4j exposes donor-network relationships.
''',
    'docs/database-design.md': '''# Database Design Notes

## PostgreSQL
Use PostgreSQL for transactional consistency, relations, constraints, and ACID behavior in the core EMS operation.

## MongoDB
Use MongoDB for operational logs, notifications, and system events because these are document-shaped, append-heavy, and less strict than relational operations.

## Neo4j
Use Neo4j to model relationships between donors, hospitals, blood banks, and requests for graph-based exploration and network analysis.

## Redis
Use Redis for in-memory cache such as dashboard totals, inventory counts, and donor search results.
''',
    'docs/api-documentation.md': '''# API Overview

## Authentication
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me

## Dashboard
- GET /api/dashboard

## Resources
- GET /api/donors
- POST /api/donors
- PUT /api/donors/:id
- DELETE /api/donors/:id
- GET /api/inventory
- POST /api/inventory
- PATCH /api/inventory/:id/reserve
- GET /api/requests
- POST /api/requests
- PATCH /api/requests/:id/status
- GET /api/hospitals
- GET /api/notifications
- GET /api/search-donors
- GET /api/reports
''',
    'docs/deployment-guide.md': '''# Azure Deployment Guide

1. Provision Azure App Service and PostgreSQL flexible server.
2. Configure environment variables in App Service settings.
3. Set `CLIENT_URL` to the frontend domain.
4. Store secrets in Azure Key Vault and reference them via App Service settings.
5. Deploy backend using Node.js runtime.
6. Deploy frontend to Azure Static Web Apps or a static host.
7. Configure CORS, rate limiting, and managed Redis / Neo4j endpoints as needed.

For local testing, use docker-compose config in the repository root.
''',
    'frontend/index.html': '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Blood Bank IMS</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
''',
    'frontend/vite.config.js': '''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173
  },
  preview: {
    host: '0.0.0.0',
    port: 4173
  }
});
''',
    'backend/.env.example': '''PORT=5000
JWT_SECRET=change-me
POSTGRES_URL=postgresql://postgres:postgres@localhost:5432/bbms
MONGO_URI=mongodb://localhost:27017/bbms
REDIS_URL=redis://localhost:6379
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
CLIENT_URL=http://localhost:5173
''',
    '.gitignore': '''node_modules
backend/node_modules
frontend/node_modules
.env
.DS_Store
dist
coverage
'''
}

for relative_path, content in files.items():
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print(f'Created {len(files)} files in {root}')
