# Troubleshooting Guide - StartHub

Common issues and solutions for the StartHub platform.

---

## 🚀 Service Issues

### Services Won't Start

**Symptom**: `bash scripts/start_all.sh` fails or services don't respond.

**Diagnostic Steps**:
```bash
# Check if ports are already in use
netstat -ano | grep LISTENING | grep -E "3000|8000|8081|1025|8025"

# Check for existing PIDs
cat logs/frontend.pid logs/fastapi.pid logs/spring.pid logs/mailhog.pid

# View recent logs
tail -n 50 logs/frontend.log
tail -n 50 logs/fastapi.log
tail -n 50 logs/spring.log
```

**Solutions**:
1. Stop all services first:
   ```bash
   bash scripts/stop_all.sh
   ```

2. Kill any stuck processes:
   ```bash
   # Windows
   taskkill /F /PID <PID>
   
   # Linux/Mac
   kill -9 <PID>
   ```

3. Restart services:
   ```bash
   bash scripts/start_all.sh
   ```

---

### Port Already in Use

**Symptom**: `Address already in use` error.

**Check Which Process Uses a Port**:
```bash
# Windows
netstat -ano | findstr :<PORT>

# Linux/Mac
lsof -ti:<PORT>
```

**Kill Process Using Port**:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Common Ports**:
- 3000 - Frontend
- 8000 - FastAPI
- 8081 - Spring Boot
- 1025 - MailHog SMTP
- 8025 - MailHog Web UI

---

## 🗄️ Database Issues

### Can't Connect to MySQL

**Symptom**: `Can't connect to MySQL server on 'localhost'`

**Solutions**:

1. **Check MySQL is running**:
   ```bash
   # Windows
   net start MySQL80
   
   # Linux
   sudo systemctl start mysql
   
   # Mac
   brew services start mysql
   ```

2. **Test connection manually**:
   ```bash
   mysql -u root -p
   ```

3. **Check credentials in `.env` files**:
   ```bash
   # FastAPI
   cat services/fastapi/.env
   # Should show: DATABASE_URL=mysql+mysqlconnector://root:PASSWORD@localhost:3306/starthub
   
   # Spring Boot
   cat services/spring-auth/.env
   # Should show: DB_PASSWORD=PASSWORD
   ```

4. **Try using 127.0.0.1 instead of localhost**:
   ```bash
   # In services/fastapi/.env
   DATABASE_URL=mysql+mysqlconnector://root:PASSWORD@127.0.0.1:3306/starthub
   ```

---

### Database Doesn't Exist

**Symptom**: `Unknown database 'starthub'`

**Solution**: Run the reload script:
```bash
cd Database/utilities
bash reload_all.sh
```

This creates the database, tables, and loads sample data.

---

### Tables Already Exist (Alembic)

**Symptom**: `Table 'user' already exists` when running Alembic migrations.

**Solution**: Mark current state as latest:
```bash
cd services/fastapi
python -m alembic -c alembic.ini stamp head
```

This tells Alembic that the database is already at the latest version.

---

### Foreign Key Constraint Errors

**Symptom**: `Cannot add or update a child row: a foreign key constraint fails`

**Cause**: Trying to insert data with invalid foreign key references.

**Solutions**:

1. **Clean database and reload**:
   ```bash
   cd Database/utilities
   bash reload_all.sh
   ```

2. **Check data order**: Load data in correct order:
   - Categories first
   - Users second
   - Startups third
   - Comments/Votes/Partnerships last

---

## 🔐 Authentication Issues

### 403 Forbidden on API Endpoints

**Symptom**: All requests to `/api/v1/*` return 403.

**Cause**: Spring Security blocking requests.

**Solution**: This should be fixed, but verify `SecurityConfig.java`:
```java
http
    .authorizeHttpRequests(auth -> auth
        .requestMatchers("/api/v1/registration", "/api/v1/registration/**").permitAll()
        .requestMatchers("/api/v1/auth/**").permitAll()
        .anyRequest().permitAll()
    )
```

---

### JWT Token Expired

**Symptom**: `403 Forbidden` despite having a token.

**Cause**: JWT tokens expire after 1 hour by default.

**Solution**: Login again to get a fresh token:
```bash
curl -X POST http://localhost:8081/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'
```

---

### Email Confirmation Not Working

**Symptom**: Can't confirm email after registration.

**Diagnostic**:
1. Check MailHog is running: http://localhost:8025
2. Look for confirmation email in MailHog
3. Check Spring Boot logs for errors

