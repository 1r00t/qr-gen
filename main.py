from typing import List
import segno
from PIL import Image, ImageDraw
from utils.image_operations import get_round_corners, apply_perspective_transform
import json


# create QR code and binary mask
qrcode = segno.make("headful.io", error="H", version=2, boost_error=False)
matrix = [[c for c in row] for row in qrcode.matrix]


# settings
pixel_size = 16
padding = 4 * pixel_size
BG_COLOR = (172, 212, 201)
DOTS_COLOR = (60, 74, 70)


# create image
w = h = (len(matrix) * pixel_size) + (padding * 2)
image = Image.new(mode="RGB", size=(w, h), color=BG_COLOR)
draw = ImageDraw.Draw(image)

# load marker mask
marker_mask = List[List[int]]
with open("./marker_mask.json", "r") as marker_mask_json:
    marker_mask = json.load(marker_mask_json)


def is_marker(x: int, y: int) -> bool:
    """tests if a pixel is inside a marker"""
    if marker_mask[x][y] == 1:
        return True
    return False


# draw QR code
for y, row in enumerate(matrix):
    for x, c in enumerate(row):
        if c == 1:
            color = "#FF0000" if is_marker(x, y) else DOTS_COLOR
            draw.rounded_rectangle(
                (
                    (padding + x * pixel_size, padding + y * pixel_size),
                    (
                        padding + x * pixel_size + pixel_size,
                        padding + y * pixel_size + pixel_size,
                    ),
                ),
                radius=7,
                fill=color,
                corners=get_round_corners(matrix, x, y),
            )

# scale down


image = apply_perspective_transform(image, pixel_size, padding, 2, (96, 121, 114))

image = image.resize((512, 512))

image.save("pil.png")
