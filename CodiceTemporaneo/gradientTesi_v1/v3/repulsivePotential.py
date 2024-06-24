import numpy as np

#---------------------------------------------------------------------------------------------------------

def calculateRepulsivePotential(i, agentsPositions, delta):
    # Inizializza il potenziale repulsivo come un vettore di zeri della stessa dimensione della posizione
    potRep = np.zeros_like(agentsPositions[i])
    
    for k in range(len(agentsPositions)):
        if k != i:
            # Calcola la distanza tra l'agente i e l'agente k manualmente
            diff = agentsPositions[i] - agentsPositions[k]
            d_ik = np.sqrt(diff[0]**2 + diff[1]**2)  # Distanza Euclidea manuale
            
            if d_ik <= delta:
                # Calcola il versore che allontana i da k e moltiplicalo per il termine di modulazione della distanza
                eta_ik = ((agentsPositions[i] - agentsPositions[k]) / d_ik) * (delta - d_ik) / d_ik
            else:
                # Se la distanza è maggiore di S, non c'è forza repulsiva
                eta_ik = np.zeros_like(agentsPositions[i])  
            # Aggiungi il contributo di eta_ik al potenziale repulsivo totale
            potRep += eta_ik  
            
    return potRep

    """ 
    Esattamente! Il risultato negativo per il potenziale repulsivo indica che l'agente si deve 
    allontanare dagli altri agenti vicini. Questo comportamento è desiderato e previsto, poiché 
    la forza repulsiva agisce in direzione opposta per evitare collisioni.
    Quando il potenziale repulsivo ha componenti negative, significa che la forza repulsiva sta 
    spingendo l'agente nella direzione opposta rispetto agli altri agenti, aumentando la distanza
    tra di loro.
    
    """

#----------------------------------------------------------------------------------------

# # Esempio di utilizzo
# posizioniAgenti = [
#     np.array([1.0, 2.0]),
#     np.array([3.0, 4.0]),
#     np.array([4.0, 5.0])
# ]
# i = 1  # Indice dell'agente per cui calcolare il potenziale repulsivo
# delta = 3  # Soglia di distanza

# potRep = calculateRepulsivePotential(i, posizioniAgenti, delta)
# print("Potenziale repulsivo per l'agente {}: {}".format(i, potRep))