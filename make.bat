@ECHO OFF

if "%1" == "" goto init

if "%1" == "init" (
	:init
    python -m venv env
    call .\env\Scripts\activate.bat
	pip install -r requirements.txt
    python res/setup.py
	goto end
)

if "%1" == "models" (
	:init
    python res/setup.py
	goto end
)

if "%1" == "dev" (
	:init
    call .\env\Scripts\activate.bat
	python -m voiceassistant --key "%2"
	goto end
)

if "%1" == "test" (
	:init
    call .\env\Scripts\activate.bat
	python -m tests
	goto end
)

if "%1" == "build" (
	:init
    call .\env\Scripts\activate.bat
	python setup.py sdist
	goto end
)

:end