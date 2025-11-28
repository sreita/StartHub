package com.example.demo.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.appuser.AppUser;
import com.example.demo.appuser.AppUserService;
import com.example.demo.appuser.PasswordResetService;
import com.example.demo.security.jwt.JwtService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final JwtService jwtService;
    private final AppUserService appUserService;
    private final PasswordResetService passwordResetService;

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@RequestBody LoginRequest request) {
        try {
            // Autenticar al usuario con Spring Security
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(request.email(), request.password())
            );

            // Si la autenticación es exitosa, obtener los detalles del usuario
            AppUser appUser = (AppUser) appUserService.loadUserByUsername(request.email());

            // Generar el token JWT
            String token = jwtService.generateToken(appUser);

            // Crear respuesta del perfil de usuario
            UserProfileResponse userProfile = new UserProfileResponse(
                (long) appUser.getId(),
                appUser.getFirstName(),
                appUser.getLastName(),
                appUser.getEmail(),
                appUser.getRegistrationDate(),
                appUser.getProfileInfo()
            );

            // Devolver el token y el perfil de usuario
            return ResponseEntity.ok(new LoginResponse(token, userProfile));
        } catch (BadCredentialsException e) {
            throw new RuntimeException("Credenciales inválidas");
        } catch (UsernameNotFoundException e) {
            throw new RuntimeException("Usuario no encontrado");
        } catch (Exception e) {
            throw new RuntimeException("Error en la autenticación: " + e.getMessage());
        }
    }

    @PostMapping("/logout")
    public ResponseEntity<String> logout() {
        // En JWT stateless, el logout se maneja principalmente del lado del cliente
        // Podrías implementar una blacklist de tokens si necesitas logout del servidor
        return ResponseEntity.ok("Logged out successfully");
    }

    @PostMapping("/recover-password")
public ResponseEntity<String> recoverPassword(@RequestBody PasswordRecoveryRequest request) {
    try {
        passwordResetService.sendPasswordResetEmail(request.email());
        return ResponseEntity.ok("Password recovery email sent");
    } catch (Exception e) {
        return ResponseEntity.badRequest().body("Error: " + e.getMessage());
    }
}

@PostMapping("/reset-password")
public ResponseEntity<String> resetPassword(@RequestBody PasswordResetRequest request) {
    try {
        System.out.println("=== Recibiendo solicitud de reset password ===");
        System.out.println("Token: " + request.token());

        passwordResetService.resetPassword(request.token(), request.newPassword());
        return ResponseEntity.ok("Password reset successfully");
    } catch (Exception e) {
        System.out.println("=== Error en reset password: " + e.getMessage() + " ===");
        return ResponseEntity.badRequest().body("Error: " + e.getMessage());
    }
}



}