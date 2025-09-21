#!/usr/bin/env python3
"""
Script per aggiornare l'archivio fotografico
Esegue la scansione e rigenera l'indice delle foto
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🔄 Aggiornamento archivio fotografico...")
    print("=" * 50)
    
    # Verifica che siamo nella directory corretta
    if not os.path.exists("generate-index.py"):
        print("❌ Errore: generate-index.py non trovato!")
        print("Assicurati di essere nella directory archivio-separato")
        return 1
    
    try:
        # Esegui lo script di generazione
        result = subprocess.run([sys.executable, "generate-index.py"], 
                              capture_output=True, text=True, check=True)
        
        print("✅ Indice aggiornato con successo!")
        print("\n📊 Output:")
        print(result.stdout)
        
        if result.stderr:
            print("\n⚠️ Avvisi:")
            print(result.stderr)
            
        print("\n🎉 Aggiornamento completato!")
        print("🔄 Ricarica la pagina per vedere le modifiche")
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore durante l'aggiornamento: {e}")
        print(f"Output: {e.stdout}")
        print(f"Errori: {e.stderr}")
        return 1
    except Exception as e:
        print(f"❌ Errore imprevisto: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPremi INVIO per chiudere...")
    sys.exit(exit_code)
