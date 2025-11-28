Testing Guide (Quick)

- Start backend (test profile): ./mvnw.cmd spring-boot:run -Dspring-boot.run.profiles=test
- Start frontend: python frontend/server.py
- Automated tests: bash frontend/test_all_features.sh

Endpoints exercised: registration, login, protected route, password reset.