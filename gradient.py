import numpy as np

from initialCoverageIndices import calculateInitialTotalCoverageIndex

#--------------------------------------------------------------------------------------------------------

# Funzione per calcolare il gradiente dell'indice di copertura totale E(0) rispetto alle posizioni degli agenti
def calculateGradientTotalCoverageIndex(initialCoverageIndices, initialAgentPositions, r, mp, delta, lowerboundIndex):
    numAgents = len(initialAgentPositions)
    gradient = np.zeros((numAgents, 2))  # Matrice per memorizzare le derivate parziali
    
    # Calcolo della funzione di copertura totale per le posizioni iniziali degli agenti
    totalCoverageIndex_0 = calculateInitialTotalCoverageIndex(initialCoverageIndices, lowerboundIndex)
    
    # Iterazione su ciascun agente per calcolare il gradiente
    for i, (agent_x, agent_y) in enumerate(initialAgentPositions):
        # Perturbazione delle coordinate dell'agente
        perturbedPositions = np.copy(initialAgentPositions)
        perturbedPositions[i][0] += delta  # Perturbazione della coordinata x
        perturbedPositions[i][1] += delta  # Perturbazione della coordinata y
        
        # Calcolo del valore della funzione nei punti perturbati
        perturbedCoverageIndex = calculateInitialTotalCoverageIndex(initialCoverageIndices, lowerboundIndex)
        
        # Calcolo delle derivate parziali utilizzando la formula delle differenze finite
        gradient[i][0] = (perturbedCoverageIndex - totalCoverageIndex_0) / (2 * delta)  # Derivata parziale rispetto a x
        gradient[i][1] = (perturbedCoverageIndex - totalCoverageIndex_0) / (2 * delta)  # Derivata parziale rispetto a y
    
    return gradient

