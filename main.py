from typing import List
import segno
from PIL import Image, ImageDraw
from utils.image_operations import get_round_corners, apply_perspective_transform


qrcode = segno.make("headful.io", error="Q", version=2, boost_error=False)

matrix = [[c for c in row] for row in qrcode.matrix]

pixel_size = 16
padding = 4 * pixel_size

w = h = (len(matrix) * pixel_size) + (padding * 2)

image = Image.new(mode="RGB", size=(w, h), color="#FFF")

draw = ImageDraw.Draw(image)


for y, row in enumerate(matrix):
    for x, c in enumerate(row):
        if c == 1:
            draw.rounded_rectangle(
                (
                    (padding + x * pixel_size, padding + y * pixel_size),
                    (
                        padding + x * pixel_size + pixel_size,
                        padding + y * pixel_size + pixel_size,
                    ),
                ),
                radius=7,
                fill="#000",
                corners=get_round_corners(matrix, x, y),
            )


image = apply_perspective_transform(image, pixel_size, padding, 2)

image = image.resize((512, 512))

image.save("pil.png")
