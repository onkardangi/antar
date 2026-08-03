package com.antar.architecture;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

/**
 * Layer dependency rules for future package layouts.
 *
 * <p>These rules intentionally use {@code allowEmptyShould(true)} while the repository foundation
 * still has no {@code domain}, {@code api}, or {@code infrastructure} packages outside Platform's
 * temporary internal foundation endpoint.
 *
 * <p>TODO(first-product-slice): remove or narrow {@code allowEmptyShould(true)} as soon as the
 * first product module introduces real layer packages. Empty-package success is not equivalent to
 * proven layer isolation.
 */
@AnalyzeClasses(packages = "com.antar", importOptions = ImportOption.DoNotIncludeTests.class)
class LayerDependencyTest {

    @ArchTest
    static final ArchRule domainPackagesMustNotDependOnApiPackages =
            noClasses()
                    .that().resideInAPackage("..domain..")
                    .should().dependOnClassesThat().resideInAPackage("..api..")
                    // Temporary: no domain packages exist yet in the foundation milestone.
                    .allowEmptyShould(true)
                    .because("domain packages must remain free of transport-layer types");

    @ArchTest
    static final ArchRule domainPackagesMustNotDependOnInfrastructurePackages =
            noClasses()
                    .that().resideInAPackage("..domain..")
                    .should().dependOnClassesThat().resideInAPackage("..infrastructure..")
                    // Temporary: no domain packages exist yet in the foundation milestone.
                    .allowEmptyShould(true)
                    .because("domain packages must remain free of infrastructure types");

    @ArchTest
    static final ArchRule apiPackagesMustNotDependDirectlyOnRepositoryClasses =
            noClasses()
                    .that().resideInAPackage("..api..")
                    .should().dependOnClassesThat().haveSimpleNameEndingWith("Repository")
                    // Temporary: Platform has an api package, but no repositories exist yet.
                    .allowEmptyShould(true)
                    .because("API packages must call application use cases, not repositories");
}
