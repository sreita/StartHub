package com.example.demo.appuser;

import java.time.LocalDateTime;
import java.util.UUID;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.example.demo.email.EmailSender;

import lombok.AllArgsConstructor;

@Service
@AllArgsConstructor
public class PasswordResetService {

    private final AppUserRepository appUserRepository;
    private final PasswordResetTokenRepository passwordResetTokenRepository;
    private final BCryptPasswordEncoder bCryptPasswordEncoder;
    private final EmailSender emailSender;

    public void sendPasswordResetEmail(String email) {
        AppUser user = appUserRepository.findByEmail(email)
                .orElseThrow(() -> new IllegalStateException("User with email " + email + " not found"));

        String token = UUID.randomUUID().toString();
        PasswordResetToken resetToken = new PasswordResetToken(
                token,
                user,
                LocalDateTime.now().plusHours(24)
        );

        passwordResetTokenRepository.save(resetToken);

        String link = "http://localhost:3000/reset_password.html?token=" + token;
        emailSender.send(
                user.getEmail(),
                buildEmail(user.getFirstName(), link));
    }

    public void resetPassword(String token, String newPassword) {
        PasswordResetToken resetToken = passwordResetTokenRepository.findByToken(token)
                .orElseThrow(() -> new IllegalStateException("Token not found"));

        if (resetToken.getConfirmedAt() != null) {
            throw new IllegalStateException("Token already used");
        }

        if (resetToken.getExpiresAt().isBefore(LocalDateTime.now())) {
            throw new IllegalStateException("Token expired");
        }

        AppUser user = resetToken.getAppUser();
        user.setPassword(bCryptPasswordEncoder.encode(newPassword));
        appUserRepository.save(user);

        resetToken.setConfirmedAt(LocalDateTime.now());
        passwordResetTokenRepository.save(resetToken);
    }

private String buildEmail(String name, String token) {
    // 🔥 Asegúrate de que use el puerto correcto de tu servidor frontend
    String resetLink = "http://127.0.0.1:5500/frontend/reset_password.html?token=" + token;

    System.out.println("=== Enlace de reset generado: " + resetLink + " ===");

    return "<div style=\"font-family:Helvetica,Arial,sans-serif;font-size:16px;margin:0;color:#0b0c0c\">\n" +
            "<p>Hola " + name + ",</p>" +
            "<p>Solicitaste restablecer tu contraseña. Haz clic en el enlace a continuación para restablecerla:</p>" +
            "<p><a href=\"" + resetLink + "\" style=\"background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;\">Restablecer Contraseña</a></p>" +
            "<p>Este enlace expirará en 24 horas.</p>" +
            "<p>Si no solicitaste esto, por favor ignora este correo.</p>" +
            "</div>";
}
}