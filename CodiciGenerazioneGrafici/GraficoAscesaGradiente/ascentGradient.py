import numpy as np
import matplotlib.pyplot as plt

# Define the function to be maximized (a simple quadratic function for this example)
def func(x, y):
    return -(x**2 + y**2) + 4

# Define the gradient of the function
def grad(x, y):
    return np.array([-2*x, -2*y])

# Generate a grid of points
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)
Z = func(X, Y)

# Initial point
x0, y0 = -1.8, -1.8
points = [(x0, y0)]

# Gradient ascent parameters
learning_rate = 0.1
num_iterations = 4

# Perform gradient ascent
for i in range(num_iterations):
    gradient = grad(x0, y0)
    x0, y0 = x0 + learning_rate * gradient[0], y0 + learning_rate * gradient[1]
    points.append((x0, y0))

# Plotting
plt.figure(figsize=(8, 6))
contour = plt.contour(X, Y, Z, levels=np.linspace(-4, 4, 20), cmap='RdYlBu')
plt.clabel(contour, inline=True, fontsize=8)
points = np.array(points)
plt.plot(points[:, 0], points[:, 1], 'k-o')
for i, point in enumerate(points):
    plt.annotate(f'P{i}', (point[0], point[1]), textcoords="offset points", xytext=(0,10), ha='center')

plt.title('Ascesa del gradiente su f(x,y)=−(x^2+y^2)+4')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.savefig("gradient_ascent_example.png")
plt.show()
