// src/test/java/com/example/demo/controller/AuthControllerTest.java
package com.example.demo.controller;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

import com.example.demo.appuser.AppUser;
import com.example.demo.appuser.AppUserService;
import com.example.demo.appuser.PasswordResetService;
import com.example.demo.security.jwt.JwtService;

class AuthControllerTest {

    private AuthController authController;
    private TestAuthenticationManager authenticationManager;
    private TestJwtService jwtService;
    private TestAppUserService appUserService;
    private TestPasswordResetService passwordResetService;

    @BeforeEach
    void setUp() {
        authenticationManager = new TestAuthenticationManager();
        jwtService = new TestJwtService();
        appUserService = new TestAppUserService();
        passwordResetService = new TestPasswordResetService();

        // Usamos reflexión para inyectar las dependencias ya que el constructor espera interfaces
        authController = new AuthController(
            authenticationManager,
            jwtService,
            appUserService,
            passwordResetService
        );
    }

    @Test
    void whenValidCredentials_thenReturnsTokenAndUserProfile() {
        // Configurar
        authenticationManager.setShouldAuthenticate(true);
        LoginRequest request = new LoginRequest("test@example.com", "password");

        // Ejecutar
        ResponseEntity<LoginResponse> response = authController.login(request);

        // Verificar
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());

        LoginResponse loginResponse = response.getBody();
        assertEquals("test-jwt-token", loginResponse.token());

        UserProfileResponse userProfile = loginResponse.user();
        assertEquals(1L, userProfile.id());
        assertEquals("John", userProfile.firstName());
        assertEquals("Doe", userProfile.lastName());
        assertEquals("test@example.com", userProfile.email());
    }

    @Test
    void whenInvalidCredentials_thenThrowsUnauthorized() {
        authenticationManager.setShouldAuthenticate(false);
        LoginRequest request = new LoginRequest("wrong@example.com", "wrongpassword");
        RuntimeException ex =
            org.junit.jupiter.api.Assertions.assertThrows(
                RuntimeException.class,
                () -> authController.login(request)
            );
        assertTrue(ex.getMessage().contains("Credenciales") || ex.getMessage().contains("credentials"));
    }

    @Test
    void whenUserNotFound_thenThrowsUnauthorized() {
        authenticationManager.setShouldAuthenticate(true);
        appUserService.setShouldThrowUserNotFound(true);
        LoginRequest request = new LoginRequest("nonexistent@example.com", "password");
        RuntimeException ex =
            org.junit.jupiter.api.Assertions.assertThrows(
                RuntimeException.class,
                () -> authController.login(request)
            );
        assertTrue(ex.getMessage().contains("Usuario") || ex.getMessage().contains("User") || ex.getMessage().contains("not found"));
    }

    @Test
    void whenLogout_thenReturnsSuccessMessage() {
        // Ejecutar
        ResponseEntity<String> response = authController.logout();

        // Verificar
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("Logged out successfully", response.getBody());
    }

    // Implementaciones de prueba que implementan las interfaces requeridas
    static class TestAuthenticationManager implements AuthenticationManager {
        private boolean shouldAuthenticate = true;

        public void setShouldAuthenticate(boolean shouldAuthenticate) {
            this.shouldAuthenticate = shouldAuthenticate;
        }

        @Override
        public Authentication authenticate(Authentication authentication) {
            if (!shouldAuthenticate) {
                throw new BadCredentialsException("Invalid credentials");
            }
            return new UsernamePasswordAuthenticationToken(
                authentication.getPrincipal(),
                authentication.getCredentials(),
                authentication.getAuthorities()
            );
        }
    }

    static class TestJwtService extends JwtService {
        @Override
        public String generateToken(org.springframework.security.core.userdetails.UserDetails userDetails) {
            return "test-jwt-token";
        }

        // Métodos simplificados para testing
        @Override
        public void init() {
            // No hacer nada para tests
        }

        @Override
        public boolean isTokenValid(String token, org.springframework.security.core.userdetails.UserDetails userDetails) {
            return true;
        }

        @Override
        public String extractUsername(String token) {
            return "test@example.com";
        }
    }

    static class TestAppUserService extends AppUserService {
        private boolean shouldThrowUserNotFound = false;

        public TestAppUserService() {
            super(null, null, null);
        }

        public void setShouldThrowUserNotFound(boolean shouldThrow) {
            this.shouldThrowUserNotFound = shouldThrow;
        }

        @Override
        public org.springframework.security.core.userdetails.UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
            if (shouldThrowUserNotFound) {
                throw new UsernameNotFoundException("User not found");
            }
            AppUser user = new AppUser();
            user.setId(1);
            user.setFirstName("John");
            user.setLastName("Doe");
            user.setEmail(email);
            user.setRegistrationDate(LocalDateTime.now());
            user.setProfileInfo("Test user profile");
            return user;
        }
    }

    static class TestPasswordResetService extends PasswordResetService {
        public TestPasswordResetService() {
            super(null, null, null, null); // Constructor simplificado
        }

        @Override
        public void sendPasswordResetEmail(String email) {
            // Implementación de prueba
        }

        @Override
        public void resetPassword(String token, String newPassword) {
            // Implementación de prueba
        }
    }
}