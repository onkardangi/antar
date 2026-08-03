package com.antar.architecture;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.classes;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

/**
 * Non-vacuous architecture checks for the current foundation repository shape.
 *
 * <p>TODO(first-product-slice): when Scripture (or the first vertical slice) introduces real
 * {@code domain}, {@code api}, {@code application}, and {@code infrastructure} packages, tighten
 * {@link LayerDependencyTest} by removing temporary {@code allowEmptyShould(true)} allowances and
 * expand these structure rules to cover cross-module dependency direction.
 */
@AnalyzeClasses(packages = "com.antar", importOptions = ImportOption.DoNotIncludeTests.class)
class ModuleStructureTest {

    private static final String[] MARKER_ONLY_MODULE_ROOTS = {
        "com.antar.identity",
        "com.antar.scripture",
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
                    .because("foundation business modules contain only marker classes until the first product slice");

    @ArchTest
    static final ArchRule foundationEndpointBelongsToPlatformInternalApi =
            classes()
                    .that().haveSimpleName("FoundationStatusController")
                    .or().haveSimpleName("FoundationStatusResponse")
                    .should().resideInAPackage("com.antar.platform.api.internal")
                    .because("the temporary foundation probe belongs to Platform, not a business module");

    @ArchTest
    static final ArchRule businessModulesDoNotDependOnPlatformApi =
            noClasses()
                    .that().resideInAnyPackage(MARKER_ONLY_MODULE_ROOTS)
                    .should().dependOnClassesThat().resideInAPackage("com.antar.platform.api..")
                    .because("marker-only modules must not depend on Platform HTTP types");
}
