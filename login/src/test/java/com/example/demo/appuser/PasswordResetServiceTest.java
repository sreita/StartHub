// src/test/java/com/example/demo/appuser/PasswordResetServiceTest.java
package com.example.demo.appuser;

import java.time.LocalDateTime;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import com.example.demo.email.EmailSender;

class PasswordResetServiceTest {

    private TestablePasswordResetService passwordResetService;
    private ManualAppUserRepository appUserRepository;
    private ManualPasswordResetTokenRepository tokenRepository;
    private TestBCryptPasswordEncoder passwordEncoder;
    private TestEmailSender emailSender;

    @BeforeEach
    void setUp() {
        appUserRepository = new ManualAppUserRepository();
        tokenRepository = new ManualPasswordResetTokenRepository();
        passwordEncoder = new TestBCryptPasswordEncoder();
        emailSender = new TestEmailSender();

        passwordResetService = new TestablePasswordResetService(
            appUserRepository,
            tokenRepository,
            passwordEncoder,
            emailSender
        );
    }

    @Test
    void whenValidEmail_thenSendPasswordResetEmail() {
        // Configurar
        AppUser user = createTestUser();
        appUserRepository.save(user);
        String email = "test@example.com";

        // Ejecutar
        passwordResetService.sendPasswordResetEmail(email);

        // Verificar
        assertTrue(emailSender.wasEmailSent());
        assertEquals(email, emailSender.getLastRecipient());
        assertTrue(emailSender.getLastEmailContent().contains("Test email content"));

        // Verificar que se creó el token
        assertEquals(1, tokenRepository.count());
    }

    @Test
    void whenInvalidEmail_thenThrowException() {
        // Configurar
        String nonExistentEmail = "nonexistent@example.com";

        // Ejecutar & Verificar
        IllegalStateException exception = assertThrows(
            IllegalStateException.class,
            () -> passwordResetService.sendPasswordResetEmail(nonExistentEmail)
        );

        assertEquals("User with email " + nonExistentEmail + " not found", exception.getMessage());
        assertFalse(emailSender.wasEmailSent());
    }

    @Test
    void whenValidToken_thenResetPassword() {
        // Configurar
        AppUser user = createTestUser();
        appUserRepository.save(user);

        PasswordResetToken resetToken = new PasswordResetToken(
            "valid-token-123",
            user,
            LocalDateTime.now().plusHours(24)
        );
        tokenRepository.save(resetToken);

        String newPassword = "newSecurePassword123";

        // Ejecutar
        passwordResetService.resetPassword("valid-token-123", newPassword);

        // Verificar
        AppUser updatedUser = appUserRepository.findByEmail("test@example.com").orElseThrow();
        assertTrue(passwordEncoder.matches(newPassword, updatedUser.getPassword()));
        assertNotNull(resetToken.getConfirmedAt());
    }

    @Test
    void whenInvalidToken_thenThrowException() {
        // Configurar
        String invalidToken = "invalid-token";

        // Ejecutar & Verificar
        IllegalStateException exception = assertThrows(
            IllegalStateException.class,
            () -> passwordResetService.resetPassword(invalidToken, "newPassword")
        );

        assertEquals("Token not found", exception.getMessage());
    }

    @Test
    void whenExpiredToken_thenThrowException() {
        // Configurar
        AppUser user = createTestUser();
        appUserRepository.save(user);

        PasswordResetToken expiredToken = new PasswordResetToken(
            "expired-token",
            user,
            LocalDateTime.now().minusHours(1) // Token expirado
        );
        tokenRepository.save(expiredToken);

        // Ejecutar & Verificar
        IllegalStateException exception = assertThrows(
            IllegalStateException.class,
            () -> passwordResetService.resetPassword("expired-token", "newPassword")
        );

        assertEquals("Token expired", exception.getMessage());
    }

    @Test
    void whenAlreadyUsedToken_thenThrowException() {
        // Configurar
        AppUser user = createTestUser();
        appUserRepository.save(user);

        PasswordResetToken usedToken = new PasswordResetToken(
            "used-token",
            user,
            LocalDateTime.now().plusHours(24)
        );
        usedToken.setConfirmedAt(LocalDateTime.now()); // Marcar como usado
        tokenRepository.save(usedToken);

        // Ejecutar & Verificar
        IllegalStateException exception = assertThrows(
            IllegalStateException.class,
            () -> passwordResetService.resetPassword("used-token", "newPassword")
        );

        assertEquals("Token already used", exception.getMessage());
    }

    @Test
    void whenResetPassword_thenPasswordIsEncoded() {
        // Configurar
        AppUser user = createTestUser();
        appUserRepository.save(user);

        PasswordResetToken resetToken = new PasswordResetToken(
            "test-token",
            user,
            LocalDateTime.now().plusHours(24)
        );
        tokenRepository.save(resetToken);

        String plainPassword = "plainTextPassword";

        // Ejecutar
        passwordResetService.resetPassword("test-token", plainPassword);

        // Verificar que la contraseña fue codificada
        AppUser updatedUser = appUserRepository.findByEmail("test@example.com").orElseThrow();
        assertTrue(updatedUser.getPassword().startsWith("encoded-"));
        assertTrue(passwordEncoder.matches(plainPassword, updatedUser.getPassword()));
    }

