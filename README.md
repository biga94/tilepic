# tilEPIC

tilEPIC is a script for creating image mosaics from Illumina EPIC array data for methylome analysis.

## Description

The tilEPIC tool is designed to generate mosaic images from data produced by Illumina EPIC arrays. This tool facilitates the visualization of fluorescence signals captured during methylome analysis, allowing researchers to inspect and analyze the data in a comprehensive visual format.

### Why This Tool Was Created

In methylome analysis, data generated from Illumina EPIC arrays can be extensive and complex. Each array captures fluorescence signals from numerous probes, producing images that need to be pieced together to form a complete visual representation of the sample. Manually assembling these images is time-consuming and prone to errors. tilEPIC automates this process, ensuring accurate and efficient mosaic creation.

### Current Use

tilEPIC is specifically designed for use with Illumina EPIC v1 8x1 chips. These chips are widely used in methylation studies and tilEPIC can handle the image data generated by these arrays, assembling them into coherent mosaics that represent the entire sample layout on the chip.
## Installation

Make sure you have Python and the following libraries installed:
- PIL (Pillow)

You can install the required libraries using:
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

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE.md) file for details.
