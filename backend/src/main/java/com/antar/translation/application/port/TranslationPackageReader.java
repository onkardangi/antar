package com.antar.translation.application.port;

import java.nio.file.Path;

public interface TranslationPackageReader {

    ResolvedTranslationPackage read(Path packageDirectory);
}
