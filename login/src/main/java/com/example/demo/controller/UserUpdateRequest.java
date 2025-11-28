package com.example.demo.controller;

public record UserUpdateRequest(
    String firstName,
    String lastName,
    String email,
    String profileInfo
) {}