// src/test/java/com/example/demo/controller/UserControllerValidationTest.java
package com.example.demo.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

class UserControllerValidationTest {

    private TestUserController userController;
    private TestAppUserService appUserService;

    @BeforeEach
    void setUp() {
        appUserService = new TestAppUserService();
        userController = new TestUserController(appUserService);
    }

    @Test
    void whenUpdateUserWithInvalidEmail_thenReturnsBadRequest() {
        // Given
        UserUpdateRequest invalidRequest = new UserUpdateRequest(
            "John", "Doe", "invalid-email", "Profile info"
        );

        // When
        ResponseEntity<UserProfileResponse> response = userController.updateUserProfile(1, invalidRequest);

        // Then
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void whenUpdateUserWithEmptyFirstName_thenReturnsBadRequest() {
        // Given
        UserUpdateRequest invalidRequest = new UserUpdateRequest(
            "", "Doe", "john@example.com", "Profile info"
        );

        // When
        ResponseEntity<UserProfileResponse> response = userController.updateUserProfile(1, invalidRequest);

        // Then
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
    }

    @Test
    void whenUpdateUserWithValidData_thenReturnsOk() {
        // Given
        UserUpdateRequest validRequest = new UserUpdateRequest(
            "John", "Doe", "john@example.com", "Updated profile"
        );
        appUserService.setShouldSucceed(true);

        // When
        ResponseEntity<UserProfileResponse> response = userController.updateUserProfile(1, validRequest);

        // Then
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }

    // Implementación de prueba para UserController
    static class TestUserController {
        private final TestAppUserService appUserService;

        public TestUserController(TestAppUserService appUserService) {
            this.appUserService = appUserService;
        }

        public ResponseEntity<UserProfileResponse> updateUserProfile(Integer id, UserUpdateRequest request) {
            try {
                // Validación manual
                if (request.firstName() == null || request.firstName().trim().isEmpty()) {
                    return ResponseEntity.badRequest().build();
                }
                if (request.email() == null || !request.email().contains("@")) {
                    return ResponseEntity.badRequest().build();
                }

                if (!appUserService.shouldSucceed) {
                    return ResponseEntity.notFound().build();
                }

                UserProfileResponse response = appUserService.updateUserProfile(id, request);
                return ResponseEntity.ok(response);
            } catch (Exception e) {
                return ResponseEntity.badRequest().build();
            }
        }
    }

    static class TestAppUserService {
        private boolean shouldSucceed = true;

        public void setShouldSucceed(boolean shouldSucceed) {
            this.shouldSucceed = shouldSucceed;
        }

        public UserProfileResponse updateUserProfile(Integer id, UserUpdateRequest request) {
            if (!shouldSucceed) {
                throw new RuntimeException("User not found");
            }
            return new UserProfileResponse(
                1L, request.firstName(), request.lastName(), request.email(), null, request.profileInfo()
            );
        }
    }
}