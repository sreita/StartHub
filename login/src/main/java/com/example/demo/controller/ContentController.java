/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.example.demo.registration.RegistrationService;

import lombok.AllArgsConstructor;

/**
 *
 * @author david
 */

@Controller
@AllArgsConstructor
public class ContentController {

    private final RegistrationService registrationService;

    @GetMapping("/req/login")
    public String login(){
       return "login";
    }

    @GetMapping("/req/signup")
    public String signup(){
        return "signup";
    }

    @GetMapping("/")
    public String redirectToLogin() {
        return "redirect:/req/login";
    }

    @GetMapping("/home")
    public String home(){
        return "home";
    }

    @GetMapping(path = "/req/success")
    public String registrationSuccess() {
        return "success_message";
    }

    @GetMapping(path = "/api/v1/registration/confirm")
    public String confirm(@RequestParam("token") String token) {
        // Llama al servicio, que contiene la lógica de validación y habilitación.
        // El servicio DEBE retornar "redirect:/req/success" (o la ruta que desees)
        return registrationService.confirmToken(token);
    }
}
