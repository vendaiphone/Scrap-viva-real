@echo off
title Viva Real Scraper - Inicializando
echo ================================
echo     Iniciando servidor Flask    
echo ================================
cd /d %~dp0

REM Verifica se ambiente virtual já existe
if not exist venv (
    echo [*] Criando ambiente virtual...
    python -m venv venv
)

REM Ativa o ambiente
call venv\Scripts\activate

REM Atualiza pip e instala dependências
echo [*] Instalando dependências...
pip install --upgrade pip >nul
pip install -r requirements.txt >nul

REM Abre o navegador automaticamente
start http://localhost:5000

REM Inicia o servidor Flask
echo [*] Iniciando servidor em localhost:5000
python app.py

pause
