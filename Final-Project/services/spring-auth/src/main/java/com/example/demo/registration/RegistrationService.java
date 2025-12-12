/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

package com.example.demo.registration;

import java.time.LocalDateTime;

import org.springframework.stereotype.Service;

import com.example.demo.appuser.AppUser;
import com.example.demo.appuser.AppUserService;
import com.example.demo.email.EmailSender;
import com.example.demo.registration.token.ConfirmationToken;
import com.example.demo.registration.token.ConfirmationTokenService;

import jakarta.transaction.Transactional;
import lombok.AllArgsConstructor;

/**
 *
 * @author david
 */

@Service
@AllArgsConstructor
public class RegistrationService {

  private final AppUserService appUserService;
  private final EmailValidator emailValidator;
  private final ConfirmationTokenService confirmationTokenService;
  private final EmailSender emailSender;

  public String register(RegistrationRequest request) {
    boolean isValidEmail = emailValidator.test(request.getEmail());
    if (!isValidEmail) {
      throw new IllegalStateException("email not valid");
    }
    String token = appUserService.signUpUser(
      new AppUser(
        request.getFirstName(),
        request.getLastName(),
        request.getEmail(),
        request.getPassword(),
        false
      )
    );
    String link = "http://localhost:8081/api/v1/registration/confirm?token=" + token;
    emailSender.send(
      request.getEmail(),
      buildEmail(request.getFirstName(), link));

    return  token;


  }

@Transactional
    public String confirmToken(String token) {
        ConfirmationToken confirmationToken = confirmationTokenService
                .getToken(token)
                .orElse(null);
        
        if (confirmationToken == null) {
            return buildErrorPage("Token no encontrado", "El token de confirmación no es válido.");
        }

        if (confirmationToken.getConfirmedAt() != null) {
            return buildErrorPage("Email ya confirmado", "Esta cuenta ya ha sido confirmada previamente.");
        }

        LocalDateTime expiredAt = confirmationToken.getExpiresAt();

        if (expiredAt.isBefore(LocalDateTime.now())) {
            return buildErrorPage("Token expirado", "El token de confirmación ha expirado.");
        }

        confirmationTokenService.setConfirmedAt(token);

        // Enable the user account
        appUserService.enableAppUser(confirmationToken.getAppUser().getEmail());

        return """
        <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cuenta Confirmada - StartHub</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        .font-display {
            font-family: 'Bebas Neue', sans-serif;
            letter-spacing: 2px;
        }

        .neo-brutalist {
            border: 4px solid #000;
            box-shadow: 8px 8px 0 #000;
            transition: all 0.2s ease;
            border-radius: 4px;
        }

        .neo-brutalist:hover {
            box-shadow: 6px 6px 0 #000;
            transform: translate(2px, 2px);
        }

        .success-animation {
            animation: successPulse 2s ease-in-out;
        }

        @keyframes successPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .confetti {
            position: absolute;
            width: 10px;
            height: 10px;
            background-color: #FFD166;
            opacity: 0.8;
            animation: confettiFall 5s linear forwards;
        }

        @keyframes confettiFall {
            0% {
                transform: translateY(-100px) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(100vh) rotate(360deg);
                opacity: 0;
            }
        }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen p-4 md:p-8">
    <!-- Contenedor principal -->
    <div class="w-full max-w-md success-animation">
        <!-- Tarjeta de confirmación -->
        <div class="neo-brutalist bg-white p-8 rounded-lg text-center">
            <!-- Icono de confirmación -->
            <div class="mb-6">
                <svg class="w-24 h-24 mx-auto text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
            </div>

            <!-- Título -->
            <h1 class="text-4xl font-bold mb-4 font-display text-green-600">
                ¡CUENTA CONFIRMADA!
            </h1>

            <!-- Mensaje de confirmación -->
            <div class="mb-8">
                <p class="text-gray-700 font-mono text-lg mb-4">
                    Confirmación exitosa
                </p>
                <p class="text-gray-600 font-mono">
                    Tu cuenta ha sido activada correctamente.
                </p>
                <p class="text-gray-600 font-mono mt-2">
                    Ya puedes iniciar sesión en la plataforma.
                </p>
            </div>

            <!-- Botón de acción -->
            <div class="text-center">
                <a href="http://localhost:3000/login.html"
                   class="neo-brutalist inline-block bg-green-500 hover:bg-black hover:text-green-400 text-white font-bold py-3 px-8 font-mono transition-all duration-200">
                    IR AL INICIO DE SESIÓN
                </a>
            </div>
        </div>
    </div>

    <script>
        // Efecto de confeti al cargar la página
        document.addEventListener('DOMContentLoaded', function() {
            const colors = ['#FFD166', '#FF5E5B', '#4CAF50', '#06D6A0', '#118AB2'];

            for (let i = 0; i < 50; i++) {
                setTimeout(() => {
                    const confetti = document.createElement('div');
                    confetti.className = 'confetti';
                    confetti.style.left = Math.random() * 100 + 'vw';
                    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                    confetti.style.animationDelay = Math.random() * 2 + 's';
                    document.body.appendChild(confetti);

                    // Eliminar el confeti después de la animación
                    setTimeout(() => {
                        confetti.remove();
                    }, 5000);
                }, i * 100);
            }
        });

        // Configurar modo noche si está activo
        const savedNightMode = localStorage.getItem('nightMode') === 'true';
        if (savedNightMode) {
            document.body.classList.add('night-mode-active');

            // Aplicar estilos de modo noche
            const style = document.createElement('style');
            style.textContent = `
                body.night-mode-active {
                    background-color: #1a1a2e !important;
                    color: #e2e8f0 !important;
                }

                .night-mode-active .neo-brutalist {
                    background-color: #16213e !important;
                    color: #e2e8f0 !important;
                    border-color: #0f3460 !important;
                    box-shadow: 8px 8px 0 #0f3460 !important;
                }

                .night-mode-active .text-gray-700,
                .night-mode-active .text-gray-600 {
                    color: #cbd5e0 !important;
                }

                .night-mode-active .bg-green-500 {
                    background-color: #2d3748 !important;
                    color: #e2e8f0 !important;
                    border-color: #0f3460 !important;
                }

                .night-mode-active .bg-green-500:hover {
                    background-color: #FF5E5B !important;
                    color: #ffffff !important;
                }
            `;
            document.head.appendChild(style);
        }
    </script>
</body>
</html>
        """;
    }

