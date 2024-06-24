import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definizione dei parametri
mp = 1
r = 150

# Creazione della griglia
x = np.linspace(-300, 300, 400)
y = np.linspace(-300, 300, 400)
X, Y = np.meshgrid(x, y)
lij_squared = X**2 + Y**2

# Definizione della funzione di misurazione Eij
Eij = np.where(lij_squared <= r**2, mp * ((lij_squared - r**2)**2 / r**4), 0)

# Creazione del grafico
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Eij, cmap='viridis')

# Etichette degli assi
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('Eij')

# Titolo del grafico
#ax.set_title('Funzione di misurazione Eij con Mp=1 e r=150')

# Salva il grafico come immagine PNG
fig.savefig("C:\\Users\\Ivan\\Desktop\\TESI\\GraficoEij\\grafico_Eij.png", format='png')


# Mostra il grafico
plt.show()

