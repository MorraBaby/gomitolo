#!/bin/bash

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 AGGIORNAMENTO SITO PORTFOLIO${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Vai nella directory del progetto
cd "$(dirname "$0")"

echo -e "${YELLOW}📁 Directory: $(pwd)${NC}"
echo ""

# Controlla se ci sono modifiche
if git diff --quiet && git diff --staged --quiet; then
    echo -e "${YELLOW}⚠️  Nessuna modifica rilevata${NC}"
    echo -e "${YELLOW}   Aggiungi foto o modifica i file prima di eseguire questo script${NC}"
    echo ""
    read -p "Premi INVIO per continuare comunque o Ctrl+C per uscire..."
fi

echo -e "${BLUE}🔄 Aggiungendo modifiche...${NC}"
git add .

echo -e "${BLUE}💾 Creando commit...${NC}"
git commit -m "Aggiornamento sito $(date '+%d/%m/%Y %H:%M')"

echo -e "${BLUE}🚀 Invio su GitHub...${NC}"
git push

echo ""
echo -e "${GREEN}✅ AGGIORNAMENTO COMPLETATO!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${YELLOW}🌐 Il sito sarà aggiornato in 1-2 minuti su:${NC}"
echo -e "${YELLOW}   https://morrababy.github.io/gomitolo/archive.html${NC}"
echo ""
echo -e "${BLUE}📊 Per monitorare il progresso:${NC}"
echo -e "${BLUE}   https://github.com/MorraBaby/gomitolo/actions${NC}"
echo ""

# Mantieni la finestra aperta
read -p "Premi INVIO per chiudere..."
