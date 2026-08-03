package com.antar.architecture;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

/**
 * Layer dependency rules for package layouts.
 *
 * <p>Scripture introduced real {@code domain}, {@code api}, {@code application}, and
 * {@code infrastructure} packages, so these rules are no longer vacuous for the first product
 * slice.
 */
@AnalyzeClasses(packages = "com.antar", importOptions = ImportOption.DoNotIncludeTests.class)
class LayerDependencyTest {

    @ArchTest
    static final ArchRule domainPackagesMustNotDependOnApiPackages =
            noClasses()
                    .that().resideInAPackage("..domain..")
                    .should().dependOnClassesThat().resideInAPackage("..api..")
                    .because("domain packages must remain free of transport-layer types");

    @ArchTest
    static final ArchRule domainPackagesMustNotDependOnInfrastructurePackages =
            noClasses()
                    .that().resideInAPackage("..domain..")
                    .should().dependOnClassesThat().resideInAPackage("..infrastructure..")
                    .because("domain packages must remain free of infrastructure types");

    @ArchTest
    static final ArchRule apiPackagesMustNotDependDirectlyOnRepositoryClasses =
            noClasses()
                    .that().resideInAPackage("..api..")
                    .should().dependOnClassesThat().haveSimpleNameEndingWith("Repository")
                    .because("API packages must call application use cases, not repositories");

    @ArchTest
    static final ArchRule applicationPackagesMustNotDependOnApiPackages =
            noClasses()
                    .that().resideInAPackage("..application..")
                    .should().dependOnClassesThat().resideInAPackage("..api..")
                    .because("application packages must remain free of transport DTOs");
}
