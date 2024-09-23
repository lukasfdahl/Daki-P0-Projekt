import matplotlib.pyplot as plt
import numpy as np

import matplotlib
import matplotlib as mpl


actual = ["Mark", "Skov", "Eng", "Hav",
              "Sump", "Mine", "Unknown"]
predicted = ["Mark", "Skov", "Eng",
           "Hav", "Sump", "Mine", "Unknown"]

harvest = np.array([[34, 1, 0, 0, 4, 0, 4],
                    [3, 67, 0, 0, 0, 1, 1],
                    [0, 7, 20, 0, 0, 0, 0],
                    [0, 0, 0, 55, 0, 0, 0],
                    [0, 2, 0, 0, 13, 0, 0],
                    [0, 0, 0, 0, 0, 9, 0],
                    [0, 2, 0, 0, 0, 0, 0]])


fig, ax = plt.subplots()
im = ax.imshow(harvest)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(predicted)), labels=predicted)
ax.set_yticks(np.arange(len(actual)), labels=actual)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(actual)):
    for j in range(len(predicted)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")

ax.set_title("TileIdentifier.py Confusion Matrix")
fig.tight_layout()
plt.show()