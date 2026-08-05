package com.antar.translation.domain;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatCode;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.Test;

class ContentVersionPolicyTest {

    private static final Instant TIMESTAMP = Instant.parse("2026-08-04T00:00:00Z");
    private final ContentVersionPolicy policy = new ContentVersionPolicy();

    @Test
    void allowsFirstImport() {
        Translation existing = base(null, null, 1);
        assertThatCode(() -> policy.assertCompatible(
                        "pkg-v1",
                        checksum('a'),
                        1,
                        existing))
                .doesNotThrowAnyException();
    }

    @Test
    void rejectsDowngrade() {
        Translation existing = base("pkg-v2", checksum('b'), 2);
        assertThatThrownBy(() -> policy.assertCompatible(
                        "pkg-v1",
                        checksum('a'),
                        1,
                        existing))
                .isInstanceOf(ContentVersionPolicyException.class)
                .extracting(ex -> ((ContentVersionPolicyException) ex).failureCode())
                .isEqualTo(ImportFailureCode.CONTENT_VERSION_DOWNGRADE);
    }

    @Test
    void rejectsSameVersionDifferentPackage() {
        Translation existing = base("pkg-a", checksum('a'), 1);
        assertThatThrownBy(() -> policy.assertCompatible(
                        "pkg-b",
                        checksum('b'),
                        1,
                        existing))
                .isInstanceOf(ContentVersionPolicyException.class)
                .extracting(ex -> ((ContentVersionPolicyException) ex).failureCode())
                .isEqualTo(ImportFailureCode.CONTENT_VERSION_CONFLICT);
    }

    @Test
    void allowsSamePackageSameChecksumSameVersion() {
        Translation existing = base("pkg-a", checksum('a'), 1);
        assertThatCode(() -> policy.assertCompatible("pkg-a", checksum('a'), 1, existing))
                .doesNotThrowAnyException();
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
    void rejectsDifferentPackageIdSameChecksum() {
        assertThatThrownBy(() ->
                        policy.assertPackageIdentity("pkg-b", checksum('a'), "pkg-a", checksum('a')))
                .isInstanceOf(ContentVersionPolicyException.class)
                .extracting(ex -> ((ContentVersionPolicyException) ex).failureCode())
                .isEqualTo(ImportFailureCode.PACKAGE_IDENTITY_CONFLICT);
    }

    @Test
    void packageLineageUpdatesTogether() {
        Translation updated = base(null, null, 1)
                .withImportedContent(
                        TranslationText.of("FIXTURE_TRANSLATION_VERSE_1"),
                        TranslationVersion.of(2),
                        "pkg-b",
                        checksum('b'),
                        TIMESTAMP);
        assertThat(updated.contentVersion().value()).isEqualTo(2);
        assertThat(updated.sourcePackageId()).contains("pkg-b");
        assertThat(updated.sourcePackageChecksum()).contains(checksum('b'));
    }

    private static Translation base(String packageId, String checksum, long version) {
        return Translation.rehydrate(
                TranslationId.generate(),
                VerseId.of(UUID.fromString("01900000-0000-7000-8000-000000000001")),
                TranslationSourceId.generate(),
                TranslationLanguage.of("en"),
                TranslationProvider.of("FIXTURE_PROVIDER"),
                TranslationText.of("FIXTURE_TRANSLATION_VERSE_1"),
                TranslationStatus.PUBLISHED,
                TranslationVersion.of(version),
                packageId,
                checksum,
                TIMESTAMP,
                TIMESTAMP);
    }

    private static String checksum(char fill) {
        return String.valueOf(fill).repeat(64);
    }
}
