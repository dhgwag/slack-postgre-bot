#!/bin/bash

# 봇 실행 스크립트

# 가상환경이 활성화되어 있는지 확인
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  가상환경이 활성화되지 않았습니다."
    echo "📦 가상환경 활성화 중..."
    source venv/bin/activate
fi

# .env 파일이 있는지 확인
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다."
    echo "📝 env.example을 참고하여 .env 파일을 생성해주세요."
    echo "   cp env.example .env"
    exit 1
fi

# 의존성이 설치되어 있는지 확인
if [ ! -d "venv/lib" ]; then
    echo "📥 의존성 설치 중..."
    pip install -r requirements.txt
fi

echo "🚀 Slack PostgreSQL Bot 시작 중..."
python main.py

