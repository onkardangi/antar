package com.antar.platform.api.internal;

import org.springframework.context.annotation.Profile;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Temporary operational connectivity probe for local and test foundation validation.
 *
 * <p>Not a product API. Enabled only for {@code local} and {@code test} profiles. Do not rely on
 * this endpoint in staging or production workflows.
 */
@RestController
@RequestMapping("/api/internal/foundation")
@Profile({"local", "test"})
class FoundationStatusController {

    @GetMapping("/status")
    ResponseEntity<FoundationStatusResponse> status() {
        return ResponseEntity.ok(new FoundationStatusResponse("UP", "antar-backend"));
    }
}
