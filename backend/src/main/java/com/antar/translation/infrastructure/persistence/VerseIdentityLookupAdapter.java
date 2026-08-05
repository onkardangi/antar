package com.antar.translation.infrastructure.persistence;

import com.antar.translation.application.port.VerseIdentityLookup;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

/**
 * Read-only Verse identity resolution against scripture.verses. No Scripture module dependency.
 */
@Component
class VerseIdentityLookupAdapter implements VerseIdentityLookup {

    private final JdbcTemplate jdbcTemplate;

    VerseIdentityLookupAdapter(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public Optional<UUID> findVerseIdByCanonicalReference(String canonicalReference) {
        List<UUID> rows = jdbcTemplate.query(
                "SELECT id FROM scripture.verses WHERE canonical_reference = ?",
                (rs, rowNum) -> (UUID) rs.getObject("id"),
                canonicalReference);
        return rows.stream().findFirst();
    }

    @Override
    public Map<String, UUID> findVerseIdsByCanonicalReferences(Collection<String> canonicalReferences) {
        if (canonicalReferences == null || canonicalReferences.isEmpty()) {
            return Map.of();
        }
        List<String> refs = List.copyOf(canonicalReferences);
        String placeholders = String.join(",", Collections.nCopies(refs.size(), "?"));
        String sql = "SELECT canonical_reference, id FROM scripture.verses WHERE canonical_reference IN ("
                + placeholders + ")";
        Map<String, UUID> result = new HashMap<>();
        jdbcTemplate.query(sql, rs -> {
            result.put(rs.getString("canonical_reference"), (UUID) rs.getObject("id"));
        }, refs.toArray());
        return Map.copyOf(result);
    }
}
