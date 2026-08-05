package com.antar.architecture;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;
import java.util.List;

@AnalyzeClasses(packages = "com.antar", importOptions = ImportOption.DoNotIncludeTests.class)
class ModuleDependencyTest {

    private static final List<String> MODULES = List.of(
            "identity",
            "scripture",
            "translation",
            "reading",
            "reflection",
            "journey",
            "guidance",
            "understanding",
            "saar",
            "search",
            "platform",
            "shared");

    @ArchTest
    static final ArchRule identityMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("identity");

    @ArchTest
    static final ArchRule scriptureMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("scripture");

    @ArchTest
    static final ArchRule translationMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("translation");

    @ArchTest
    static final ArchRule readingMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("reading");

    @ArchTest
    static final ArchRule reflectionMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("reflection");

    @ArchTest
    static final ArchRule journeyMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("journey");

    @ArchTest
    static final ArchRule guidanceMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("guidance");

    @ArchTest
    static final ArchRule understandingMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("understanding");

    @ArchTest
    static final ArchRule saarMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("saar");

    @ArchTest
    static final ArchRule searchMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("search");

    @ArchTest
    static final ArchRule platformMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("platform");

    @ArchTest
    static final ArchRule sharedMustNotDependOnForeignInfrastructure =
            forbidForeignInfrastructure("shared");

    @ArchTest
    static final ArchRule platformMustNotDependOnScripture =
            noClasses()
                    .that().resideInAPackage("com.antar.platform..")
                    .should().dependOnClassesThat().resideInAPackage("com.antar.scripture..")
                    .because("Platform must not depend on Scripture business types");

    @ArchTest
    static final ArchRule scriptureMustNotDependOnTranslation =
            noClasses()
                    .that().resideInAPackage("com.antar.scripture..")
                    .should().dependOnClassesThat().resideInAPackage("com.antar.translation..")
                    .because("Scripture must not depend on Translation");

    private static ArchRule forbidForeignInfrastructure(String module) {
        String[] otherInfrastructure = MODULES.stream()
                .filter(other -> !other.equals(module))
                .map(other -> "com.antar." + other + ".infrastructure..")
                .toArray(String[]::new);

        return noClasses()
                .that().resideInAPackage("com.antar." + module + "..")
                .should().dependOnClassesThat().resideInAnyPackage(otherInfrastructure)
                .because(module + " must not depend on another module's infrastructure package");
    }
}
