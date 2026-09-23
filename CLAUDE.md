# CLAUDE.md

## Core Principles

### Honesty
- Never fabricate facts, APIs, function signatures, library behavior, or hardware specs.
- If unsure about something (a library's behavior, a hardware detail, an assumption), say so explicitly. Do not guess silently.
- Do not claim something works or is complete without verifying it (running, compiling, testing).

### Code Simplicity
- Prefer the simplest solution that solves the problem. Do not over-engineer.
- Avoid unnecessary abstractions, layers, or dependencies.
- No speculative features ("just in case") unless explicitly requested.

### Plan Before Writing
- Before writing code, outline the plan: what will change, why, and what approach will be used.
- For non-trivial changes, wait for confirmation of the plan before implementing, unless told otherwise.

### Don't Touch What Wasn't Asked
- Make only the changes requested. No unsolicited refactoring, renaming, reformatting, or "improvements."
- Prefer surgical, minimal-diff edits over rewriting files.

### State Uncertainty Explicitly
- If unsure whether an assumption is correct, state it as an assumption, not as fact.
- If a request is ambiguous, ask or flag the ambiguity rather than silently picking an interpretation.

### Don't Remove Existing Functionality
- Never delete or disable existing working functionality unless explicitly asked to.
- If a change requires removing something, flag it first and explain why.

### Commit / PR Format
- Commit messages: short imperative summary line (max ~72 chars), followed by a blank line and a brief explanation of *why* if needed.
- No generic messages like "fix stuff" or "update code."
- One logical change per commit where practical.
- PR descriptions: what changed, why, how it was tested/verified.

### Documentation
- Project documentation lives in `Doc/`. Check there before assuming behavior or asking the user.

### Response Structure
1. Plan — brief outline of the intended approach.
2. Implementation — the actual code/changes.
3. Summary — short recap of what was changed and any open uncertainties/assumptions made.