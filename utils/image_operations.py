from typing import List, Union
from PIL import Image
import random
import numpy as np
import cv2


def get_round_corners(
    matrix: List[List[int]], x: int, y: int
) -> Union[bool, bool, bool, bool]:
    rows = len(matrix)
    cols = len(matrix[0])

    # Determine if the pixel is located at the edge of the matrix
    is_top_edge = y == 0
    is_right_edge = x == cols - 1
    is_bottom_edge = y == rows - 1
    is_left_edge = x == 0

    # Determine if the pixel has neighboring pixels on each side
    has_top_neighbor = not is_top_edge and matrix[y - 1][x]
    has_right_neighbor = not is_right_edge and matrix[y][x + 1]
    has_bottom_neighbor = not is_bottom_edge and matrix[y + 1][x]
    has_left_neighbor = not is_left_edge and matrix[y][x - 1]

    # Randomly select one corner to be rounded for each side with no neighbors
    top_left = (
        not has_top_neighbor and not has_left_neighbor and random.choice([True, False])
    )
    top_right = (
        not has_top_neighbor and not has_right_neighbor and random.choice([True, False])
    )
    bottom_right = (
        not has_bottom_neighbor
        and not has_right_neighbor
        and random.choice([True, False])
    )
    bottom_left = (
        not has_bottom_neighbor
        and not has_left_neighbor
        and random.choice([True, False])
    )

    return [top_left, top_right, bottom_right, bottom_left]


def apply_perspective_transform(
    image: Image, pixel_size: int, padding: int, pixel_amount: int
):
    # Load the image using PIL
    width, height = image.size

    # Define the source and destination points for the perspective transformation
    source_points = np.float32(
        [
            (padding, padding),
            (width - padding, padding),
            (width - padding, height - padding),
            (padding, height - padding),
        ]
    )
    destination_points = np.float32(
        [
            (padding + pixel_size * pixel_amount, padding),
            (
                width - (padding + pixel_size * pixel_amount),
                padding + pixel_size * pixel_amount,
            ),
            (width - padding, height - (padding + pixel_size * pixel_amount)),
            (padding, height - padding),
        ]
    )

    # Create a perspective transformation matrix
    perspective_matrix = cv2.getPerspectiveTransform(source_points, destination_points)

    # Apply the perspective transformation using OpenCV
    transformed_image = cv2.warpPerspective(
        np.array(image),
        perspective_matrix,
        (width, height),
        borderValue=(255, 255, 255),
    )

    # Convert the transformed image to PIL format
    transformed_image = Image.fromarray(transformed_image)

    # Return the transformed image
    return transformed_image
