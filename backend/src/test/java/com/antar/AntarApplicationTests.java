package com.antar;

import com.antar.support.AbstractIntegrationTest;
import com.antar.support.SkipInfrastructureTestsIfRequested;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
@SkipInfrastructureTestsIfRequested
class AntarApplicationTests extends AbstractIntegrationTest {

    @Test
    void contextLoads() {
    }
}
