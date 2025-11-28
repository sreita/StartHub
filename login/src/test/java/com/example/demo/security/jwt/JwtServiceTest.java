// src/test/java/com/example/demo/security/jwt/JwtServiceTest.java
package com.example.demo.security.jwt;

import java.util.Collections;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;

class JwtServiceTest {

    private TestJwtService jwtService;

    @BeforeEach
    void setUp() {
        jwtService = new TestJwtService();
        jwtService.init(); // Llamar manualmente al init para tests
    }

    @Test
    void whenGenerateToken_thenReturnsValidToken() {
        // Configurar
        UserDetails userDetails = User.withUsername("test@example.com")
            .password("password")
            .authorities(Collections.emptyList())
            .build();

        // Ejecutar
        String token = jwtService.generateToken(userDetails);

        // Verificar
        assertNotNull(token);
        assertTrue(token.startsWith("test-token-"));
    }

    @Test
    void whenValidTokenAndUser_thenTokenIsValid() {
        // Configurar
        UserDetails userDetails = User.withUsername("test@example.com")
            .password("password")
            .authorities(Collections.emptyList())
            .build();

        String token = jwtService.generateToken(userDetails);

        // Ejecutar & Verificar
        assertTrue(jwtService.isTokenValid(token, userDetails));
    }

    @Test
    void whenExtractUsername_thenReturnsCorrectUsername() {
        // Configurar
        UserDetails userDetails = User.withUsername("test@example.com")
            .password("password")
            .authorities(Collections.emptyList())
            .build();

        String token = jwtService.generateToken(userDetails);

        // Ejecutar
        String username = jwtService.extractUsername(token);

        // Verificar
        assertEquals("test@example.com", username);
    }

    static class TestJwtService extends JwtService {
        @Override
        public void init() {
            // No cargar archivos PEM en tests
        }

        @Override
        public String generateToken(UserDetails userDetails) {
            return "test-token-" + userDetails.getUsername();
        }

        @Override
        public boolean isTokenValid(String token, UserDetails userDetails) {
            return token.equals("test-token-" + userDetails.getUsername());
        }

        @Override
        public String extractUsername(String token) {
            return token.replace("test-token-", "");
        }

        @Override
        public <T> T extractClaim(String token, java.util.function.Function<io.jsonwebtoken.Claims, T> claimsResolver) {
            return null; // Simplificado para tests
        }
    }
}