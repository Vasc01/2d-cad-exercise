from backend.transformer import CartesianTransformer
from matplotlib_settings import *

cartesian_transformer = CartesianTransformer()

point_x = -5
point_y = 10

delta_x = 2
delta_y = 3

new_x, new_y = cartesian_transformer.move(point_x, point_y, delta_x, delta_y)
c = cartesian_transformer.move(point_x, point_y, delta_x, delta_y)

print(type(c), c)
print("original x,y:", point_x, point_y,
      "new x,y:", new_x, new_y)


ax.scatter(point_x, point_y, color='blue')
ax.scatter(new_x, new_y, color='red')
plt.show()
