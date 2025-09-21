#!/usr/bin/env python3
"""
Script per generare automaticamente l'indice delle foto dell'archivio
"""

import os
import json
from pathlib import Path

# Mappa mesi in IT/EN -> numero
MONTH_MAP = {
    # Italiano
    'GENNAIO': 1, 'FEBBRAIO': 2, 'MARZO': 3, 'APRILE': 4, 'MAGGIO': 5, 'GIUGNO': 6,
    'LUGLIO': 7, 'AGOSTO': 8, 'SETTEMBRE': 9, 'OTTOBRE': 10, 'NOVEMBRE': 11, 'DICEMBRE': 12,
    # Abbreviazioni IT comuni
    'GEN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAG': 5, 'GIU': 6,
    'LUG': 7, 'AGO': 8, 'SET': 9, 'OTT': 10, 'NOV': 11, 'DIC': 12,
    # Inglese
    'JANUARY': 1, 'FEBRUARY': 2, 'MARCH': 3, 'APRIL': 4, 'MAY': 5, 'JUNE': 6,
    'JULY': 7, 'AUGUST': 8, 'SEPTEMBER': 9, 'OCTOBER': 10, 'NOVEMBER': 11, 'DECEMBER': 12,
    # Abbreviazioni EN
    'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
    'JUL': 7, 'AUG': 8, 'SEP': 9, 'SEPT': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12,
}

def parse_year_month_from_path(path_parts):
    """Restituisce (year:int|None, month:int|None, folder_label:str, folder_number:int)
    Rileva anno/mese da path tipo src/archivio/2025/01-SETTEMBRE/...
    e costruisce un'etichetta folder coerente tipo "2025 SETTEMBRE".
    """
    year = None
    month_num = None
    folder_label = None
    folder_number = 0

    if len(path_parts) >= 4 and path_parts[-3].isdigit():
        year = int(path_parts[-3])
        month_raw = path_parts[-2]
        
        # Estrai numero dalla cartella (es: "9 - SETTEMBRE" -> 9, "01-SETTEMBRE" -> 1)
        if ' - ' in month_raw:
            # Formato "9 - SETTEMBRE"
            number_part, month_name = month_raw.split(' - ', 1)
            try:
                folder_number = int(number_part.strip())
            except ValueError:
                folder_number = 0
            cleaned = month_name.strip()
        elif '-' in month_raw and not ' - ' in month_raw:
            # Formato "01-SETTEMBRE"
            number_part, month_name = month_raw.split('-', 1)
            try:
                folder_number = int(number_part)
            except ValueError:
                folder_number = 0
            cleaned = month_name
        else:
            cleaned = month_raw
            folder_number = 0
            
        # Pulisci e normalizza per lookup
        cleaned = cleaned.replace("'", "").replace(" 25", "").replace(" 24", "").replace(" 23", "")
        key = cleaned.strip().upper()
        month_num = MONTH_MAP.get(key)
        folder_label = f"{year} {cleaned}"
    else:
        # Fallback su nome cartella corrente
        current_folder = path_parts[-2] if len(path_parts) > 2 else "ROOT"
        folder_label = current_folder.replace("'", "")

    return year, month_num, folder_label, folder_number

def extract_file_number(filename):
    """Estrae il numero dal nome del file per l'ordinamento.
    Es: "01-Barceloneta, Barcellona.jpg" -> 1
    Es: "Barceloneta, Barcellona 2.jpg" -> 2 (fallback)
    """
    # Prova prima il formato "01-nome.jpg"
    if '-' in filename:
        number_part = filename.split('-')[0]
        try:
            return int(number_part)
        except ValueError:
            pass
    
    # Fallback: cerca numeri alla fine del nome (prima dell'estensione)
    import re
    match = re.search(r' (\d+)\.', filename)
    if match:
        return int(match.group(1))
    
    return 0

