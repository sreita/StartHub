# Testing Guide (Quick)

## Quick Start Commands

- Start all services: `bash scripts/start_all.sh`
- Stop all services: `bash scripts/stop_all.sh`
- Smoke test (health checks): `python scripts/test/test_manual.py`

## Automated Test Suites

### Comprehensive Tests (Python)

Located in `scripts/test/`:

1. **test_crud_complete.py** - Complete CRUD test suite
   - User registration, email confirmation, login
   - User profile management and updates
   - Startup CRUD (Create, Read, List, Update, Delete)
   - Startup with statistics
   - Vote CRUD (Create, Read, Update, Delete)
   - Comment CRUD (Create, Read, Update, Delete)
   - User deletion and post-deletion verification

2. **test_users_startups.py** - Users and Startups focus
   - User registration and confirmation
   - Login and re-login
   - Profile operations
   - Startup CRUD operations
   - Startup listing and statistics

3. **test_votes_comments.py** - Votes and Comments focus
   - Complete vote operations
   - Vote count verification
   - Comment CRUD operations
   - Content validation

4. **test_search.py** - Search functionality
   - Basic search by term
   - Filter by categories
   - Filter by votes/comments
   - Sorting (relevance, votes, comments, recent)
   - Pagination
   - Autocomplete
   - Startup detail retrieval

5. **test_manual.py** - Quick smoke test
   - FastAPI health check
   - Rapid service validation

### Running Python Tests

```bash
# Full CRUD test suite (recommended)
python scripts/test/test_crud_complete.py

# Specific feature tests
python scripts/test/test_users_startups.py
python scripts/test/test_votes_comments.py
python scripts/test/test_search.py

# Quick smoke test
python scripts/test/test_manual.py
```

### Legacy Shell Scripts

Located in `scripts/test/`:

- **test_backend.sh** - Backend endpoints validation
- **test_frontend.sh** - Frontend resources validation
- **test_all_features.sh** - Integration test suite

> 📖 **For detailed integration testing documentation**, see [Integration Testing Guide](INTEGRATION_TESTING.md)

### Running Python Tests

```bash
# Full CRUD test suite (recommended)
python scripts/test/test_crud_complete.py

# Specific feature tests
python scripts/test/test_users_startups.py
python scripts/test/test_votes_comments.py
python scripts/test/test_search.py

# Quick smoke test
python scripts/test/test_manual.py
```

### Legacy Shell Scripts

Located in `scripts/test/`:

- **test_backend.sh** - Backend endpoints validation
- **test_frontend.sh** - Frontend resources validation
- **test_all_features.sh** - Integration test suite

> 📖 **For detailed integration testing documentation**, see [Integration Testing Guide](INTEGRATION_TESTING.md)

## Test Coverage

### Complete CRUD Test (test_crud_complete.py)

**User Operations**:
1. Registration with unique email
2. Email confirmation via token
3. Login and JWT retrieval
4. Profile retrieval
5. Profile update
6. Re-login after update
7. User deletion
8. Post-deletion verification (profile inaccessible, login fails)

**Startup Operations**:
1. Create startup
2. Read startup details
3. Update startup (name, description, category)
4. List all startups
5. List user's startups
6. Get startup with statistics (votes, comments)
7. Delete startup
8. Verify deletion

**Vote Operations**:
1. Create upvote
2. Read vote counts
3. Change vote to downvote
4. Delete vote
5. Verify vote removal

**Comment Operations**:
1. Create comment
2. List comments for startup
3. Update comment content
4. Delete comment
5. Verify comment removal

### Search Test (test_search.py)

**Search Features**:
- Search by keyword
- Filter by single category
- Filter by multiple categories
- Filter by minimum votes
- Filter by minimum comments
- Sort by relevance, votes, comments, or recency
- Pagination (page and limit parameters)
- Autocomplete suggestions
- Detailed startup view

## Running Tests

```bash
# Start all services first
bash scripts/start_all.sh

# Wait for services to initialize (5-10 seconds)
sleep 10

# Run comprehensive CRUD tests
python scripts/test/test_crud_complete.py

# Run specific test suites
python scripts/test/test_users_startups.py
python scripts/test/test_votes_comments.py
python scripts/test/test_search.py

# Legacy shell script tests
bash scripts/test/test_backend.sh
bash scripts/test/test_frontend.sh
bash scripts/test/test_all_features.sh
```

## Test Output

All Python tests provide colored output:
- ✅ **Green** - Successful operation
- ❌ **Red** - Failed operation
- ℹ️ **Yellow** - Informational message
- 🔵 **Blue** - Section headers

Each test includes:
- Clear section markers
- Step-by-step progress
- Detailed error messages
- Final summary report

See `COMPLETE_MANUAL_TESTING.md` for detailed manual testing scenarios.