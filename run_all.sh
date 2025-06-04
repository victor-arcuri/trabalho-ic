#!/bin/bash

API_URL="http://127.0.0.1:8000"

source venv/bin/activate

echo "Iniciando API..."
uvicorn api.main:app --reload > api.log 2>&1 &

echo "Aguardando a API responder em $API_URL..."

until curl -s "$API_URL" > /dev/null; do
    printf '.'
    sleep 1
done

echo ""
echo "API está online!"

echo "Abrindo totem..."
gnome-terminal -- bash -c "source venv/bin/activate; python3 -m totem.main; exec bash"

echo "Abrindo catraca..."
gnome-terminal -- bash -c "source venv/bin/activate; python3 -m catraca.main; exec bash"

echo "Tudo iniciado!"