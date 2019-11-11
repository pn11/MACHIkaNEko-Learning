'''Create cat-only image file'''
import logging
from PIL import Image
import sys

if __name__ == '__main__':
    argv = sys.argv
    try:
        image_file = argv[1]
        out_file = argv[2]
        width = int(argv[3])
    except:
        logging.error(f'Usage: python {__file__} image_file out_file width')
        exit()

    im = Image.open(image_file)
    im.resize((width, width), Image.LANCZOS).save(f'{out_file}')    
