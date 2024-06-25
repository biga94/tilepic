from PIL import Image, ImageFile
import os
import argparse

# Aumenta il limite per la dimensione delle immagini per evitare DecompressionBombError
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_t_value(filename):
    base_name = os.path.basename(filename)
    t_index = base_name.find('_T') + 2
    t_value = int(base_name[t_index:t_index+2])  # Assumiamo che T sia seguito da due cifre
    return t_value

def get_r_value(filename):
    base_name = os.path.basename(filename)
    r_index = base_name.find('_R') + 2
    r_value = int(base_name[r_index:r_index+2])  # Assumiamo che R sia seguito da due cifre
    return r_value

def get_num_value(filename):
    base_name = os.path.basename(filename)
    num_part = base_name.split('_')[2]
    num_value = int(num_part.split('-')[0])
    return num_value

def create_mosaic(image_list, output_path, vertical_shift_percent=0.5, horizontal_shift_percent=0.01):
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

def main(image_dir, output_path, prefix, color, vertical_shift_percent, horizontal_shift_percent):
    image_files = [os.path.join(image_dir, file) for file in os.listdir(image_dir) if file.endswith(('jpg', 'jpeg', 'png')) and color in file and prefix in file]
    create_mosaic(image_files, output_path, vertical_shift_percent, horizontal_shift_percent)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crea un mosaico di immagini per un campione specificato.')
    parser.add_argument('image_dir', type=str, help='Directory contenente le immagini')
    parser.add_argument('output_path', type=str, help='Percorso per salvare il mosaico finale')
    parser.add_argument('prefix', type=str, help='Prefisso per filtrare le immagini del campione (es. R01C01)')
    parser.add_argument('color', type=str, help='Colore per filtrare le immagini (es. green o red)')
    parser.add_argument('--vertical_shift_percent', type=float, default=0.5, help='Percentuale di sovrapposizione verticale (default: 0.5)')
    parser.add_argument('--horizontal_shift_percent', type=float, default=0.01, help='Percentuale di sovrapposizione orizzontale (default: 0.01)')

    args = parser.parse_args()
    main(args.image_dir, args.output_path, args.prefix, args.color, args.vertical_shift_percent, args.horizontal_shift_percent)