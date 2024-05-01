import numpy as np

#--------------------------------------------------------------------------------------------------------

def generateInitialAgentPositions(numAgents: int, initialAreaSize: int):
    # Calcola il numero di celle in cui distribuire gli agenti
    numCells = int(np.sqrt(numAgents))
    
    # Calcola le dimensioni di ciascuna cella
    cellSize = initialAreaSize / numCells
    
    # Lista per memorizzare le posizioni degli agenti
    initialAgentPositions = []
    
    # Genera le posizioni degli agenti distribuendoli equamente nelle celle
    for i in range(numCells):
        for j in range(numCells):
            # Calcola le coordinate del centro della cella
            x_center = (i + 0.5) * cellSize
            y_center = (j + 0.5) * cellSize
            
            # Aggiungi la posizione dell'agente alla lista
            initialAgentPositions.append((x_center, y_center))
    
    return initialAgentPositions
