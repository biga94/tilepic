from PIL import Image, ImageFile
import os
from concurrent.futures import ProcessPoolExecutor
import argparse

# Aumenta il limite per la dimensione delle immagini per evitare DecompressionBombError
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_t_value(filename):
    base_name = os.path.basename(filename)
    t_index = base_name.find('_T') + 2
    t_value = int(base_name[t_index:t_index+2])  # Assumiamo che T sia seguito da due cifre
    return t_value

def get_num_value(filename):
    base_name = os.path.basename(filename)
    num_part = base_name.split('_')[2]
    num_value = int(num_part.split('-')[0])
    return num_value

def create_mosaic(image_list, output_path, vertical_shift_percent=0.5, horizontal_shift_percent=0.048):
    image_list.sort(key=lambda x: (get_num_value(x), get_t_value(x)))

    images = []
    for img_file in image_list:
        try:
            img = Image.open(img_file)
            img.verify()
            img = Image.open(img_file)
            img.load()
            images.append(img)
        except (IOError, SyntaxError) as e:
            print(f"Immagine {img_file} corrotta o non valida: {e}")
            continue

    if not images:
        print("Nessuna immagine valida trovata.")
        return

    img_width, img_height = images[0].size
    vertical_overlap = int(img_height * vertical_shift_percent)
    horizontal_overlap = int(img_width * horizontal_shift_percent)

    num_rows = len(set(get_num_value(img) for img in image_list))
    num_cols = 13

    mosaic_width = img_width * num_cols - horizontal_overlap * (num_cols - 1)
    mosaic_height = img_height * num_rows - vertical_overlap * (num_rows - 1)
    mosaic_image = Image.new('RGB', (mosaic_width, mosaic_height))

    for img, file in zip(images, image_list):
        t_value = get_t_value(file) - 1
        num_value = get_num_value(file) - 1
        x = t_value * (img_width - horizontal_overlap)
        y = num_value * (img_height - vertical_overlap)
        mosaic_image.paste(img, (x, y))

    mosaic_image.save(output_path, format='PNG')

def process_sample(prefix, image_files, image_dir, vertical_shift_percent=0.5, horizontal_shift_percent=0.048):
    sample_images = [os.path.join(image_dir, file) for file in image_files if prefix in file and 'green' in file]
    mosaic_path = os.path.join(image_dir, f"{prefix}_mosaic.png")
    create_mosaic(sample_images, mosaic_path, vertical_shift_percent, horizontal_shift_percent)
    return mosaic_path

def create_final_chip(image_dir, output_path, vertical_shift_percent=0.5, horizontal_shift_percent=0.048):
    image_files = [file for file in os.listdir(image_dir) if file.endswith(('jpg', 'jpeg', 'png'))]
    sample_prefixes = [f"R0{i}C01" for i in range(1, 9)]
    mosaic_paths = []

    # Utilizza ProcessPoolExecutor per parallelizzare la creazione dei mosaici
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_sample, prefix, image_files, image_dir, vertical_shift_percent, horizontal_shift_percent) for prefix in sample_prefixes]
        for future in futures:
            mosaic_paths.append(future.result())

    # Carica tutti i mosaici
    mosaics = [Image.open(mosaic) for mosaic in mosaic_paths]

    # Assumi che tutti i mosaici abbiano la stessa larghezza
    mosaic_width = mosaics[0].width
    mosaic_height = mosaics[0].height

    # Crea una nuova immagine per il chip finale
    final_chip_height = mosaic_height * len(mosaics)
    final_chip_image = Image.new('RGB', (mosaic_width, final_chip_height))

    # Aggiungi ogni mosaico al chip finale
    for i, mosaic in enumerate(mosaics):
        final_chip_image.paste(mosaic, (0, i * mosaic_height))

    # Salva il chip finale
    final_chip_image.save(output_path, format='PNG')

def main(image_dir, output_path, vertical_shift_percent=0.5, horizontal_shift_percent=0.048):
    create_final_chip(image_dir, output_path, vertical_shift_percent, horizontal_shift_percent)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create the final chip by merging all sample mosaics.')
    parser.add_argument('image_dir', type=str, help='Directory containing the images')
    parser.add_argument('output_path', type=str, help='Path to save the final chip')
    parser.add_argument('--vertical_shift_percent', type=float, default=0.5, help='Vertical overlap percentage (default: 0.5)')
    parser.add_argument('--horizontal_shift_percent', type=float, default=0.048, help='Horizontal overlap percentage (default: 0.048)')

    args = parser.parse_args()
    main(args.image_dir, args.output_path, args.vertical_shift_percent, args.horizontal_shift_percent)