**Solutions**:

1. **Start MailHog**:
   ```bash
   bash scripts/start_mailhog.sh
   ```

2. **Check Spring Boot mail configuration**:
   ```yaml
   # services/spring-auth/src/main/resources/application.yml
   spring:
     mail:
       host: localhost
       port: 1025
   ```

3. **Manually confirm user** (development only):
   ```sql
   UPDATE User SET enabled = 1 WHERE email = 'user@example.com';
   ```

---

## 🌐 Frontend Issues

### Blank Page / Empty Body

**Symptom**: Frontend pages load but appear blank.

**Solutions**:

1. **Check frontend server is running**:
   ```bash
   curl http://localhost:3000/home.html
   ```

2. **Check browser console** (F12) for errors

3. **Restart frontend**:
   ```bash
   # Get PID
   cat logs/frontend.pid
   
   # Kill process
   kill $(cat logs/frontend.pid)
   
   # Restart
   cd scripts
   python dev-server.py > ../logs/frontend.log 2>&1 &
   echo $! > ../logs/frontend.pid
   ```

---

### JavaScript Modules Won't Load

**Symptom**: `Failed to load module script` errors.

**Cause**: Files served with incorrect MIME type.

**Solution**: Use `dev-server.py` instead of opening files directly:
```bash
# ❌ Don't do this
file:///path/to/frontend/home.html

# ✅ Do this
http://localhost:3000/home.html
```

---

### CORS Errors

**Symptom**: `Access-Control-Allow-Origin` errors in console.

**Solutions**:

1. **Check FastAPI CORS settings**:
   ```bash
   # services/fastapi/.env
   CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,*
   ```

2. **Check Spring Boot CORS** (should be configured automatically)

3. **Use correct URLs**:
   - Frontend: `http://localhost:3000`
   - FastAPI: `http://127.0.0.1:8000`
   - Spring Boot: `http://localhost:8081`

---

### Startups Won't Load

**Symptom**: Home page is empty or shows loading spinner forever.

**Diagnostic Steps**:
```bash
# Test FastAPI directly
curl http://127.0.0.1:8000/startups

# Check database has data
mysql -u root -p starthub -e "SELECT COUNT(*) FROM Startup;"
```

**Solutions**:

1. **Load sample data**:
   ```bash
   cd Database/utilities
   bash reload_all.sh
   ```

2. **Check browser console** for errors

3. **Verify API URLs in JavaScript**:
   ```javascript
   // frontend/js/home.js
   const API_BASE_URL = 'http://127.0.0.1:8000';
   ```

---

## 📧 MailHog Issues

### MailHog Won't Start

**Symptom**: `bash scripts/start_mailhog.sh` fails.

**Solutions**:

1. **Check MailHog is installed**:
   ```bash
   ls tools/mailhog/
   # Should show MailHog binary
   ```

2. **Install MailHog**:
   ```bash
   bash scripts/setup_mailhog.sh
   ```

3. **Check ports are free**:
   ```bash
   netstat -ano | findstr :1025
   netstat -ano | findstr :8025
   ```

4. **Run manually to see errors**:
   ```bash
   ./tools/mailhog/MailHog.exe
   ```

---

### Emails Not Appearing in MailHog

**Symptom**: Registration successful but no email in MailHog.

**Solutions**:

1. **Check MailHog is running**:
   ```bash
   curl http://localhost:8025
   ```

2. **Check Spring Boot logs** for email sending errors:
   ```bash
   tail -f logs/spring.log | grep -i mail
   ```

3. **Verify mail configuration**:
   ```yaml
   # application.yml
   spring:
     mail:
       host: localhost
       port: 1025  # NOT 25!
   ```

---

## 🧪 Testing Issues

### Tests Fail with Database Errors

**Symptom**: `pytest` or `mvnw test` fails with DB errors.

**Solutions**:

1. **FastAPI tests use SQLite** (not MySQL):
   ```bash
   # Check conftest.py uses SQLite for tests
   cd services/fastapi
   pytest tests/ -v
   ```

2. **Spring Boot tests use H2** (not MySQL):
   ```yaml
   # src/test/resources/application-test.yml
   spring:
     datasource:
       url: jdbc:h2:mem:testdb
   ```

3. **Don't run tests against production database**

---

### Test Scripts Can't Find Services

**Symptom**: `test_backend.sh` or `test_frontend.sh` reports services offline.

