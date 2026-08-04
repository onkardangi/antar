# Review file schema

Every Verse review file is Markdown named `{chapter}.{verse}.md` (example: `1.1.md`).

## Required sections (exact headings)

```markdown
# Canonical Reference

# Status

# Sources

# Source Comparison

# Differences

# Editorial Notes

# Decision

# Approval

# Audit Log
```

Section order must match the list above.

## Field rules

### Canonical Reference

A single line with the reference, e.g. `1.1`. Must match the filename stem.

### Status

Exactly one allowed status token on its own line (see `status.md`).

### Sources

A Markdown table including columns:

| Source ID | Revision | License | Retrieved | Checksum | Status |

Additional columns are allowed after these.

### Source Comparison

Document every source used. For each source, include:

- Source reference
- Observed Sanskrit (when comparing sources; otherwise state that text lives in the chapter workspace extraction)
- Observed transliteration
- Normalization notes

No editorial opinion in this section.

### Differences

Explicitly document differences between sources.

If none:

```text
No differences currently observed.
```

Do not silently assume equality.

### Editorial Notes

Human notes only. May be empty (`_None._`).

### Decision

Human decision record. Initial value:

```text
No editorial decision recorded.
```

### Approval

Must contain labels:

```text
Reviewer:

Second Reviewer:

Date:
```

Values may be blank unless Status is `APPROVED`.

When Status is `APPROVED`, Reviewer and Date must be non-blank.

### Audit Log

Must exist and contain at least one entry. Append-only for future changes.

Initial entry example:

```text
- Review file created.
```
