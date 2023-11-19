package com.server.track_project.Config;

import com.server.track_project.Jwt.JwtTokenProvider;
import com.server.track_project.Jwt.JwtSecurityConfig;
import com.server.track_project.Jwt.JwtAuthEntryPoint;
import com.server.track_project.Jwt.JwtAccessDeniedHandler;
import org.springframework.boot.autoconfigure.security.servlet.PathRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.header.writers.frameoptions.XFrameOptionsHeaderWriter;
import org.springframework.security.web.util.matcher.AntPathRequestMatcher;

@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class securityConfig {

    private final JwtTokenProvider jwtTokenProvider;
    private final JwtAuthEntryPoint jwtAuthEntryPoint;
    private final JwtAccessDeniedHandler jwtAccessDeniedHandler;

    public securityConfig(
            JwtTokenProvider jwtTokenProvider,
            JwtAuthEntryPoint jwtAuthEntryPoint,
            JwtAccessDeniedHandler jwtAccessDeniedHandler
    ) {
        this.jwtTokenProvider = jwtTokenProvider;
        this.jwtAuthEntryPoint = jwtAuthEntryPoint;
        this.jwtAccessDeniedHandler = jwtAccessDeniedHandler;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf ->
                        csrf
                                .ignoringRequestMatchers(new AntPathRequestMatcher("/h2-console/**"))
                                .disable()
                )
                .exceptionHandling(ex ->
                        ex
                                .accessDeniedHandler(jwtAccessDeniedHandler)
                                .authenticationEntryPoint(jwtAuthEntryPoint)
                )
                .sessionManagement(session ->
                        session
                                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                )
                .authorizeHttpRequests((auth) ->
                        auth
                                .requestMatchers(new AntPathRequestMatcher("/**")).permitAll()
                                .requestMatchers(PathRequest.toH2Console()).permitAll()
                )
                .headers(head ->
                        head
                                .addHeaderWriter(new XFrameOptionsHeaderWriter(
                                        XFrameOptionsHeaderWriter.XFrameOptionsMode.SAMEORIGIN))
                )
                .apply(new JwtSecurityConfig(jwtTokenProvider));

        return http.build();
    }

    @Bean
    public BCryptPasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }


}
