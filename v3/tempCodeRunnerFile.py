# Esempio di utilizzo
posizioniAgenti = [
    np.array([1.0, 2.0]),
    np.array([3.0, 4.0]),
    np.array([4.0, 5.0])
]
i = 1  # Indice dell'agente per cui calcolare il potenziale repulsivo
delta = 3  # Soglia di distanza

potRep = calculateRepulsivePotential(i, posizioniAgenti, delta)
print("Potenziale repulsivo per l'agente {}: {}".format(i, potRep))