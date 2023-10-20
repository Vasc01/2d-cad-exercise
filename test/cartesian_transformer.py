from backend.transformer import CartesianTransformer

transformer = CartesianTransformer().set_reference(5, 5)

point_x = 10
point_y = 10

reference_x = 8
reference_y = 8


# move relative-------------------------------------------
print("move relative")

move_in_x = 2
move_in_y = 3

new_x, new_y = transformer.move(point_x, point_y, move_in_x, move_in_y)
c = transformer.move(point_x, point_y, move_in_x, move_in_y)

print(type(c))
print(c)
print("original_x:", point_x, "original_y:", point_y, "new_x:", new_x, "new_y", new_y)

print()

# rotate--------------------------------------------------
print("rotate")
theta = 90
new_x, new_y = transformer.rotate(point_x, point_y, theta)
print("original_x:", point_x, "original_y:", point_y, "new_x:", new_x, "new_y", new_y)
print()

# mirror--------------------------------------------------
print("mirror")
axis = "xy"
new_x, new_y = transformer.mirror(point_x, point_y, axis)
print("original_x:", point_x, "original_y:", point_y, "new_x:", new_x, "new_y", new_y)

axis = "x"
new_x, new_y = transformer.mirror(point_x, point_y, axis)
print("original_x:", point_x, "original_y:", point_y, "new_x:", new_x, "new_y", new_y)

print()

# scale--------------------------------------------------
print("scale")

new_x, new_y = transformer.scale(point_x, point_y, 2, 2)
print("original_x:", point_x, "original_y:", point_y, "new_x:", new_x, "new_y", new_y)

new_x, new_y = transformer.scale(point_x, point_y, 2, 2)
print("original_x:", point_x, "original_y:", point_y, "new_x:", new_x, "new_y", new_y)
print()

# mirror custom y = -x -----------------------------------------
print("mirror custom y = -x")
mirror_matrix_yx = [[0, -1, 0],
                    [-1, 0, 0],
                    [0, 0, 1]]

new_x, new_y = transformer.transform(point_x, point_y, mirror_matrix_yx)
print("original_x:", point_x, "original_y:", point_y, "new_x:", new_x, "new_y", new_y)
