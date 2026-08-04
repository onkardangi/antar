# Review status vocabulary

Allowed values for `# Status` in a Verse review file:

| Status | Meaning |
|--------|---------|
| `UNREVIEWED` | Review file exists but work has not started |
| `READY_FOR_REVIEW` | Sources attached; awaiting human review |
| `UNDER_REVIEW` | Active editorial examination |
| `APPROVED` | Human-approved for promotion into canonical draft/corpus workflow |
| `REJECTED` | Rejected for canonical use as currently evidenced |
| `NEEDS_SOURCE` | Additional or replacement source evidence required |
| `SOURCE_MISSING` | Required secondary evidence failed acquisition or is unusable |
| `SOURCE_CONFLICT` | Sources disagree; resolution required before approval |

## Rules

1. Tooling may create files as `READY_FOR_REVIEW` or `UNREVIEWED` only.
2. Transition to `APPROVED` is human-only and requires Approval + Audit Log updates.
3. Chapter workspace JSONL statuses and review-file statuses should be kept consistent by editors; automated sync is not required in Phase 1.
4. `APPROVED` here does **not** by itself import into PostgreSQL.
