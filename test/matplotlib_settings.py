import matplotlib.pyplot as plt
import numpy as np


fig, ax = plt.subplots()

ax.grid()

ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

plt.xlim(-20, 20)
plt.ylim(-20, 20)

minor_ticks = np.arange(-20, 20, 1)
ax.set_xticks(minor_ticks)
ax.set_yticks(minor_ticks)
