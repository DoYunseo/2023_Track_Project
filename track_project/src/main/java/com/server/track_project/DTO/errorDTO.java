package com.server.track_project.DTO;

import java.util.ArrayList;
import java.util.List;
import org.springframework.validation.FieldError;

public class errorDTO {

    private final int status;
    private final String message;
    private List<FieldError> fieldErrors = new ArrayList<>();

    public errorDTO(int status, String message) {
        this.status = status;
        this.message = message;
    }

    public int getStatus() {
        return status;
    }

    public String getMessage() {
        return message;
    }

    public void addFieldError(String objectName, String path, String message) {
        FieldError error = new FieldError(objectName, path, message);
        fieldErrors.add(error);
    }

    public List<FieldError> getFieldErrors() {
        return fieldErrors;
    }
}
