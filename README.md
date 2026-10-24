# LaundryCare - Laundry and Dry Cleaning Management System

## Project Overview
LaundryCare is a web-based application designed to manage laundry and dry cleaning services. It helps customers place orders, track order progress, view deliveries, check payment details, and receive notifications.

## Features
- Customer Registration and Login
- Customer Profile and Address Management
- Laundry Service Selection
- Order Placement and Tracking
- Processing Stage Management
- Delivery Management
- Payment and Billing Records
- Customer Notifications
- Daily Orders Report
- Revenue Report

## Technologies Used
- Frontend: HTML, CSS, JavaScript, React, Tailwind CSS
- Backend: Python, Django, Django REST Framework
- Database: SQLite
- Version Control: Git and GitHub

## Project Structure
- `backend/` - Django backend, database models, views, APIs, and templates
- `frontend/` - React frontend application

## Local Setup

### Backend
1. Create and activate a Python virtual environment.
2. Open a terminal in the `backend` directory.
3. Install Django and the other required dependencies.
4. Run database migrations:

   `python manage.py migrate`

5. Start the server:

   `python manage.py runserver`

Backend URL: http://127.0.0.1:8000/

### Frontend
1. Open a terminal in the `frontend` directory.
2. Install dependencies:

   `npm install`

3. Start the development server:

   `npm run dev`

Frontend URL: http://localhost:5173/

## Testing

The project has been tested for customer order placement, quantity validation, order tracking, delivery validation, payment calculations, payment status updates, customer notifications, reports, and password reset functionality.

Gmail SMTP email delivery has been configured and tested successfully for password reset emails.

## Project Status

The application is in the final testing and deployment preparation stage. Gmail SMTP email delivery and password reset functionality have been verified. Frontend and backend deployment and production configuration are pending.

## Documentation

Project documentation, including the Entity Relationship Diagram (ERD), Data Flow Diagram (DFD), and UI Design, is available in the `docs/` directory.
