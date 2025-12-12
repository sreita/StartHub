package com.example.demo.security.config;

import java.io.IOException;
import java.util.Arrays;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Lazy;
import org.springframework.http.HttpStatus;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import com.example.demo.appuser.AppUserService;
import com.example.demo.security.jwt.JwtAuthFilter;
import com.example.demo.security.jwt.JwtService;
import com.fasterxml.jackson.databind.ObjectMapper;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

  private final AppUserService appUserService;
  private final BCryptPasswordEncoder bCryptPasswordEncoder;
  private final JwtService jwtService;

  // Inyectamos el filtro como un campo para romper la dependencia circular
  @Autowired
  @Lazy
  private JwtAuthFilter jwtAuthFilter;

  public SecurityConfig(
    AppUserService appUserService,
    BCryptPasswordEncoder bCryptPasswordEncoder,
    JwtService jwtService
  ) {
    this.appUserService = appUserService;
    this.bCryptPasswordEncoder = bCryptPasswordEncoder;
    this.jwtService = jwtService;
  }

  @Bean
  public UserDetailsService userDetailsService() {
    return appUserService;
  }

  @Bean
  public SecurityFilterChain securityFilterChain(HttpSecurity http)
    throws Exception {
    http
      .csrf(csrf -> csrf.disable()) // Deshabilitar CSRF para APIs stateless
      .cors(cors -> cors.configurationSource(corsConfigurationSource()))
      .authorizeHttpRequests(auth ->
        auth
          // Endpoints públicos: login, registro y la UI de thymeleaf
          .requestMatchers("/api/v1/auth/**")
          .permitAll()
          .requestMatchers("/api/v1/registration", "/api/v1/registration/**")
          .permitAll()
          .requestMatchers("/api/v1/startups")
          .permitAll() // Permitir listar startups
          .requestMatchers("/api/v1/startups/{id}")
          .permitAll() // Permitir ver detalles
          .requestMatchers("/startup_info.html")
          .permitAll() // Permitir acceso a la página de detalles
          .requestMatchers(
            "/",
            "/login",
            "/signup",
            "/req/**",
            "/home",
            "/css/**",
            "/js/**",
            "/process-login"
          )
          .permitAll()
          .requestMatchers("/reset-password")
          .permitAll()
          .requestMatchers("/forgot-password")
          .permitAll()
          // Endpoints protegidos
          .requestMatchers("/api/v1/users/**")
          .authenticated()
          .requestMatchers("/startup_form.html")
          .authenticated()
          .requestMatchers("/profile.html")
          .authenticated()
          // Permitir el resto de peticiones
          .anyRequest()
          .permitAll()
      )
      // Deshabilitar formLogin para usar solo JWT en APIs
      // .formLogin(form -> ...)
      .logout(logout -> logout.permitAll())
      .sessionManagement(session ->
        session
          // Usar política STATELESS
          .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
      )
      .authenticationProvider(authenticationProvider())
      // Añadir nuestro filtro de JWT antes del filtro de autenticación estándar
      .addFilterBefore(
        jwtAuthFilter,
        UsernamePasswordAuthenticationFilter.class
      )
      .exceptionHandling(exception ->
        exception
          // Para rutas protegidas sin autenticación, devolver 401
          .authenticationEntryPoint(
            (request, response, authException) -> {
              // Si es una petición a API, devolver JSON con 401
              if (request.getRequestURI().startsWith("/api/")) {
                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                response.setContentType("application/json");
                response.getWriter().write("{\"error\":\"Unauthorized\",\"message\":\"" + authException.getMessage() + "\"}");
              } else {
                // Para rutas de UI, redirigir a login
                response.sendRedirect("/login");
              }
            }
          )
      );

    return http.build();
  }

  @Bean
  public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration configuration = new CorsConfiguration();
    configuration.setAllowedOriginPatterns(
      Arrays.asList(
        "http://localhost:*",
        "http://127.0.0.1:*",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000"
      )
    );
    configuration.setAllowedMethods(
      Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS")
    );
    configuration.setAllowedHeaders(Arrays.asList("*"));
    configuration.setAllowCredentials(true);

    UrlBasedCorsConfigurationSource source =
      new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", configuration);
    return source;
  }

  @Bean
  public AuthenticationProvider authenticationProvider() {
    DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
    authProvider.setUserDetailsService(userDetailsService());
    authProvider.setPasswordEncoder(bCryptPasswordEncoder);
    return authProvider;
  }

  @Bean
  public AuthenticationManager authenticationManager(
    AuthenticationConfiguration config
  ) throws Exception {
    return config.getAuthenticationManager();
  }

  // --- New Code for JWT Authentication Success Handler (Se mantiene igual) ---
  private static class JwtAuthenticationSuccessHandler
    implements AuthenticationSuccessHandler {

    private final JwtService jwtService;
    private final AppUserService appUserService;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public JwtAuthenticationSuccessHandler(
      JwtService jwtService,
      AppUserService appUserService
    ) {
      this.jwtService = jwtService;
      this.appUserService = appUserService;
    }

    @Override
    public void onAuthenticationSuccess(
      HttpServletRequest request,
      HttpServletResponse response,
      Authentication authentication
    ) throws IOException, ServletException {
      UserDetails userDetails = (UserDetails) authentication.getPrincipal();
      String jwt = jwtService.generateToken(userDetails);

      response.setStatus(HttpStatus.OK.value());
      response.setContentType("application/json");
      objectMapper.writeValue(
        response.getWriter(),
        java.util.Collections.singletonMap("token", jwt)
      );
    }
  }
}
