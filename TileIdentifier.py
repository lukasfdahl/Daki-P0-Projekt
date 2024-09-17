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



def categorize_pixel(r : int, b : int, g : int) -> str:
    light_green = (103, 161, 15)
    dark_green = (23, 59, 11)
    blue = (0, 83, 179)
    black = (18, 16, 17)
    yellow = (194, 175, 11)
    brown = (70, 43, 0)
    white = (154, 149, 145)
    grey = (131, 125, 93) 

    color_list = [light_green, dark_green, blue, black, yellow, brown, white, grey]

    clossest_value = 9999
    clossest_color = (0, 0, 0)

    for color in color_list:
        closeness = calculate_closeness((r, b, g), color)
        if (closeness < clossest_value):
            clossest_value = closeness
            clossest_color = color

    
    if (clossest_color == light_green):
        return "Lys Grøn"
    elif (clossest_color == dark_green):
        return "Mørk Grøn"
    elif (clossest_color == blue):
        return 'Blå'
    elif (clossest_color ==  black):
        return 'Sort'
    elif (clossest_color == yellow):
        return 'Gul'
    elif (clossest_color == brown):
        return 'Brun'
    elif (clossest_color == white):
        return 'Hvid'
    elif (clossest_color == grey):
        return 'Grå'
    else:
        return 'Ukendt'



    if r < 50 and g < 50 and b < 50:
        return 'Sort'
    
    # Hvid
    elif r > 200 and g > 200 and b > 200:
        return 'Hvid'

    # Grå
    elif abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
        return 'Grå'

    # Gul
    elif r > 200 and g > 200 and b < 100:
        return 'Gul'

    # Brun
    elif r > 100 and g < 100 and b < 50:
        return 'Brun'

    # Lys Grøn 
    elif g > 200 and r > 100 and b < 100:
        return 'Lys Grøn'

    # Mørk Grøn
    elif g > 100 and r < 100 and b < 100:
        return 'Mørk Grøn'

    # Blå
    elif b > 150 and r < 100 and g < 100:
        return 'Blå'

    # 'Ukendt'
    else:
        return 'Ukendt'
    
def calculate_closeness(check_color : tuple[int, int, int], target_color : tuple[int, int, int]) -> float:
    red_closeness = exp_function(abs(check_color[0] - target_color[0]))
    blue_closeness = exp_function(abs(check_color[1] - target_color[1]))
    green_closeness = exp_function(abs(check_color[2] - target_color[2])) 

    return red_closeness + blue_closeness + green_closeness

def exp_function(val : np.float64):
    return (val ** 2) * 0.002 + 1

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