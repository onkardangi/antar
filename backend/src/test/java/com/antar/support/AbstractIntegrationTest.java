package com.antar.support;

import java.util.concurrent.atomic.AtomicBoolean;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.utility.DockerImageName;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;

/**
 * Shared Spring Boot integration-test support.
 *
 * <p>PostgreSQL and Redis containers are singleton JVM-scoped resources. They start once on first
 * use and remain running for the entire Surefire JVM so cached Spring contexts never observe
 * recycled ports.
 *
 * <p>Docker is required by default. Concrete infrastructure test classes are annotated with
 * {@link SkipInfrastructureTestsIfRequested}. Developers without Docker may opt out with
 * {@code -Dantar.skipInfrastructureTests=true}. CI must not set that property and must confirm
 * infrastructure tests executed.
 */
@ActiveProfiles("test")
public abstract class AbstractIntegrationTest {

    private static final DockerImageName POSTGRES_IMAGE =
            DockerImageName.parse("pgvector/pgvector:pg16").asCompatibleSubstituteFor("postgres");

    private static final DockerImageName REDIS_IMAGE = DockerImageName.parse("redis:7-alpine");

    private static final AtomicBoolean STARTED = new AtomicBoolean(false);

    static final PostgreSQLContainer POSTGRES = new PostgreSQLContainer(POSTGRES_IMAGE);

    static final GenericContainer<?> REDIS = new GenericContainer<>(REDIS_IMAGE).withExposedPorts(6379);

    private static void ensureInfrastructureStarted() {
        if (!STARTED.compareAndSet(false, true)) {
            return;
        }

        if (!DockerClientFactory.instance().isDockerAvailable()) {
            STARTED.set(false);
            throw new IllegalStateException(
                    "Docker is required for Antar infrastructure tests. "
                            + "Start Docker, or opt out locally with -Dantar.skipInfrastructureTests=true. "
                            + "CI must not skip these tests.");
        }

        try {
            POSTGRES.start();
            REDIS.start();
        } catch (RuntimeException ex) {
            STARTED.set(false);
            throw ex;
        }
    }

    @DynamicPropertySource
    static void registerInfrastructureProperties(DynamicPropertyRegistry registry) {
        ensureInfrastructureStarted();
        registry.add("spring.datasource.url", POSTGRES::getJdbcUrl);
        registry.add("spring.datasource.username", POSTGRES::getUsername);
        registry.add("spring.datasource.password", POSTGRES::getPassword);
        registry.add("spring.data.redis.host", REDIS::getHost);
        registry.add("spring.data.redis.port", () -> REDIS.getMappedPort(6379));
    }
}
