init:
    python -m venv env
    ./env/Scripts/activate
	pip install -r requirements.txt

dev:
    ./env/Scripts/activate
    python -m voiceassistant

test:
    ./env/Scripts/activate
    python -m tests