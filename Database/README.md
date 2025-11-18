# StarHub Database

Relational model for the StartHub system: startups, users, comments, and votes, with supporting views and seed data.

---

## Folder Structure

```
Database/
├─ schema/              # Structure (DDL) and views
│  ├─ schema.sql
│  └─ views.sql
├─ seeds/               # Sample data (DML)
│  ├─ seed_categories.sql
│  ├─ seed_users.sql
│  ├─ seed_startups.sql
│  ├─ seed_partnerships.sql
│  ├─ seed_comments.sql
│  └─ seed_votes.sql
├─ queries/
│  └─ queries.sql
├─ utilities/           # Maintenance scripts
│  ├─ reload_all.sql    # Rebuild DB from scratch (schema + views + seeds)
│  └─ truncate_all.sql  # Wipe data keeping structure
└─ verifiers/
	├─ verify_data.sql
	└─ verify_views.sql
```

Note: The MySQL Workbench diagram is at `Database/schema/Relational model.mwb`.

---

## Quick Setup (MySQL)

- Create/recreate the database (schema + views + seeds) with the master script:
```bash
mysql -u root -p < Database/utilities/reload_all.sql
```

- Verify:
```sql
SHOW TABLES;
SELECT COUNT(*) FROM `User`;
SELECT COUNT(*) FROM Startup;
SELECT COUNT(*) FROM Comment;
SELECT COUNT(*) FROM Vote;
```

- Clean data and keep structure:
```bash
mysql -u root -p starthub < Database/utilities/truncate_all.sql
```

---

## Backend Integration (FastAPI)

- The backend uses SQLAlchemy and Alembic. Ensure `backend/.env` points to this DB (`DATABASE_URL`).
- If the DB already exists (e.g., created with these scripts), and the first migration tries to create existing tables, align Alembic history with:
```bash
alembic -c backend/alembic.ini stamp head
```
- Future model changes should be managed via Alembic revisions.

---

## Included Features
- Users, categories, startups
- Comment and vote system (up/down)
- Collaboration relationships (User ↔ Startup)
- Analytical views in `schema/views.sql`