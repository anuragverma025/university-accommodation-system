# 🛠️ How It Works: University Accommodation System

This document provides a deep-dive into the internal orchestration of the University Accommodation Office Management System, covering the Database, Backend, and Frontend layers.

---

## 1. Database Layer (MySQL 8.0)

The database is designed to be the "source of truth" and handles both storage and critical business logic.

### 🧬 Normalization (3NF)
The schema is normalized to the **Third Normal Form (3NF)** to eliminate data redundancy.
- **Example**: Student contact info is in `students`, but their next-of-kin info is in a separate `next_of_kin` table (linked by `banner_id`). This prevents repeating kin data for every student record.

### ⚡ Advanced SQL Objects
*   **Stored Procedures (`sp_place_student`)**: Handles the **Atomic Transaction** of assigning a student to a room. It ensures that the `leases` record is created AND the student's `status` is updated to 'Placed' simultaneously.
*   **Functions (`fn_get_student_total_debt`)**: A reusable calculation that sums up all `amount_due` from `invoices` where `date_paid` is NULL for a specific student.
*   **Triggers (`trg_rooms_before_insert`)**: Enforces integrity at the lowest level. It ensures a room belongs to **exactly one** residence type (Hall or Apartment).
*   **Views**: Abstract complex JOINs into simple virtual tables (e.g., `v_unpaid_invoices` joins Students, Leases, and Invoices).

---

## 2. Backend Layer (FastAPI)

The backend is a high-performance Python API that acts as a secure bridge.

### 🔐 Security & Auth
*   **JWT (JSON Web Tokens)**: Located in `backend/app/auth.py`. 
    *   When you login, the server validates your password using `passlib` (PBKDF2 hashing).
    *   It issues a signed JWT containing your `username` and `role`.
*   **Role-Based Access Control (RBAC)**:
    *   Endpoints are protected by decorators like `Depends(WRITE_ROLES)`.
    *   If a `viewer` tries to `DELETE`, the backend rejects it with a `403 Forbidden` before it ever touches the database.

### 🛠️ Generic CRUD Engine (`main.py`)
Commonly, APIs have hundreds of lines of repetitive code for every table. This project uses **SQLAlchemy Core Reflection**:
1.  At startup, it "reflects" (reads) the MySQL schema.
2.  It uses a `TABLE_CONFIG` dictionary to map URL strings (like `/api/students`) to actual DB tables.
3.  A single function handles GET/POST/PUT/DELETE for **all 10 tables** dynamically.

---

## 3. Frontend Layer (React + Vite)

The frontend is a modern, responsive dashboard built for administrative efficiency.

### 🔄 Data Orchestration
*   **Centralized API Client (`frontend/src/lib/api.ts`)**: Every request goes through the `apiRequest` helper. It automatically checks if a user is logged in and attaches the `Authorization: Bearer <token>` header to the request.
*   **Config-Driven UI**: The fields you see in forms and tables are defined in `frontend/src/config/entities.ts`. This makes the UI easy to extend—if you add a column to the DB, you just add one line to the config, and the UI handles the rest.

### 🎨 Visuals & UX
*   **Tailwind CSS**: Provides the modern, professional layout.
*   **Framer Motion**: Adds micro-animations to the "Pulse" dashboard and page transitions, making the app feel high-end and responsive.

---

## 4. End-to-End Data Flow Example
**Scenario: A Manager updates a Student's address.**

1.  **UI**: Manager edits the address in the `EntityStudio` and clicks **Save**.
2.  **Frontend**: The `apiPut` function sends a request to `PUT /api/students/B001` with the new address in the body.
3.  **Backend**: The `update_record` route in `main.py` receives the request.
4.  **Auth**: The backend decodes the JWT to ensure the user is at least a `manager`.
5.  **ORM**: SQLAlchemy generates an `UPDATE students SET street = ... WHERE banner_id = 'B001'` query.
6.  **Database**: MySQL executes the update, checking any constraints (e.g., if the student exists).
7.  **Response**: The Backend sends back the updated student record in JSON.
8.  **UI**: The Frontend updates the local state and shows a "Success" notification.

---
*End of Documentation*
