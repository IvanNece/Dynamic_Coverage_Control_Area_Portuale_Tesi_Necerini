import numpy as np

from coverageIndices import calculateCoverageIndices, calculateTotalCoverageIndex
from gradient import gradientOfCoverageIndex

from v3.repulsivePotential import calculateRepulsivePotential
    
    
#-------------------------------------------------------------------------------------------------------

def coverageAlgorithmV3(targetsTrajectories: list, agentsPosition: list, r, mp, lb, h, NUMAGENTS, NUMSECONDS, EPSILON, DELTA):
    # Assicurati che agentsPosition sia un array NumPy bidimensionale
    agentsPosition = np.array(agentsPosition)
    
    # NUMSECONDS x NUMAGENTS x 2 (x, y coordinates)
    agentsTrajectories = np.zeros((NUMSECONDS, NUMAGENTS, 2))  
    
    for t in range(NUMSECONDS):
        # calcola gli indici di copertura per ogni target data la posizione corrente degli agenti
        # calcolo Ej(t) per ogni target j
        coverageIndices_t = calculateCoverageIndices(targetsTrajectories, agentsPosition, t, r, mp )
        
        gradients_t = np.zeros((NUMAGENTS, 2))  # 2 per x e y
        
        # Calcola il gradiente dell'indice di copertura per ogni agente
        gradients_t = gradientOfCoverageIndex(targetsTrajectories, agentsPosition, t, r, mp, lb, h)

        # Uso del ciclo for classico per iterare sugli agenti
        for i in range(NUMAGENTS):
            potRep = calculateRepulsivePotential(i, agentsPosition, DELTA)
            agentsPosition[i] += EPSILON * gradients_t[i] + potRep
            # DAL GRAFICO V3 SI VEDE COME EFFETTIVAMENTE, A DIFFERENZA DEL GRAFICO V1, ALLA FINE
            # NON CI SIANO COLLISIONI TRA GLI AGENTI. NOTA BENE
            
        # Salva la posizione aggiornata di tutti gli agenti al tempo t
        agentsTrajectories[t] = agentsPosition.copy()
 

    return agentsTrajectories