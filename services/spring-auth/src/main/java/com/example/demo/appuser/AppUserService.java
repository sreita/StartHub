package com.example.demo.appuser;

import java.time.LocalDateTime;
import java.util.UUID;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import com.example.demo.controller.UserProfileResponse;
import com.example.demo.controller.UserUpdateRequest;
import com.example.demo.registration.token.ConfirmationToken;
import com.example.demo.registration.token.ConfirmationTokenService;

import jakarta.transaction.Transactional;
import lombok.AllArgsConstructor;


@Service
@AllArgsConstructor

public class AppUserService implements UserDetailsService {

  private final static String USER_NOT_FOUND_MSG = "User with email %s not found";
  private final AppUserRepository appUserRepository;
  private final BCryptPasswordEncoder bCryptPasswordEncoder;
  private final ConfirmationTokenService confirmationTokenService;


  public UserProfileResponse getUserProfile(Integer id) {
        AppUser appUser = appUserRepository.findById(id)
                .orElseThrow(() -> new UsernameNotFoundException("User not found with id: " + id));

        return new UserProfileResponse(
                (long) appUser.getId(),
                appUser.getFirstName(),
                appUser.getLastName(),
                appUser.getEmail(),
                appUser.getRegistrationDate(),
                appUser.getProfileInfo()
        );
    }

    public UserProfileResponse updateUserProfile(Integer id, UserUpdateRequest updateRequest) {
        AppUser appUser = appUserRepository.findById(id)
                .orElseThrow(() -> new UsernameNotFoundException("User not found with id: " + id));

        if (updateRequest.firstName() != null && !updateRequest.firstName().isEmpty()) {
            appUser.setFirstName(updateRequest.firstName());
        }
        if (updateRequest.lastName() != null && !updateRequest.lastName().isEmpty()) {
            appUser.setLastName(updateRequest.lastName());
        }
        if (updateRequest.profileInfo() != null && !updateRequest.profileInfo().isEmpty()) {
            appUser.setProfileInfo(updateRequest.profileInfo());
        }
        // Email no se actualiza en este endpoint ya que requiere revalidación

        appUserRepository.save(appUser);

        return new UserProfileResponse(
                (long) appUser.getId(),
                appUser.getFirstName(),
                appUser.getLastName(),
                appUser.getEmail(),
                appUser.getRegistrationDate(),
                appUser.getProfileInfo()
        );
    }

    public void deleteUser(Integer id) {
        AppUser appUser = appUserRepository.findById(id)
                .orElseThrow(() -> new UsernameNotFoundException("User not found with id: " + id));
        appUserRepository.delete(appUser);
    }

  @Override
  public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
    return appUserRepository.findByEmail(email)
        .orElseThrow(() -> new UsernameNotFoundException(
            String.format(USER_NOT_FOUND_MSG, email)));
  }


  @Transactional
  public String signUpUser(AppUser appUser) {
    var optionalAppUser = appUserRepository
        .findByEmail(appUser.getEmail())
        ;

    if (optionalAppUser.isPresent()) {
    // TODO check of attributes are the same and
    // TODO if email not confirmed send confirmation email
      AppUser existingAppUser = optionalAppUser.get();

      if (existingAppUser.getEnabled()) {
        throw new IllegalStateException("email already taken");
      }

      String token = UUID.randomUUID().toString();
    ConfirmationToken confirmationToken = new ConfirmationToken(
        token,
        LocalDateTime.now(),
        LocalDateTime.now().plusMinutes(15),
        existingAppUser
    );
    confirmationTokenService.saveConfirmationToken(confirmationToken);
    return token;


    }
    String encodedPassword = bCryptPasswordEncoder
        .encode(appUser.getPassword());

    appUser.setPassword(encodedPassword);

    appUserRepository.save(appUser);

    String token = UUID.randomUUID().toString();
    ConfirmationToken confirmationToken = new ConfirmationToken(
        token,
        LocalDateTime.now(),
        LocalDateTime.now().plusMinutes(15),
        appUser
    );
    confirmationTokenService.saveConfirmationToken(confirmationToken);

    //todo: send email
    return  token;


  }


    public int enableAppUser(String email) {
        return appUserRepository.enableAppUser(email);
    }

}
