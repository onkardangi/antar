package com.antar.architecture;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.classes;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

/**
 * Non-vacuous architecture checks for module markers and package ownership.
 *
 * <p>Scripture now contains real layer packages and is excluded from marker-only roots.
 */
@AnalyzeClasses(packages = "com.antar", importOptions = ImportOption.DoNotIncludeTests.class)
class ModuleStructureTest {

    private static final String[] MARKER_ONLY_MODULE_ROOTS = {
        "com.antar.identity",
        "com.antar.reading",
        "com.antar.reflection",
        "com.antar.journey",
        "com.antar.guidance",
        "com.antar.understanding",
        "com.antar.saar",
        "com.antar.search",
        "com.antar.shared"
    };

    @ArchTest
    static final ArchRule moduleMarkerClassesFollowNamingAndPackageConvention =
            classes()
                    .that().haveSimpleNameEndingWith("Module")
                    .should()
                    .resideInAPackage(
                            "com.antar.(identity|scripture|reading|reflection|journey|guidance|understanding|saar|search|platform|shared)")
                    .andShould()
                    .beTopLevelClasses()
                    .because("each bounded context exposes exactly one *Module marker in its root package");

    @ArchTest
    static final ArchRule markerOnlyModulesContainOnlyModuleClasses =
            classes()
                    .that().resideInAnyPackage(MARKER_ONLY_MODULE_ROOTS)
                    .should().haveSimpleNameEndingWith("Module")
                    .because("unstarted business modules contain only marker classes until their vertical slice begins");

    @ArchTest
    static final ArchRule foundationEndpointBelongsToPlatformInternalApi =
            classes()
                    .that().haveSimpleName("FoundationStatusController")
                    .or().haveSimpleName("FoundationStatusResponse")
                    .should().resideInAPackage("com.antar.platform.api.internal")
                    .because("the temporary foundation probe belongs to Platform, not a business module");

    @ArchTest
    static final ArchRule markerOnlyModulesDoNotDependOnPlatformApi =
            noClasses()
                    .that().resideInAnyPackage(MARKER_ONLY_MODULE_ROOTS)
                    .should().dependOnClassesThat().resideInAPackage("com.antar.platform.api..")
                    .because("marker-only modules must not depend on Platform HTTP types");

    @ArchTest
    static final ArchRule scriptureJpaEntitiesRemainInInfrastructurePersistence =
            classes()
                    .that().resideInAPackage("com.antar.scripture..")
                    .and().areAnnotatedWith(jakarta.persistence.Entity.class)
                    .should().resideInAPackage("com.antar.scripture.infrastructure.persistence..")
                    .because("JPA entities must remain inside Scripture infrastructure persistence");

    @ArchTest
    static final ArchRule scriptureApiMustNotDependOnJpaEntities =
            noClasses()
                    .that().resideInAPackage("com.antar.scripture.api..")
                    .should().dependOnClassesThat()
                    .resideInAPackage("com.antar.scripture.infrastructure.persistence..")
                    .because("Scripture API must not expose or depend on persistence types");

    @ArchTest
    static final ArchRule scriptureControllersMustNotDependOnRepositories =
            noClasses()
                    .that().resideInAPackage("com.antar.scripture.api..")
                    .and().haveSimpleNameEndingWith("Controller")
                    .should().dependOnClassesThat().haveSimpleNameEndingWith("Repository")
                    .because(
                            "Scripture controllers must call application query services,"
                                    + " never repositories directly");

    @ArchTest
    static final ArchRule scriptureApplicationMustNotDependOnInfrastructure =
            noClasses()
                    .that().resideInAPackage("com.antar.scripture.application..")
                    .should().dependOnClassesThat()
                    .resideInAPackage("com.antar.scripture.infrastructure..")
                    .because("Scripture application use cases must use ports, not infrastructure adapters");

    @ArchTest
    static final ArchRule scriptureDomainMustNotDependOnApplication =
            noClasses()
                    .that().resideInAPackage("com.antar.scripture.domain..")
                    .should().dependOnClassesThat()
                    .resideInAPackage("com.antar.scripture.application..")
                    .because("Scripture domain must not depend on application use cases");

    @ArchTest
    static final ArchRule scriptureImportCliMustNotDependOnJpaRepositories =
            noClasses()
                    .that().resideInAPackage("com.antar.scripture.infrastructure.importcmd..")
                    .should().dependOnClassesThat()
                    .resideInAPackage("com.antar.scripture.infrastructure.persistence..")
                    .because("import CLI must orchestrate through the application use case only");

    @ArchTest
    static final ArchRule scriptureApiMustNotContainImportOrIngestTypes =
            classes()
                    .that()
                    .resideInAPackage("com.antar.scripture.api..")
                    .should()
                    .haveSimpleNameNotContaining("Import")
                    .andShould()
                    .haveSimpleNameNotContaining("Ingest")
                    .andShould()
                    .haveSimpleNameNotContaining("PackageLoad")
                    .because("Scripture Reader API must not expose package import/ingestion types");
}
