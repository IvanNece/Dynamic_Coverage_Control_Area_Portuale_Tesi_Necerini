import numpy as np

from coverageIndices import calculateCoverageIndices, calculateTotalCoverageIndex
from gradient import gradientOfCoverageIndex

from v2.brownianMotion import creationOfBrownianMotionTrajectories
    
    
#-------------------------------------------------------------------------------------------------------

def coverageAlgorithmV2(targetsTrajectories: list, agentsInitialPosition: list, r, mp, lb, h, NUMAGENTS, NUMSECONDS, EPSILON):
    # Assicurati che agentsPosition sia un array NumPy bidimensionale
    agentsInitialPositions = np.array(agentsInitialPosition)
    
    # NUMSECONDS x NUMAGENTS x 2 (x, y coordinates)
    agentsTrajectories = np.zeros((NUMSECONDS, NUMAGENTS, 2))  
    
    agentsTrajectories[0] = agentsInitialPositions

    #CALCOLO DEL MOTO BROWNIANO
    #Creazione delle traiettorie del moto browniano per la durata specificata
    m_i_t = creationOfBrownianMotionTrajectories(NUMSECONDS)
    
    for t in range(NUMSECONDS-1):
        gradients_t = gradientOfCoverageIndex(targetsTrajectories, agentsTrajectories[t], t, r, mp, lb, h)

        for i in range(NUMAGENTS):
            agentsTrajectories[t+1][i][0] = (agentsTrajectories[t][i][0]) + (EPSILON*gradients_t[i][0]) + m_i_t[t][0]
            agentsTrajectories[t+1][i][1] = (agentsTrajectories[t][i][1]) + (EPSILON*gradients_t[i][1]) + m_i_t[t][1]
        

    return agentsTrajectories
