#!/bin/bash

# 봇 실행 스크립트

# 가상환경이 존재하는지 확인하고 없으면 생성
VENV_CREATED=false
if [ ! -d "venv" ] || [ ! -f "venv/bin/python" ]; then
    echo "📦 가상환경이 없습니다. 생성 중..."
    if command -v python3 >/dev/null 2>&1; then
        if python3 -m venv venv 2>&1; then
            VENV_CREATED=true
        else
            echo "⚠️  가상환경 생성에 실패했습니다."
            echo "💡 python3-venv 패키지가 필요합니다. 다음 명령어로 설치하세요:"
            echo "   sudo apt install python3-venv"
            echo ""
            echo "또는 시스템 Python을 사용하려면 venv 디렉토리를 삭제하세요:"
            echo "   rm -rf venv"
            exit 1
        fi
    elif command -v python >/dev/null 2>&1; then
        if python -m venv venv 2>&1; then
            VENV_CREATED=true
        else
            echo "⚠️  가상환경 생성에 실패했습니다."
            exit 1
        fi
    else
        echo "❌ Python이 설치되어 있지 않습니다."
        exit 1
    fi
fi

# 가상환경이 손상되었는지 확인 (pip가 없으면 재생성)
if [ -f "venv/bin/python" ] && ! venv/bin/python -m pip --version >/dev/null 2>&1; then
    echo "⚠️  가상환경이 손상되었습니다. 재생성 중..."
    rm -rf venv
    if command -v python3 >/dev/null 2>&1; then
        if ! python3 -m venv venv 2>&1; then
            echo "⚠️  가상환경 재생성에 실패했습니다."
            echo "💡 python3-venv 패키지가 필요합니다. 다음 명령어로 설치하세요:"
            echo "   sudo apt install python3-venv"
            exit 1
        fi
    elif command -v python >/dev/null 2>&1; then
        if ! python -m venv venv 2>&1; then
            echo "⚠️  가상환경 재생성에 실패했습니다."
            exit 1
        fi
    else
        echo "❌ Python이 설치되어 있지 않습니다."
        exit 1
    fi
fi

# 가상환경 활성화 (activate 파일이 있으면)
if [ -z "$VIRTUAL_ENV" ] && [ -f "venv/bin/activate" ]; then
    echo "📦 가상환경 활성화 중..."
    . venv/bin/activate
fi

# .env 파일이 있는지 확인
if [ ! -f .env ]; then
    echo "⚠️  .env 파일이 없습니다."
    echo "📝 env.example을 참고하여 .env 파일을 생성해주세요."
    echo "   cp env.example .env"
    exit 1
fi

# 의존성이 설치되어 있는지 확인 (python-dotenv 패키지 확인)
if [ ! -f "venv/bin/python" ] || ! venv/bin/python -c "import dotenv" 2>/dev/null; then
    echo "📥 의존성 설치 중..."
    if [ -f "venv/bin/python" ]; then
        # python -m pip를 사용 (pip 실행 파일이 없어도 작동)
        if ! venv/bin/python -m pip --version >/dev/null 2>&1; then
            echo "⚠️  가상환경에 pip가 없습니다. ensurepip로 설치 시도 중..."
            venv/bin/python -m ensurepip --upgrade 2>/dev/null || {
                echo "❌ pip 설치에 실패했습니다."
                echo "💡 python3-venv 패키지를 설치하세요:"
                echo "   sudo apt install python3-venv"
                exit 1
            }
        fi
        venv/bin/python -m pip install --upgrade pip
        venv/bin/python -m pip install -r requirements.txt
    elif command -v pip3 >/dev/null 2>&1; then
        pip3 install -r requirements.txt
    else
        echo "❌ pip이 설치되어 있지 않습니다."
        exit 1
    fi
    # 설치 확인
    if [ -f "venv/bin/python" ] && ! venv/bin/python -c "import dotenv" 2>/dev/null; then
        echo "⚠️  의존성 설치에 실패했습니다. 수동으로 설치해주세요:"
        echo "   venv/bin/python -m pip install -r requirements.txt"
        exit 1
    fi
fi

echo "🚀 Slack PostgreSQL Bot 시작 중..."
# 가상환경의 python을 사용하거나 python3를 사용
if [ -f "venv/bin/python" ]; then
    venv/bin/python main.py
elif command -v python3 >/dev/null 2>&1; then
    python3 main.py
else
    python main.py
fi

