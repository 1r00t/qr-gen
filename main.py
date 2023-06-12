import segno
from PIL import Image, ImageDraw, ImageOps
from utils.image_operations import get_round_corners, apply_perspective_transform
from utils.pattern_mask import generate_qr_code_mask, is_marker

# Settings
pixel_size = 16
padding = 4 * pixel_size
BG_COLOR = (128, 128, 128)
QUIET_COLOR = (225, 225, 225)
MODULE_COLOR = (64, 64, 64)
MARKER_COLOR = (0, 0, 0)

# Create QR code and binary mask
qrcode = segno.make("headful.io", error="H")

matrix = qrcode.matrix
version = int(qrcode.version)

# Create image
w = h = (len(matrix) * pixel_size) + (padding * 2)
image = Image.new(mode="RGB", size=(w, h), color=QUIET_COLOR)
draw = ImageDraw.Draw(image)

# generate finder and alignment pattern mask
pattern_mask = generate_qr_code_mask(version)

# Draw QR code
for y, row in enumerate(matrix):
    for x, c in enumerate(row):
        if c == 1:
            color = MARKER_COLOR if is_marker(pattern_mask, (x, y)) else MODULE_COLOR
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

# Scale down the image
scaled_down_image = ImageOps.scale(image, (512 / image.width) * 0.75)
image = Image.new("RGB", (512, 512), color=BG_COLOR)
x = (image.width - scaled_down_image.width) // 2
y = (image.height - scaled_down_image.height) // 2
image.paste(scaled_down_image, (x, y))

# Apply perspective transform
image = apply_perspective_transform(image, pixel_size, padding, 2, BG_COLOR)

image.save("pil.png")
