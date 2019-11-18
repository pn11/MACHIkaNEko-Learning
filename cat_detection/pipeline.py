import logging
import subprocess
import sys

def fileparts(path):
    '''inspired by fileparts function in Matlab
    '''
    def count_non_zero_length(word_list):
        count = 0
        for w in word_list:
            if len(w) > 0:
                count += 1
        return count

    path = path.split("/")
    filepath = "/".join(path[:-1])

    path = path[-1].split(".")
    if len(path) == 1:
        name = path[0]
        ext = ""
    else:
        if count_non_zero_length(path) == 1:
            name = ".".join(path)
            ext = ""
        else:
            name = ".".join(path[:-1])
            ext = path[-1]

    return filepath, name, ext


if __name__ == '__main__':
   argv = sys.argv

   # detect cats from a image
   res = subprocess.run(["./detect_cat_single_image.sh", argv[1]], capture_output=True)

   lines = res.stdout.decode().split('\n')

   id_ = 0
   for l in lines[:-1]:
       if l[0] == '#':
          continue
       spl = l.split('\t')
       x1, y1, x2, y2 = [round(float(x)) for x in spl[:4]]
       conf, cls_conf, cls_pred = spl[4:]
       if cls_pred == 'cat':
          path, name, _  = fileparts(argv[1])
          label = path.split('/')[-1]
          # create bounding box of cat
          res = subprocess.run(f"source venv/bin/activate; python create_cat_bb.py {argv[1]} output/{label}-{id_}-{name}.png {x1} {y1} {x2} {y2}", capture_output=True, shell=True)
          # resize image
          res = subprocess.run(f"source venv/bin/activate; python resize_image.py output/{label}-{id_}-{name}.png output/resized-{label}-{id_}-{name}.png 224", capture_output=True, shell=True)
          id_ += 1
       else:
          logging.info(f'{cls_pred} detected')

   print(f'{argv[1]}\t{id_}')
