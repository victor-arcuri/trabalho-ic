@echo off
set API_URL=http://127.0.0.1:8000

echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Iniciando API...
start cmd /k "call venv\Scripts\activate.bat && uvicorn api.main:app --reload > api.log 2>&1"

echo Aguardando a API responder em %API_URL%...

:wait_loop
curl -s %API_URL% > nul
if errorlevel 1 (
    timeout /t 1 > nul
    goto wait_loop
)

echo API está online!

echo Abrindo totem...
start cmd /k "call venv\Scripts\activate.bat && python -m totem.main"

echo Abrindo catraca...
start cmd /k "call venv\Scripts\activate.bat && python -m catraca.main"

echo Tudo iniciado!
