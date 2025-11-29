"""
Slack PostgreSQL Bot
Slack 메시지를 받아 PostgreSQL 데이터베이스에 쿼리를 실행하는 봇
"""

import os
import time
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_anthropic import ChatAnthropic
from pydantic import SecretStr

# 환경변수 로드
load_dotenv()

# Slack Bot 초기화
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
if not slack_bot_token:
    raise ValueError("SLACK_BOT_TOKEN 환경변수가 설정되지 않았습니다.")

app = App(token=slack_bot_token)

# PostgreSQL 연결
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL 환경변수가 설정되지 않았습니다.")

try:
    db = SQLDatabase.from_uri(database_url)
    print("✅ PostgreSQL 데이터베이스 연결 성공")
except Exception as e:
    print(f"❌ PostgreSQL 연결 실패: {e}")
    raise

# LLM 초기화 (Anthropic Claude)
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")

llm = ChatAnthropic(
    model_name="claude-3-5-haiku-20241022",
    temperature=0,
    max_tokens_to_sample=1024,
    api_key=SecretStr(anthropic_api_key),
    timeout=None,
    stop=None,
)

# LangChain SQL Agent 생성
agent_executor = create_sql_agent(llm=llm, db=db, verbose=True)


def process_user_query(user_query: str, say, client, channel: str) -> None:
    """
    사용자 쿼리를 처리하는 공통 함수
    """
    if not user_query or not user_query.strip():
        return

    # 실행 시간 측정 시작
    start_time = time.time()

    # 먼저 "생각중이에요..." 메시지 전송
    thinking_message = say("생각중이에요...")

    # 메시지 타임스탬프와 채널 정보 추출
    message_ts = thinking_message.get("ts")
    message_channel = thinking_message.get("channel") or channel

    try:
        # LangChain agent를 사용하여 쿼리 처리 및 DB 상호작용
        response = agent_executor.run(user_query)

        # 실행 시간 계산
        elapsed_time = time.time() - start_time
        execution_time = f"\n\n⏱️ 실행 시간: {elapsed_time:.2f}초"

        # 기존 메시지를 최종 응답으로 업데이트 (실행 시간 포함)
        final_response = f"{str(response)}{execution_time}"
        client.chat_update(channel=message_channel, ts=message_ts, text=final_response)
    except Exception as e:
        # 실행 시간 계산
        elapsed_time = time.time() - start_time
        execution_time = f"\n\n⏱️ 실행 시간: {elapsed_time:.2f}초"

        error_message = f"❌ 오류가 발생했습니다: {str(e)}{execution_time}"
        print(f"Error: {e}")

        # 기존 메시지를 에러 메시지로 업데이트 (실행 시간 포함)
        client.chat_update(channel=message_channel, ts=message_ts, text=error_message)


@app.event("app_mention")
def handle_app_mention(event, say, client):
    """
    봇이 멘션되었을 때 호출되는 핸들러
    사용자의 질문을 받아 SQL 쿼리를 실행하고 결과를 반환합니다.
    """
    user_query = event.get("text", "")

    # 봇 멘션 제거 (예: "<@U123456> 질문내용" -> "질문내용")
    if "<@" in user_query:
        parts = user_query.split(">", 1)
        if len(parts) > 1:
            user_query = parts[1].strip()

    if not user_query:
        say("질문을 입력해주세요.")
        return

    print(
        f"🔔 멘션 수신 - 채널: {event.get('channel')}, 사용자: {event.get('user')}, 텍스트: {user_query[:50]}..."
    )

    # 공통 처리 함수 사용
    process_user_query(user_query, say, client, event.get("channel"))


@app.event("message")
def handle_message(event, say, client):
    """
    모든 메시지 이벤트 핸들러
    초대받은 채널의 모든 메시지를 수신하고 처리합니다.
    """
    # 봇 자신의 메시지는 무시 (무한 루프 방지)
    if event.get("bot_id") or event.get("subtype") == "bot_message":
        return

    # 서브타입이 있는 메시지는 무시 (예: message_changed, message_deleted 등)
    if event.get("subtype") and event.get("subtype") not in ["", None]:
        return

    # 메시지 텍스트 추출
    user_query = event.get("text", "").strip()

    if not user_query:
        return

    # 봇 멘션 제거 (멘션된 경우)
    if "<@" in user_query:
        parts = user_query.split(">", 1)
        if len(parts) > 1:
            user_query = parts[1].strip()

    # 메시지 정보 로깅 (디버깅용)
    print(
        f"📨 메시지 수신 - 채널: {event.get('channel')}, 사용자: {event.get('user')}, 텍스트: {user_query[:50]}{'...' if len(user_query) > 50 else ''}"
    )

    # 쿼리 처리
    process_user_query(user_query, say, client, event.get("channel"))


if __name__ == "__main__":
    slack_app_token = os.environ.get("SLACK_APP_TOKEN")
    if not slack_app_token:
        raise ValueError("SLACK_APP_TOKEN 환경변수가 설정되지 않았습니다.")

    print("🚀 Slack PostgreSQL Bot 시작 중...")
    handler = SocketModeHandler(app, slack_app_token)
    handler.start()
