package com.server.track_project.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Email;
import lombok.*;
import com.server.track_project.Entity.User;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.util.Set;
import java.util.stream.Collectors;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class userDTO {

    @NotNull
    @Size(min = 3, max = 50)
    private String id;

    @JsonProperty(access = JsonProperty.Access.WRITE_ONLY)
    @NotNull
    @Size(min = 3, max = 100)
    private String password;

    @NotNull
    @Email
    private String email;

    private Set<authDTO> authDTOSet;

    public static userDTO from(User user) {
        if (user == null)
            return null;

        return userDTO.builder()
                .id(user.getId())
                .email(user.getEmail())
                .authDTOSet(user.getAuth().stream()
                        .map(authority -> authDTO.builder().auth(authority.getAuth()).build())
                        .collect(Collectors.toSet()))
                .build();
    }

}
