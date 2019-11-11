# Cat Detection by YOLOv3

## Prerequisite

- Follow the instruction of `Pytorch-YOLOv3/README.md` to download weights etc.
- `python3 -m venv venv; source venv/bin/activate; pip install -r requirements.txt`

## Usage

```sh
python pipeline.py IMAGE_NAME
```

will detect cat from input image and create new trimmed cat-only images in `output` directory.
