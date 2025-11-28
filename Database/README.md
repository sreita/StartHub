# StartHub Database

Relational database schema for the StartHub system, including users, startups, comments, votes, partnerships, and categories.

---

## 📁 Directory Structure

```
Database/
├── schema/              # Database structure (DDL) and views
│   ├── schema.sql       # Table definitions and relationships
│   ├── views.sql        # Analytical views
│   └── Relational model.mwb  # MySQL Workbench diagram
├── seeds/               # Sample data (DML)
│   ├── seed_categories.sql
│   ├── seed_users.sql
│   ├── seed_startups.sql
│   ├── seed_partnerships.sql
│   ├── seed_comments.sql
│   └── seed_votes.sql
├── queries/             # Example queries
│   └── queries.sql
├── utilities/           # Database maintenance scripts
│   ├── reload_all.sh    # Rebuild database from scratch (schema + views + seeds)
│   └── truncate_all.sh  # Clean all data keeping structure
└── verifiers/           # Data validation scripts
    ├── verify_data.sql  # Verify sample data loaded correctly
    └── verify_views.sql # Verify views are working
```

---

## 🗄️ Database Schema

The database uses **MySQL 8.0+** with **utf8mb4_unicode_ci** collation.

### Main Tables

- **User** - Registered users with authentication data
- **Category** - Startup categories (Technology, Health, Education, etc.)
- **Startup** - Created startups with details and metrics
- **Comment** - User comments on startups
- **Vote** - User votes (upvote/downvote) on startups
- **Partnership** - Collaboration relationships between users and startups
- **ConfirmationToken** - Email verification tokens (Spring Boot)
- **PasswordResetToken** - Password recovery tokens (Spring Boot)

### Key Features

- **Foreign Keys**: Enforced referential integrity
- **Cascading Deletes**: Automatic cleanup of related records
- **Timestamps**: `created_at` on all tables
- **Indexes**: Optimized for common queries
- **Views**: Analytical views for reporting

---

## 🚀 Quick Setup

### 1. Rebuild Database from Scratch

This will drop the existing database, recreate it, and load all sample data:

```bash
cd Database/utilities
bash reload_all.sh
```

The script will:
1. Drop and recreate the `starthub` database
2. Load schema (tables and relationships)
3. Load views
4. Load all seed data (users, startups, comments, votes, partnerships, categories)
5. Display data counts for verification

**Note**: This script requires MySQL Shell (`mysqlsh`) to be installed. It will auto-detect the correct command for your OS.

### 2. Clean Data (Keep Schema)

To remove all data but preserve the table structure:

```bash
cd Database/utilities
bash truncate_all.sh
```

This will:
- Prompt for confirmation
- Disable foreign key checks
- Truncate all tables
- Reset AUTO_INCREMENT counters
- Re-enable foreign key checks

---

## 📊 Sample Data

After running `reload_all.sh`, you'll have:

- **15 users** - Sample user accounts
- **5 categories** - Technology, Health, Education, Finance, Environment
- **12 startups** - Diverse startup examples across categories
- **25 comments** - User feedback on startups
- **26 votes** - Mix of upvotes and downvotes
- **13 partnerships** - User-startup collaboration relationships

---

## 🔍 Verification

### Verify Data Loaded Correctly

```bash
mysql -u root -p starthub < Database/verifiers/verify_data.sql
```

This shows:
- Count of records in each table
- Sample records from each table

### Verify Views Work

```bash
mysql -u root -p starthub < Database/verifiers/verify_views.sql
```

This tests all analytical views.

### Quick Manual Check

```sql
USE starthub;
SHOW TABLES;
SELECT COUNT(*) AS users FROM User;
SELECT COUNT(*) AS startups FROM Startup;
SELECT COUNT(*) AS comments FROM Comment;
SELECT COUNT(*) AS votes FROM Vote;
```

---

## 🔧 Manual Setup (Alternative)

If you prefer to run SQL scripts manually:

### 1. Create Database and Schema

```bash
mysql -u root -p
```

```sql
CREATE DATABASE IF NOT EXISTS starthub
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE starthub;
SOURCE Database/schema/schema.sql;
SOURCE Database/schema/views.sql;
```

### 2. Load Sample Data

```sql
SOURCE Database/seeds/seed_categories.sql;
SOURCE Database/seeds/seed_users.sql;
SOURCE Database/seeds/seed_startups.sql;
SOURCE Database/seeds/seed_partnerships.sql;
SOURCE Database/seeds/seed_comments.sql;
SOURCE Database/seeds/seed_votes.sql;
```

### 3. Verify

```sql
SOURCE Database/verifiers/verify_data.sql;
SOURCE Database/verifiers/verify_views.sql;
```

