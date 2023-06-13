import segno
from PIL import Image, ImageDraw, ImageOps
from utils.image_operations import get_round_corners, apply_perspective_transform
from utils.pattern_mask import generate_qr_code_mask, is_marker

# Settings
PIXEL_SIZE = 16
PADDING = 4 * PIXEL_SIZE
IMAGE_SIZE = 512
BG_COLOR = (128, 128, 128)
QUIET_COLOR = (225, 225, 225)
MODULE_COLOR = (32, 32, 32)
PATTERN_COLOR = (0, 0, 0)

# Create QR code and binary mask
qrcode = segno.make("headful.io", error="H", version=8)

matrix = qrcode.matrix
version = int(qrcode.version)

print(f"image version: {version}")
print(f"image size: {IMAGE_SIZE}")

# Create image
w = h = (len(matrix) * PIXEL_SIZE) + (PADDING * 2)
image = Image.new(mode="RGB", size=(w, h), color=QUIET_COLOR)
draw = ImageDraw.Draw(image)

# generate finder and alignment pattern mask
pattern_mask = generate_qr_code_mask(version)

# Draw QR code
for y, row in enumerate(matrix):
    for x, c in enumerate(row):
        if c == 1:
            color = PATTERN_COLOR if is_marker(pattern_mask, (x, y)) else MODULE_COLOR
            draw.rounded_rectangle(
                (
                    (PADDING + x * PIXEL_SIZE, PADDING + y * PIXEL_SIZE),
                    (
                        PADDING + x * PIXEL_SIZE + PIXEL_SIZE,
                        PADDING + y * PIXEL_SIZE + PIXEL_SIZE,
                    ),
                ),
                radius=7,
                fill=color,
                corners=get_round_corners(matrix, x, y),
            )

# Scale down the image
scaled_down_image = ImageOps.scale(image, (IMAGE_SIZE / image.width) * 0.75)
image = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), color=BG_COLOR)
x = (image.width - scaled_down_image.width) // 2
y = (image.height - scaled_down_image.height) // 2
image.paste(scaled_down_image, (x, y))

# Apply perspective transform
# TODO: make the angle not dependent on IMAGE_SIZE
image = apply_perspective_transform(image, PIXEL_SIZE, PADDING, 2, BG_COLOR)

image.save("pil.png")
