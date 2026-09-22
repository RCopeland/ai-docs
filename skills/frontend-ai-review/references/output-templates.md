# Frontend AI Review Output Templates

Use these templates by default.

## Engineer-Facing Review

```markdown
## Findings
- [severity] `path:line` issue and why it matters

## Validation review
- checks run or missing
- test coverage assessment
- notable verification gaps

## System-level summary
- behavior or flow changes
- layers touched
- coupling or architectural impact
- highest-risk areas
```

## User Review Summary

```markdown
## User review summary
- what changed in plain language
- what areas the user should review manually
- anything that looks risky or deserves questions

## Open questions / manual review focus
- question 1
- question 2
```

## If There Are No Findings

```markdown
## Findings
- No blocking or required issues found in the reviewed scope.

## Validation review
...

## System-level summary
...

## User review summary
...
```

## Tone Rules

- findings should be concise and evidence-based
- summaries should be plain language, not jargon-heavy
- the user summary should help a reviewer know where to click, test, or ask questions
- when relevant, call out accessibility, responsive, and state-transition behaviors to review manually
