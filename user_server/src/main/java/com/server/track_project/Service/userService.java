package com.server.track_project.Service;

import java.util.Collections;

import com.server.track_project.Exception.NotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.server.track_project.DTO.userDTO;
import com.server.track_project.Entity.User;
import com.server.track_project.Entity.Authority;
import com.server.track_project.Entity.UserRepository;
import com.server.track_project.Exception.DuplicateException;


@Service
public class userService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;

    public userService(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Transactional
    public userDTO signUp(userDTO userDTO) {
        if (userRepository.findById(userDTO.getId()).orElse(null) != null) {
            throw new DuplicateException("이미 가입되어 있는 유저입니다.");
        }

        Authority authority = Authority.builder()
                .auth("ROLE_USER")
                .build();

        User user = User.builder()
                .id(userDTO.getId())
                .password(passwordEncoder.encode(userDTO.getPassword()))
                .email(userDTO.getEmail())
                .auth(Collections.singleton(authority))
                .activated(true)
                .build();

        return userDTO.from(userRepository.save(user));
    }

    @Transactional(readOnly = true)
    public userDTO getUser(String id) {
        return userDTO.from(userRepository.findById(id).orElseThrow(() -> new NotFoundException("Member not found")));
    }

}
