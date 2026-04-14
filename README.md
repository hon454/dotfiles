# dotfiles

개인 개발 환경 설정 파일 모음. 새 머신 세팅이나 설정 동기화를 위한 레포지토리.

## 구조

```
dotfiles/
├── claude/                    # Claude Code 설정
│   └── .claude/
│       └── statusline.py
└── zsh/                       # Zsh 설정
    └── .config/
        └── zsh/
            ├── aliases.zsh
            └── omz.zsh
```

각 최상위 디렉토리(claude, zsh, ...)는 하나의 **패키지**다.
패키지 안의 디렉토리 구조는 홈 디렉토리(`~`)를 기준으로 한 경로를 그대로 따른다.

## Quick Start

AI 코딩 도구(Claude Code, Cursor, Copilot 등)에 아래 프롬프트를 붙여넣으면 자동으로 설정된다.

```
이 dotfiles 레포의 README.md를 읽고, 인터뷰를 통해 레포 내용을 적용해줘.
```

## 수동 설정

### 1. 레포 클론

```bash
git clone https://github.com/hon454/dotfiles.git ~/Workspace/dotfiles
cd ~/Workspace/dotfiles
```

### 2. GNU Stow 설치

이 레포는 [GNU Stow](https://www.gnu.org/software/stow/)를 사용해 심링크를 관리한다.
Stow는 패키지 안의 디렉토리 구조를 보고, 홈 디렉토리에 심링크를 자동으로 생성해주는 도구다.

```bash
brew install stow
```

### 3. 패키지 적용

원하는 패키지를 선택해서 적용한다. `-t ~`는 심링크를 홈 디렉토리에 생성하라는 의미다.

```bash
# 전체 적용
stow -t ~ claude zsh

# 개별 적용
stow -t ~ claude
stow -t ~ zsh
```

적용을 해제하려면 `-D` 플래그를 사용한다.

```bash
stow -D -t ~ claude
```

### 4. 패키지별 추가 설정

#### Claude Code

커스텀 statusline 스크립트. 3줄 레이아웃으로 세션 정보를 표시한다.

- **Line 1**: 프로젝트명, Git 브랜치/ahead·behind, worktree, staged/unstaged/untracked, 라인 변경량
- **Line 2**: 모델명, 에이전트명, 컨텍스트 사용량(토큰 수 + 퍼센트 + 캐시율), 세션 비용, 레이트 리밋(5h/7d)
- **Line 3**: Codex CLI 실시간 레이트 리밋(5h/7d) — [Codex CLI](https://github.com/openai/codex)가 설치되고 로그인(`codex login`)되어 있을 때만 표시

Line 3(Codex 리밋)을 사용하려면 [Codex CLI](https://github.com/openai/codex)가 설치되고 로그인되어 있어야 한다(`~/.codex/auth.json` 필요). 인증 정보가 없으면 자동으로 숨겨진다.

```bash
npm install -g @openai/codex
codex login
```

`~/.claude/settings.json`에 아래 설정을 추가한다:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py",
    "refreshInterval": 5
  }
}
```

#### Zsh

Oh My Zsh 업데이트 설정과 터미널 전용 에일리어스.

**터미널별 alias:**

| 터미널 | 필요 조건 | alias |
|---|---|---|
| [cmux](https://cmux.com/ko) | cmux 설치 | `cc`, `ccc`, `ccr`, `ccw` |

`.zshrc`에 아래 두 줄을 추가한다:

```bash
source ~/.config/zsh/omz.zsh    # Oh My Zsh source 라인 위에 추가
source ~/.config/zsh/aliases.zsh
```
