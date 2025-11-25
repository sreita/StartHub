package com.example.demo.registration;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.example.demo.appuser.AppUser;
import com.example.demo.appuser.AppUserService;
import com.example.demo.email.EmailSender;
import com.example.demo.registration.token.ConfirmationToken;
import com.example.demo.registration.token.ConfirmationTokenService;

// Tests manuales sin Mockito para RegistrationService
class RegistrationServiceManualTest {

    private RegistrationService registrationService;
    private ManualAppUserService manualAppUserService;
    private ManualEmailValidator manualEmailValidator;
    private ManualConfirmationTokenService manualConfirmationTokenService;
    private ManualEmailSender manualEmailSender;

    @BeforeEach
    void setUp() {
        manualAppUserService = new ManualAppUserService();
        manualEmailValidator = new ManualEmailValidator();
        manualConfirmationTokenService = new ManualConfirmationTokenService();
        manualEmailSender = new ManualEmailSender();

        registrationService = new RegistrationService(
            manualAppUserService,
            manualEmailValidator,
            manualConfirmationTokenService,
            manualEmailSender
        );
    }

    @Test
    void testRegister_WithValidEmail_ShouldReturnToken() {
        // Given
        RegistrationRequest request = new RegistrationRequest(
            "John", "Doe", "john.doe@example.com", "password123"
        );
        manualEmailValidator.setValid(true);
        manualAppUserService.setUserExists(false);

        // When
        String result = registrationService.register(request);

        // Then
        assertNotNull(result);
        assertTrue(result.length() > 0);
        assertTrue(manualAppUserService.isSignUpUserCalled());
        assertTrue(manualEmailSender.isSendCalled());
        assertEquals(request.getEmail(), manualEmailSender.getLastTo());
    }

    @Test
    void testRegister_WithInvalidEmail_ShouldThrowException() {
        // Given
        RegistrationRequest request = new RegistrationRequest(
            "John", "Doe", "invalid-email", "password123"
        );
        manualEmailValidator.setValid(false);

        // When & Then
        IllegalStateException exception = assertThrows(
            IllegalStateException.class,
            () -> registrationService.register(request)
        );
        assertEquals("email not valid", exception.getMessage());
        assertFalse(manualAppUserService.isSignUpUserCalled());
        assertFalse(manualEmailSender.isSendCalled());
    }

    @Test
    void testRegister_WhenUserAlreadyExistsAndEnabled_ShouldThrowException() {
        // Given
        RegistrationRequest request = new RegistrationRequest(
            "John", "Doe", "existing@example.com", "password123"
        );
        manualEmailValidator.setValid(true);
        manualAppUserService.setUserExists(true);
        manualAppUserService.setUserEnabled(true);

        // When & Then
        IllegalStateException exception = assertThrows(
            IllegalStateException.class,
            () -> registrationService.register(request)
        );
        assertEquals("email already taken", exception.getMessage());
    }

    @Test
    void testRegister_WhenUserExistsButNotEnabled_ShouldRegenerateToken() {
        // Given
        RegistrationRequest request = new RegistrationRequest(
            "John", "Doe", "existing@example.com", "password123"
        );
        manualEmailValidator.setValid(true);
        manualAppUserService.setUserExists(true);
        manualAppUserService.setUserEnabled(false);

        // When
        String result = registrationService.register(request);

        // Then
        assertNotNull(result);
        assertTrue(manualEmailSender.isSendCalled());
        assertEquals(request.getEmail(), manualEmailSender.getLastTo());
    }

    @Test
    void testConfirmToken_WithValidToken_ShouldReturnSuccessHtml() {
        // Given
        String token = "valid-token";
        AppUser appUser = new AppUser("John", "Doe", "john@example.com", "password", false);
        ConfirmationToken confirmationToken = new ConfirmationToken(
            token,
            LocalDateTime.now().minusMinutes(5),
            LocalDateTime.now().plusMinutes(10),
            appUser
        );
        manualConfirmationTokenService.setTokenToReturn(Optional.of(confirmationToken));

        // When
        String result = registrationService.confirmToken(token);

        // Then
        assertNotNull(result);
        assertTrue(result.contains("¡CUENTA CONFIRMADA!"));
        assertTrue(manualConfirmationTokenService.isSaveConfirmationTokenCalled());
        assertTrue(manualAppUserService.isEnableAppUserCalled());
        assertEquals(appUser.getEmail(), manualAppUserService.getLastEnabledEmail());
    }

    @Test
    void testConfirmToken_WithNonExistentToken_ShouldThrowException() {
        // Given
        String token = "non-existent-token";
        manualConfirmationTokenService.setTokenToReturn(Optional.empty());

        // When & Then
        IllegalStateException exception = assertThrows(
            IllegalStateException.class,
            () -> registrationService.confirmToken(token)
        );
        assertEquals("token not found", exception.getMessage());
    }

