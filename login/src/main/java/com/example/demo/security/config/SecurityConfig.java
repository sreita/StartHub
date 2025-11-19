package com.example.demo.security.config;

import org.springframework.boot.autoconfigure.security.servlet.PathRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

import com.example.demo.appuser.AppUserService;

import lombok.RequiredArgsConstructor;

@Configuration
@EnableWebSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final AppUserService appUserService;
    private final BCryptPasswordEncoder bCryptPasswordEncoder;

    @Bean
    public UserDetailsService userDetailsService() {
        return appUserService;
    }

    @Bean
    public AuthenticationProvider authenticationProvider(UserDetailsService userDetailsService) {
        DaoAuthenticationProvider provider = new DaoAuthenticationProvider();
        provider.setUserDetailsService(userDetailsService);
        provider.setPasswordEncoder(bCryptPasswordEncoder);
        return provider;
    }

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {

        http.csrf(AbstractHttpConfigurer::disable);

        http.formLogin(login -> {
            login.loginPage("/req/login").permitAll();
            login.loginProcessingUrl("/process-login");
            // ➡️ CAMBIO CLAVE 1: Usar una ruta protegida después del éxito, o usar la ruta correcta.
            // Si el index es la página de bienvenida, debería ser accesible a todos.
            // Si /index es tu dashboard, usa /dashboard (y deja que .anyRequest().authenticated() lo proteja).
            login.defaultSuccessUrl("/home", true); // Cambio a /home o /dashboard (si es protegida)
        });

        http.authorizeHttpRequests(auth -> {
            auth
                // RUTAS DE RECURSOS ESTÁTICOS Y PÚBLICAS
                .requestMatchers(PathRequest.toStaticResources().atCommonLocations()).permitAll()
                .requestMatchers("/css/**", "/js/**", "/images/**", "/webjars/**").permitAll()

                // RUTAS PÚBLICAS DE VISTAS (LOGIN, SIGNUP)
                .requestMatchers("/", "/index").permitAll() // Hacemos que la raíz y el index sean accesibles
                .requestMatchers("/req/**").permitAll()
                .requestMatchers("/login", "/signup").permitAll()
                .requestMatchers("/req/success").permitAll()
                .requestMatchers("/home").permitAll()

                // RUTAS PÚBLICAS DE API (REGISTRO Y PROCESAMIENTO)
                .requestMatchers("/api/v1/registration/**").permitAll()
                .requestMatchers("/process-login").permitAll() // La URL de procesamiento de login debe ser permitida

                // CUALQUIER OTRA RUTA (DASHBOARD) REQUIERE AUTENTICACIÓN
                .anyRequest().authenticated();
        });

        return http.build();
    }
}