**Solution**: Start services first:
```bash
bash scripts/start_all.sh

# Wait 10 seconds for services to start
sleep 10

# Run tests
bash scripts/test_backend.sh
bash scripts/test_frontend.sh
```

---

## 🔧 Build Issues

### Maven Build Fails

**Symptom**: `./mvnw.cmd clean package` fails.

**Solutions**:

1. **Check Java version**:
   ```bash
   java -version
   # Should be Java 21 or higher
   ```

2. **Clean Maven cache**:
   ```bash
   cd services/spring-auth
   ./mvnw.cmd clean
   rm -rf target/
   ./mvnw.cmd package -DskipTests
   ```

3. **Check Maven wrapper exists**:
   ```bash
   ls .mvn/wrapper/
   # Should show maven-wrapper.jar and maven-wrapper.properties
   ```

---

### Python Dependencies Won't Install

**Symptom**: `pip install -r requirements.txt` fails.

**Solutions**:

1. **Upgrade pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Use virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   # source .venv/bin/activate    # Linux/Mac
   pip install -r services/fastapi/requirements.txt
   ```

3. **Install system dependencies** (Linux):
   ```bash
   # For MySQL connector
   sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
   ```

---

## 🐍 Python Environment Issues

### ModuleNotFoundError

**Symptom**: `ModuleNotFoundError: No module named 'app'`

**Solutions**:

1. **Activate virtual environment**:
   ```bash
   source .venv/Scripts/activate  # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r services/fastapi/requirements.txt
   ```

3. **Run from correct directory**:
   ```bash
   cd services/fastapi
   python -m uvicorn app.main:app --reload
   ```

---

### Wrong Python Version

**Symptom**: Syntax errors or incompatible features.

**Solution**: Use Python 3.12+:
```bash
python --version
# Should be Python 3.12 or higher

# Create venv with specific Python
python3.12 -m venv .venv
```

---

## 🔄 Git Issues

### Can't Pull / Merge Conflicts

**Symptom**: Git pull fails with conflicts.

**Solution**:
```bash
# Stash local changes
git stash

# Pull latest
git pull origin integration/all-features

# Reapply changes
git stash pop

# Resolve conflicts if any
git status
```

---

### Accidentally Committed .env

**Symptom**: `.env` file with passwords in Git history.

**Solution**:
```bash
# Remove from tracking
git rm --cached services/fastapi/.env
git rm --cached services/spring-auth/.env

# Add to .gitignore (already done)
echo "**/.env" >> .gitignore

# Commit
git commit -m "Remove .env files from tracking"
```

**Note**: Passwords are already exposed in history. Change them!

---

## 🆘 Emergency Recovery

### Everything is Broken

1. **Stop all services**:
   ```bash
   bash scripts/stop_all.sh
   ```

2. **Clean everything**:
   ```bash
   rm -rf logs/*.log logs/*.pid
   rm -rf services/fastapi/app/__pycache__
   rm -rf services/spring-auth/target
   ```

3. **Rebuild database**:
   ```bash
   cd Database/utilities
   bash reload_all.sh
   ```

4. **Reinstall Python dependencies**:
   ```bash
   source .venv/Scripts/activate
   pip install --force-reinstall -r services/fastapi/requirements.txt
   ```

5. **Rebuild Spring Boot**:
   ```bash
   cd services/spring-auth
   ./mvnw.cmd clean package -DskipTests
   ```

6. **Restart everything**:
   ```bash
   bash scripts/start_all.sh
   ```

---

## 📞 Getting Help

If none of these solutions work:

1. **Check logs**:
   ```bash
   tail -n 100 logs/fastapi.log
   tail -n 100 logs/spring.log
   tail -n 100 logs/frontend.log
   ```

2. **Run diagnostic scripts**:
   ```bash
   # Shell script tests
   bash scripts/test/test_backend.sh
   bash scripts/test/test_frontend.sh
   bash scripts/test/test_all_features.sh
   
   # Python test suites
   source .venv/Scripts/activate
   python scripts/test/test_crud_complete.py
   python scripts/test/test_manual.py  # Quick smoke test
   ```

3. **Check documentation**:
   - [Project Status](PROJECT_STATUS.md)
   - [Testing Guide](TESTING_GUIDE.md)
   - [Main README](../README.md)

4. **Verify prerequisites**:
   - Java 21+: `java -version`
   - Python 3.12+: `python --version`
   - MySQL 8.0+: `mysql --version`
   - Git Bash (Windows)

---

**Last Updated**: November 28, 2025  
**Tested On**: Windows 10/11 with Git Bash
