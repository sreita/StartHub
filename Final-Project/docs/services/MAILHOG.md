# MailHog - Email Testing for StartHub

MailHog is a fake SMTP server that captures all outgoing emails for testing purposes. This allows you to test email functionality without sending real emails.

## 🚀 Quick Start

### 1. Install MailHog

```bash
bash scripts/setup_mailhog.sh
```

This will download MailHog to the `tools/mailhog/` directory.

### 2. Start MailHog

```bash
bash scripts/start_mailhog.sh
```

Or start all services (including MailHog):

```bash
bash scripts/start_all.sh
```

### 3. Access MailHog Web UI

Open your browser and go to: **http://localhost:8025**

Here you can see all captured emails in a user-friendly interface.

## 📧 Using MailHog

### Ports

- **SMTP Server**: `localhost:1025` (for sending emails)
- **Web UI**: `http://localhost:8025` (for viewing emails)

### Testing Email Functionality

1. Start MailHog
2. Register a new user in StartHub
3. Check MailHog Web UI to see the confirmation email
4. Click the confirmation link to activate the account

### Example: Register User

```bash
curl -X POST "http://localhost:8081/api/v1/registration" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "password": "SecurePass123!"
  }'
```

Then visit http://localhost:8025 to see the confirmation email.

## 🛠️ Management Commands

### Start MailHog

```bash
bash scripts/start_mailhog.sh
```

### Stop MailHog

```bash
bash scripts/stop_mailhog.sh
```

Or stop all services:

```bash
bash scripts/stop_all.sh
```

### Check if MailHog is Running

```bash
netstat -ano | grep 1025
```

Or visit http://localhost:8025 in your browser.

## 📊 API Access

MailHog provides a simple API for programmatic access:

### Get all messages

```bash
curl http://localhost:8025/api/v2/messages
```

### Get a specific message

```bash
curl http://localhost:8025/api/v2/messages/{MESSAGE_ID}
```

### Delete all messages

```bash
curl -X DELETE http://localhost:8025/api/v1/messages
```

## 🔧 Spring Boot Configuration

The Spring Boot application is already configured to use MailHog in `application.yml`:

```yaml
spring:
  mail:
    host: localhost
    port: 1025
    username: hello
    password: hello
```

## 📝 Notes

- MailHog is **only for development/testing**. Never use it in production!
- All emails are stored **in memory** and will be lost when MailHog is stopped
- The `tools/` directory is in `.gitignore`, so MailHog won't be committed to the repository
- Each developer needs to run `bash scripts/setup_mailhog.sh` on their machine

## 🐛 Troubleshooting

### Port 1025 already in use

```bash
# Windows
netstat -ano | findstr :1025
taskkill /F /PID <PID>

# Linux/Mac
lsof -ti:1025 | xargs kill -9
```

### MailHog won't start

1. Make sure ports 1025 and 8025 are free
2. Check the logs: `cat logs/mailhog.log`
3. Try running manually: `./tools/mailhog/MailHog.exe`

### Emails not appearing

1. Check MailHog is running: http://localhost:8025
2. Check Spring Boot logs for connection errors
3. Verify Spring Boot configuration uses `localhost:1025`

## 📚 More Information

- Official MailHog Repository: https://github.com/mailhog/MailHog
- MailHog Documentation: https://github.com/mailhog/MailHog/blob/master/docs/CONFIG.md
