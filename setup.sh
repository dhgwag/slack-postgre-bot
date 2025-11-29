#!/bin/bash

# 가상환경 생성 및 설정 스크립트

echo "🔧 가상환경 생성 중..."
python3 -m venv venv

echo "✅ 가상환경 생성 완료!"
echo ""
echo "📦 가상환경 활성화 방법:"
echo "   source venv/bin/activate"
echo ""
echo "📥 의존성 설치 방법:"
echo "   pip install -r requirements.txt"
echo ""
echo "🚀 봇 실행 방법:"
echo "   python main.py"

