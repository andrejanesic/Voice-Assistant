@ECHO OFF

if "%1" == "" goto init

if "%1" == "init" (
	:init
    python -m venv env
    call .\env\Scripts\activate.bat
	pip install -r requirements.txt
	goto end
)

if "%1" == "test" (
	REM Todo add test
	REM nosetests tests
	goto end
)

:end