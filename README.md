# dotfiles

개인 개발 환경 설정 파일 모음. 새 머신 세팅이나 설정 동기화를 위한 레포지토리.

## 구조

```
dotfiles/
├── claude/          # Claude Code 설정
│   └── statusline.py
```

## 설정 방법

레포를 클론한 뒤, 필요한 설정을 심링크로 연결한다.

```bash
git clone https://github.com/hon454/dotfiles.git ~/Workspace/dotfiles
```

### Claude Code

커스텀 statusline 스크립트. 프로젝트/Git 상태, 모델, 컨텍스트 사용량, 비용, 레이트 리밋을 2줄로 표시한다.

```bash
ln -sf ~/Workspace/dotfiles/claude/statusline.py ~/.claude/statusline.py
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
