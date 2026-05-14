package com.example.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.security.authentication.AbstractAuthenticationToken;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.oauth2.core.DelegatingOAuth2TokenValidator;
import org.springframework.security.oauth2.core.OAuth2TokenValidator;
import org.springframework.security.oauth2.jwt.*;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.oauth2.server.resource.authentication.JwtGrantedAuthoritiesConverter;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.boot.actuate.autoconfigure.security.servlet.EndpointRequest;

/**
 * Hardened SecurityConfig template for a stateless JWT-protected API.
 *
 * Intentional choices:
 *   * Stateless — no JSESSIONID, no server-side session.
 *   * CSRF disabled — no browser-managed credential is used; tokens travel in
 *     the Authorization header. Document the rationale below; do not silently
 *     disable CSRF if cookies are introduced later.
 *   * Algorithm pinned to RS256 — no algorithm negotiation from token headers.
 *   * Explicit audience validation — Spring's defaults validate issuer/exp/nbf
 *     but NOT audience.
 *   * Separate actuator chain — /actuator/health is public for probes; every
 *     other actuator endpoint requires authentication.
 *   * No permitAll on application paths. Public endpoints, if any, must be
 *     enumerated and reviewed individually.
 */
@Configuration
@EnableMethodSecurity
public class SecurityConfig {

    @Value("${security.jwt.issuer-uri}")
    private String issuerUri;

    @Value("${security.jwt.audience}")
    private String expectedAudience;

    // Application API chain — order matters; specific matchers first.
    @Bean
    SecurityFilterChain apiSecurityFilterChain(HttpSecurity http) throws Exception {
        http
            .securityMatcher("/api/**")
            // Stateless API: no session, no CSRF token mechanism.
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .csrf(csrf -> csrf.disable()) // rationale: bearer token in Authorization header, not cookie
            .cors(Customizer.withDefaults()) // configure CorsConfigurationSource elsewhere; never allow * with credentials
            .authorizeHttpRequests(auth -> auth
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(jwt -> jwt
                .decoder(jwtDecoder())
                .jwtAuthenticationConverter(jwtAuthenticationConverter())
            ));
        return http.build();
    }

    // Actuator chain — health is public for probes; everything else authenticated.
    @Bean
    SecurityFilterChain actuatorSecurityFilterChain(HttpSecurity http) throws Exception {
        http
            .securityMatcher(EndpointRequest.toAnyEndpoint())
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(EndpointRequest.to("health")).permitAll()
                .anyRequest().hasAuthority("SCOPE_actuator")
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(jwt -> jwt.decoder(jwtDecoder())));
        return http.build();
    }

    @Bean
    JwtDecoder jwtDecoder() {
        // Pin algorithm explicitly. Do not let the token header pick.
        NimbusJwtDecoder decoder = NimbusJwtDecoder
            .withIssuerLocation(issuerUri)
            .jwsAlgorithm(SignatureAlgorithm.RS256)
            .build();

        OAuth2TokenValidator<Jwt> withIssuer = JwtValidators.createDefaultWithIssuer(issuerUri);
        OAuth2TokenValidator<Jwt> withAudience = new AudienceValidator(expectedAudience);
        decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(withIssuer, withAudience));

        return decoder;
    }

    @Bean
    JwtAuthenticationConverter jwtAuthenticationConverter() {
        JwtGrantedAuthoritiesConverter granted = new JwtGrantedAuthoritiesConverter();
        granted.setAuthorityPrefix("SCOPE_");
        granted.setAuthoritiesClaimName("scope");
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(granted);
        return converter;
    }

    /** Explicit audience validator — Spring does not enforce audience by default. */
    static final class AudienceValidator implements OAuth2TokenValidator<Jwt> {
        private final String expectedAudience;
        AudienceValidator(String expectedAudience) { this.expectedAudience = expectedAudience; }
        @Override
        public org.springframework.security.oauth2.core.OAuth2TokenValidatorResult validate(Jwt jwt) {
            if (jwt.getAudience() != null && jwt.getAudience().contains(expectedAudience)) {
                return org.springframework.security.oauth2.core.OAuth2TokenValidatorResult.success();
            }
            return org.springframework.security.oauth2.core.OAuth2TokenValidatorResult.failure(
                new org.springframework.security.oauth2.core.OAuth2Error(
                    "invalid_token", "Required audience '" + expectedAudience + "' missing", null));
        }
    }
}