---

## 🔄 Backend Integration

### FastAPI Configuration

FastAPI uses SQLAlchemy ORM and connects via the `.env` file:

```bash
# services/fastapi/.env
DATABASE_URL=mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/starthub
```

**Alembic Migrations**: If you've manually created the database using these scripts and Alembic tries to recreate existing tables:

```bash
cd services/fastapi
python -m alembic -c alembic.ini stamp head
```

This aligns Alembic's migration history without changing the database.

### Spring Boot Configuration

Spring Boot connects to the same MySQL database:

```bash
# services/spring-auth/.env
DB_URL=jdbc:mysql://localhost:3306/starthub
DB_USERNAME=root
DB_PASSWORD=YOUR_PASSWORD
```

Spring Boot manages its own tables (`User`, `ConfirmationToken`, `PasswordResetToken`) and shares the `User` table with FastAPI.

---

## 📐 Entity Relationships

### User ↔ Startup
- One user can create multiple startups
- One startup has one owner (creator)

### User ↔ Startup (Partnership)
- Many-to-many relationship
- Users can collaborate on multiple startups
- Startups can have multiple collaborators

### User → Comment
- One user can write multiple comments
- Each comment belongs to one user

### User → Vote
- One user can vote on multiple startups (one vote per startup)
- Each vote belongs to one user

### Startup ← Comment
- One startup can have multiple comments
- Each comment is about one startup

### Startup ← Vote
- One startup can receive multiple votes
- Each vote is for one startup

### Startup → Category
- Each startup belongs to one category
- One category can have multiple startups

---

## 🛠️ Maintenance Scripts

### reload_all.sh

**Purpose**: Completely rebuild the database from scratch.

**When to use**:
- Initial project setup
- After major schema changes
- When you need fresh sample data
- Database is corrupted or inconsistent

**Features**:
- Auto-detects MySQL Shell command (Windows/Linux)
- Colored output with progress indicators
- Displays data counts after loading
- Error handling and validation

### truncate_all.sh

**Purpose**: Remove all data but keep the schema intact.

**When to use**:
- Testing with clean state
- Removing test data before production deployment
- Resetting AUTO_INCREMENT counters

**Features**:
- Confirmation prompt before execution
- Disables foreign keys during truncation
- Resets AUTO_INCREMENT values
- Safe and reversible (schema preserved)

---

## 🎨 MySQL Workbench Model

The visual database diagram is available at:

```
Database/schema/Relational model.mwb
```

Open with MySQL Workbench to:
- View entity relationships graphically
- Edit schema visually
- Generate SQL DDL
- Document the database structure

---

## 📝 Views

Analytical views are defined in `Database/schema/views.sql`:

### Available Views

- **startup_summary** - Startup details with vote and comment counts
- **user_activity** - User engagement metrics
- **category_stats** - Startup distribution by category
- **popular_startups** - Top-rated startups by votes

**Usage Example**:
```sql
SELECT * FROM startup_summary ORDER BY upvotes DESC LIMIT 10;
```

---

## 🔐 Security Notes

- **Passwords**: User passwords in seed data are hashed with BCrypt
- **Test Data**: Sample data is for development only, not for production
- **Credentials**: Never commit real passwords to `.env` files
- **Access**: Grant appropriate MySQL privileges for application users

---

## 🐛 Troubleshooting

### "Database already exists" Error

**Solution**: The `reload_all.sh` script drops the database first. If you get this error, manually drop it:

```sql
DROP DATABASE IF EXISTS starthub;
```

### Foreign Key Constraint Errors

**Cause**: Trying to insert/update/delete data that violates relationships.

**Solution**: Use `truncate_all.sh` which temporarily disables foreign key checks.

### MySQL Shell Not Found

**Error**: `mysqlsh: command not found` or `Could not find MySQL Shell`

**Solution**: Install MySQL Shell or edit `reload_all.sh` to use `mysql` instead:

```bash
# Change this line:
MYSQL_CMD="mysqlsh --sql -u root -p"

# To:
MYSQL_CMD="mysql -u root -p"
```

### Character Encoding Issues

**Symptom**: Special characters (á, é, í, ñ) display incorrectly.

**Solution**: Ensure database uses `utf8mb4_unicode_ci`:

```sql
ALTER DATABASE starthub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 📚 Additional Resources

- [Main Project README](../README.md)
- [FastAPI Documentation](../services/fastapi/README.md)
- [Testing Guide](../docs/TESTING_GUIDE.md)
- [Troubleshooting Guide](../docs/TROUBLESHOOTING.md)

---

**Last Updated**: November 28, 2025  
**Database Version**: 1.0  
**MySQL Version**: 8.0+
