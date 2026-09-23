#!/bin/bash
# Setup ambiente local (venv)

set -e

echo "Criando venv..."
python3 -m venv venv

echo "Ativando venv e instalando dependências..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup concluído!"
echo ""
echo "Para usar:"
echo "  source venv/bin/activate"
echo "  python src/ingest.py      # Cria índice"
echo "  python src/search.py \"termo\"  # Busca"
echo ""
echo "Ou use o wrapper:"
echo "  ./search-local \"termo\""