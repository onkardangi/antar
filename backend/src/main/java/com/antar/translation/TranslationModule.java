package com.antar.translation;

/**
 * Translation bounded context marker.
 *
 * <p>Owns licensed translation editions and per-Verse translation text. References Scripture Verse
 * identity only. Does not own Sanskrit, commentary, or Reader composition.
 */
public final class TranslationModule {

    private TranslationModule() {
    }
}
