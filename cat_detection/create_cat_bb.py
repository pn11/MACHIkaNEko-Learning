'''Create cat-only image file'''
import logging
from PIL import Image
import sys

if __name__ == '__main__':
    argv = sys.argv
    try:
        image_file = argv[1]
        out_file = argv[2]
        x1, y1, x2, y2 = [int(x) for x in argv[3:]]
    except:
        logging.error(f'Usage: python {__file__} image_file out_file x1 y1 x2 y2')
        exit()

    im = Image.open(image_file)
    im.crop((x1, y1, x2, y2)).save(f'{out_file}')

