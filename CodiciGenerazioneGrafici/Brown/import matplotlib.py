import matplotlib.pyplot as plt
import numpy as np

# Set parameters for the Brownian motion
T = 150  # total time
N = 150  # number of time steps
dt = T / N  # time step size
mu = 0.0  # mean
sigma = 1.0  # standard deviation

# Time array
t = np.linspace(0, T, N)

# Generate Brownian motion components
np.random.seed(0)
theta = np.random.uniform(0, 2 * np.pi, N)
gauss = np.random.normal(mu, sigma, N)
eta_x = gauss * np.cos(theta)
eta_y = gauss * np.sin(theta)

# Cumulative sum to get the Brownian motion path
brownian_x = np.cumsum(eta_x) * np.sqrt(dt)
brownian_y = np.cumsum(eta_y) * np.sqrt(dt)

# Plot Brownian motion components
fig, ax = plt.subplots(2, 2, figsize=(12, 10))

# Plot the Brownian motion path
ax[0, 0].plot(brownian_x, brownian_y, label="Percorso Browniano")
ax[0, 0].set_title("Percorso del moto Browniano")
ax[0, 0].set_xlabel("X")
ax[0, 0].set_ylabel("Y")
ax[0, 0].legend()

# Plot the X component of Brownian motion
ax[0, 1].plot(t, brownian_x, label="Componente X")
ax[0, 1].set_title("Componente X del moto Browniano")
ax[0, 1].set_xlabel("Tempo")
ax[0, 1].set_ylabel("X")
ax[0, 1].legend()

# Plot the Y component of Brownian motion
ax[1, 0].plot(t, brownian_y, label="Componente Y")
ax[1, 0].set_title("Componente Y del moto Browniano")
ax[1, 0].set_xlabel("Tempo")
ax[1, 0].set_ylabel("Y")
ax[1, 0].legend()

# Histogram of Gaussian increments
ax[1, 1].hist(gauss, bins=30, density=True, alpha=0.6, color='g')
ax[1, 1].set_title("Istogramma degli incrementi Gaussiani")
ax[1, 1].set_xlabel("Valore")
ax[1, 1].set_ylabel("Frequenza")

# Adjust layout to increase space between plots
plt.subplots_adjust(wspace=0.5, hspace=0.5, top=0.9, bottom=0.1, left=0.1, right=0.9)

plt.tight_layout()
fig.savefig("C:\\Users\\Ivan\\Desktop\\TESI\\Brown\\Brownian_motion_components.png", format='png')
plt.show()
