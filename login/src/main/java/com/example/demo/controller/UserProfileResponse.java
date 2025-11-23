package com.example.demo.controller;

import java.time.LocalDateTime;

public record UserProfileResponse(
    Long id,
    String firstName,
    String lastName,
    String email,
    LocalDateTime registrationDate,
    String profileInfo
) {
}