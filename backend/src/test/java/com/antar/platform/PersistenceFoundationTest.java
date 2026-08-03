package com.antar.platform;

import static org.assertj.core.api.Assertions.assertThat;

import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootTest
@SkipInfrastructureTestsIfRequested
class PersistenceFoundationTest extends AbstractIntegrationTest {

    private static final List<String> EXPECTED_SCHEMAS = List.of(
            "identity",
            "scripture",
            "reading",
            "reflection",
            "guidance",
            "understanding",
            "saar",
            "search",
            "platform");

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Autowired
    private RedisConnectionFactory redisConnectionFactory;

    @Test
    void postgresqlIsReachableAndFlywayCreatedExpectedSchemas() {
        Integer one = jdbcTemplate.queryForObject("SELECT 1", Integer.class);
        assertThat(one).isEqualTo(1);

        List<String> schemas = jdbcTemplate.queryForList(
                """
                SELECT schema_name
                FROM information_schema.schemata
                WHERE schema_name IN (
                    'identity', 'scripture', 'reading', 'reflection',
                    'guidance', 'understanding', 'saar', 'search', 'platform'
                )
                ORDER BY schema_name
                """,
                String.class);

        assertThat(schemas).containsExactlyInAnyOrderElementsOf(EXPECTED_SCHEMAS);

        Boolean vectorInstalled = jdbcTemplate.queryForObject(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM pg_extension
                    WHERE extname = 'vector'
                )
                """,
                Boolean.class);
        assertThat(vectorInstalled).isTrue();

        List<Map<String, Object>> flywayHistory = jdbcTemplate.queryForList(
                """
                SELECT version, success
                FROM flyway_schema_history
                ORDER BY installed_rank
                """);
        assertThat(flywayHistory).isNotEmpty();
        assertThat(flywayHistory.getFirst().get("version").toString()).isIn("1", "001");
        assertThat(flywayHistory.getFirst().get("success")).isEqualTo(true);
    }

    @Test
    void redisIsReachableThroughSpring() {
        try (var connection = redisConnectionFactory.getConnection()) {
            String pong = connection.ping();
            assertThat(pong).isEqualTo("PONG");
        }
    }
}
