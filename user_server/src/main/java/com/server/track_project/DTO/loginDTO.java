package com.server.track_project.DTO;

import lombok.*;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class loginDTO {

    @NotNull
    @Size(min = 3, max = 50)
    private String id;

    @NotNull
    @Size(min = 3, max = 100)
    private String password;
}
