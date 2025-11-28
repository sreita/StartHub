// src/test/java/com/example/demo/security/SecurityConfigurationTest.java
package com.example.demo.security;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.test.context.ActiveProfiles;

import com.example.demo.security.config.SecurityConfig;

@SpringBootTest
@ActiveProfiles("test")
class SecurityConfigurationTest {

    @Autowired
    private SecurityConfig securityConfig;

    @Test
    void whenSecurityConfigLoaded_thenNotNull() {
        assertNotNull(securityConfig, "SecurityConfig should be loaded");
    }

    @Test
    void whenSecurityFilterChainBeanExists_thenNotNull() {
        // Verificar que el SecurityFilterChain está configurado
        assertDoesNotThrow(() -> {
            SecurityFilterChain filterChain = securityConfig.securityFilterChain(null);
            assertNotNull(filterChain, "SecurityFilterChain should not be null");
        }, "SecurityFilterChain bean should be created without errors");
    }

    @Test
    void whenAuthenticationManagerBeanExists_thenNotNull() {
        // Verificar que el AuthenticationManager está configurado
        assertDoesNotThrow(() -> {
            Object authManager = securityConfig.authenticationManager(null);
            assertNotNull(authManager, "AuthenticationManager should not be null");
        }, "AuthenticationManager bean should be created without errors");
    }
}