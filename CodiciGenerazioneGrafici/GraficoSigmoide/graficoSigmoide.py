import numpy as np
import matplotlib.pyplot as plt

def sigmoid(Ej, E_star):
    return (np.tanh(Ej - E_star) + 1) / 2

# Definire i parametri
E_star = 2.0  # Puoi cambiare questo valore a seconda delle tue necessità
E_values = np.linspace(-10, 10, 400)  # Generare valori di E da -10 a 10

# Calcolare i valori della funzione sigmoide
sigma_values = sigmoid(E_values, E_star)

# Tracciare il grafico
fig, ax = plt.subplots(figsize=(10, 6))

# Grafico della funzione sigmoide
ax.plot(E_values, sigma_values, label=r'$\sigma(Ej) = \frac{\tanh(Ej - E^*) + 1}{2}$', color='b', linewidth=2)

# Linea verticale per E_star
ax.axvline(x=E_star, color='r', linestyle='--', label=r'$E^*$', linewidth=2)

# Annotazione per E_star
ax.annotate(r'$E^*$', xy=(E_star, 0.5), xytext=(E_star + 1, 0.5),
            arrowprops=dict(facecolor='black', shrink=0.05))

# Titolo e etichette
#ax.set_title('Grafico della Funzione Sigmoide', fontsize=16)
ax.set_xlabel(r'$Ej$', fontsize=14)
ax.set_ylabel(r'$\sigma(Ej)$', fontsize=14)

# Legenda
ax.legend(fontsize=12)

# Griglia
ax.grid(True, linestyle='--', alpha=0.7)

# Migliorare la visualizzazione degli assi
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.xaxis.set_tick_params(width=1.5)
ax.yaxis.set_tick_params(width=1.5)

# Salvare il grafico
fig.savefig("C:\\Users\\Ivan\\Desktop\\TESI\\GraficoSigmoide\\graficoSig.png", format='png', dpi=300, bbox_inches='tight')

# Mostrare il grafico
plt.show()

