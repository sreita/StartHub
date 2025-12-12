package com.example.demo.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.appuser.AppUser;
import com.example.demo.appuser.AppUserService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final AppUserService appUserService;

    @GetMapping("/me")
    public ResponseEntity<UserProfileResponse> getCurrentUserProfile(Authentication authentication) {
        AppUser currentUser = (AppUser) authentication.getPrincipal();
        UserProfileResponse profile = appUserService.getUserProfile(currentUser.getId());
        return ResponseEntity.ok(profile);
    }

    @PutMapping("/me")
    public ResponseEntity<UserProfileResponse> updateCurrentUserProfile(
            @RequestBody UserUpdateRequest updateRequest,
            Authentication authentication) {
        
        AppUser currentUser = (AppUser) authentication.getPrincipal();
        UserProfileResponse updatedProfile = appUserService.updateUserProfile(currentUser.getId(), updateRequest);
        return ResponseEntity.ok(updatedProfile);
    }

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

    @DeleteMapping("/me")
    public ResponseEntity<String> deleteCurrentUser(Authentication authentication) {
        AppUser currentUser = (AppUser) authentication.getPrincipal();
        appUserService.deleteUser(currentUser.getId());
        return ResponseEntity.ok("User account deleted successfully");
    }
}