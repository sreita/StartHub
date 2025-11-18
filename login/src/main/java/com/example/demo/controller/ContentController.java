/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 *
 * @author david
 */

@Controller
public class ContentController {


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

}
