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

This script generates a mosaic image for a single sample. You need to specify the directory containing the images, the output path for the mosaic, the sample prefix, and the color channel.

- **Sample Prefix (e.g., `R01C01`)**: This identifies the specific sample. The prefix indicates the row and column of the sample on the chip. For example, `R01C01` refers to the sample located in row 1, column 1.
- **Color Channel (e.g., `green`)**: Specifies the fluorescence signal used in the imaging process. Illumina EPIC arrays typically use `green` and `red` channels to capture different signals.

**Example Command:**

To create a mosaic for the sample with prefix `R01C01` and using the `green` color channel:

```sh
python tilEPIC.py "path/to/image/directory" "path/to/output.png" R01C01 green
```
To specify different vertical and horizontal overlap percentages:

```sh
python tilEPIC.py "path/to/image/directory" "path/to/output.png" R01C01 green --vertical_shift_percent 0.6 --horizontal_shift_percent 0.05
```

### tilEPIC_complete.py

This script generates the final mosaic by merging all sample mosaics. You need to specify the directory containing the images and the output path for the final mosaic.

**Example Command:**

To create the final mosaic by merging all samples:

```sh
python tilEPIC_complete.py "path/to/image/directory" "path/to/final/output.png"
```

Again, to specify different vertical and horizontal overlap percentages:

```sh
python tilEPIC_complete.py "path/to/image/directory" "path/to/final/output.png" --vertical_shift_percent 0.6 --horizontal_shift_percent 0.05
```

## Contribution

Contributions are welcome! Feel free to open issues or pull requests!
