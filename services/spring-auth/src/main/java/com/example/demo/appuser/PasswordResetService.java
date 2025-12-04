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
    String resetLink = token;

    System.out.println("=== Enlace de reset generado: " + resetLink + " ===");

    return "<!DOCTYPE html>" +
       "<html lang=\"es\">" +
       "<head>" +
           "<meta charset=\"UTF-8\">" +
           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">" +
           "<title>Restablecer Contraseña - StartHub</title>" +
           "<style>" +
               "@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto+Mono:wght@400;700&display=swap');" +
               "body { margin: 0; padding: 0; background-color: #f5f5f5; font-family: 'Roboto Mono', monospace; color: #333; line-height: 1.6; }" +
               ".email-container { max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 4px solid #000; box-shadow: 8px 8px 0 #000; }" +
               ".header { background-color: #FF5E5B; padding: 20px; text-align: center; border-bottom: 4px solid #000; }" +
               ".logo { font-family: 'Bebas Neue', sans-serif; font-size: 32px; color: #000; letter-spacing: 2px; margin: 0; }" +
               ".content { padding: 30px; }" +
               ".greeting { font-size: 24px; font-weight: bold; margin-bottom: 20px; font-family: 'Bebas Neue', sans-serif; letter-spacing: 1px; }" +
               ".message { margin-bottom: 30px; font-size: 16px; }" +
               ".reset-button { display: inline-block; background-color: #FFD166; color: #000; padding: 15px 30px; text-decoration: none; font-weight: bold; border: 3px solid #000; box-shadow: 4px 4px 0 #000; transition: all 0.2s ease; font-family: 'Roboto Mono', monospace; margin: 20px 0; text-align: center; }" +
               ".expiration-notice { background-color: #f8f8f8; border: 2px solid #000; padding: 15px; margin: 20px 0; font-size: 14px; text-align: center; }" +
               ".footer { background-color: #000; color: #fff; padding: 20px; text-align: center; font-size: 14px; border-top: 4px solid #FF5E5B; }" +
               ".social-links { margin: 15px 0; }" +
               ".social-links a { color: #FFD166; text-decoration: none; margin: 0 10px; }" +
               ".divider { height: 2px; background-color: #000; margin: 20px 0; }" +
               "@media only screen and (max-width: 600px) {" +
                   ".email-container { width: 100%; border: none; box-shadow: none; }" +
                   ".content { padding: 20px; }" +
                   ".reset-button { display: block; width: 80%; margin: 20px auto; }" +
               "}" +
           "</style>" +
       "</head>" +
       "<body>" +
           "<div class=\"email-container\">" +
               "<div class=\"header\">" +
                   "<h1 class=\"logo\">STARTHUB</h1>" +
               "</div>" +
               "<div class=\"content\">" +
                   "<p class=\"greeting\">¡Hola " + name + "!</p>" +
                   "<div class=\"message\">" +
                       "<p>Recibimos una solicitud para restablecer la contraseña de tu cuenta en StartHub.</p>" +
                       "<p>Haz clic en el botón a continuación para crear una nueva contraseña:</p>" +
                   "</div>" +
                   "<div style=\"text-align: center;\">" +
                       "<a href=\"" + resetLink + "\" class=\"reset-button\">" +
                           "RESTABLECER CONTRASEÑA" +
                       "</a>" +
                   "</div>" +
                   "<div class=\"expiration-notice\">" +
                       "<p><strong>IMPORTANTE:</strong> Este enlace expirará en 24 horas por razones de seguridad.</p>" +
                   "</div>" +
                   "<div class=\"divider\"></div>" +
                   "<div class=\"message\">" +
                       "<p>Si no solicitaste restablecer tu contraseña, puedes ignorar este mensaje.</p>" +
                       "<p>Si tienes problemas para restablecer tu contraseña, no dudes en contactar a nuestro equipo de soporte.</p>" +
                   "</div>" +
               "</div>" +
               "<div class=\"footer\">" +
                   "<p>&copy; 2024 StartHub. Todos los derechos reservados.</p>" +
                   "<div class=\"social-links\">" +
                       "<a href=\"#\">Web</a> | " +
                       "<a href=\"#\">Twitter</a> | " +
                       "<a href=\"#\">LinkedIn</a>" +
                   "</div>" +
                   "<p>Este es un mensaje automático, por favor no respondas a este correo.</p>" +
               "</div>" +
           "</div>" +
       "</body>" +
       "</html>";
}
}