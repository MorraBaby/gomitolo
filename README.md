# Andrea Moraschinelli - Archive

Sito indipendente per l'archivio fotografico di Andrea Moraschinelli.

## Struttura

- `index.html` - Reindirizza a archive.html
- `archive.html` - Pagina principale dell'archivio
- `polas.html` - Galleria polaroid
- `style.css` - Stili CSS
- `src/` - Cartella contenente tutte le foto
- `generate-index.py` - Script per aggiornare l'indice delle foto
- `photo-index.json` - Indice delle foto generato automaticamente

## Come aggiornare l'archivio

1. Aggiungi le foto nella cartella `src/archivio/`
2. Esegui: `python3 generate-index.py`
3. Le foto appariranno automaticamente nell'archivio

## Deploy

Questo sito può essere deployato su Netlify o qualsiasi altro servizio di hosting statico.
