# Coimbra Bus Management System

An application developed in **Python** and **SQL** to manage trips, customers, buses, and internal operations for the fictional transport company **Coimbra Bus**.

> **Note:**  
> The entire project (code, menus, and user interface) is written in **European Portuguese (Portugal)**.
---

## About the Project

This project implements a database-driven application that supports the core operations of a transportation company.  
The system allows **customers** to search and book trips, while **administrators** can manage buses, routes, trips, customers, messages, and platform-wide statistics.

The system combines:
- **Python** — interface, menus, and application logic  
- **SQL** — data management, queries, inserts, updates, and transactions  

---

## Features

### Customer
- Account registration and login with validation  
- View all available trips  
- Search trips by destination, date, or distance  
- View detailed trip information  
- Reserve and purchase tickets  
- Manage tickets (past, future, and canceled)  
- Check messages (read and unread)

### Administrator
- Dedicated login with an administrator interface  
- Bus management (view, add, edit, delete)  
- Trip and route management  
- Customer management, including assigning **Gold** status  
- Send messages (general or individual)  
- Global database visualization  
- Advanced statistics:
  - Best-selling trips  
  - Most-used routes  
  - Monthly and yearly sales  
  - Trips with no reservations  
  - Canceled reservations  
  - Customers in waiting lists  

---

## Application Structure

The application includes **11 classes** and **23 functions**, organized in a modular structure for clarity and maintainability.

The main entry point of the system is: CoimbraBus.py

The project also includes:
- User interface diagram  
- Entity–Relationship diagram  
- Physical database diagram  

---

## Interface Diagram

Below is the user interface diagram used to structure the application's navigation flow:

![User Interface Diagram](./Interface_Diagram.png)

---

## Database and Table Files Included

The repository includes two text files used to set up the database:

### 1. `ScriptSQL_DBB_Data.txt` (example / pre-filled data)
Contains sample data used to populate the database for testing the Coimbra Bus system.
Note: some data may be outdated or deprecated and should be adjusted as needed.

### 2. `ScriptSQL_ONDA_Tables.txt` (SQL schema & operations)
Contains the SQL scripts required to create the tables, relationships, and base structure of the system.  
These scripts must be executed before running the application.

---
## Technologies Used
- **Python 3**
- **SQL (PostgreSQL)**
- **ONDA** — used for creating ER and physical diagrams  

--- 
