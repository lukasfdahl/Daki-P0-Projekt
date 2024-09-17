import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

# Main function containing the backbone of the program
def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    image_path = r"C:\Users\lukas\Downloads\King Domino dataset\3.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return
    image = cv.imread(image_path)
    tiles = get_tiles(image)
    print(len(tiles))
    
    # Create an empty image to store classified colors (same dimensions as the original image)
    classified_image = np.zeros_like(image)
    
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            print(f"Tile ({x}, {y}):")
            # Classify each pixel in the tile and update the classified image
            classified_tile = classify_tile(tile)
            classified_image[y*100:(y+1)*100, x*100:(x+1)*100] = classified_tile

    # Save the newly created classified image
    classified_image_path = r"C:\Users\lukas\Downloads\King Domino dataset\classified_image_pixel_based.jpg"
    cv.imwrite(classified_image_path, classified_image)
    print(f"Classified image saved at {classified_image_path}")
    
    # Display the image using matplotlib
    plt.imshow(cv.cvtColor(classified_image, cv.COLOR_BGR2RGB))  # Convert from BGR to RGB for correct color display
    plt.title("Classified Image (Pixel-Based)")
    plt.axis('off')  # Hide axis for a cleaner view
    plt.show()

# Break a board into tiles
def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles

# Classify each pixel in a tile and return the classified tile
def classify_tile(tile: np.ndarray) -> np.ndarray:
    classified_tile = np.zeros_like(tile)  # Create an empty array with the same shape as the tile

    rows, cols, _ = tile.shape
    for y in range(rows):
        for x in range(cols):
            blue, green, red = tile[y, x]  # Note: OpenCV stores in BGR format
            terrain = categorize_pixel(red, green, blue)  # Classify the pixel
            classified_tile[y, x] = get_color_for_terrain(terrain)  # Assign the corresponding color
    return classified_tile

# Determine the type of terrain for each pixel
def categorize_pixel(r: int, g: int, b: int) -> str:
    light_green = [(103, 161, 15), (82, 149, 17), (59, 123, 11)]
    dark_green = [(23, 59, 11), (55, 89, 38), (41, 95, 20), (31, 48, 29), (21, 35, 12)]
    blue = [(0, 83, 179), (0, 55, 118)]
    black = [(18, 16, 17)]
    yellow = [(194, 175, 11), (196, 156, 7), (180, 157, 1), (186, 162, 4)]
    brown = [(68, 45, 1)]
    white = [(154, 149, 145)]
    grey = [(131, 125, 93), (140, 128, 80), (119, 101, 53), (122, 113, 84), (110, 97, 44)]

    color_list = [light_green, dark_green, blue, black, yellow, brown, white, grey]

    closest_value = 9999
    closest_color = (0, 0, 0)

    for color_collection in color_list:

        for color in color_collection:
            closeness = calculate_closeness((r, g, b), color)
            if closeness < closest_value:
                closest_value = closeness
                closest_color = color_collection

    if closest_color == light_green:
        return "Lys Grøn"
    elif closest_color == dark_green:
        return "Mørk Grøn"
    elif closest_color == blue:
        return 'Blå'
    elif closest_color == black:
        return 'Sort'
    elif closest_color == yellow:
        return 'Gul'
    elif closest_color == brown:
        return 'Brun'
    elif closest_color == white:
        return 'Hvid'
    elif closest_color == grey:
        return 'Grå'
    else:
        return 'Ukendt'

# Calculate the "closeness" of two colors
def calculate_closeness(check_color : tuple[int, int, int], target_color : tuple[int, int, int]) -> float:
    red_closeness = exp_function(abs(check_color[0] - target_color[0]))
    blue_closeness = exp_function(abs(check_color[1] - target_color[1]))
    green_closeness = exp_function(abs(check_color[2] - target_color[2])) 

    return red_closeness + blue_closeness + green_closeness

def exp_function(val : np.float64):
    return val *((val ** 2) * 0.05 + 1)

# Return the corresponding color for a terrain type
def get_color_for_terrain(terrain: str) -> tuple:
    color_map = {
        "Lys Grøn": (15, 161, 103),
        "Mørk Grøn": (11, 59, 23),
        "Blå": (179, 83, 0),
        "Sort": (17, 16, 18),
        "Gul": (11, 175, 194),
        "Brun": (1, 43, 68),
        "Hvid": (145, 149, 154),
        "Grå": (93, 125, 131),
        "Ukendt": (0, 0, 0)  # Default to black if unknown
    }
    return color_map.get(terrain, (0, 0, 0))  # Return black for 'Ukendt'

if __name__ == "__main__":
    main()