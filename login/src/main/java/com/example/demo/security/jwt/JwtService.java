package com.example.demo.security.jwt;

import java.io.InputStream;
import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Date;
import java.util.function.Function;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.io.Decoders;
import jakarta.annotation.PostConstruct;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Service
public class JwtService {

    private PrivateKey privateKey;
    private PublicKey publicKey;

    @PostConstruct
    public void init() {
        try {
            privateKey = loadPrivateKey();
            publicKey = loadPublicKey();
            log.info("Claves RSA cargadas correctamente.");
        } catch (Exception e) {
            log.error("Error al cargar las claves RSA", e);
            throw new RuntimeException("No se pudieron cargar las claves RSA, la aplicación no puede iniciar.", e);
        }
    }

    private PrivateKey loadPrivateKey() throws Exception {
        try (InputStream stream = getClass().getClassLoader().getResourceAsStream("certs/private.pem")) {
            if (stream == null) {
                throw new RuntimeException("No se encontró el archivo de clave privada: certs/private.pem");
            }
            byte[] keyBytes = stream.readAllBytes();
            String privateKeyPEM = new String(keyBytes)
                .replace("-----BEGIN PRIVATE KEY-----", "")
                .replace("-----END PRIVATE KEY-----", "")
                .replaceAll("\\s", "");
            
            byte[] decodedKey = Decoders.BASE64.decode(privateKeyPEM);
            
            PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(decodedKey);
            KeyFactory kf = KeyFactory.getInstance("RSA");
            return kf.generatePrivate(keySpec);
        }
    }

    private PublicKey loadPublicKey() throws Exception {
        try (InputStream stream = getClass().getClassLoader().getResourceAsStream("certs/public.pem")) {
            if (stream == null) {
                throw new RuntimeException("No se encontró el archivo de clave pública: certs/public.pem");
            }
            byte[] keyBytes = stream.readAllBytes();
            String publicKeyPEM = new String(keyBytes)
                .replace("-----BEGIN PUBLIC KEY-----", "")
                .replace("-----END PUBLIC KEY-----", "")
                .replaceAll("\\s", "");

            byte[] decodedKey = Decoders.BASE64.decode(publicKeyPEM);

            X509EncodedKeySpec keySpec = new X509EncodedKeySpec(decodedKey);
            KeyFactory kf = KeyFactory.getInstance("RSA");
            return kf.generatePublic(keySpec);
        }
    }

    public String generateToken(UserDetails userDetails) {
        long now = System.currentTimeMillis();
        long validityInMs = 3600 * 1000; // 1 hora

        return Jwts.builder()
                .subject(userDetails.getUsername())
                .issuedAt(new Date(now))
                .expiration(new Date(now + validityInMs))
                .signWith(privateKey, Jwts.SIG.RS256)
                .compact();
    }

    public boolean isTokenValid(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return (username.equals(userDetails.getUsername())) && !isTokenExpired(token);
    }

    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    private boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    private Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }

    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    private Claims extractAllClaims(String token) {
        return Jwts.parser()
                .verifyWith(publicKey)
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }
}
