from backend.transformer import CartesianTransformer
from test.matplotlib_settings import *

cartesian_transformer = CartesianTransformer()

point_x = 5
point_y = 5

new_x, new_y = cartesian_transformer.scale(x=point_x, y=point_y, factor_x=2, factor_y=2)

print("original x,y:", point_x, point_y,
      "new x,y:", new_x, new_y)

ax.scatter(point_x, point_y, color='blue')
ax.scatter(new_x, new_y, color='red')
plt.show()
