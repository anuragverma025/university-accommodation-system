# 🎓 University Accommodation Office - Viva Study Guide

This guide is designed to help you ace your Viva. It covers the **Database Design**, **Application Architecture**, and **Sample Queries**.

> [!TIP]
> **To get this as a PDF:** Open this file in your editor/browser, press **Ctrl + P**, and select **"Save as PDF"**.

---

## 1. Project Overview
A full-stack management system for University Accommodations (Halls and Apartments). 
- **Frontend**: React + Vite + TailwindCSS (Modern, Responsive, Component-based)
- **Backend**: FastAPI (Python) - High performance, asynchronous.
- **Database**: MySQL 8.0 - Relational, ACID compliant.

---

## 2. Database Design & Normalization

### Normal Forms (3NF)
We followed the **Third Normal Form (3NF)** rules to ensure zero data redundancy:
1.  **1NF (First Normal Form)**: Every cell contains a single value, and each record is unique (Primary Keys).
2.  **2NF (Second Normal Form)**: No partial dependencies. Every non-key column depends on the *entire* primary key.
3.  **3NF (Third Normal Form)**: No transitive dependencies. Non-key columns do not depend on other non-key columns. 
    - *Example*: We store `advisor_staff_id` in the Student table, but not the Adviser's phone number. The phone number is in the `staff` table, linked by ID.

### Key Relationships (ER Diagram structure)
- **Adviser (1:M)**: One staff member can be an adviser to many students.
- **Hall Manager (1:1)**: One hall has exactly one manager.
- **Lease (M:1)**: Many leases can exist for one student over different years, but each lease belongs to exactly one student.
- **Next-of-Kin (1:1)**: Every student can have one primary next-of-kin record.

---

## 3. Advanced DBMS Features (Teacher's Favorites)

### ✅ Stored Procedures (`sp_place_student`)
**What is it?** A prepared SQL code that you can save and reuse.
**Why we used it?** To handle "Transactions." When we place a student, we must:
1. Create a Lease.
2. Update Student status to 'Placed'.
If one fails, the other rolls back (Atomicity). This maintains data integrity.

### ✅ Functions (`fn_get_student_total_debt`)
**What is it?** A reusable calculation stored in the database.
**Why we used it?** To instantly calculate a student's total debt (sum of unpaid invoices). It's more efficient than recalculating it in the backend every time.

### ✅ Triggers
We implemented **Before Insert Triggers** to ensure a room belongs to either a Hall or an Apartment, but never both. This prevents logical conflicts in our data.

---

## 4. Query Mapping (Assignment Requirements a-n)

| Item | Requirement | SQL Logic / View Name | 
| :--- | :--- | :--- |
| **(a)** | Hall Managers | `v_hall_managers` (Joins `halls` + `staff`) |
| **(b)** | Student Leases | `v_student_leases` (Joins `students` + `leases` + `rooms`) |
| **(c)** | Summer Leases | `v_summer_leases` (Filtered `WHERE summer = TRUE`) |
| **(d)** | Rent Paid | `v_student_rent_paid` (Aggregates `SUM(amount_due)` where `date_paid` is NOT NULL) |
| **(e)** | Unpaid Invoices | `v_unpaid_invoices` (Filtered `WHERE date_paid IS NULL`) |
| **(f)** | Bad Inspections | `v_unsatisfactory_inspections` (Filtered `WHERE is_satisfactory = FALSE`) |
| **(h)** | Waiting List | `v_waiting_list` (Filtered `WHERE status = 'Waiting'`) |
| **(l)** | Rent Stats | `v_hall_rent_stats` (Uses `MIN`, `MAX`, `AVG` aggregations) |
| **(n)** | Senior Staff | `v_senior_staff` (Calculated using `TIMESTAMPDIFF`) |

---

## 5. Potential Viva Questions & Answers

**Q: Why choose FastAPI instead of Django (Python)?**
*A: FastAPI is designed for performance and speed. It uses asynchronous programming (`async/await`) and automatically produces interactive documentation (Swagger).*

**Q: What is a "Constraint" and which ones did you use?**
*A: A constraint is a rule for data. We used **Primary Keys** (uniqueness), **Foreign Keys** (relational links), **Unique** (prevent duplicate emails), and **Check Constraints** (ensuring rent is > 0).*

**Q: How do you handle authentication?**
*A: We use **JWT (JSON Web Tokens)**. When a user logs in, the server gives them a signed token. The frontend sends this token in the header of every request to prove who is logged in.*

**Q: Why store Next-of-Kin in a separate table?**
*A: To follow 3NF. Since Next-of-Kin data has its own attributes (name, relationship, phone), keeping it in the Student table would lead to "Transitive Dependency," which is un-normalized.*

---
*End of Guide*
