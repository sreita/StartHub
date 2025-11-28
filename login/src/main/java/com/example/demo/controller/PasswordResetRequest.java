package com.example.demo.controller;

public record PasswordResetRequest(String token, String newPassword) {
}