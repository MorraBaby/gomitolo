#!/bin/bash
cd "$(dirname "$0")"
python3 generate-index.py
echo ""
echo "Premi INVIO per chiudere..."
read
