package com.antar.scripture.domain;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class ContentVersionPolicyTest {

    private static final Instant TIMESTAMP = Instant.parse("2026-08-04T00:00:00Z");
    private final ContentVersionPolicy policy = new ContentVersionPolicy();

    @Test
    void allowsFirstImportWhenSanskritAbsent() {
        Verse verse = emptyVerse();
        policy.assertCompatible("pkg-a", checksum('a'), 1, verse);
    }

    @Test
    void rejectsDowngrade() {
        Verse verse = importedVerse("pkg-a", checksum('a'), 2, "FIXTURE_NON_SCRIPTURAL_VERSE_1");
        assertThatThrownBy(() -> policy.assertCompatible("pkg-b", checksum('b'), 1, verse))
                .isInstanceOf(ContentVersionPolicyException.class)
                .extracting(ex -> ((ContentVersionPolicyException) ex).failureCode())
                .isEqualTo(ImportFailureCode.CONTENT_VERSION_DOWNGRADE);
    }

    @Test
    void rejectsSameVersionDifferentPackage() {
        Verse verse = importedVerse("pkg-a", checksum('a'), 1, "FIXTURE_NON_SCRIPTURAL_VERSE_1");
        assertThatThrownBy(() -> policy.assertCompatible("pkg-b", checksum('b'), 1, verse))
                .isInstanceOf(ContentVersionPolicyException.class)
                .extracting(ex -> ((ContentVersionPolicyException) ex).failureCode())
                .isEqualTo(ImportFailureCode.CONTENT_VERSION_CONFLICT);
    }

    @Test
    void allowsSamePackageSameChecksumSameVersion() {
        Verse verse = importedVerse("pkg-a", checksum('a'), 1, "FIXTURE_NON_SCRIPTURAL_VERSE_1");
        policy.assertCompatible("pkg-a", checksum('a'), 1, verse);
    }

    @Test
    void rejectsPackageIdentityConflict() {
        assertThatThrownBy(() ->
                        policy.assertPackageIdentity("pkg-a", checksum('a'), "pkg-a", checksum('b')))
                .isInstanceOf(ContentVersionPolicyException.class)
                .extracting(ex -> ((ContentVersionPolicyException) ex).failureCode())
                .isEqualTo(ImportFailureCode.PACKAGE_IDENTITY_CONFLICT);
    }

    @Test
    void packageLineageUpdatesTogether() {
        Verse updated = emptyVerse()
                .withImportedContent(
                        "FIXTURE_NON_SCRIPTURAL_VERSE_1",
                        2,
                        "pkg-b",
                        checksum('b'),
                        TIMESTAMP);
        assertThat(updated.contentVersion()).isEqualTo(2);
        assertThat(updated.sourcePackageId()).contains("pkg-b");
        assertThat(updated.sourcePackageChecksum()).contains(checksum('b'));
    }

    private static Verse emptyVerse() {
        return Verse.rehydrate(
                VerseId.of(UUID.randomUUID()),
                ChapterId.of(UUID.randomUUID()),
                VerseNumber.of(1),
                CanonicalReference.parse("12.1"),
                null,
                PublicationStatus.PUBLISHED,
                1,
                TIMESTAMP,
                TIMESTAMP);
    }

    private static Verse importedVerse(
            String packageId, String checksum, long version, String text) {
        return emptyVerse().withImportedContent(text, version, packageId, checksum, TIMESTAMP);
    }

    private static String checksum(char fill) {
        return String.valueOf(fill).repeat(64);
    }
}
