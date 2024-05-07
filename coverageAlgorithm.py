import numpy as np

from coverageIndices import calculateCoverageIndices, calculateTotalCoverageIndex
from gradient import gradientOfCoverageIndex
    
#-------------------------------------------------------------------------------------------------------

#TODO VEDERE SE FUNZIONA CON UN DEBUG AL VOLO

def coverageAlgorithm(targetsTrajectories: list, agentsPosition: list, r, mp, lb, NUMTARGETS, NUMAGENTS, NUMSECONDS, EPSILON):
    # NUMSECONDS x NUMAGENTS x 2 (x, y coordinates)
    agentsTrajectories = np.zeros((NUMSECONDS, NUMAGENTS, 2))  
    
    for t in range(NUMSECONDS):
        # calcola gli indici di copertura per ogni target data la posizione corrente degli agenti
        # calcolo Ej(t) per ogni target j
        coverageIndices_t = calculateCoverageIndices(targetsTrajectories, agentsPosition, t, r, mp )
        
        # calcola l'indice di copertura totale combinando gli indici di tutti i target
        # calcolo E(t)
        totalCoverageIndex_t = calculateTotalCoverageIndex(coverageIndices_t, t, lb)
        
            
        # Prima di iniziare il ciclo, creiamo un array di zeri con la stessa forma delle posizioni
        # degli agenti (NUM_AGENTS righe e 2 colonne per le coordinate x e y). Questo assicura che
        # l'array possa contenere i gradienti per ogni agente.
        # Calcola il gradiente dell'indice di copertura per ogni agente per determinare la direzione di movimento ottimale
        # Preallocazione dell'array per i gradienti con la stessa dimensione delle posizioni degli agenti
        gradient_t = np.zeros((NUMAGENTS, 2))  # 2 per x e y
        # Uso del ciclo for classico per iterare sugli agenti
        for i in range(NUMAGENTS):
            # Calcolo del gradiente per l'agente i-esimo
            gradient_t[i] = gradientOfCoverageIndex(targetsTrajectories, agentsPosition, r, mp, lb)
            # Aggiornamento della posizione dell'agente i-esimo
            agentsPosition[i] += EPSILON * gradient_t
            
        # Salva la posizione aggiornata di tutti gli agenti al tempo t
        agentsTrajectories[t] = agentsPosition.copy()
        #TODO CONTROLLARE COME E' STRUTTURATO L'ARRAY DELLE POSIZIONI DEGLI AGENTI

    return agentsTrajectories

    
