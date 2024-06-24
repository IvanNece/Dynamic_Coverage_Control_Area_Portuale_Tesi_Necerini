import numpy as np
import matplotlib.pyplot as plt

# Define parameters
delta = 1.0  # Threshold distance for repulsion
#d: Intervallo di distanza che va da 0 a 2 volte la soglia delta suddiviso in 400 punti. 
#Questo rappresenta la gamma di distanze su cui verrà calcolata la forza repulsiva.
d = np.linspace(0, 2*delta, 400)  # Distance range

# Calculate repulsive potential, NO, CALCOLO SOLO DELL'INTENSITA' DELLA FORZA REPULSIVA
eta_ik = np.where(d <= delta, (delta - d) / d, 0)

# Plot the repulsive potential
fig, ax = plt.subplots(figsize=(8, 6))  # Define the figure and axis
ax.plot(d, eta_ik, label=r'$\frac{\delta - d_{ik}(t)}{d_{ik}(t)}$', color='orange')
ax.axvline(x=delta, color='red', linestyle='--', label=r'$\delta$')
ax.set_xlabel(r'$d_{ik}(t)$')
ax.set_ylabel(r'$\frac{\delta - d_{ik}(t)}{d_{ik}(t)}$')
#ax.set_title('Intensità del potenziale repulsivo')
ax.legend()
ax.grid(True)
plt.show()

# Save the figure
fig.savefig("C:\\Users\\Ivan\\Desktop\\TESI\\CodiciGenerazioneGrafici\\GraficoPotRepV3\\intensPotRep.png", format='png')

