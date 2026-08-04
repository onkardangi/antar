# `content/checksums/`

SHA-256 manifests for immutable content artifacts.

## Policy summary

- Algorithm: **SHA-256**, lowercase hex.
- Raw artifacts are checksummed at acquisition / inspection time.
- Normalized packages are checksummed when produced.
- Registry `sha256` values must match these manifests.
- Changing a raw file requires a **new** artifact path and new checksum entry; never overwrite history silently.

See [`docs/content/02_CONTENT_PIPELINE.md`](../../docs/content/02_CONTENT_PIPELINE.md) for full checksum policy.

## Files

| File | Role |
|------|------|
| `raw.sha256` | Manifest of registered raw artifacts |
| `normalized.sha256` | Manifest of normalized packages (empty until first package) |
