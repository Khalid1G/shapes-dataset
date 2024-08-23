import os
import random
import math
from PIL import Image, ImageDraw

# Constants
IMAGE_SIZE = 224
NUM_IMAGES_PER_SHAPE = 10000
SHAPES = [
    "circle",
    "semicircle",
    "oval",
    "triangle",
    "square",
    "rectangle",
    "parallelogram",
    "rhombus",
    "trapezoid",
    "kite",
    "pentagon",
    "hexagon",
    "heptagon",
    "octagon",
    "nonagon",
    "decagon",
    "star",
]

# Shapes that should only rotate at 0° or 90°
FIXED_ANGLE_SHAPES = [
    "square",
    "rectangle",
    "parallelogram",
    "rhombus",
    "trapezoid",
    "kite",
]

OUTPUT_DIR = "./2D_Geometric_Shapes_Dataset"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def rotate_and_position_shape(image, shape_image, angle, cx, cy):
    """Rotates and positions the shape on the base image."""
    rotated_shape = shape_image.rotate(angle, expand=True)
    shape_width, shape_height = rotated_shape.size
    paste_position = (cx - shape_width // 2, cy - shape_height // 2)
    image.paste(rotated_shape, paste_position, rotated_shape)


def draw_shape(shape, color, size):
    """Draws a specific shape on a new image and returns it."""
    shape_image = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE))
    shape_draw = ImageDraw.Draw(shape_image)
    cx, cy = IMAGE_SIZE // 2, IMAGE_SIZE // 2

    if shape == "circle":
        radius = size // 2
        bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
        shape_draw.ellipse(bbox, fill=color)

    elif shape == "semicircle":
        radius = size // 2
        bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
        shape_draw.pieslice(bbox, start=0, end=180, fill=color)

    elif shape == "oval":
        bbox = [cx - size, cy - size // 2, cx + size, cy + size // 2]
        shape_draw.ellipse(bbox, fill=color)

    elif shape == "triangle":
        points = [
            (cx, cy - size // 2),
            (cx - size // 2, cy + size // 2),
            (cx + size // 2, cy + size // 2),
        ]
        shape_draw.polygon(points, fill=color)

    elif shape == "square":
        half_size = size // 2
        bbox = [cx - half_size, cy - half_size, cx + half_size, cy + half_size]
        shape_draw.rectangle(bbox, fill=color)

    elif shape == "rectangle":
        half_width = size // 2
        half_height = int(size * 0.75)
        bbox = [cx - half_width, cy - half_height, cx + half_width, cy + half_height]
        shape_draw.rectangle(bbox, fill=color)

    elif shape == "parallelogram":
        points = [
            (cx - size // 2, cy - size // 4),
            (cx + size // 2, cy - size // 4),
            (cx + size // 2 - 20, cy + size // 4),
            (cx - size // 2 - 20, cy + size // 4),
        ]
        shape_draw.polygon(points, fill=color)

    elif shape == "rhombus":
        points = [
            (cx, cy - size // 2),
            (cx - size // 2, cy),
            (cx, cy + size // 2),
            (cx + size // 2, cy),
        ]
        shape_draw.polygon(points, fill=color)

    elif shape == "trapezoid":
        points = [
            (cx - size // 2, cy + size // 2),
            (cx + size // 2, cy + size // 2),
            (cx + size // 4, cy - size // 2),
            (cx - size // 4, cy - size // 2),
        ]
        shape_draw.polygon(points, fill=color)

    elif shape == "kite":
        points = [
            (cx, cy - size // 2),
            (cx - size // 4, cy),
            (cx, cy + size // 2),
            (cx + size // 4, cy),
        ]
        shape_draw.polygon(points, fill=color)

    elif shape in ["pentagon", "hexagon", "heptagon", "octagon", "nonagon", "decagon"]:
        sides = {
            "pentagon": 5,
            "hexagon": 6,
            "heptagon": 7,
            "octagon": 8,
            "nonagon": 9,
            "decagon": 10,
        }[shape]
        draw_regular_polygon(shape_draw, cx, cy, size // 2, sides, color)

    elif shape == "star":
        outer_radius = size // 2
        inner_radius = size // 4
        points = []
        for i in range(10):
            radius = inner_radius if i % 2 == 0 else outer_radius
            x = cx + radius * math.cos(2 * math.pi * i / 10)
            y = cy + radius * math.sin(2 * math.pi * i / 10)
            points.append((x, y))
        shape_draw.polygon(points, fill=color)

    return shape_image


def draw_regular_polygon(draw, cx, cy, radius, sides, color):
    """Draws a regular polygon with a given number of sides."""
    points = [
        (
            cx + radius * math.cos(2 * math.pi * i / sides),
            cy + radius * math.sin(2 * math.pi * i / sides),
        )
        for i in range(sides)
    ]
    draw.polygon(points, fill=color)


def create_image(shape):
    """Creates a single image with a random shape."""
    image = Image.new("RGB", (IMAGE_SIZE, IMAGE_SIZE), "white")
    color = random.choice(
        ["red", "green", "blue", "yellow", "purple", "orange", "pink"]
    )

    size = random.randint(30, 100)

    # Determine angle based on shape type
    if shape in FIXED_ANGLE_SHAPES:
        angle = random.choice([0, 90, 180, 270])
    else:
        angle = random.randint(0, 360)

    # Create the shape image and rotate it
    shape_image = draw_shape(shape, color, size)
    max_dim = int(math.sqrt(2) * size)
    cx = random.randint(max_dim // 2, IMAGE_SIZE - max_dim // 2)
    cy = random.randint(max_dim // 2, IMAGE_SIZE - max_dim // 2)

    rotate_and_position_shape(image, shape_image, angle, cx, cy)

    return image


def generate_dataset():
    """Generates a dataset of images for each shape."""
    for shape in SHAPES:
        shape_dir = os.path.join(OUTPUT_DIR, shape)
        os.makedirs(shape_dir, exist_ok=True)
        for i in range(NUM_IMAGES_PER_SHAPE):
            image = create_image(shape)
            image_path = os.path.join(shape_dir, f"{shape}_{i+1}.png")
            image.save(image_path)


if __name__ == "__main__":
    generate_dataset()
    print(f"Dataset generated in {OUTPUT_DIR}")
