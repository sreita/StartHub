/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

package com.example.demo.registration.token;

import java.time.LocalDateTime;
import java.util.Optional;

import org.springframework.stereotype.Service;

import lombok.AllArgsConstructor;

/**
 *
 * @author david
 */

@Service
@AllArgsConstructor
public class ConfirmationTokenService {

  private final ConfirmationTokenRepository confirmationTokenRepository;

  public void saveConfirmationToken(ConfirmationToken token) {
      confirmationTokenRepository.save(token);
  }

  public Optional<ConfirmationToken> getToken(String token) {
      return confirmationTokenRepository.findByToken(token);
  }

  public void setConfirmedAt(String token) {
      confirmationTokenRepository.updateConfirmedAt(
token, LocalDateTime.now());
  }

}
