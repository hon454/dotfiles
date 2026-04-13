# AGENTS.md

Personal dotfiles repository. Version-controlled configuration files for quick environment restoration on new machines.

**Instruction files (AGENTS.md, CLAUDE.md, etc.) must be written in English.**

## Directory Structure

Each top-level directory is a **stow package**. The internal structure mirrors the home directory (`~`).

```
dotfiles/
├── claude/              # Claude Code
│   └── .claude/
└── zsh/                 # Zsh
    └── .config/
        └── zsh/
```

## Symlink Management

This repo uses [GNU Stow](https://www.gnu.org/software/stow/) for symlink management. Apply packages with `stow -t ~ <package>`.

## Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/).

- `feat`: Add new configuration files
- `fix`: Fix bugs in existing configurations
- `refactor`: Restructure configurations without changing behavior
- `docs`: Update README or instruction files (AGENTS.md, CLAUDE.md, etc.)
- `chore`: Update repo management files (.gitignore, etc.)

Use the tool directory name as scope: `feat(claude): add statusline script`

## Adding New Configurations

1. Create a new top-level directory named after the tool (lowercase)
2. Inside it, mirror the home directory path where the config file belongs
3. Update the **Structure** sections in README.md and AGENTS.md
4. Document any additional setup steps in README.md under the package
5. Apply with `stow -t ~ <package>`
6. Never commit sensitive information (API keys, tokens, etc.)
