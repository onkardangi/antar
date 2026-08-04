package com.antar.scripture.application.port;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;

/**
 * Reads an on-disk Package Format v1 directory after path resolution.
 */
public interface ScripturePackageReader {

    ResolvedScripturePackage read(Path packageDirectory);
}
