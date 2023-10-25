from backend.transformer import CartesianTransformer
from test.matplotlib_settings import *

cartesian_transformer = CartesianTransformer()

mirror_matrix_yx = [[0, -1, 0],
                    [-1, 0, 0],
                    [0, 0, 1]]

point_x = 10
point_y = 10

new_x, new_y = cartesian_transformer.transform(x=point_x, y=point_y, matrix=mirror_matrix_yx)

print("mirror custom y = -x")
print("original x,y:", point_x, point_y,
      "new x,y:", new_x, new_y)

ax.scatter(point_x, point_y, color='blue')
ax.scatter(new_x, new_y, color='red')
plt.show()