    public String buildEmail(String name, String link) {
    return """
           <!DOCTYPE html>
           <html lang="es">
           <head>
               <meta charset="UTF-8">
               <meta name="viewport" content="width=device-width, initial-scale=1.0">
               <title>Confirmaci\u00f3n de Cuenta - StartHub</title>
               <style>
                   @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto+Mono:wght@400;700&display=swap');

                   body {
                       margin: 0;
                       padding: 0;
                       background-color: #f5f5f5;
                       font-family: 'Roboto Mono', monospace;
                       color: #333;
                       line-height: 1.6;
                   }

                   .email-container {
                       max-width: 600px;
                       margin: 0 auto;
                       background-color: #ffffff;
                       border: 4px solid #000;
                       box-shadow: 8px 8px 0 #000;
                   }

                   .header {
                       background-color: #FF5E5B;
                       padding: 20px;
                       text-align: center;
                       border-bottom: 4px solid #000;
                   }

                   .logo {
                       font-family: 'Bebas Neue', sans-serif;
                       font-size: 32px;
                       color: #000;
                       letter-spacing: 2px;
                       margin: 0;
                   }

                   .content {
                       padding: 30px;
                   }

                   .greeting {
                       font-size: 24px;
                       font-weight: bold;
                       margin-bottom: 20px;
                       font-family: 'Bebas Neue', sans-serif;
                       letter-spacing: 1px;
                   }

                   .message {
                       margin-bottom: 30px;
                       font-size: 16px;
                   }

                   .activation-button {
                       display: inline-block;
                       background-color: #FFD166;
                       color: #000;
                       padding: 15px 30px;
                       text-decoration: none;
                       font-weight: bold;
                       border: 3px solid #000;
                       box-shadow: 4px 4px 0 #000;
                       transition: all 0.2s ease;
                       font-family: 'Roboto Mono', monospace;
                       margin: 20px 0;
                       text-align: center;
                   }

                   .expiration-notice {
                       background-color: #f8f8f8;
                       border: 2px solid #000;
                       padding: 15px;
                       margin: 20px 0;
                       font-size: 14px;
                       text-align: center;
                   }

                   .footer {
                       background-color: #000;
                       color: #fff;
                       padding: 20px;
                       text-align: center;
                       font-size: 14px;
                       border-top: 4px solid #FF5E5B;
                   }

                   .social-links {
                       margin: 15px 0;
                   }

                   .social-links a {
                       color: #FFD166;
                       text-decoration: none;
                       margin: 0 10px;
                   }

                   .divider {
                       height: 2px;
                       background-color: #000;
                       margin: 20px 0;
                   }

                   @media only screen and (max-width: 600px) {
                       .email-container {
                           width: 100%;
                           border: none;
                           box-shadow: none;
                       }

                       .content {
                           padding: 20px;
                       }

                       .activation-button {
                           display: block;
                           width: 80%;
                           margin: 20px auto;
                       }
                   }
               </style>
           </head>
           <body>
               <div class="email-container">
                   <div class="header">
                       <h1 class="logo">STARTHUB</h1>
                   </div>

                   <div class="content">
                       <p class="greeting">\u00a1Hola_""" + name + "!</p>\n" +
            "            \n" +
            "            <div class=\"message\">\n" +
            "                <p>Gracias por registrarte en StartHub. Estamos emocionados de tenerte en nuestra comunidad de emprendedores.</p>\n" +
            "                <p>Para completar tu registro y comenzar a explorar startups, necesitamos que confirmes tu dirección de correo electrónico.</p>\n" +
            "            </div>\n" +
            "            \n" +
            "            <div style=\"text-align: center;\">\n" +
            "                <a href=\"" + link + "\" class=\"activation-button\">\n" +
            "                    CONFIRMAR MI CUENTA\n" +
            "                </a>\n" +
            "            </div>\n" +
            "            \n" +
            "            <div class=\"expiration-notice\">\n" +
            "                <p><strong>IMPORTANTE:</strong> Este enlace expirará en 15 minutos por razones de seguridad.</p>\n" +
            "            </div>\n" +
            "            \n" +
            "            <div class=\"divider\"></div>\n" +
            "            \n" +
            "            <div class=\"message\">\n" +
            "                <p>Si no te registraste en StartHub, puedes ignorar este mensaje.</p>\n" +
            "                <p>Si tienes problemas para confirmar tu cuenta, no dudes en contactar a nuestro equipo de soporte.</p>\n" +
            "            </div>\n" +
            "        </div>\n" +
            "        \n" +
            "        <div class=\"footer\">\n" +
            "            <p>&copy; 2024 StartHub. Todos los derechos reservados.</p>\n" +
            "            <div class=\"social-links\">\n" +
            "                <a href=\"#\">Web</a> | \n" +
            "                <a href=\"#\">Twitter</a> | \n" +
            "                <a href=\"#\">LinkedIn</a>\n" +
            "            </div>\n" +
            "            <p>Este es un mensaje automático, por favor no respondas a este correo.</p>\n" +
            "        </div>\n" +
            "    </div>\n" +
            "</body>\n" +
            "</html>";
}

private String buildErrorPage(String title, String message) {
    return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error - StartHub</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100 flex items-center justify-center min-h-screen">
            <div class="bg-white p-8 rounded-lg shadow-md max-w-md w-full text-center">
                <div class="text-red-500 text-6xl mb-4">⚠️</div>
                <h1 class="text-2xl font-bold text-gray-800 mb-4">""" + title + """
                </h1>
                <p class="text-gray-600 mb-6">""" + message + """
                </p>
                <a href="http://localhost:3000/login.html" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded inline-block">
                    Volver al Login
                </a>
            </div>
        </body>
        </html>
        """;
}

}
