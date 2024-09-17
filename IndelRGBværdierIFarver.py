def classify_color(rgb):
    
    r, g, b = rgb

    # Sort
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

# Eksempel på brug:
pixel_rgb = (120, 250, 50)  # Lys grøn
print(classify_color(pixel_rgb))  

pixel_rgb = (40, 120, 30)  # Mørk grøn
print(classify_color(pixel_rgb)) 

pixel_rgb = (110, 60, 30)  # Brun
print(classify_color(pixel_rgb))  

pixel_rgb = (10, 10, 10)  # Sort
print(classify_color(pixel_rgb)) 
