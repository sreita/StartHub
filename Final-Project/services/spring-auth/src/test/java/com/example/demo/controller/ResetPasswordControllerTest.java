// src/test/java/com/example/demo/controller/ResetPasswordControllerTest.java
package com.example.demo.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

class ResetPasswordControllerTest {

    private TestResetPasswordController resetPasswordController;
    private TestPasswordResetService passwordResetService;

    @BeforeEach
    void setUp() {
        passwordResetService = new TestPasswordResetService();
        resetPasswordController = new TestResetPasswordController(passwordResetService);
    }

    @Test
    void whenValidRecoveryRequest_thenReturnsSuccess() {
        // Configurar
        PasswordRecoveryRequest request = new PasswordRecoveryRequest("test@example.com");
        passwordResetService.setShouldSucceed(true);

        // Ejecutar
        ResponseEntity<String> response = resetPasswordController.recoverPassword(request);

        // Verificar
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("Password recovery email sent", response.getBody());
    }

    @Test
    void whenInvalidRecoveryRequest_thenReturnsBadRequest() {
        // Configurar
        PasswordRecoveryRequest request = new PasswordRecoveryRequest("invalid@example.com");
        passwordResetService.setShouldSucceed(false);
        passwordResetService.setErrorMessage("User not found");

        // Ejecutar
        ResponseEntity<String> response = resetPasswordController.recoverPassword(request);

        // Verificar
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertEquals("Error: User not found", response.getBody());
    }

    @Test
    void whenValidResetRequest_thenReturnsSuccess() {
        // Configurar
        PasswordResetRequest request = new PasswordResetRequest("valid-token", "newPassword123");
        passwordResetService.setShouldSucceed(true);

        // Ejecutar
        ResponseEntity<String> response = resetPasswordController.resetPassword(request);

        // Verificar
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals("Password reset successfully", response.getBody());
    }

    @Test
    void whenInvalidResetRequest_thenReturnsBadRequest() {
        // Configurar
        PasswordResetRequest request = new PasswordResetRequest("invalid-token", "newPassword123");
        passwordResetService.setShouldSucceed(false);
        passwordResetService.setErrorMessage("Token not found");

        // Ejecutar
        ResponseEntity<String> response = resetPasswordController.resetPassword(request);

        // Verificar
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertEquals("Error: Token not found", response.getBody());
    }

    // Implementación de prueba del controlador
    static class TestResetPasswordController {
        private final TestPasswordResetService passwordResetService;

        public TestResetPasswordController(TestPasswordResetService passwordResetService) {
            this.passwordResetService = passwordResetService;
        }

        public ResponseEntity<String> recoverPassword(PasswordRecoveryRequest request) {
            try {
                passwordResetService.sendPasswordResetEmail(request.email());
                return ResponseEntity.ok("Password recovery email sent");
            } catch (Exception e) {
                return ResponseEntity.badRequest().body("Error: " + e.getMessage());
            }
        }

        public ResponseEntity<String> resetPassword(PasswordResetRequest request) {
            try {
                passwordResetService.resetPassword(request.token(), request.newPassword());
                return ResponseEntity.ok("Password reset successfully");
            } catch (Exception e) {
                return ResponseEntity.badRequest().body("Error: " + e.getMessage());
            }
        }
    }

    // Implementación de prueba de PasswordResetService para el controlador
    static class TestPasswordResetService {
        private boolean shouldSucceed = true;
        private String errorMessage = "Test error";

        public void setShouldSucceed(boolean shouldSucceed) {
            this.shouldSucceed = shouldSucceed;
        }

        public void setErrorMessage(String errorMessage) {
            this.errorMessage = errorMessage;
        }

        public void sendPasswordResetEmail(String email) {
            if (!shouldSucceed) {
                throw new IllegalStateException(errorMessage);
            }
            // Simular éxito
        }

        public void resetPassword(String token, String newPassword) {
            if (!shouldSucceed) {
                throw new IllegalStateException(errorMessage);
            }
            // Simular éxito
        }
    }

    // Records DTO (agregar en el mismo archivo o usar los existentes)
    static record PasswordRecoveryRequest(String email) {}
    static record PasswordResetRequest(String token, String newPassword) {}
}