def scan_archive_directory(archive_dir="src/archivio/"):
    """Scansiona la directory archivio e genera la lista delle foto, POLAROID e pensieri"""
    photos = []
    polaroids = []
    thoughts = []
    
    if not os.path.exists(archive_dir):
        print(f"❌ Directory {archive_dir} non trovata!")
        return {"photos": photos, "polaroids": polaroids, "thoughts": thoughts}
    
    # Estensioni immagini supportate
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.tiff'}
    # Estensioni file di testo supportate
    text_extensions = {'.txt', '.md'}
    
    # Scansiona ricorsivamente
    for root, dirs, files in os.walk(archive_dir):
        for file in files:
            file_ext = Path(file).suffix.lower()
            
            # Controlla se è un'immagine
            if file_ext in image_extensions:
                # Percorso completo del file
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, ".")
                # Timestamp di modifica/aggiunta (usato per ordinamento recency)
                try:
                    mtime = os.path.getmtime(full_path)
                except Exception:
                    mtime = 0.0
                
                # Estrai anno/mese e label cartella
                path_parts = Path(relative_path).parts
                current_folder = path_parts[-2] if len(path_parts) > 2 else "ROOT"
                year_val, month_val, folder_name, folder_number = parse_year_month_from_path(path_parts)
                if current_folder == "EXTRA":
                    folder_name = "EXTRA"
                    folder_number = 0
                
                # Estrai numero dal nome del file
                file_number = extract_file_number(file)
                
                # Controlla se è una POLAROID
                if file.upper().startswith("POLAROID"):
                    polaroids.append({
                        "src": relative_path.replace("\\", "/"),
                        "folder": folder_name,
                        "year": year_val,
                        "month": month_val,
                        "folder_number": folder_number,
                        "file_number": file_number,
                        "mtime": mtime
                    })
                else:
                    # Foto normale
                    photos.append({
                        "src": relative_path.replace("\\", "/"),  # Normalizza path per web
                        "folder": folder_name,
                        "year": year_val,
                        "month": month_val,
                        "folder_number": folder_number,
                        "file_number": file_number,
                        "mtime": mtime
                    })
            
            # Controlla se è un file di testo (pensiero)
            elif file_ext in text_extensions:
                # Percorso completo del file
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, ".")
                # Timestamp di modifica/aggiunta
                try:
                    mtime = os.path.getmtime(full_path)
                except Exception:
                    mtime = 0.0
                
                # Estrai anno/mese e label cartella
                path_parts = Path(relative_path).parts
                current_folder = path_parts[-2] if len(path_parts) > 2 else "ROOT"
                year_val, month_val, folder_name, folder_number = parse_year_month_from_path(path_parts)
                if current_folder == "EXTRA":
                    folder_name = "EXTRA"
                    folder_number = 0
                
                # Estrai numero dal nome del file
                file_number = extract_file_number(file)
                
                # Leggi il contenuto del file di testo
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    if content:  # Solo se il file non è vuoto
                        thoughts.append({
                            "src": relative_path.replace("\\", "/"),
                            "content": content,
                            "folder": folder_name,
                            "year": year_val,
                            "month": month_val,
                            "folder_number": folder_number,
                            "file_number": file_number,
                            "mtime": mtime
                        })
                except Exception as e:
                    print(f"⚠️ Errore lettura file {full_path}: {e}")
    
    # Ordina per numero di cartella (più grande prima) e poi per numero di file
    def photo_sort_key(x):
        folder_num = x.get("folder_number") or 0
        file_num = x.get("file_number") or 0
        # Ordina per numero cartella (decrescente) e poi per numero file (crescente)
        return (-folder_num, file_num)

    photos.sort(key=photo_sort_key)
    polaroids.sort(key=photo_sort_key)
    thoughts.sort(key=photo_sort_key)
    
    return {"photos": photos, "polaroids": polaroids, "thoughts": thoughts}

def main():
    print("🔄 Scansionando l'archivio fotografico...")
    
    result = scan_archive_directory()
    photos = result["photos"]
    polaroids = result["polaroids"]
    thoughts = result["thoughts"]
    
    if not photos and not polaroids and not thoughts:
        print("⚠️ Nessun contenuto trovato nell'archivio!")
        return
    
    # Genera il file JSON
    output_file = "photo-index.json"
    
    # Rimuovi chiavi ausiliarie year/month dall'output
    sanitized = {
        "photos": [{"src": p["src"], "folder": p["folder"]} for p in photos],
        "polaroids": [{"src": p["src"], "folder": p["folder"]} for p in polaroids],
        "thoughts": [{"src": t["src"], "content": t["content"], "folder": t["folder"]} for t in thoughts],
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sanitized, f, indent=2, ensure_ascii=False)

    # Genera anche indice progetti WORK
    projects = []
    projects_root = Path('src/PROGETTI_WORK')
    if projects_root.exists():
        for proj_dir in sorted([p for p in projects_root.iterdir() if p.is_dir()]):
            name = proj_dir.name
            primarie_dir = proj_dir / 'primarie'
            secondarie_dir = proj_dir / 'secondarie'
            primarie = []
            secondarie = []
            # Raccogli immagini in sottocartelle se esistono, altrimenti prova direttamente nella radice del progetto
            def list_imgs(d: Path):
                files = []
                if d.exists():
                    for f in sorted(d.iterdir()):
                        if f.is_file() and f.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}:
                            files.append(str(f).replace('\\', '/'))
                return files
            primarie = list_imgs(primarie_dir) or list_imgs(proj_dir)
            secondarie = list_imgs(secondarie_dir)
            if primarie or secondarie:
                projects.append({
                    'name': name,
                    'primarie': primarie,
                    'secondarie': secondarie,
                })
    with open('projects-index.json', 'w', encoding='utf-8') as pf:
        json.dump({'projects': projects}, pf, indent=2, ensure_ascii=False)
    
    print(f"✅ Indice generato!")
    print(f"📸 Trovate {len(photos)} foto normali")
    print(f"📷 Trovate {len(polaroids)} POLAROID")
    print(f"💭 Trovati {len(thoughts)} pensieri")
    print(f"📄 File salvato in: {output_file}")
    
    # Mostra alcune foto di esempio
    if photos:
        print("\n📸 Prime 5 foto trovate:")
        for i, photo in enumerate(photos[:5]):
            print(f"  {i+1}. {photo['folder']}: {os.path.basename(photo['src'])}")
    
    if polaroids:
        print("\n📷 POLAROID trovate:")
        for i, polaroid in enumerate(polaroids):
            print(f"  {i+1}. {polaroid['folder']}: {os.path.basename(polaroid['src'])}")
    
    if thoughts:
        print("\n💭 Pensieri trovati:")
        for i, thought in enumerate(thoughts[:3]):  # Mostra solo i primi 3
            content_preview = thought['content'][:50] + "..." if len(thought['content']) > 50 else thought['content']
            print(f"  {i+1}. {thought['folder']}: {content_preview}")

if __name__ == "__main__":
    main()
