package com.antar.translation.application.imports;

import com.antar.translation.application.port.ResolvedTranslationPackage;
import com.antar.translation.domain.Translation;
import java.util.List;

public interface ImportMutationProbe {

    void afterTranslationsSaved(ResolvedTranslationPackage pkg, List<Translation> updated);
}
