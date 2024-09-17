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

    if light_green >= 50.0 or light_green >= 30.0 and brown >= 20.0:
        return "Eng"
    if dark_green >= 50.0 or dark_green>= 30.0 and brown >= 20.0:
        return "Skov"
    if blue >= 50.0 or blue >= 30.0 and brown >= 10.0 and yellow >= 10.0:
        return "Hav"
    if black >= 50.0 or black >= 30.0 and grey >= 20.0 and brown >= 10.0:
        return "Mine"
    if yellow >= 50.0 or yellow >= 30.0 and brown >= 15.0:
        return "Mark"
    if grey >= 50.0 or grey >= 30.0 and brown >= 15.0:
        return "Sump"

    return "Unknown"


if __name__ == "__main__":
    main()