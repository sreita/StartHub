package com.example.demo.appuser;

import java.time.LocalDateTime;
import java.util.Collection;
import java.util.Collections;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Lob;
import jakarta.persistence.Table;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@EqualsAndHashCode
@Entity
@Table(name = "User") // RESPETA la mayúscula
public class AppUser implements UserDetails {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @Column(name = "user_id")
  private int id;

  @Column(name = "first_name", nullable = false, length = 100)
  private String firstName;

  @Column(name = "last_name", nullable = false, length = 100)
  private String lastName;

  @Column(name = "email", nullable = false, unique = true, length = 255)
  private String email;

  @Column(name = "password_hash", nullable = false, length = 255)
  private String password;

  @Column(name = "is_admin")
  private Boolean isAdmin = false;

  @Column(name = "registration_date", insertable = false, updatable = false)
  private LocalDateTime registrationDate;

  @Lob
  @Column(name = "profile_info")
  private String profileInfo;

  @Column(name = "is_locked")
  private Boolean locked = false;

  @Column(name = "is_enabled")
  private Boolean enabled = false;

  // Constructor personalizado PARA REGISTRO
  public AppUser(
    String firstName,
    String lastName,
    String email,
    String password,
    Boolean isAdmin
  ) {
    this.firstName = firstName;
    this.lastName = lastName;
    this.email = email;
    this.password = password;
    this.isAdmin = isAdmin;
  }

  @Override
  public Collection<? extends GrantedAuthority> getAuthorities() {
    String role = isAdmin != null && isAdmin ? "ROLE_ADMIN" : "ROLE_USER";
    return Collections.singletonList(new SimpleGrantedAuthority(role));
  }

  @Override
  public String getUsername() {
    return this.email;
  }

  @Override
  public boolean isAccountNonExpired() {
    return true;
  }

  @Override
  public boolean isAccountNonLocked() {
    // usar el campo locked (defensivo contra null)
    return this.locked == null ? true : !this.locked;
  }

  @Override
  public boolean isCredentialsNonExpired() {
    return true;
  }

  @Override
  public boolean isEnabled() {
    // usar el campo enabled (defensivo contra null)
    return this.enabled != null && this.enabled;
  }
}
