# Agent Guidelines

## Code Modification Rules

Agents must **only write or modify code under the `mybrowser/` folder**.
The following folders and files must **not** be modified:

- `browser/`
- `docs/`
- `server/`
- `docker/`
- `Makefile`
- `uv.lock`
- `README.md`
- Any other files outside of `mybrowser/`

**Exception:** Agents must update `CHANGELOG.md` (at the repository root) after completing any user request. Prepend a new entry at the top of the file (below the `# CHANGELOG` heading) with the current date and a summary of what was done.


## Code Quality

- Delete unused import statements from any files you modify.
- Use **black** to format Python code.

## Testing

- Use **pytest** for unit tests.
- Test should be written in 'mybroswer/tests'
- Run tests with the **uv** command:

```bash
uv run pytest
```
