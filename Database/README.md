# 🌟 StarHub Database

Relational Database Model for the **StarHub Startup Management System** — a platform designed to manage startups, user interactions, votes, and collaborations.

---

## 🧩 Project Overview

This repository contains the full SQL structure, sample data, and utility scripts for the StarHub relational database.  
It is built to support startup registration, user interaction (comments and votes), and partnership relationships between users and startups.

---

## 📁 Folder Structure

starthub-database/
│
├── schema/ # Database structure and constraints
│ ├── schema.sql # Table creation scripts (DDL)
│ ├── views.sql # View definitions
│ └── starthub_model.mwb # MySQL Workbench diagram (optional)
│
├── seeds/ # Sample data (DML)
│ ├── seed_categories.sql
│ ├── seed_users.sql
│ ├── seed_startups.sql
│ ├── seed_comments.sql
│ ├── seed_votes.sql
│ ├── seed_partnerships.sql
│ └── seed_all.sql
│
├── queries/ # Example and validation queries
│ └── queries.sql
│
└── utils/ # Maintenance and automation scripts
├── reload_all.sql # Rebuilds the database from scratch
└── truncate_all.sql # Cleans all tables while keeping structure

---

## ⚙️ Setup Instructions

### 1️⃣ Create the database
Open MySQL Workbench or your terminal and run:
CREATE DATABASE starthub;
USE starthub;

### 2️⃣ Run the setup script
Execute the master script to build everything automatically:
mysql -u root -p < utils/reload_all.sql

### 3️⃣ Verify successful setup
You can check your tables with:
SHOW TABLES;
SELECT * FROM StartupDetails LIMIT 5;
SELECT * FROM StartupVoteStats LIMIT 5;

## 🧹 Maintenance
Reload database from scratch
mysql -u root -p < utils/reload_all.sql

Clean all data but keep structure
mysql -u root -p starthub < utils/truncate_all.sql

## 📊 Included Features
✅ User management with admin flag
✅ Startup registration with categories
✅ Commenting and voting system
✅ Many-to-many partnerships (User ↔ Startup)
✅ Views for analytical reporting:
- StartupDetails
- StartupVoteStats