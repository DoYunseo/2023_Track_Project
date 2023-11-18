package com.server.track_project.Entity;

import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long>{
    @EntityGraph(attributePaths = "auth")
    Optional<User> findById(String id);
}
