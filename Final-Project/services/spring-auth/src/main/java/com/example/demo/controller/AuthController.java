package com.example.demo.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
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
        // Authenticate user with Spring Security
        // BadCredentialsException and UsernameNotFoundException exceptions
        // will be handled by GlobalExceptionHandler
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.email(), request.password())
        );

        // If authentication is successful, get user details
        AppUser appUser = (AppUser) appUserService.loadUserByUsername(request.email());

        // Generate JWT token
        String token = jwtService.generateToken(appUser);

        // Create user profile response
        UserProfileResponse userProfile = new UserProfileResponse(
            (long) appUser.getId(),
            appUser.getFirstName(),
            appUser.getLastName(),
            appUser.getEmail(),
            appUser.getRegistrationDate(),
            appUser.getProfileInfo()
        );

        // Return token and user profile
        return ResponseEntity.ok(new LoginResponse(token, userProfile));
    }

    @PostMapping("/logout")
    public ResponseEntity<String> logout() {
        // In JWT stateless architecture, logout is primarily handled on the client side
        // You could implement a token blacklist if server-side logout is needed
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