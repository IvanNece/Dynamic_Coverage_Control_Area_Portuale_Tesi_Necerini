import numpy as np

from coverageIndices import calculateCoverageIndices, calculateTotalCoverageIndex
from gradient import gradientOfCoverageIndex

from v3.repulsivePotential import calculateRepulsivePotential
    
    
#-------------------------------------------------------------------------------------------------------

def coverageAlgorithmV3(targetsTrajectories: list, agentsInitialPosition: list, r, mp, lb, h, NUMAGENTS, NUMSECONDS, EPSILON, DELTA):
    # Assicurati che agentsPosition sia un array NumPy bidimensionale
    agentsInitialPositions = np.array(agentsInitialPosition)
    
    # NUMSECONDS x NUMAGENTS x 2 (x, y coordinates)
    agentsTrajectories = np.zeros((NUMSECONDS, NUMAGENTS, 2))  
    
    agentsTrajectories[0] = agentsInitialPositions
    
    for t in range(NUMSECONDS-1):
        
        gradients_t = gradientOfCoverageIndex(targetsTrajectories, agentsTrajectories[t], t, r, mp, lb, h)

        # Uso del ciclo for classico per iterare sugli agenti
        for i in range(NUMAGENTS):
            potRep = calculateRepulsivePotential(i, agentsTrajectories[t], DELTA)
            agentsTrajectories[t+1][i][0] = (agentsTrajectories[t][i][0]) + (EPSILON*gradients_t[i][0]) + potRep[0]
            agentsTrajectories[t+1][i][1] = (agentsTrajectories[t][i][1]) + (EPSILON*gradients_t[i][1]) + potRep[1]

    return agentsTrajectories