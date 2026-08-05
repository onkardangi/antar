package com.antar.translation.application.port;

import java.util.Collection;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

/**
 * Read-only Verse identity lookup. Resolves canonical references to Scripture Verse UUIDs.
 */
public interface VerseIdentityLookup {

    Optional<UUID> findVerseIdByCanonicalReference(String canonicalReference);

    Map<String, UUID> findVerseIdsByCanonicalReferences(Collection<String> canonicalReferences);
}