    @Test
    void testConfirmToken_WithAlreadyConfirmedToken_ShouldThrowException() {
        // Given
        String token = "already-confirmed-token";
        AppUser appUser = new AppUser("John", "Doe", "john@example.com", "password", false);
        ConfirmationToken confirmationToken = new ConfirmationToken(
            token,
            LocalDateTime.now().minusMinutes(5),
            LocalDateTime.now().plusMinutes(10),
            appUser
        );
        confirmationToken.setConfirmedAt(LocalDateTime.now());
        manualConfirmationTokenService.setTokenToReturn(Optional.of(confirmationToken));

        // When & Then
        IllegalStateException exception = assertThrows(
            IllegalStateException.class,
            () -> registrationService.confirmToken(token)
        );
        assertEquals("email already confirmed", exception.getMessage());
    }

    @Test
    void testConfirmToken_WithExpiredToken_ShouldThrowException() {
        // Given
        String token = "expired-token";
        AppUser appUser = new AppUser("John", "Doe", "john@example.com", "password", false);
        ConfirmationToken confirmationToken = new ConfirmationToken(
            token,
            LocalDateTime.now().minusMinutes(20),
            LocalDateTime.now().minusMinutes(5), // Expired 5 minutes ago
            appUser
        );
        manualConfirmationTokenService.setTokenToReturn(Optional.of(confirmationToken));

        // When & Then
        IllegalStateException exception = assertThrows(
            IllegalStateException.class,
            () -> registrationService.confirmToken(token)
        );
        assertEquals("token expired", exception.getMessage());
    }

    @Test
    void testBuildEmail_ShouldReturnValidHtml() {
        // Given
        String name = "John";
        String link = "http://localhost:8080/api/v1/registration/confirm?token=test-token";

        // When
        String result = registrationService.buildEmail(name, link);

        // Then
        assertNotNull(result);
        assertTrue(result.contains("<!DOCTYPE html>"));
        assertTrue(result.contains("John"));
        assertTrue(result.contains(link));
        assertTrue(result.contains("CONFIRMAR MI CUENTA"));
    }

    // Manual implementations for dependencies

    private static class ManualAppUserService extends AppUserService {
        private boolean signUpUserCalled = false;
        private boolean enableAppUserCalled = false;
        private boolean userExists = false;
        private boolean userEnabled = false;
        private String lastEnabledEmail;

        public ManualAppUserService() {
            super(null, null, null);
        }

        @Override
        public String signUpUser(AppUser appUser) {
            signUpUserCalled = true;
            if (userExists) {
                if (userEnabled) {
                    throw new IllegalStateException("email already taken");
                }
                // For existing but not enabled user, return a new token
                return UUID.randomUUID().toString();
            }
            return UUID.randomUUID().toString();
        }

        @Override
        public int enableAppUser(String email) {
            enableAppUserCalled = true;
            lastEnabledEmail = email;
            return 1;
        }

        public boolean isSignUpUserCalled() {
            return signUpUserCalled;
        }

        public boolean isEnableAppUserCalled() {
            return enableAppUserCalled;
        }

        public String getLastEnabledEmail() {
            return lastEnabledEmail;
        }

        public void setUserExists(boolean userExists) {
            this.userExists = userExists;
        }

        public void setUserEnabled(boolean userEnabled) {
            this.userEnabled = userEnabled;
        }
    }

    private static class ManualEmailValidator extends EmailValidator {
        private boolean isValid = true;

        @Override
        public boolean test(String email) {
            return isValid;
        }

        public void setValid(boolean valid) {
            isValid = valid;
        }
    }

    private static class ManualConfirmationTokenService extends ConfirmationTokenService {
        private Optional<ConfirmationToken> tokenToReturn = Optional.empty();
        private boolean saveConfirmationTokenCalled = false;

        public ManualConfirmationTokenService() {
            super(null);
        }

        @Override
        public Optional<ConfirmationToken> getToken(String token) {
            return tokenToReturn;
        }

        @Override
        public void saveConfirmationToken(ConfirmationToken token) {
            saveConfirmationTokenCalled = true;
        }

        @Override
        public void setConfirmedAt(String token) {
            // Implementation for manual test
        }

        public void setTokenToReturn(Optional<ConfirmationToken> token) {
            this.tokenToReturn = token;
        }

        public boolean isSaveConfirmationTokenCalled() {
            return saveConfirmationTokenCalled;
        }
    }

    private static class ManualEmailSender implements EmailSender {
        private boolean sendCalled = false;
        private String lastTo;
        private String lastEmail;

        @Override
        public void send(String to, String email) {
            sendCalled = true;
            lastTo = to;
            lastEmail = email;
        }

        public boolean isSendCalled() {
            return sendCalled;
        }

        public String getLastTo() {
            return lastTo;
        }

        public String getLastEmail() {
            return lastEmail;
        }
    }
}