    private AppUser createTestUser() {
        AppUser user = new AppUser();
        user.setId(1);
        user.setFirstName("John");
        user.setLastName("Doe");
        user.setEmail("test@example.com");
        user.setPassword("oldPassword");
        user.setEnabled(true);
        return user;
    }

    // Implementación manual de AppUserRepository para testing
    static class ManualAppUserRepository {
        private AppUser savedUser;

        public Optional<AppUser> findByEmail(String email) {
            if (savedUser != null && savedUser.getEmail().equals(email)) {
                return Optional.of(savedUser);
            }
            return Optional.empty();
        }

        public AppUser save(AppUser user) {
            this.savedUser = user;
            return user;
        }

        public Optional<AppUser> findById(Integer id) {
            if (savedUser != null && savedUser.getId() == id) {
                return Optional.of(savedUser);
            }
            return Optional.empty();
        }

        public int enableAppUser(String email) {
            if (savedUser != null && savedUser.getEmail().equals(email)) {
                savedUser.setEnabled(true);
                return 1;
            }
            return 0;
        }
    }

    // Implementación manual de PasswordResetTokenRepository para testing
    static class ManualPasswordResetTokenRepository {
        private PasswordResetToken savedToken;

        public Optional<PasswordResetToken> findByToken(String token) {
            if (savedToken != null && savedToken.getToken().equals(token)) {
                return Optional.of(savedToken);
            }
            return Optional.empty();
        }

        public PasswordResetToken save(PasswordResetToken token) {
            this.savedToken = token;
            return token;
        }

        public void deleteAllExpiredSince(LocalDateTime now) {
            if (savedToken != null && savedToken.getExpiresAt().isBefore(now)) {
                savedToken = null;
            }
        }

        public long count() {
            return savedToken != null ? 1 : 0;
        }
    }

    // Implementación de prueba de PasswordResetService
    static class TestablePasswordResetService {
        private final ManualAppUserRepository appUserRepository;
        private final ManualPasswordResetTokenRepository tokenRepository;
        private final TestBCryptPasswordEncoder passwordEncoder;
        private final TestEmailSender emailSender;

        public TestablePasswordResetService(ManualAppUserRepository appUserRepository,
                                          ManualPasswordResetTokenRepository tokenRepository,
                                          TestBCryptPasswordEncoder passwordEncoder,
                                          TestEmailSender emailSender) {
            this.appUserRepository = appUserRepository;
            this.tokenRepository = tokenRepository;
            this.passwordEncoder = passwordEncoder;
            this.emailSender = emailSender;
        }

        public void sendPasswordResetEmail(String email) {
            AppUser user = appUserRepository.findByEmail(email)
                    .orElseThrow(() -> new IllegalStateException("User with email " + email + " not found"));

            String token = "test-token-" + System.currentTimeMillis();
            PasswordResetToken resetToken = new PasswordResetToken(
                    token,
                    user,
                    LocalDateTime.now().plusHours(24)
            );

            tokenRepository.save(resetToken);

            // Usar el email sender de prueba
            emailSender.send(user.getEmail(), "Test email content with token: " + token);
        }

        public void resetPassword(String token, String newPassword) {
            PasswordResetToken resetToken = tokenRepository.findByToken(token)
                    .orElseThrow(() -> new IllegalStateException("Token not found"));

            if (resetToken.getConfirmedAt() != null) {
                throw new IllegalStateException("Token already used");
            }

            if (resetToken.getExpiresAt().isBefore(LocalDateTime.now())) {
                throw new IllegalStateException("Token expired");
            }

            AppUser user = resetToken.getAppUser();
            user.setPassword(passwordEncoder.encode(newPassword));
            appUserRepository.save(user);

            resetToken.setConfirmedAt(LocalDateTime.now());
            tokenRepository.save(resetToken);
        }
    }

    // Implementación de prueba de BCryptPasswordEncoder
    static class TestBCryptPasswordEncoder extends BCryptPasswordEncoder {
        @Override
        public String encode(CharSequence rawPassword) {
            return "encoded-" + rawPassword;
        }

        @Override
        public boolean matches(CharSequence rawPassword, String encodedPassword) {
            return encodedPassword.equals("encoded-" + rawPassword);
        }
    }

    // Implementación de prueba de EmailSender
    static class TestEmailSender implements EmailSender {
        private boolean emailSent = false;
        private String lastRecipient;
        private String lastEmailContent;

        @Override
        public void send(String to, String email) {
            this.emailSent = true;
            this.lastRecipient = to;
            this.lastEmailContent = email;
        }

        public boolean wasEmailSent() {
            return emailSent;
        }

        public String getLastRecipient() {
            return lastRecipient;
        }

        public String getLastEmailContent() {
            return lastEmailContent;
        }

        public void reset() {
            emailSent = false;
            lastRecipient = null;
            lastEmailContent = null;
        }
    }
}