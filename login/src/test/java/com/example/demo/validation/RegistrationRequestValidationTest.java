// src/test/java/com/example/demo/validation/RegistrationRequestValidationTest.java
package com.example.demo.validation;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

import com.example.demo.registration.RegistrationRequest;

class RegistrationRequestValidationTest {

    @Test
    void whenValidRegistrationRequest_thenNoValidationErrors() {
        // Given
        RegistrationRequest request = new RegistrationRequest(
            "John", "Doe", "john.doe@example.com", "SecurePassword123"
        );

        // When & Then
        assertDoesNotThrow(() -> validateRegistrationRequest(request));
    }

    @Test
    void whenRegistrationRequestWithInvalidEmail_thenValidationFails() {
        // Given
        RegistrationRequest request = new RegistrationRequest(
            "John", "Doe", "invalid-email", "SecurePassword123"
        );

        // When & Then
        IllegalArgumentException exception = assertThrows(
            IllegalArgumentException.class,
            () -> validateRegistrationRequest(request)
        );
        assertTrue(exception.getMessage().contains("email"));
    }

    @Test
    void whenRegistrationRequestWithWeakPassword_thenValidationFails() {
        // Given
        RegistrationRequest request = new RegistrationRequest(
            "John", "Doe", "john.doe@example.com", "123"
        );

        // When & Then
        IllegalArgumentException exception = assertThrows(
            IllegalArgumentException.class,
            () -> validateRegistrationRequest(request)
        );
        assertTrue(exception.getMessage().contains("password"));
    }

    @Test
    void whenRegistrationRequestWithEmptyFirstName_thenValidationFails() {
        // Given
        RegistrationRequest request = new RegistrationRequest(
            "", "Doe", "john.doe@example.com", "SecurePassword123"
        );

        // When & Then
        IllegalArgumentException exception = assertThrows(
            IllegalArgumentException.class,
            () -> validateRegistrationRequest(request)
        );
        assertTrue(exception.getMessage().contains("firstName"));
    }

    @Test
    void whenRegistrationRequestWithNullLastName_thenValidationFails() {
        // Given
        RegistrationRequest request = new RegistrationRequest(
            "John", null, "john.doe@example.com", "SecurePassword123"
        );

        // When & Then
        IllegalArgumentException exception = assertThrows(
            IllegalArgumentException.class,
            () -> validateRegistrationRequest(request)
        );
        assertTrue(exception.getMessage().contains("lastName"));
    }

    private void validateRegistrationRequest(RegistrationRequest request) {
        if (request.getFirstName() == null || request.getFirstName().trim().isEmpty()) {
            throw new IllegalArgumentException("firstName cannot be empty");
        }
        if (request.getLastName() == null || request.getLastName().trim().isEmpty()) {
            throw new IllegalArgumentException("lastName cannot be empty");
        }
        if (request.getEmail() == null || !request.getEmail().contains("@")) {
            throw new IllegalArgumentException("email must be valid");
        }
        if (request.getPassword() == null || request.getPassword().length() < 8) {
            throw new IllegalArgumentException("password must be at least 8 characters");
        }
    }
}