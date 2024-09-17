import cv2 as cv
import numpy as np
import os

# Main function containing the backbone of the program
def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    image_path = r"C:\Users\lukas\Downloads\King Domino dataset\1.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return
    image = cv.imread(image_path)
    tiles = get_tiles(image)
    print(len(tiles))
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            print(f"Tile ({x}, {y}):")
            print(get_terrain(tile))
            print("=====")

# Break a board into tiles
def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles

# Determine the type of terrain in a tile
def get_terrain(tile : np.ndarray):
    rows, colums, _ = tile.shape

    pixel_values = []

    for y in range(rows):
        for x in range(colums):
            blue, green, red = tile[x, y]
            pixel_value = categorize_pixel(red, green, blue)
            if (pixel_value != None):
                pixel_values.append(pixel_value)
    
    light_green, dark_green, blue, black, yellow, brown, white, grey = get_pixel_percentage(pixel_values)

    return get_tile_type(light_green, dark_green, blue, black, yellow, brown, white, grey)



def categorize_pixel(r: int, g: int, b: int) -> str:
    light_green = [(103, 161, 15), (82, 149, 17)]
    dark_green = [(23, 59, 11), (55, 89, 38), (41, 95, 20)]
    blue = [(0, 83, 179)]
    black = [(18, 16, 17)]
    yellow = [(194, 175, 11), (196, 156, 7)]
    brown = [(68, 45, 1)]
    white = [(154, 149, 145)]
    grey = [(131, 125, 93), (140, 128, 80), (119, 101, 53)]

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

#light_green, dark_green, blue, black, yellow, brown, white, grey
def get_pixel_percentage(pixel_values : list[str]):
    count = len(pixel_values)
    light_green, dark_green, blue, black, yellow, brown, white, grey = 0, 0, 0, 0, 0, 0, 0, 0
    
    for pixel in pixel_values:
        if pixel == "Sort":
            black += 1
        elif pixel == "Hvid":
            white += 1
        elif pixel == "Grå":
            grey += 1
        elif pixel == "Gul":
            yellow += 1
        elif pixel == "Brun":
            brown += 1
        elif pixel == "Lys Grøn":
            light_green += 1
        elif pixel == "Mørk Grøn":
            dark_green += 1
        elif pixel == "Blå":
            blue += 1
            
    return light_green / count * 100, dark_green / count * 100, blue / count * 100, black / count * 100, yellow / count * 100, brown / count * 100, white / count * 100, grey / count * 100

def get_tile_type(light_green : float, dark_green : float, blue : float, black : float, yellow : float, brown : float, white : float, grey : float) -> str:
    print(f"light_green = {light_green} , dark_green = {dark_green}, blue = {blue} , black = {black}, yellow = {yellow}, brown = {brown}, white =  {white}, grey = {grey}")
    return "Unknown"


if __name__ == "__main__":
    main()