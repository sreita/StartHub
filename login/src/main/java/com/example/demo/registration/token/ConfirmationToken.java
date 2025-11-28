/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

package com.example.demo.registration.token;

import java.sql.Types;
import java.time.LocalDateTime;

import org.hibernate.annotations.JdbcTypeCode;

import com.example.demo.appuser.AppUser;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@Entity
@Table(name = "ConfirmationToken")

/**
 *
 * @author david
 */


public class ConfirmationToken {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "token_id")
    @JdbcTypeCode(Types.INTEGER)
    private int id;

    @Column(nullable = false)
    private String token;

    @Column(nullable = false, name = "created_at")
    private LocalDateTime createdAt;

    @Column(nullable = false, name = "expires_at")
    private LocalDateTime expiresAt;

    @Column(name = "confirmed_at")
    private LocalDateTime confirmedAt;


    @ManyToOne
    @JoinColumn(
        nullable = false,
        name = "app_user_id"
    )

    private AppUser appUser;

    public ConfirmationToken(String token,
                            LocalDateTime createdAt,
                            LocalDateTime expiresAt,
                            AppUser appUser) {
        this.token = token;
        this.createdAt = createdAt;
        this.expiresAt = expiresAt;
        this.appUser = appUser;
    }

}
