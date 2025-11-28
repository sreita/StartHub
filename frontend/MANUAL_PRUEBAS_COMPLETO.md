# Manual de Pruebas del Frontend (StartHub)

Este documento guía 10 escenarios clave para validar el frontend contra el backend de prueba (puerto 8081).

- Backend: `http://localhost:8081/api/v1`
- Frontend: `http://localhost:3000`

## Escenarios

1) Navegación básica: abrir `home.html`, `login.html`, `signup.html`, `profile.html` sin errores de consola.
2) Registro: en `signup.html` crear un usuario y validar mensaje de éxito.
3) Login: en `login.html` iniciar sesión y verificar `localStorage.authToken` y `localStorage.user`.
4) Navbar: al iniciar sesión, validar que muestre opciones de usuario y logout.
5) Modo noche: alternar y verificar persistencia de preferencia tras recargar.
6) Perfil: en `profile.html` cargar datos, actualizar perfil y verificar respuesta.
7) Recuperar contraseña: en `forgot_password.html` solicitar recuperación y validar mensaje.
8) Restablecer contraseña: simular POST `/auth/reset-password` y validar respuesta.
9) Protección de rutas: acceder a endpoints protegidos sin token → 401/403; con token → 200/403.
10) Logout: cerrar sesión, vaciar `localStorage` y volver a `home.html`.

## Verificaciones en DevTools
- Console sin errores rojos.
- Network: status codes y payloads correctos.
- Application → Local Storage: claves `authToken`, `user` presentes tras login y ausentes tras logout.

## Problemas comunes
- 404 de CSS: no críticos para funcionalidad.
- CORS: usar `python frontend/server.py` que ya habilita CORS.
- Backend no iniciado: arrancar con perfil `test` (H2) en 8081.