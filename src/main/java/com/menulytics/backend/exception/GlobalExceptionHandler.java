package com.menulytics.backend.exception;

import com.menulytics.backend.dto.ApiResponse;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public ApiResponse<String> handleException(Exception e) {
        return new ApiResponse<>(
                false,
                "Something went wrong: " + e.getMessage(),
                null
        );
    }
}