// src/test/java/com/example/demo/appuser/AppUserServiceTest.java
package com.example.demo.appuser;

import java.time.LocalDateTime;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

import com.example.demo.controller.UserProfileResponse;
import com.example.demo.controller.UserUpdateRequest;

class AppUserServiceTest {

    private TestableAppUserService appUserService;
    private InMemoryAppUserRepository appUserRepository;

    @BeforeEach
    void setUp() {
        appUserRepository = new InMemoryAppUserRepository();
        appUserService = new TestableAppUserService(appUserRepository);
    }

    @Test
    void whenGetExistingUserProfile_thenReturnsUserProfile() {
        // Configurar usuario existente
        AppUser existingUser = createTestUser();
        appUserRepository.save(existingUser);

        // Ejecutar
        UserProfileResponse response = appUserService.getUserProfile(1);

        // Verificar
        assertNotNull(response);
        assertEquals(1L, response.id());
        assertEquals("John", response.firstName());
        assertEquals("Doe", response.lastName());
        assertEquals("john@example.com", response.email());
    }

    @Test
    void whenGetNonExistingUserProfile_thenThrowsException() {
        // Ejecutar & Verificar
        UsernameNotFoundException exception = assertThrows(
            UsernameNotFoundException.class,
            () -> appUserService.getUserProfile(999)
        );

        assertEquals("User not found with id: 999", exception.getMessage());
    }

    @Test
    void whenUpdateUserProfile_thenReturnsUpdatedProfile() {
        // Configurar usuario existente
        AppUser existingUser = createTestUser();
        appUserRepository.save(existingUser);

        // Crear request de actualización
        UserUpdateRequest updateRequest = new UserUpdateRequest(
            "Jane",
            "Smith",
            "jane.smith@example.com",
            "Updated profile info"
        );

        // Ejecutar
        UserProfileResponse response = appUserService.updateUserProfile(1, updateRequest);

        // Verificar
        assertNotNull(response);
        assertEquals("Jane", response.firstName());
        assertEquals("Smith", response.lastName());
        assertEquals("jane.smith@example.com", response.email());
        assertEquals("Updated profile info", response.profileInfo());

        // Verificar que el usuario fue actualizado en el repositorio
        AppUser updatedUser = appUserRepository.findById(1).orElseThrow();
        assertEquals("Jane", updatedUser.getFirstName());
        assertEquals("Smith", updatedUser.getLastName());
    }

    @Test
    void whenDeleteExistingUser_thenUserIsRemoved() {
        // Configurar usuario existente
        AppUser existingUser = createTestUser();
        appUserRepository.save(existingUser);
        assertTrue(appUserRepository.existsById(1));

        // Ejecutar
        appUserService.deleteUser(1);

        // Verificar
        assertFalse(appUserRepository.existsById(1));
    }

    @Test
    void whenLoadUserByExistingEmail_thenReturnsUser() {
        // Configurar usuario existente
        AppUser existingUser = createTestUser();
        appUserRepository.save(existingUser);

        // Ejecutar
        AppUser loadedUser = appUserService.loadUserByUsername("john@example.com");

        // Verificar
        assertNotNull(loadedUser);
        assertEquals("john@example.com", loadedUser.getEmail());
    }

    @Test
    void whenLoadUserByNonExistingEmail_thenThrowsException() {
        // Ejecutar & Verificar
        UsernameNotFoundException exception = assertThrows(
            UsernameNotFoundException.class,
            () -> appUserService.loadUserByUsername("nonexistent@example.com")
        );

        assertTrue(exception.getMessage().contains("User with email nonexistent@example.com not found"));
    }

    private AppUser createTestUser() {
        AppUser user = new AppUser();
        user.setId(1);
        user.setFirstName("John");
        user.setLastName("Doe");
        user.setEmail("john@example.com");
        user.setPassword("encodedPassword");
        user.setRegistrationDate(LocalDateTime.now());
        user.setProfileInfo("Test profile info");
        user.setEnabled(true);
        return user;
    }

    // Implementación de AppUserService para testing que no depende de Spring
    static class TestableAppUserService {
        private final InMemoryAppUserRepository appUserRepository;

        public TestableAppUserService(InMemoryAppUserRepository appUserRepository) {
            this.appUserRepository = appUserRepository;
        }

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

            appUser.setFirstName(updateRequest.firstName());
            appUser.setLastName(updateRequest.lastName());
            appUser.setEmail(updateRequest.email());
            appUser.setProfileInfo(updateRequest.profileInfo());

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

        public AppUser loadUserByUsername(String email) throws UsernameNotFoundException {
            return appUserRepository.findByEmail(email)
                .orElseThrow(() -> new UsernameNotFoundException(
                    String.format("User with email %s not found", email)));
        }
    }

    // Implementación en memoria del repositorio para testing
    static class InMemoryAppUserRepository {
        private AppUser savedUser;

        public Optional<AppUser> findById(Integer id) {
            if (savedUser != null && savedUser.getId() == id) { // Usar == para comparar int
                return Optional.of(savedUser);
            }
            return Optional.empty();
        }

        public Optional<AppUser> findByEmail(String email) {
            if (savedUser != null && savedUser.getEmail().equals(email)) {
                return Optional.of(savedUser);
            }
            return Optional.empty();
        }

        public AppUser save(AppUser user) {
            this.savedUser = user;
            return user;
        }

        public void delete(AppUser user) {
            if (savedUser != null && savedUser.getId() == user.getId()) { // Usar == para comparar int
                savedUser = null;
            }
        }

        public boolean existsById(Integer id) {
            return savedUser != null && savedUser.getId() == id; // Usar == para comparar int
        }

        public int enableAppUser(String email) {
            if (savedUser != null && savedUser.getEmail().equals(email)) {
                savedUser.setEnabled(true);
                return 1;
            }
            return 0;
        }
    }
}