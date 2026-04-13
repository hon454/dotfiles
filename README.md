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

## 설정 방법

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

커스텀 statusline 스크립트. 프로젝트/Git 상태, 모델, 컨텍스트 사용량, 비용, 레이트 리밋을 2줄로 표시한다.

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

Oh My Zsh 업데이트 설정과 cmux 에일리어스. `.zshrc`에 아래 두 줄을 추가한다:

```bash
source ~/.config/zsh/omz.zsh    # Oh My Zsh source 라인 위에 추가
source ~/.config/zsh/aliases.zsh
```
