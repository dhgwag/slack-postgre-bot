# Slack PostgreSQL Bot

Slack과 PostgreSQL을 연동하는 봇 프로젝트입니다. 자연어 질문을 받아 PostgreSQL 데이터베이스에 쿼리를 실행하고 결과를 반환합니다.

## 기능

- Slack에서 봇을 멘션하여 자연어로 데이터베이스 질문
- LangChain과 Anthropic Claude를 사용한 SQL 쿼리 생성 및 실행
- PostgreSQL 데이터베이스와의 자동 연동

## 설치 방법

### 1. 가상환경 생성 및 활성화

**방법 1: 자동 스크립트 사용 (권장)**
```bash
./setup.sh
source venv/bin/activate
```

**방법 2: 수동으로 생성**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

`env.example` 파일을 참고하여 `.env` 파일을 생성하고 필요한 환경변수를 설정하세요:

```bash
cp env.example .env
```

`.env` 파일에 다음 정보를 입력하세요:

- `SLACK_BOT_TOKEN`: Slack Bot Token (xoxb-로 시작)
- `SLACK_APP_TOKEN`: Slack App-Level Token (xapp-로 시작)
- `DATABASE_URL`: PostgreSQL 연결 문자열 (예: `postgresql://user:password@host:port/dbname`)
- `ANTHROPIC_API_KEY`: Anthropic Claude API 키

### 4. Slack 앱 설정

1. [Slack API](https://api.slack.com/apps)에서 새 앱 생성
2. Socket Mode 활성화
3. Bot Token Scopes에 다음 권한 추가:
   - `app_mentions:read` - 멘션된 메시지 읽기
   - `chat:write` - 메시지 보내기
   - `channels:history` - 채널 메시지 히스토리 읽기 (초대받은 채널의 모든 메시지 수신용)
   - `groups:history` - 그룹 메시지 히스토리 읽기 (프라이빗 채널용)
   - `im:history` - DM 메시지 히스토리 읽기
4. Event Subscriptions에서 다음 이벤트 구독:
   - `app_mention` - 봇이 멘션된 경우
   - `message.channels` - 공개 채널의 모든 메시지
   - `message.groups` - 프라이빗 채널의 모든 메시지
   - `message.im` - DM 메시지

## 실행 방법

**방법 1: 자동 스크립트 사용 (권장)**
```bash
./run.sh
```
이 스크립트는 자동으로 가상환경을 활성화하고 봇을 실행합니다.

**방법 2: 수동으로 실행**
```bash
source venv/bin/activate  # 가상환경 활성화
python main.py
```

## 사용 방법

봇이 초대받은 채널에서 질문을 입력하면 자동으로 처리됩니다:

```
사용자 수를 알려줘
최근 주문 내역을 보여줘
총 매출액은 얼마야?
```

또는 봇을 멘션하여 사용할 수도 있습니다:

```
@YourBot 사용자 수를 알려줘
```

## 프로젝트 구조

```
slack-postgre-bot/
├── main.py            # 메인 봇 코드
├── requirements.txt   # Python 의존성
├── env.example        # 환경변수 템플릿
├── setup.sh           # 가상환경 설정 스크립트
├── run.sh             # 봇 실행 스크립트
├── .env              # 환경변수 (로컬에서 생성)
├── .gitignore        # Git 무시 파일
└── README.md         # 프로젝트 문서
```

## 주의사항

- `.env` 파일은 절대 Git에 커밋하지 마세요 (이미 .gitignore에 포함됨)
- 데이터베이스 연결 정보와 API 키는 안전하게 관리하세요

