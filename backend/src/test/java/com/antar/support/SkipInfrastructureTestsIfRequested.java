package com.antar.support;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.junit.jupiter.api.condition.DisabledIfSystemProperty;

/**
 * Disables Docker-backed infrastructure tests when developers explicitly opt out.
 *
 * <p>CI must not set {@code antar.skipInfrastructureTests=true}.
 */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@DisabledIfSystemProperty(
        named = "antar.skipInfrastructureTests",
        matches = "true",
        disabledReason = "Skipped because antar.skipInfrastructureTests=true")
public @interface SkipInfrastructureTestsIfRequested {
}
