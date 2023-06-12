from itertools import product


def generate_qr_code_mask(version):
    size = version * 4 + 17  # Calculate the size of the QR code matrix
    mask = [[0] * size for _ in range(size)]  # Initialize the matrix with all zeros

    # Add the finder patterns
    _add_finder_pattern(mask, 0, 0)
    _add_finder_pattern(mask, size - 7, 0)
    _add_finder_pattern(mask, 0, size - 7)

    # Add the alignment patterns
    if version >= 2:
        alignment_coords = _get_alignment_positions(version)
        for coord in alignment_coords:
            _add_alignment_pattern(mask, coord[0], coord[1])

    return mask


def _is_alignment_within_finder(pos, qr_size):
    x, y = pos
    finder_positions = [(0, 0), (0, qr_size - 7), (qr_size - 7, 0)]
    alignment_size = 5

    for fp_x, fp_y in finder_positions:
        if any(
            (x + i, y + j)
            in [(fp_x + dx, fp_y + dy) for dx in range(7) for dy in range(7)]
            for i in range(alignment_size)
            for j in range(alignment_size)
        ):
            return False

    return True


def _get_alignment_positions(version):
    positions = []
    if version > 1:
        n_patterns = version // 7 + 2
        first_pos = 6
        positions.append(first_pos)
        matrix_width = 17 + 4 * version
        last_pos = matrix_width - 1 - first_pos
        second_last_pos = (
            (first_pos + last_pos * (n_patterns - 2) + (n_patterns - 1) // 2)
            // (n_patterns - 1)
        ) & -2
        pos_step = last_pos - second_last_pos
        second_pos = last_pos - (n_patterns - 2) * pos_step
        positions.extend(range(second_pos, last_pos + 1, pos_step))
    positions = list(product(positions, repeat=2))
    positions_clean = []
    for position in positions:
        if _is_alignment_within_finder(position, matrix_width):
            positions_clean.append(position)
    return positions_clean


def _add_finder_pattern(mask, x, y):
    for i in range(7):
        mask[x + i][y] = 1
        mask[x + i][y + 6] = 1
        mask[x][y + i] = 1
        mask[x + 6][y + i] = 1

    for i in range(2, 5):
        for j in range(2, 5):
            mask[x + i][y + j] = 1


def _add_alignment_pattern(mask, x, y):
    x = x - 2
    y = y - 2
    alignment_pattern = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
    ]

    for i in range(5):
        for j in range(5):
            mask[x + i][y + j] = alignment_pattern[i][j]


def is_marker(pattern_mask, point):
    x, y = point
    if pattern_mask[x][y] == 1:
        return True
    return False
