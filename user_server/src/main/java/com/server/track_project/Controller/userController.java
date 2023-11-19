package com.server.track_project.Controller;

import com.server.track_project.DTO.userDTO;
import com.server.track_project.Service.userService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;

@RestController
@RequestMapping("/user/*")
public class userController {

    private final userService userService;

    public userController(userService userService) {
        this.userService = userService;
    }

    @PostMapping("/signUp")
    public ResponseEntity<userDTO> signUp(@Valid @RequestBody userDTO userDTO) {
        return ResponseEntity.ok(userService.signUp(userDTO));
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('USER', 'ADMIN')")
    public ResponseEntity<userDTO> getUserInfo(@PathVariable String id) {
        return ResponseEntity.ok(userService.getUser(id));
    }

}
