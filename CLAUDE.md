# CLAUDE.md

개인 dotfiles 레포지토리. 개발 환경 설정 파일을 버전 관리하고, 새 머신에서 빠르게 환경을 복원하기 위한 용도.

## 디렉토리 구조

설정 파일은 **도구별 디렉토리**로 구분한다. 디렉토리명은 도구 이름을 소문자로 사용한다.

```
dotfiles/
├── claude/          # Claude Code
├── ghostty/         # Ghostty (예시)
└── zsh/             # Zsh (예시)
```

## 커밋 컨벤션

[Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따른다.

- `feat`: 새로운 설정 파일 추가
- `fix`: 기존 설정의 버그 수정
- `refactor`: 동작 변경 없는 설정 구조 개선
- `docs`: README, CLAUDE.md 등 문서 변경
- `chore`: .gitignore 등 레포 관리 파일 변경

스코프는 도구 디렉토리명을 사용한다: `feat(claude): add statusline script`

## 설정 추가 시 규칙

1. 해당 도구의 디렉토리에 설정 파일을 추가한다
2. README.md의 **구조** 섹션에 디렉토리를 추가한다
3. README.md에 심링크 명령어와 필요한 추가 설정을 문서화한다
4. 민감한 정보(API 키, 토큰 등)는 절대 커밋하지 않는다
