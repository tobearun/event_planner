# 🗓️ Flask Event Planner

A role-based event management web app built using Flask. It allows users to register/login, view events, register for them, and — depending on their role — create or manage events.

## 🚀 Features

### 👤 User Authentication
- Secure registration and login using **bcrypt** for password hashing.
- **Role-based access control** with 3 roles:
  - **Admin** – can delete any event (coming soon).
  - **Creator** – can create, edit, and manage their own events.
  - **User** – can view and register for events.

### 📅 Event Management
- Creators can create events with title, description, date, and venue.
- All users can view upcoming events.
- Logged-in users can register for events.

### 🧾 User Dashboard
- Logged-in users can see the list of events they have registered for.
- Displays event title, date, venue, and description in an organized list.

### ✅ Registration Validation
- Prevents duplicate event registration for the same user.
- Flash messages for success, errors, or duplicate registrations.

## 🔐 Tech Stack

- **Flask**: Web framework
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and validation
- **Flask-Bcrypt**: Password hashing
- **Flask-SQLAlchemy**: ORM for database operations
- **SQLite**: Default database used for development

## ⚙️ How It Works

- Each `User` has a `role` field that determines what they can do.
- `Event` is linked to a `creator` (User with role "creator").
- `EventRegistration` tracks which users are registered for which events.
- Relationships between models are set up properly to avoid circular imports.

## 🧠 Learning-Oriented Build

This project was developed as a learning project with the following principles:
- **Code snippets over copy-paste** to encourage debugging and understanding.
- **Minimal scaffolding** to understand how routes, forms, models, and templates connect.
- **Step-by-step supervision** to catch and fix bugs quickly while learning.

## 🔧 Future Features (Planned)
- Admin dashboard for deleting/editing all events.
- Creator dashboard with edit/delete options for their own events.
- Pagination or filtering of events.
- Email confirmation for event registration.

---
