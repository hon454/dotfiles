# CLAUDE.md

Personal dotfiles repository. Version-controlled configuration files for quick environment restoration on new machines.

**CLAUDE.md must be written in English.**

## Directory Structure

Configuration files are organized into **per-tool directories**. Directory names use the tool name in lowercase.

```
dotfiles/
├── claude/          # Claude Code
```

## Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/).

- `feat`: Add new configuration files
- `fix`: Fix bugs in existing configurations
- `refactor`: Restructure configurations without changing behavior
- `docs`: Update README, CLAUDE.md, or other documentation
- `chore`: Update repo management files (.gitignore, etc.)

Use the tool directory name as scope: `feat(claude): add statusline script`

## Adding New Configurations

1. Place configuration files in the corresponding tool directory
2. Add the directory to the **Structure** section in README.md
3. Document symlink commands and any additional setup steps in README.md
4. Never commit sensitive information (API keys, tokens, etc.)
