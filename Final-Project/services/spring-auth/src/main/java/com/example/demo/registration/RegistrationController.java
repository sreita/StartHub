package com.example.demo.registration;

import java.util.HashMap;
import java.util.Map;

import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.AllArgsConstructor;

@RestController
@RequestMapping(path = "api/v1/registration")
@AllArgsConstructor

public class RegistrationController {

  private final RegistrationService registrationService;


  @PostMapping
  public ResponseEntity<Map<String, String>> register(@RequestBody RegistrationRequest request) {
    String token = registrationService.register(request);
    Map<String, String> response = new HashMap<>();
    response.put("token", token);
    response.put("message", "User registered. Please confirm your email.");
    return ResponseEntity.ok(response);
  }

    @GetMapping(path = "confirm")
    public ResponseEntity<String> confirm(@RequestParam("token") String token) {
        String html = registrationService.confirmToken(token);
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.TEXT_HTML);
        
        return new ResponseEntity<>(html, headers, HttpStatus.OK);
    }

}
