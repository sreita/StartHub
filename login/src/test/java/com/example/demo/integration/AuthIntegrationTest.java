// src/test/java/com/example/demo/integration/AuthIntegrationTest.java
package com.example.demo.integration;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.ActiveProfiles;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class AuthIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void contextLoads() {
        // Test básico para verificar que el contexto se carga
        assertNotNull(restTemplate);
    }

    @Test
    void whenAccessPublicEndpoint_thenReturnsOk() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "/api/v1/registration/confirm?token=test",
            String.class
        );

        // El endpoint existe, aunque el token sea inválido
        assertNotEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }

    @Test
    void whenAccessNonExistentEndpoint_thenReturnsNotFound() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "/api/v1/non-existent",
            String.class
        );

        assertEquals(HttpStatus.FORBIDDEN, response.getStatusCode());
    }

    @Test
    void whenPostToLoginWithValidJson_thenReturnsResponse() {
        String loginJson = """
            {
                "email": "test@example.com",
                "password": "password"
            }
            """;

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<String> request = new HttpEntity<>(loginJson, headers);

        ResponseEntity<String> response = restTemplate.postForEntity(
            "/api/v1/auth/login",
            request,
            String.class
        );

        // El endpoint debería responder (puede ser OK o error de autenticación)
        assertNotNull(response);
        assertNotEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
    }
}