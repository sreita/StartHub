package com.example.demo.controller;

import com.example.demo.appuser.AppUser;
import com.example.demo.appuser.AppUserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final AppUserService appUserService;

    @GetMapping("/{id}")
    public ResponseEntity<UserProfileResponse> getUserProfile(@PathVariable Integer id) {
        UserProfileResponse profile = appUserService.getUserProfile(id);
        return ResponseEntity.ok(profile);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserProfileResponse> updateUserProfile(
            @PathVariable Integer id,
            @RequestBody UserUpdateRequest updateRequest,
            Authentication authentication) {

        // Verificar que el usuario solo puede editar su propio perfil
        AppUser currentUser = (AppUser) authentication.getPrincipal();
        if (currentUser.getId() != id) {
            throw new RuntimeException("You can only edit your own profile");
        }

        UserProfileResponse updatedProfile = appUserService.updateUserProfile(id, updateRequest);
        return ResponseEntity.ok(updatedProfile);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteUser(
            @PathVariable Integer id,
            Authentication authentication) {

        AppUser currentUser = (AppUser) authentication.getPrincipal();
        if (currentUser.getId() != id) {
            throw new RuntimeException("You can only delete your own account");
        }

        appUserService.deleteUser(id);
        return ResponseEntity.ok("User account deleted successfully");
    }
}