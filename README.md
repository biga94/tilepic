# tilEPIC

tilEPIC è uno script per creare mosaici di immagini da dati di array Illumina EPIC per l'analisi del metiloma.

## Descrizione

Questo progetto include due script principali:
- `tilEPIC.py`: Crea mosaici di immagini per un singolo campione.
- `create_final_chip.py`: Crea un mosaico finale unendo tutti i campioni.

## Installazione

Assicurati di avere Python e le seguenti librerie installate:
- PIL (Pillow)

Puoi installare le librerie necessarie usando:
```sh
pip install pillow
```
## Usage

### tilEPIC.py

To create a mosaic for a single sample:

```sh
python tilEPIC.py "path/to/image/directory" "path/to/output.png" R01C01 green --vertical_shift_percent 0.5 --horizontal_shift_percent 0.01
```

### tilEPIC_complete.py

To create the final mosaic by merging all samples:

```sh
python tilEPIC_complete.py "path/to/image/directory" "path/to/final/output.png" --vertical_shift_percent 0.5 --horizontal_shift_percent 0.048
```

## Contribution

Contributions are welcome! Feel free to open issues or pull requests!
