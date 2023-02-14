init:
    python -m venv env
    ./env/Scripts/activate
	pip install -r requirements.txt
    python res/setup.py

models:
    python res/setup.py

dev:
    ./env/Scripts/activate
    python -m voiceassistant --key $(APIKEY)

test:
    ./env/Scripts/activate
    python -m tests

build:
    ./env/Scripts/activate
    python setup.py sdist