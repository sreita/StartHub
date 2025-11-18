/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

package com.example.demo.registration;

import java.util.function.Predicate;

import org.springframework.stereotype.Service;

/**
 *
 * @author david
 */


@Service

public class EmailValidator implements Predicate<String> {

  @Override
  public boolean test(String email) {
//Para hacer: validar el email

    return true;
  }

}
